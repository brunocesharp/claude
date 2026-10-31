# Customização das skills (por projeto)

Adaptada do mecanismo de customização do BMAD v7 (`customize.toml` + overrides esparsos). Aqui o override é **por projeto** do workspace; os níveis de equipe e pessoal ficam para depois.

## Arquivos

| Arquivo | Onde | Quem edita |
|---------|------|------------|
| `customize.toml` | Pasta da skill, no plugin (`plugins/<plugin>/skills/<skill>/`) | Ninguém: é a base, com os campos customizáveis e os padrões. Atualizar o plugin a sobrescreve |
| `<skill>.toml` | `docs/{projeto}/_custom/` | O time (skill `sdd-customize`). Versionado com a documentação. O plugin nunca toca |

**Precedência:** override do projeto > base.

## Regras de merge

| Valor na base | Override | Resultado |
|---------------|----------|-----------|
| Escalar (texto, número, booleano) | Escalar do mesmo tipo | O override vence |
| Tabela | Tabela | Merge profundo, com as mesmas regras em cada chave |
| Lista de tabelas em que **todo** item tem `id` (ou todo item tem `code`) | Lista de tabelas com a mesma chave | Item com a mesma chave é **mesclado no lugar** (só os campos informados mudam); chave nova é acrescentada no fim |
| Outra lista | Lista | Acumula: base, depois override |
| Qualquer | Chave que não existe na base | Ignorada, com aviso (não é customizável) |
| Qualquer | Tipo diferente (tabela no lugar de lista, texto no lugar de número...) | Ignorado, com aviso |

- **Sem remoção:** o override não apaga item da base. Para desligar, use o campo que a skill oferece (ex.: `enabled = false` numa lente). Para mudar mais que isso, fale com quem mantém o plugin.
- Diferença em relação ao BMAD: lá, item com a mesma chave **substitui** o original inteiro; aqui ele é **mesclado**, para o override poder trazer só o campo que muda.

## Override esparso

Escreva no override **só o que muda**. Todo campo omitido é herdado da base — e recebe as melhorias das próximas versões do plugin. Copiar o `customize.toml` inteiro congela os padrões de hoje: o `customize.py` avisa quando mais da metade dos valores do override é igual à base.

## Campos comuns (todas as skills customizáveis)

```toml
[workflow]
persistent_facts = []            # texto literal ou "file:glob" relativo à raiz do workspace
activation_steps_prepend = []    # passos antes do fluxo
activation_steps_append = []     # passos depois do fluxo
on_complete = ""                 # ação ao terminar com sucesso
```

Ordem de ativação: resolver a customização → `activation_steps_prepend` → carregar `persistent_facts` → fluxo da skill (usando os demais campos) → `activation_steps_append` → `on_complete`.

## Skills customizáveis

| Skill | Campos próprios |
|-------|-----------------|
| `discovery-research` | `default_region`, `known_competitors`, `strong_competitor_criteria`, `min_criteria`, `max_strong_competitors` |
| `spec-functional` | `gherkin_keywords`, `template`, `extra_rules` |
| `plan-epics` | `max_stories_per_epic`, `max_size`, `checkpoint_rules`, `title_prefixes` |
| `sprint-planning` | `situacao_format` |
| `create-story` | `template`, `branch_pattern`, `extra_context_sections` |
| `dev-story` | `commands` (por `code`), `definition_of_done`, `commit_message` |
| `story-review` | `lenses` (por `id`), `block_on` |
| `retrospective` | `team_questions` |
| `correct-course` | `approvers` |
| `execucao-recorrente` | `habilitado`, `acoes`, `max_tentativas`, `commit_ao_concluir` |
| `criacao-story-recorrente` | `habilitado`, `max_prontas`, `dependencias_em`, `exige_confirmacao`, `max_tentativas` |

O `customize.toml` de cada skill descreve cada campo.

## Exemplos

`docs/loja/_custom/story-review.toml` — desliga a lente de contratos e acrescenta uma de acessibilidade:

```toml
[[workflow.lenses]]
id = "contratos"
enabled = false

[[workflow.lenses]]
id = "acessibilidade"
name = "Acessibilidade"
enabled = true
focus = "Rótulos, contraste, navegação por teclado e leitores de tela nas telas novas"
```

`docs/loja/_custom/dev-story.toml` — padrões do time e suíte via Makefile no .NET:

```toml
[workflow]
persistent_facts = ["file:docs/padroes/*.md", "Nomes de classes e métodos em inglês"]
definition_of_done = ["Swagger atualizado para endpoint novo"]

[[workflow.commands]]
code = "dotnet"
suite = "make test"
```

Resultado: a lista `definition_of_done` fica com os 3 itens padrão + o novo; o comando `dotnet` mantém `build` e `test` da base e troca só a `suite`.

## Ver o resultado

```
uv run _sdd/scripts/customize.py --skill-dir <pasta da skill> --project docs/{projeto} [--key workflow.lenses]
```

Para apagar a customização de uma skill num projeto, apague o `docs/{projeto}/_custom/<skill>.toml`: a skill volta aos padrões.
