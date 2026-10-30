# Configuração do workspace (`_sdd/`)

Criada e atualizada pela skill `sdd-setup`; lida por todas as skills de documentação no Passo 0.

## Arquivos

```
{workspace}/
├── _sdd/
│   ├── config.toml         # equipe — versionado no Git
│   ├── config.user.toml    # pessoal — no .gitignore (_sdd/*.user.toml)
│   ├── version.toml        # versões do último setup (gerado, não editar)
│   └── scripts/            # cópia dos scripts de runtime: config.py, workspace.py, status.py, epics.py, sddlib.py
└── docs/                   # (ou o valor de paths.docs_root)
```

**Precedência:** `config.user.toml` vence `config.toml`.

**Formato:** só chaves pontuadas na raiz, valores texto entre aspas, sem cabeçalhos `[tabela]`:

```toml
workspace.name = "docs-time"
language.documents = "pt-BR"
```

O setup só **acrescenta** chaves que faltam, no fim do arquivo. Valores existentes nunca são alterados por ele: para mudar, edite a linha.

Configuração **do projeto** (nome, stack, repositório) continua em `docs/{projeto}/project-config.json` (`discovery-init`). O setup não pergunta nada de projeto.

## Chaves

| Chave | Módulo | Arquivo | Padrão | Uso |
|-------|--------|---------|--------|-----|
| `workspace.name` | sdd | config.toml | nome da pasta | Título do workspace no `sdd-setup` e no `docs/workspace.md` |
| `user.name` | sdd | config.user.toml | usuário do sistema | Como as skills chamam a pessoa |
| `user.skill_level` | sdd | config.user.toml | `intermediario` | `iniciante`: explica termos e o porquê de cada pergunta, dá exemplos; `intermediario`: explica só o que não é óbvio; `experiente`: direto, sem explicações de conceito |
| `language.conversation` | sdd | config.user.toml | `pt-BR` | Idioma da conversa |
| `language.documents` | sdd | config.toml | `pt-BR` | Idioma dos documentos gerados (títulos de seção dos templates inclusive) |
| `paths.docs_root` | sdd | config.toml | `docs` | Pasta de documentação. Diferente de `docs`: as skills trocam `docs/` por ela em todos os caminhos |
| `backlog.prefixes` | spec-plan | config.toml | `sim` | `sim`: títulos com `[FEATURE]`, `[TASK]`, `[HT]`...; `nao`: títulos sem prefixo |

Termos de código (nomes de classe, chaves, cenários Gherkin `Dado/Quando/Então` ou `Given/When/Then`) seguem `language.documents`.

## Como as skills leem (Passo 0, item 6)

1. Leia `_sdd/config.toml` e `_sdd/config.user.toml` na raiz do workspace (o pessoal vence). Ou rode `uv run _sdd/scripts/config.py --key <chave>` (JSON).
2. Sem `_sdd/`: use os padrões da tabela e sugira **uma vez** na conversa rodar o `sdd-setup`. Não bloqueie.
3. Chave ausente (setup antigo): use o padrão e siga; o próximo `sdd-setup` pergunta.

## Perguntas de um plugin (para quem mantém o marketplace)

Cada plugin que tem perguntas declara um registro em `plugins/sdd/skills/sdd-setup/modules/<plugin>.toml`:

```toml
[module]
code = "spec-plan"            # código do módulo (chave em version.toml)
plugin = "spec-plan"          # pasta em plugins/ e nome do /plugin install
version = "1.0.0"             # igual ao plugin.json do plugin
skills = ["spec-functional", "plan-execution"]

[[module.config_questions]]
key = "backlog.prefixes"      # única entre todos os módulos
prompt = "Pergunta mostrada ao usuário"
default = "sim"               # texto; aceita {directory_name} e {os_user}
scope = "team"                # team (padrão) ou user
```

Migrações (ex.: renomear uma skill, converter um formato antigo) também são declaradas no registro e listadas pelo `migrate.py`; os passos ficam num guia em `references/migracoes/<id>.md`:

```toml
[[module.migrations]]
id = "execution-plan-para-epicos"
title = "Converter execution-plan.md em épicos e stories"
kind = "optional"             # upgrade: pendente quando a versão gravada < to; optional: só a pedido
to = "1.1.0"
guide = "references/migracoes/execution-plan-para-epicos.md"
```

Ao subir a versão de um plugin, suba também a do registro (o teste `test_versao_dos_registros_igual_ao_plugin_json` confere). Pergunta nova aparece no próximo `sdd-setup` de cada workspace; as já respondidas não são repetidas. Mecanismo adaptado do `bmad setup` (BMAD v7: `[[bmod.config_questions]]` com `key`, `prompt`, `default` e `scope`).
