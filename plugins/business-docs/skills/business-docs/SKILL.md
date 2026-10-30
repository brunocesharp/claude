---
name: business-docs
description: >
  Analisa código implementado (.NET + Angular) e gera documentação de regras de negócio em docs/{projeto}/business/.
  Use quando o usuário mencionar "documentar regras de negócio", "gerar docs de negócio", "business docs",
  "documentar domínio", "docs/{projeto}/business", "atualizar documentação de negócio", "documentar lógica de negócio"
  ou pedir para documentar uma área do sistema.
  NÃO use para especificação funcional (use spec-functional) nem para plano de execução (use plan-execution).
metadata:
  version: 1.1.0
  category: documentation
  output: docs/{projeto}/business/{area}.md
---

# Business Documentation Generator

Analisa código-fonte implementado e documenta regras de negócio em `docs/{projeto}/business/`, uma área por vez,
usando tasks atômicas (menos de 1 hora cada).

## Referências obrigatórias

Antes de executar qualquer passo, leia:
- `references/template-business-rule.md` — estrutura padrão de cada arquivo gerado
- `references/areas.md` — modelo do mapa de áreas (o mapa do projeto fica em `docs/{projeto}/business/areas.md`)

---

## Pré-requisito

### Passo 0 — Identificar o projeto

A raiz de trabalho é uma pasta de documentação com vários projetos, cada um em `docs/{projeto}/`.

1. Se o usuário citou o projeto, use a pasta dele.
2. Senão, leia `docs/workspace.md`: com um único projeto, use-o e avise; com vários, liste e pergunte qual.
3. Sem `docs/workspace.md`, procure `docs/*/project.md`.
4. Se o projeto não existir, ofereça iniciá-lo com `discovery-init`.
5. Leia `docs/{projeto}/project-config.json` (nome, stack, repositório; ver o schema em `discovery-init/references/project-config-schema.md`). Se não existir, use o `project.md` e ofereça criar o config a partir dele.
6. Leia a configuração do workspace, se existir: `_sdd/config.toml` e `_sdd/config.user.toml` na raiz (o pessoal vence; chaves em `sdd-setup/references/config-schema.md`). Converse em `language.conversation`, escreva os documentos em `language.documents`, chame o usuário por `user.name` e ajuste as explicações a `user.skill_level`; se `paths.docs_root` não for `docs`, use-o no lugar de `docs/` em todos os caminhos. Sem `_sdd/`, use os padrões (pt-BR, nível intermediário, `docs/`) e sugira uma vez rodar o `sdd-setup`, sem bloquear.

`{projeto}` é a pasta escolhida; todos os caminhos abaixo são relativos à raiz de trabalho.

### Localizar o código

Leia `docs/{projeto}/project.md` e use o caminho de **Código local**. Se estiver `a definir`, pergunte onde o código está (ou use o diretório atual, se ele for o repositório do projeto) e registre o caminho no `project.md`.

Se o projeto tiver vários repositórios (`docs/{projeto}/repositorios.md`, skill `multi-repo`), as regras de negócio costumam estar no backend: use os repositórios de papel backend e worker, e o frontend só para regras de tela. No `areas.md`, prefixe cada caminho com o nome do repositório (`opbh-api/src/...`).

### Verificar configuração de áreas

O mapa de áreas é do projeto, não da skill: fica em `docs/{projeto}/business/areas.md`. Se não existir, crie a partir do modelo `references/areas.md` (nunca edite o arquivo da skill). Verifique se os caminhos de código listados existem no código do projeto.

**Se os caminhos não baterem com o projeto:**
1. Faça Glob em `**/Domain/Entities/`, `**/Application/Services/`, `**/Application/Validators/`
   e `**/src/app/**/` para descobrir a estrutura real
2. Apresente ao usuário as áreas identificadas automaticamente
3. Pergunte: "Quer que eu atualize `docs/{projeto}/business/areas.md` antes de gerar a documentação?"
4. Atualize esse arquivo com os caminhos corretos antes de continuar

**Se os caminhos existirem:** siga normalmente a partir do Passo 1.

---

## Passo 1: Inventário

Liste todos os arquivos em `docs/{projeto}/business/` (Glob: `docs/{projeto}/business/**/*.md`).

Para cada arquivo encontrado, leia e extraia:
- Quais regras (RN-XXX) já estão documentadas
- Qual área está coberta
- Data da última atualização no frontmatter

Se a pasta não existir, ela será criada no Passo 3 ao escrever o primeiro arquivo.

---

## Passo 2: Análise de código

Para cada área sem cobertura ou desatualizada (conforme `docs/{projeto}/business/areas.md`), analise os arquivos correspondentes:

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

**Formato do título:** `[business-docs] Documentar {área}: docs/{projeto}/business/{arquivo}.md`

A descrição de cada task deve incluir:
- Arquivo destino
- Caminhos dos arquivos de código a analisar (backend e frontend)
- Regras já existentes (se for atualização)
- Regras novas identificadas no Passo 2

> Se uma área tiver mais de 8 regras, divida em duas tasks com sufixos distintos
> (ex: `fila-pontuacao.md` e `fila-entrada-saida.md`).

---

## Passo 4: Executar tasks

Execute na ordem de prioridade definida em `docs/{projeto}/business/areas.md`. Para cada task:

1. Marque como `in_progress`
2. Releia o arquivo existente em `docs/{projeto}/business/` (se houver) para não duplicar regras
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
| docs/{projeto}/business/fila.md | criado | RN-001 a RN-005 |

Total: X arquivos, Y regras documentadas
```

---

## Exemplos

**Exemplo 1: Documentação inicial completa**
Usuário diz: "gera a documentação de regras de negócio do projeto"
Ações:
1. Pré-requisito verifica `areas.md` — caminhos batem com o projeto
2. Inventário encontra `docs/{projeto}/business/` vazia
3. Análise identifica 7 áreas (backend + Angular) com regras no código
4. 7 tasks criadas, uma por área, executadas em ordem de prioridade
Resultado: 7 arquivos criados em `docs/{projeto}/business/`

**Exemplo 2: Atualização incremental**
Usuário diz: "atualiza a documentação de negócio da fila"
Ações:
1. Inventário encontra `docs/{projeto}/business/fila.md` com RN-001 a RN-005
2. Análise encontra nova regra implementada em `FilaService.cs`
3. 1 task de atualização criada
4. `fila.md` atualizado com RN-006 adicionada
Resultado: arquivo atualizado sem sobrescrever regras existentes

**Exemplo 3: Área específica**
Usuário diz: "documenta as regras de apresentação de projetos"
Ações:
1. Pré-requisito verifica caminhos de `areas.md`
2. Inventário verifica `docs/{projeto}/business/apresentacoes.md`
3. Analisa `Apresentacao.cs` e componente Angular correspondente
4. 1 task criada e executada
Resultado: `docs/{projeto}/business/apresentacoes.md` criado com regras de backend e frontend

---

## Troubleshooting

**Caminhos de código não encontrados**
Execute Glob amplo (`**/Entities/*.cs`, `**/services/*.ts`) para descobrir a estrutura real.
Atualize `docs/{projeto}/business/areas.md` antes de continuar.

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
