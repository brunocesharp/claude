# Áreas de Domínio — Mapeamento para Documentação

Este arquivo é **configuração por projeto**. Atualize os caminhos de código para refletir
a estrutura real do repositório antes de executar a skill.

Para descobrir a estrutura, use Glob:
- Backend: `**/Domain/Entities/*.cs`, `**/Application/Services/*.cs`
- Frontend: `**/src/app/**/*.service.ts`, `**/src/app/**/*.guard.ts`

---

## Como estruturar uma área

```markdown
## Área: {Nome da Área}

**Arquivo destino:** `docs/business/{nome-kebab}.md`
**Prioridade:** {1 = núcleo | 2 = entidade central | 3 = evento | 4 = cadastro | 5 = infraestrutura}

**Backend (.NET):**
- `{caminho/relativo/ao/arquivo}.cs` — {o que analisar}

**Frontend (Angular):**
- `{caminho/relativo/ao/arquivo}.ts` — {o que analisar}

**Regras esperadas:**
- {regra 1}
- {regra 2}

**Complexidade estimada:** {N} regras → {N} task(s) (~{X}min)
```

---

## Áreas do projeto atual

> Substitua esta seção pelas áreas reais do projeto.
> O exemplo abaixo usa o projeto OPBH como referência — adapte conforme necessário.

---

## Área: Sistema de Fila

**Arquivo destino:** `docs/business/fila.md`
**Prioridade:** 1

**Backend (.NET):**
- `backend/src/OPBH.Domain/Entities/Participante.cs` — pontuação, reset e invariantes de fila
- `backend/src/OPBH.Application/Services/FilaService.cs` — orquestração das regras
- `backend/src/OPBH.Application/Validators/` — validações de entrada relacionadas a fila
- `backend/src/OPBH.Infrastructure/Repositories/ParticipanteRepository.cs` — queries de ordenação

**Frontend (Angular):**
- `frontend/src/app/fila/services/fila.service.ts` — estado e chamadas HTTP

**Regras esperadas:**
- Pontuação por presença (+2 por encontro)
- Reset após apresentação
- Mínimo de 1 presença para entrar na fila
- Desempate por última apresentação
- Saída voluntária zera pontuação

**Complexidade estimada:** 5-7 regras → 1 task (~45min)

---

## Área: Participantes

**Arquivo destino:** `docs/business/participantes.md`
**Prioridade:** 5

**Backend (.NET):**
- `backend/src/OPBH.Domain/Entities/Participante.cs`
- `backend/src/OPBH.Application/Services/ParticipanteService.cs`
- `backend/src/OPBH.Application/Validators/` — arquivos de participante
- `backend/src/OPBH.Application/DTOs/Participante/`

**Frontend (Angular):**
- `frontend/src/app/participantes/services/participante.service.ts`
- `frontend/src/app/participantes/validators/` — validações de formulário

**Regras esperadas:**
- Código sequencial (P + 4 dígitos)
- Unicidade de código e email
- Validação de formato de Instagram (@)
- Validação de email
- Flag `desconsiderar_fila`

**Complexidade estimada:** 4-6 regras → 1 task (~30min)

---

## Área: Projetos e Autorias

**Arquivo destino:** `docs/business/projetos.md`
**Prioridade:** 2

**Backend (.NET):**
- `backend/src/OPBH.Domain/Entities/Projeto.cs`
- `backend/src/OPBH.Domain/Entities/Autoria.cs`
- `backend/src/OPBH.Application/Services/ProjetoService.cs`
- `backend/src/OPBH.Application/Validators/` — arquivos de projeto

**Frontend (Angular):**
- `frontend/src/app/projetos/services/projeto.service.ts`

**Regras esperadas:**
- Código sequencial (J + 4 dígitos)
- Máximo de 3 autores por projeto
- Autor principal (ordem = 1)
- Reset de pontuação de todos os autores ao apresentar
- Contagem de vezes apresentado

**Complexidade estimada:** 5-7 regras → 1 task (~40min)

---

## Área: Encontros e Presença

**Arquivo destino:** `docs/business/encontros.md`
**Prioridade:** 3

**Backend (.NET):**
- `backend/src/OPBH.Domain/Entities/Encontro.cs`
- `backend/src/OPBH.Domain/Entities/Presenca.cs`
- `backend/src/OPBH.Application/Services/EncontroService.cs`
- `backend/src/OPBH.Application/Validators/` — arquivos de encontro

**Frontend (Angular):**
- `frontend/src/app/encontros/services/encontro.service.ts`
- `frontend/src/app/encontros/guards/` — guards de rota

**Regras esperadas:**
- Código sequencial (E + 4 dígitos)
- Unicidade de presença por encontro
- Histórico imutável (encontros passados não podem ser excluídos)
- Data do encontro limitada (máx 30 dias no futuro)

**Complexidade estimada:** 4-6 regras → 1 task (~35min)

---

## Área: Apresentações

**Arquivo destino:** `docs/business/apresentacoes.md`
**Prioridade:** 4

**Backend (.NET):**
- `backend/src/OPBH.Domain/Entities/Apresentacao.cs`
- `backend/src/OPBH.Application/Services/EncontroService.cs` — método de apresentação

**Frontend (Angular):**
- `frontend/src/app/encontros/services/apresentacao.service.ts`

**Regras esperadas:**
- Uma apresentação por projeto por encontro
- Atualiza estatísticas do projeto (vezes apresentado, data última apresentação)
- Dispara reset de pontuação dos autores

**Complexidade estimada:** 3-5 regras → 1 task (~25min)

---

## Área: Autenticação e Controle de Acesso

**Arquivo destino:** `docs/business/auth.md`
**Prioridade:** 7

**Backend (.NET):**
- `backend/src/OPBH.Domain/Entities/User.cs`
- `backend/src/OPBH.Domain/Enums/UserRole.cs`
- `backend/src/OPBH.Application/Services/AuthService.cs`
- `backend/src/OPBH.Infrastructure/Services/JwtService.cs`
- `backend/src/OPBH.API/Controllers/AuthController.cs`

**Frontend (Angular):**
- `frontend/src/app/core/guards/auth.guard.ts`
- `frontend/src/app/core/interceptors/auth.interceptor.ts`
- `frontend/src/app/auth/services/auth.service.ts`

**Regras esperadas:**
- Papéis: Admin e Participante
- Regras de acesso por papel
- Expiração de token JWT
- Redirecionamento por papel após login

**Complexidade estimada:** 4-6 regras → 1 task (~35min)

---

## Área: Códigos Sequenciais

**Arquivo destino:** `docs/business/codigos-sequenciais.md`
**Prioridade:** 6

**Backend (.NET):**
- `backend/src/OPBH.Application/Services/` — métodos de geração de código
- `backend/src/OPBH.Domain/Entities/` — campos Codigo nas entidades

**Frontend (Angular):**
- (sem regras Angular para esta área — lógica exclusiva do backend)

**Regras esperadas:**
- Formato E/P/J + 4 dígitos
- Geração automática sequencial
- Imutabilidade do código após criação

**Complexidade estimada:** 2-4 regras → 1 task (~20min)

---

## Prioridade de execução

Execute nesta ordem (da mais crítica à mais periférica):

1. `fila.md` — núcleo do sistema
2. `projetos.md` — entidade central de valor
3. `encontros.md` — evento principal
4. `apresentacoes.md` — efeitos colaterais críticos
5. `participantes.md` — cadastro base
6. `codigos-sequenciais.md` — infraestrutura de identidade
7. `auth.md` — controle de acesso

---

## Como identificar novas áreas

Se durante a análise do código você encontrar lógica de negócio não coberta acima:

1. Verifique se cabe em uma área existente
2. Se não couber, crie um novo bloco de área neste arquivo com nome kebab-case
3. Estime complexidade e decida se merece task própria ou se pode ser incorporada a uma existente
4. Documente no arquivo destino seguindo o template em `template-business-rule.md`
