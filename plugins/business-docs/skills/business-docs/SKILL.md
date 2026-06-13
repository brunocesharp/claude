---
name: business-docs
description: >
  Analisa código implementado (.NET + Angular) e gera documentação de regras de negócio em docs/business/.
  Use quando o usuário mencionar "documentar regras de negócio", "gerar docs de negócio", "business docs",
  "documentar domínio", "docs/business", "atualizar documentação de negócio", "documentar lógica de negócio"
  ou pedir para documentar uma área do sistema.
  NÃO use para especificação funcional (use spec-functional) nem para plano de execução (use plan-execution).
metadata:
  version: 1.1.0
  category: documentation
  output: docs/business/{area}.md
---

# Business Documentation Generator

Analisa código-fonte implementado e documenta regras de negócio em `docs/business/`, uma área por vez,
usando tasks atômicas (menos de 1 hora cada).

## Referências obrigatórias

Antes de executar qualquer passo, leia:
- `references/template-business-rule.md` — estrutura padrão de cada arquivo gerado
- `references/areas.md` — mapeamento de áreas para arquivos destino e código-fonte

---

## Pré-requisito: Verificar configuração de áreas

Leia `references/areas.md` e verifique se os caminhos de código listados existem no projeto atual.

**Se os caminhos não baterem com o projeto:**
1. Faça Glob em `**/Domain/Entities/`, `**/Application/Services/`, `**/Application/Validators/`
   e `**/src/app/**/` para descobrir a estrutura real
2. Apresente ao usuário as áreas identificadas automaticamente
3. Pergunte: "Quer que eu atualize `references/areas.md` para este projeto antes de gerar a documentação?"
4. Atualize `areas.md` com os caminhos corretos antes de continuar

**Se os caminhos existirem:** siga normalmente a partir do Passo 1.

---

## Passo 1: Inventário

Liste todos os arquivos em `docs/business/` (Glob: `docs/business/**/*.md`).

Para cada arquivo encontrado, leia e extraia:
- Quais regras (RN-XXX) já estão documentadas
- Qual área está coberta
- Data da última atualização no frontmatter

Se a pasta não existir, ela será criada no Passo 3 ao escrever o primeiro arquivo.

---

## Passo 2: Análise de código

Para cada área sem cobertura ou desatualizada (conforme `references/areas.md`), analise os arquivos correspondentes:

### Backend (.NET)

| Camada | O que procurar |
|--------|----------------|
| `Domain/Entities/` | Invariantes, construtores com validação, métodos de domínio, Result Pattern |
| `Domain/ValueObjects/` | Regras de formato e imutabilidade |
| `Application/Commands/` e `Application/Queries/` | Regras orquestradas, validações cross-entity |
| `Application/Validators/` | Validações de entrada com FluentValidation |
| `Infrastructure/Repositories/` | Constraints de dados, queries com filtros de negócio |

Para cada regra encontrada extraia: trigger, condição, ação e localização (arquivo:linha).

### Frontend (Angular)

| Camada | O que procurar |
|--------|----------------|
| `src/app/**/services/` | Lógica de negócio no cliente, chamadas HTTP com parâmetros de regra |
| `src/app/**/guards/` | Regras de acesso a rotas (autorização, autenticação) |
| `src/app/**/validators/` | Validações de formulário com regra de negócio embutida |
| `src/app/**/store/` | Estado derivado de regras (seletores, reducers com condições) |

Documente regras Angular apenas quando expressarem lógica de negócio, não lógica de apresentação.

---

## Passo 3: Criar tasks

Use `TaskCreate` para criar uma task por arquivo de documentação a gerar ou atualizar.

**Formato do título:** `[business-docs] Documentar {área}: docs/business/{arquivo}.md`

A descrição de cada task deve incluir:
- Arquivo destino
- Caminhos dos arquivos de código a analisar (backend e frontend)
- Regras já existentes (se for atualização)
- Regras novas identificadas no Passo 2

> Se uma área tiver mais de 8 regras, divida em duas tasks com sufixos distintos
> (ex: `fila-pontuacao.md` e `fila-entrada-saida.md`).

---

## Passo 4: Executar tasks

Execute na ordem de prioridade definida em `references/areas.md`. Para cada task:

1. Marque como `in_progress`
2. Releia o arquivo existente em `docs/business/` (se houver) para não duplicar regras
3. Analise os arquivos de código listados na task
4. Escreva o arquivo seguindo o template de `references/template-business-rule.md`
5. Marque como `completed`

**Regras de escrita:**
- Não duplicar regras já documentadas — apenas referencie a RN-XXX existente
- Manter numeração sequencial global (próximo = maior existente + 1)
- Documentar apenas o que está implementado no código
- Citar arquivo e linha de cada regra

---

## Passo 5: Relatório final

Ao concluir todas as tasks, exiba:

```
## Documentação gerada

| Arquivo | Status | Regras documentadas |
|---------|--------|---------------------|
| docs/business/fila.md | criado | RN-001 a RN-005 |

Total: X arquivos, Y regras documentadas
```

---

## Exemplos

**Exemplo 1: Documentação inicial completa**
Usuário diz: "gera a documentação de regras de negócio do projeto"
Ações:
1. Pré-requisito verifica `areas.md` — caminhos batem com o projeto
2. Inventário encontra `docs/business/` vazia
3. Análise identifica 7 áreas (backend + Angular) com regras no código
4. 7 tasks criadas, uma por área, executadas em ordem de prioridade
Resultado: 7 arquivos criados em `docs/business/`

**Exemplo 2: Atualização incremental**
Usuário diz: "atualiza a documentação de negócio da fila"
Ações:
1. Inventário encontra `docs/business/fila.md` com RN-001 a RN-005
2. Análise encontra nova regra implementada em `FilaService.cs`
3. 1 task de atualização criada
4. `fila.md` atualizado com RN-006 adicionada
Resultado: arquivo atualizado sem sobrescrever regras existentes

**Exemplo 3: Área específica**
Usuário diz: "documenta as regras de apresentação de projetos"
Ações:
1. Pré-requisito verifica caminhos de `areas.md`
2. Inventário verifica `docs/business/apresentacoes.md`
3. Analisa `Apresentacao.cs` e componente Angular correspondente
4. 1 task criada e executada
Resultado: `docs/business/apresentacoes.md` criado com regras de backend e frontend

---

## Troubleshooting

**Caminhos de código não encontrados**
Execute Glob amplo (`**/Entities/*.cs`, `**/services/*.ts`) para descobrir a estrutura real.
Atualize `references/areas.md` antes de continuar.

**Regra já existe com numeração diferente**
Mantenha a numeração mais antiga. Adicione `(também conhecida como RN-XX)` no cabeçalho da regra.

**Código não encontrado para uma regra**
Documente com `status: pendente-implementacao` e anote que foi identificada apenas em testes ou comentários.

**Área muito grande para uma task**
Divida pelo critério natural do domínio: operações de escrita vs leitura, ou por sub-entidade relacionada.

**Arquivo existente incompleto**
Faça merge: preserve seções existentes, adicione apenas o que falta. Nunca sobrescreva conteúdo já validado.

**Regra Angular vs regra de backend**
Se a mesma regra existe em ambas as camadas, documente uma única vez com dois campos `Implementação`:
```
**Implementação:**
- Backend: `Application/Services/FilaService.cs` linha 42
- Frontend: `src/app/fila/services/fila.service.ts` linha 18
```
