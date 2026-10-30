# 03 — Estado e scripts (`_sdd/`)

- **Pedido:** "Estado / scripts quero seguir o mesmo do BMAD" (linha 5)
- **Tamanho:** G
- **Depende de:** 02
- **Situação:** [ ] a fazer

## Contexto

### Como o BMAD faz
- `_bmad/` na raiz do projeto/workspace: runtime, configuração e scripts dos módulos.
- `_bmad/scripts/`: scripts Python executados com `uv run` para carregar configuração e resolver customizações (ex.: `resolve_customization.py --skill <caminho> --project-root <raiz> --key agent`, que devolve JSON).
- As skills **não interpretam** TOML/YAML de cabeça: chamam o script e recebem JSON pronto. Isso deixa o comportamento determinístico.
- `_bmad-output/`: documentos e tickets.

### Como está hoje
- Nenhum script. Todo estado (fase do projeto, status do plano) é lido e escrito pelo modelo, editando Markdown.
- Estado espalhado: `project.md` (checkbox), `workspace.md` (coluna Situação), `execution-plan.md` (Status).

## Objetivo

Ter uma pasta de runtime no workspace e um pequeno conjunto de scripts que leem/validam/atualizam o estado de forma determinística, usados por todas as skills novas.

## Proposta

1. **Estrutura no workspace** (criada pelo `sdd setup`):
   ```
   _sdd/
   ├── config.toml / config.user.toml     # respostas do setup (02)
   ├── custom/                            # overrides (04) — começa vazia
   ├── version.toml                       # versão de cada plugin no último setup (para migrações)
   └── scripts/                           # cópia dos scripts do plugin (ou nada — ver decisão)
   docs/
   └── {projeto}/implementacao/sprint-status.yaml   # estado de entrega (06)
   ```
2. **Scripts** (Python ≥ 3.11, `uv run`, dependências inline PEP 723):
   | Script | Faz |
   |--------|-----|
   | `config.py` | Resolve a configuração com a precedência do 02 e devolve JSON (`--key` opcional) |
   | `customize.py` | Resolve overrides de uma skill (04) e devolve JSON |
   | `status.py` | Lê/valida/atualiza o `sprint-status.yaml`: `show`, `next` (próxima story `ready-for-dev`/`backlog`), `set <id> <estado>` com validação das transições do 06, `check` (consistência com os arquivos de story) |
   | `workspace.py` | Lista projetos (`workspace.md` + `docs/*/project-config.json`) e a fase de cada um — usado pelo `sdd status` e pelo Passo 0 |
   | `migrate.py` | Roda migrações declaradas pelos plugins entre versões (renomear skill, mover `custom/`, converter `execution-plan.md` antigo) |
3. **Saída sempre em JSON** e código de saída ≠ 0 em erro de validação (ex.: transição inválida), para a skill mostrar a mensagem ao usuário.
4. **Degradação sem `uv`**: cada skill que usa script tem um parágrafo "Sem `uv`": o modelo lê/edita o arquivo seguindo as mesmas regras (documentadas em `references/`). O `sdd status` avisa quando `uv` não está disponível.
5. **Consolidar o estado**: `project.md` e `workspace.md` continuam sendo o resumo para pessoas, mas passam a ser **derivados** — as skills de entrega atualizam o `sprint-status.yaml` e, a partir dele, a linha do `workspace.md` (ex.: Situação "Desenvolvimento — épico 2, 3/7 stories").

## Decisões em aberto

- **Onde ficam os scripts**: (a) copiados para `_sdd/scripts/` no setup (igual ao BMAD; funciona sem saber onde o plugin está instalado) ou (b) chamados direto da pasta do plugin (sem cópia, sempre atualizados). Verificar como uma skill descobre o caminho do próprio plugin (a skill recebe o diretório base ao ser invocada; `${CLAUDE_PLUGIN_ROOT}` vale em hooks/MCP). Recomendação: (a), pela previsibilidade, com o `sdd setup` atualizando a cópia. faça o recomendado
- Python + `uv` (igual ao BMAD) ou Node (sem dependência nova para quem já tem Node). Recomendação: Python + `uv`. faça o recomendado
- Hooks do Claude Code para validar o `sprint-status.yaml` ao salvar — opcional, avaliar depois. Implementar o hook

## Critérios de aceite

- [ ] Scripts com testes mínimos (pytest) num workspace de exemplo em `plugins/sdd/tests/fixtures/`.
- [ ] `status.py set` recusa transição inválida com mensagem clara.
- [ ] Todas as skills que usam script descrevem o modo sem `uv`.
- [ ] `sdd setup` cria `_sdd/` e grava `version.toml`; rodar de novo é idempotente.
- [ ] Testado no Windows (PowerShell) e em shell POSIX.

## Arquivos impactados

`plugins/sdd/scripts/**` (novo), `plugins/sdd/skills/sdd/**`, `.gitignore` do repositório (ignorar `__pycache__`, `.venv`).
