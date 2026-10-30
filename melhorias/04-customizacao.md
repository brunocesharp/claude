# 04 — Customização das skills

- **Pedido:** "Quero adicionar a opção de customização" (linha 6)
- **Tamanho:** G
- **Depende de:** 02, 03
- **Situação:** [x] implementada em 30/10/2026 — ver "Resultado" no fim.

## Contexto

### Como o BMAD v7 faz
- Cada skill tem um `customize.toml` (schema do que é customizável) que **não se edita**.
- Overrides ficam em `_bmad/custom/<skill>.toml` (equipe, versionado) e `_bmad/custom/<skill>.user.toml` (pessoal, no `.gitignore`). Precedência: pessoal > equipe > base.
- Regras de merge: escalar substitui; tabela faz merge profundo; array de tabelas com `code`/`id` substitui por chave e acrescenta as novas; outros arrays acumulam; **não há remoção** (para suprimir, sobrescreve com efeito neutro; para mais, fork).
- O que se customiza: persona do agente, `persistent_facts` (fatos literais ou `file:` com glob), `principles`, `activation_steps_prepend`/`append`, `on_complete`, menu, e campos próprios de cada workflow (caminhos de saída, templates, toggles, lentes da revisão).
- Overrides devem ser **esparsos** (copiar o `customize.toml` inteiro congela os padrões e esconde melhorias futuras).
- Skill `bmad-customize` escreve o override e mostra o resultado resolvido.

### Como está hoje
- Não há customização. Configuração específica de projeto já vai para `docs/{projeto}/` (ex.: mapa de áreas do `business-docs`), mas o comportamento das skills só muda editando o `SKILL.md` — e isso se perde na atualização do plugin.

## Objetivo

Permitir que o time e cada pessoa ajustem templates, convenções e passos das skills sem editar os plugins e sem perder os ajustes nas atualizações.

## Proposta

1. **`customize.toml` em cada skill que aceitar customização**, começando pelas de maior valor:
   | Skill | Campos customizáveis |
   |-------|----------------------|
   | `plan-epics` / `create-story` (07, 08) | template da story, seções obrigatórias, nomenclatura de itens, tamanho máximo de story |
   | `dev-story` (09) | comandos de build/teste por stack, Definição de Pronto, se roda `code-review` ao final |
   | `code-review` (10) | lentes da revisão, mínimo de achados, profundidade padrão |
   | `spec-functional` | idioma do Gherkin, template |
   | `architecture-*` | convenções de nome, pastas, bibliotecas (ex.: MediatR x outro mediador) |
   | todas | `persistent_facts` (ex.: `file:docs/padroes/*.md`), `activation_steps_prepend`/`append`, `on_complete` |
2. **Overrides no workspace**: `_sdd/custom/<skill>.toml` e `_sdd/custom/<skill>.user.toml`, com as mesmas regras de merge e precedência do BMAD (implementadas em `customize.py`, 03).
3. **Override por projeto** (extensão nossa, útil no workspace com vários projetos): `docs/{projeto}/_custom/<skill>.toml`, entre o de equipe e o pessoal. Precedência final: pessoal > projeto > equipe > base.
4. **Ativação padrão nas skills** (bloco no início de cada `SKILL.md` customizável): resolver a customização → `activation_steps_prepend` → carregar `persistent_facts` → configuração → fluxo da skill → `activation_steps_append` / `on_complete`.
5. **Skill `sdd-customize`** (ou modo do hub `sdd`): pergunta o que mudar, grava o override **esparso**, mostra o resultado resolvido e avisa se o override está copiando a base inteira.

## Decisões em aberto

- Incluir o nível "projeto" (item 3) ou ficar só com equipe/pessoal como o BMAD. Só tem projeto por enquanto
- Quais skills entram na primeira leva. Recomendação: só as skills novas do fluxo de entrega (07–12) + `spec-functional`; as `architecture-*` numa segunda leva. Faça o recomendado
- Persona/agentes: o BMAD customiza personas (PO, dev, arquiteto). Aqui não há agentes com persona — decidir se faz sentido criar (fora do pedido). Deixar de fora por enquanto.

## Critérios de aceite

- [ ] `references/customizacao.md` no plugin `sdd` com regras de merge, precedência e exemplos.
- [ ] `customize.py` com testes cobrindo cada regra de merge.
- [ ] Ao menos 3 skills com `customize.toml` e o bloco de ativação.
- [ ] Atualizar o plugin não altera nada em `_sdd/custom/`.
- [ ] README com seção "Customizar as skills".

## Arquivos impactados

`plugins/sdd/**`, `customize.toml` nas skills escolhidas, `README.md`, `CLAUDE.md` (padrões de design das skills).

## Resultado (30/10/2026)

**Arquivos:**
- `customize.toml` na pasta de cada skill: a base, com os campos e os padrões comentados.
- `docs/{projeto}/_custom/<skill>.toml`: o override do projeto. Atualizar o plugin nunca toca esse arquivo, o que atende ao critério "atualizar o plugin não altera os overrides".
- O nível do override é **só o projeto**, como decidido.

**Primeira leva (8 skills):** `spec-functional`, `plan-epics`, `sprint-planning`, `create-story`, `dev-story`, `story-review`, `retrospective` e `correct-course`. Campos comuns:
- `persistent_facts` (texto ou `file:glob`);
- `activation_steps_prepend` e `activation_steps_append`;
- `on_complete`.

Campos próprios de cada skill:

| Skill | Campos |
|-------|--------|
| `spec-functional` | `gherkin_keywords`, `template`, `extra_rules` |
| `plan-epics` | `max_stories_per_epic`, `max_size`, `checkpoint_rules`, `title_prefixes` |
| `sprint-planning` | `situacao_format` |
| `create-story` | `template`, `branch_pattern`, `extra_context_sections` |
| `dev-story` | `commands` (por `code`), `definition_of_done`, `commit_message` |
| `story-review` | `lenses` (por `id`; desligar com `enabled = false` ou acrescentar), `block_on` |
| `retrospective` | `team_questions` |
| `correct-course` | `approvers` |

**Bloco de ativação** `## Customização (por projeto)` em cada uma das 8 skills, com a ordem: prepend → fatos → campos → append/on_complete. O bloco lista onde cada campo é usado e traz o caminho sem `uv`.

**`customize.py`:**
- Regras de merge do BMAD: um valor simples é substituído; uma tabela é mesclada em profundidade; uma lista de tabelas com `id`/`code` é mesclada item a item; as demais listas acumulam.
- Chave desconhecida e tipo errado são ignorados, com aviso.
- **Desvio do BMAD:** um item com o mesmo `id` é *mesclado*, em vez de substituído inteiro, para o override ser esparso.
- Expande `file:glob` dos fatos e avisa quando o override não é esparso.
- `--skill <nome>` localiza a skill instalada: pelo `installed_plugins.json` (respeitando `CLAUDE_CONFIG_DIR`), pelo `.claude/skills/` do Skills CLI ou pelo repositório local. O layout do cache foi conferido nesta máquina: `cache/<marketplace>/<plugin>/<versão>/skills/<skill>`.

**Skill `sdd-customize`** (plugin `sdd`): mostra os campos, traduz o pedido em campos sem inventar campo, grava o override esparso e confere o resultado.

**Fora desta leva:** personas (decisão: deixar de fora); as `architecture-*` (segunda leva); níveis de equipe e pessoal.

**Critérios de aceite:**
- `references/customizacao.md` com regras, precedência e exemplos: feito.
- Testes de cada regra de merge, da localização e dos 8 `customize.toml` + bloco de ativação: 75 testes no total.
- Ao menos 3 skills customizáveis: são 8.
- README com a seção "Customizar as skills": feito.
