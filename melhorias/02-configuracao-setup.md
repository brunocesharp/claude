# 02 — Configuração: perguntas do setup

- **Pedido:** "Configuração quero seguir Perguntas do bmad setup" (linha 4)
- **Tamanho:** M
- **Depende de:** — (base para 01 e 03)
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD faz
- O setup grava as respostas em `_bmad/config.toml` (equipe) e `_bmad/config.user.toml` (pessoal). São regenerados a cada setup, e o setup **lembra as respostas anteriores**.
- Para fixar uma resposta para o time, existe `_bmad/custom/config.toml` (nunca tocado pelo instalador).
- Perguntas do instalador da v6 (referência — a página da v7 não lista as perguntas; conferir no código do BMAD antes de fechar):
  - `user_name` — como o agente chama o usuário
  - `communication_language` — idioma da conversa
  - `document_output_language` — idioma dos documentos gerados
  - `output_folder` — pasta de saída dos artefatos
  - `project_name`
  - `user_skill_level` — iniciante / intermediário / experiente (ajusta o nível das explicações)
  - pastas de artefatos de planejamento, de implementação e de conhecimento do projeto
  - ferramentas/IDEs e módulos a instalar

### Como está hoje
- Só existe configuração **por projeto** (`docs/{projeto}/project-config.json`, do `discovery-init`).
- Idioma é fixo (português) dentro das skills; não há nome do usuário, nível nem preferências de time.

## Objetivo

Separar **configuração do workspace** (vale para todos os projetos, perguntada no `sdd setup`) de **configuração do projeto** (o `project-config.json` que já existe).

## Proposta

1. **Perguntas do `sdd setup`** (uma por vez, com valor padrão e "a definir" permitido):

   | Chave | Pergunta | Padrão | Arquivo |
   |-------|----------|--------|---------|
   | `user.name` | Como devo te chamar? | — | `config.user.toml` |
   | `user.skill_level` | Seu nível: iniciante, intermediário ou experiente? | intermediário | `config.user.toml` |
   | `language.conversation` | Idioma da conversa | pt-BR | `config.toml` |
   | `language.documents` | Idioma dos documentos | pt-BR | `config.toml` |
   | `paths.docs_root` | Pasta de documentação | `docs` | `config.toml` |
   | `team.backlog_prefixes` | Usar a nomenclatura da Tribo (`[TASK]`, `[HT]`...) nos itens? | sim | `config.toml` |
   | `delivery.review_depth` | Revisão padrão: rápida (1 revisor) ou completa (várias lentes)? | completa | `config.toml` |
   | `delivery.status_tracking` | Onde acompanhar o status: arquivo (`sprint-status.yaml`) ou ferramenta externa (Redmine/Jira) + arquivo | arquivo | `config.toml` |
   | `delivery.auto_mode` | Permitir `dev-story` sem supervisão para stories marcadas como seguras? | não | `config.toml` |

2. **Precedência** (igual ao BMAD): `_sdd/custom/config.user.toml` > `_sdd/custom/config.toml` > `_sdd/config.user.toml` > `_sdd/config.toml`.
3. **`.gitignore` do workspace**: o setup oferece acrescentar `_sdd/*.user.toml` e `_sdd/custom/*.user.toml`.
4. **Uso pelas skills**: o Passo 0 ganha um item "ler a configuração do workspace" (via script do 03, ou leitura direta dos TOML). As skills passam a usar `language.documents` e `user.skill_level` em vez de assumir português e nível médio.
5. **`project-config.json`** continua como está; o setup não pergunta nada de projeto.

## Decisões em aberto

- Lista final de perguntas: conferir as perguntas reais do `bmad setup` (código do módulo `bmad` no GitHub) e decidir quais fazem sentido aqui. Sim
- TOML (como o BMAD v7) ou JSON (como o `project-config.json`). Recomendação: TOML, pela compatibilidade com as regras de merge da customização (04). Usar o recomendado
- Mudar o Passo 0 em **todas** as skills de documentação (regra do `CLAUDE.md`). Sim mudar

## Critérios de aceite

- [ ] `references/config-schema.md` no hub `sdd` com cada chave, tipo, padrão e arquivo.
- [ ] Setup lembra respostas anteriores e só pergunta chaves novas numa atualização.
- [ ] Passo 0 atualizado em todas as skills de documentação, com o mesmo texto.
- [ ] Uma skill de exemplo (ex.: `discovery-vision`) respeitando `language.documents` e `user.skill_level`.

## Arquivos impactados

`plugins/sdd/skills/sdd/**`, Passo 0 de todas as skills de documentação, `CLAUDE.md` (seção Workspace).

## Resultado (30/10/2026)

**O que o código do BMAD v7 mostrou** (repositório `bmad-code-org/BMAD-METHOD`, `skills/bmad/scripts/setup.py`):
- A v7 **não** pergunta mais `user_name`, `communication_language`, `document_output_language` nem `user_skill_level` (o `migrate_v6.py` marca essas chaves como obsoletas). O núcleo só grava `project_name` e `output_folder`.
- Cada módulo declara as próprias perguntas no manifesto (`[[bmod.config_questions]]` com `key`, `prompt`, `default` e `scope` team|user). O setup lista só as pendentes, faz essas e nenhuma outra, e nunca altera um valor existente.

**Como ficou aqui:**
- O mesmo mecanismo, com registro por plugin em `plugins/sdd/skills/sdd-setup/modules/<plugin>.toml`.
- Mantive as perguntas de nome, nível e idioma, porque as skills passam a usá-las (item 6 do Passo 0).
- Saiu `delivery.status_tracking` (decisão "Redmine: não", na tarefa 06).
- `delivery.review_depth` e `delivery.auto_mode` entram com o registro do plugin de entrega (tarefas 09 e 10).
- Sem `_sdd/custom/config*.toml`: como o setup nunca regrava valores, basta editar o `config.toml`. Precedência: `config.user.toml` > `config.toml`.

**Critérios de aceite:** todos atendidos.
- `references/config-schema.md` criado.
- O setup só pergunta chaves novas (coberto por teste).
- Passo 0 atualizado em 12 skills, com o mesmo texto; o `plan-execution` tem texto próprio e usa `backlog.prefixes`.
- A `discovery-vision` serve de exemplo de uso de `user.skill_level` e `language.documents`.
