# Feature Forms — Referência

## Conceito

Forms da Feature ficam em `features/[nome]/forms/` e centralizam:
- **Criação do FormGroup** via `FormBuilder`
- **Validators customizados** da feature
- **Tipagem forte** do valor do formulário
- **Mapeamento** para DTO de envio

---

## Form Builder centralizado

```typescript
// src/app/features/users/forms/user.form.ts
import { inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { CreateUserDto, UpdateUserDto, UserRole } from '../../../core/models/user.model';

// Tipagem forte do formulário
export interface UserFormValue {
  name:            string;
  email:           string;
  password:        string;
  confirmPassword: string;
  roles:           UserRole[];
}

// Validator customizado — confirma senha
export function passwordMatchValidator(control: AbstractControl): ValidationErrors | null {
  const password        = control.get('password');
  const confirmPassword = control.get('confirmPassword');

  if (!password || !confirmPassword) return null;
  if (password.value !== confirmPassword.value) {
    confirmPassword.setErrors({ passwordMismatch: true });
    return { passwordMismatch: true };
  }
  confirmPassword.setErrors(null);
  return null;
}

// Validator customizado — domínio de e-mail bloqueado
export function blockedDomainValidator(blocked: string[]) {
  return (control: AbstractControl): ValidationErrors | null => {
    const email = control.value as string;
    if (!email) return null;
    const domain = email.split('@')[1];
    return blocked.includes(domain)
      ? { blockedDomain: { domain } }
      : null;
  };
}

// Factory function — cria o FormGroup com tipagem
export function createUserForm(fb: FormBuilder, editMode = false): FormGroup {
  return fb.nonNullable.group(
    {
      name: ['', [
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(100)
      ]],
      email: ['', [
        Validators.required,
        Validators.email,
        blockedDomainValidator(['tempmail.com', 'guerrillamail.com'])
      ]],
      password: [
        '',
        editMode
          ? []  // senha opcional no modo edição
          : [Validators.required, Validators.minLength(8)]
      ],
      confirmPassword: [
        '',
        editMode ? [] : [Validators.required]
      ],
      roles: [
        [UserRole.Viewer] as UserRole[],
        [Validators.required]
      ]
    },
    { validators: passwordMatchValidator }
  );
}

// Mapeia valor do form para DTO de criação
export function toCreateUserDto(value: UserFormValue): CreateUserDto {
  return {
    name:     value.name.trim(),
    email:    value.email.toLowerCase().trim(),
    password: value.password,
    roles:    value.roles
  };
}

// Mapeia valor do form para DTO de edição
export function toUpdateUserDto(value: Partial<UserFormValue>): UpdateUserDto {
  return {
    ...(value.name  ? { name: value.name.trim() }   : {}),
    ...(value.email ? { email: value.email.trim() }  : {}),
    ...(value.roles ? { roles: value.roles }          : {})
  };
}
```

---

## Componente de Form completo

```typescript
// src/app/features/users/components/user-form/user-form.component.ts
import {
  Component, input, output, inject, OnInit,
  ChangeDetectionStrategy
} from '@angular/core';
import { ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { User, UserRole, CreateUserDto, UpdateUserDto } from '../../../../core/models/user.model';
import {
  createUserForm,
  toCreateUserDto,
  toUpdateUserDto,
  UserFormValue
} from '../../forms/user.form';

@Component({
  selector: 'app-user-form',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="onSubmit()" class="form-grid">

      <!-- Nome -->
      <div class="field" [class.invalid]="isInvalid('name')">
        <label for="name">Nome *</label>
        <input id="name" formControlName="name" placeholder="Nome completo" />
        @if (isInvalid('name')) {
          <span class="error">
            @if (form.get('name')?.errors?.['required'])   { Nome é obrigatório. }
            @if (form.get('name')?.errors?.['minlength'])  { Mínimo 3 caracteres. }
          </span>
        }
      </div>

      <!-- Email -->
      <div class="field" [class.invalid]="isInvalid('email')">
        <label for="email">E-mail *</label>
        <input id="email" type="email" formControlName="email" placeholder="email@empresa.com" />
        @if (isInvalid('email')) {
          <span class="error">
            @if (form.get('email')?.errors?.['required'])      { E-mail é obrigatório. }
            @if (form.get('email')?.errors?.['email'])         { E-mail inválido. }
            @if (form.get('email')?.errors?.['blockedDomain']) { Domínio de e-mail não permitido. }
          </span>
        }
      </div>

      <!-- Senha (apenas criação) -->
      @if (!isEditMode()) {
        <div class="field" [class.invalid]="isInvalid('password')">
          <label for="password">Senha *</label>
          <input id="password" type="password" formControlName="password" />
          @if (isInvalid('password')) {
            <span class="error">Senha deve ter no mínimo 8 caracteres.</span>
          }
        </div>

        <div class="field" [class.invalid]="isInvalid('confirmPassword')">
          <label for="confirmPassword">Confirmar senha *</label>
          <input id="confirmPassword" type="password" formControlName="confirmPassword" />
          @if (isInvalid('confirmPassword') && form.errors?.['passwordMismatch']) {
            <span class="error">As senhas não coincidem.</span>
          }
        </div>
      }

      <!-- Perfis -->
      <div class="field">
        <label>Perfis *</label>
        <div class="checkbox-group">
          @for (role of availableRoles; track role) {
            <label class="checkbox-label">
              <input type="checkbox" [value]="role" (change)="onRoleChange(role, $event)" />
              {{ role }}
            </label>
          }
        </div>
      </div>

      <!-- Ações -->
      <div class="form-actions">
        <button type="button" (click)="cancel.emit()">Cancelar</button>
        <button
          type="submit"
          [disabled]="form.invalid || loading()"
          class="primary"
        >
          {{ loading() ? 'Salvando...' : isEditMode() ? 'Salvar' : 'Criar' }}
        </button>
      </div>

    </form>
  `
})
export class UserFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);

  readonly user    = input<User | null>(null);
  readonly loading = input<boolean>(false);

  readonly save   = output<CreateUserDto | UpdateUserDto>();
  readonly cancel = output<void>();

  readonly availableRoles = Object.values(UserRole);
  readonly isEditMode     = () => !!this.user();

  form = createUserForm(this.fb, false);

  ngOnInit(): void {
    const user = this.user();
    if (user) {
      // Modo edição: recria o form e preenche os valores
      this.form = createUserForm(this.fb, true);
      this.form.patchValue({
        name:  user.name,
        email: user.email,
        roles: user.roles
      });
    }
  }

  isInvalid(field: string): boolean {
    const control = this.form.get(field);
    return !!(control?.invalid && (control.dirty || control.touched));
  }

  onRoleChange(role: UserRole, event: Event): void {
    const checked      = (event.target as HTMLInputElement).checked;
    const currentRoles = this.form.get('roles')!.value as UserRole[];
    const updated      = checked
      ? [...currentRoles, role]
      : currentRoles.filter(r => r !== role);
    this.form.get('roles')!.setValue(updated);
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    const value = this.form.getRawValue() as UserFormValue;
    const dto   = this.isEditMode()
      ? toUpdateUserDto(value)
      : toCreateUserDto(value);

    this.save.emit(dto);
  }
}
```

---

## Validator assíncrono (verificação no backend)

```typescript
// src/app/features/users/forms/async-validators.ts
import { inject } from '@angular/core';
import { AbstractControl, AsyncValidatorFn, ValidationErrors } from '@angular/forms';
import { Observable, of } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap, map, catchError, first } from 'rxjs/operators';
import { UserApiService } from '../../../core/http/user-api.service';

export function emailAvailableValidator(excludeId?: string): AsyncValidatorFn {
  const api = inject(UserApiService);

  return (control: AbstractControl): Observable<ValidationErrors | null> => {
    if (!control.value) return of(null);

    return of(control.value).pipe(
      debounceTime(400),
      distinctUntilChanged(),
      switchMap(email =>
        api.checkEmailAvailable(email, excludeId).pipe(
          map(available => (available ? null : { emailTaken: true })),
          catchError(() => of(null))
        )
      ),
      first()
    );
  };
}
```
