---
name: sdd-setup
description: Hub do workspace de documentação. Faz o setup e a atualização da configuração do workspace (pasta _sdd/ com config.toml, config.user.toml e scripts), mostra o status da instalação (plugins, versões, perguntas pendentes, projetos) e recomenda o próximo passo do fluxo. Use quando o usuário disser "sdd setup", "configurar o workspace", "setup", "instalar", "atualizar o sdd", "atualizar a configuração", "mudar a configuração", "mudar idioma", "sdd status", "status da instalação", "o que está instalado", "por onde começo", "o que faço agora", "qual o próximo passo", "ajuda com as skills". NÃO use para iniciar um projeto (use discovery-init), cadastrar repositórios (use multi-repo) ou customizar uma skill.
metadata:
  version: 1.0.0
  category: workspace
  output: _sdd/config.toml, _sdd/config.user.toml, _sdd/version.toml, _sdd/scripts/
---

# SDD Setup

Ponto de entrada do workspace. Três ações, que podem vir juntas:

| Ação | Quando | Grava? |
|------|--------|--------|
| **Setup / atualizar** | Primeira vez no workspace, plugin atualizado, pergunta nova, mudar uma resposta | Sim, em `_sdd/` |
| **Status** | "o que está instalado", "está tudo certo?" | Não |
| **Ajuda** | "por onde começo", "o que faço agora" | Não |

Leia antes de executar:
- `references/config-schema.md` — chaves de configuração, arquivos, precedência e como as skills leem.
- `references/proximos-passos.md` — como recomendar o próximo passo (ação Ajuda).
- `references/sprint-status.md` — formato, estados e transições do `sprint-status.yaml` (quadro de entrega de cada projeto).

## Scripts

| Script | Onde roda | Faz |
|--------|-----------|-----|
| `setup.py` | `${CLAUDE_SKILL_DIR}/scripts/` | Status da instalação, perguntas pendentes, grava `_sdd/` |
| `migrate.py` | `${CLAUDE_SKILL_DIR}/scripts/` | Lista e registra migrações declaradas pelos módulos |
| `config.py` | `_sdd/scripts/` (cópia) | Configuração resolvida, em JSON |
| `workspace.py` | `_sdd/scripts/` (cópia) | Projetos: fase, situação, repositórios, quadro do sprint e próxima ação |
| `status.py` | `_sdd/scripts/` (cópia) | Lê, valida e muda estados do `sprint-status.yaml`; `sync` com os épicos |
| `epics.py` | `_sdd/scripts/` (cópia) | Valida os arquivos de épico, a cobertura cenário → story e extrai o texto literal da spec |
| `story.py` | `_sdd/scripts/` (cópia) | Confere a completude do arquivo de uma story |
| `review.py` | `_sdd/scripts/` (cópia) | Revisão: diff de todos os repositórios da story e integridade do registro (Arquivos alterados × git) |
| `session.py` | `_sdd/scripts/` (cópia) | Monta (e, com confirmação, executa) o comando que abre uma sessão nova do Claude numa janela de terminal |

Os de `_sdd/scripts/` são usados também pelas skills dos outros plugins. O plugin traz ainda um hook que valida o `sprint-status.yaml` sempre que o Claude grava ou edita esse arquivo (precisa do `uv`; sem ele, o hook não faz nada).

---

## Onde fica o `_sdd/`

`_sdd/` fica na **raiz do workspace de documentação** (a pasta que contém `docs/`), nunca no repositório de skills nem num repositório de código.

- `{workspace}` = a pasta mais próxima, a partir do diretório atual e subindo, que contém `_sdd/`.
- Sem `_sdd/` em nenhum nível: é o primeiro setup e `{workspace}` é o diretório atual. Antes de criar, confira: se o diretório atual for um repositório de código (tem `.git` e `*.sln`, `package.json`, `pom.xml`... sem `docs/`) ou este repositório de skills (tem `.claude-plugin/marketplace.json`), avise e pergunte qual é a pasta de documentação.

## Como chamar o script

```
uv run --no-cache "${CLAUDE_SKILL_DIR}/scripts/setup.py" --workspace-root "{workspace}" [--modules <códigos>] <modo>
```

- Sem `uv`: use `python "${CLAUDE_SKILL_DIR}/scripts/setup.py" ...` (precisa de Python 3.11 ou mais novo; `setup.py`, `migrate.py` e `config.py` não têm dependências; `workspace.py` e `status.py` precisam do pacote `pyyaml`). Sem nenhum dos dois, diga isso, sugira instalar o `uv` (https://docs.astral.sh/uv/) e, se o usuário quiser seguir mesmo assim, faça à mão: grave a configuração seguindo `references/config-schema.md` e leia os arquivos do projeto (`project.md`, `workspace.md`, `sprint-status.yaml`) diretamente.
- `--modules`: os módulos instalados, separados por vírgula. Um módulo está instalado quando ao menos uma das skills dele aparece na sua lista de skills disponíveis (com ou sem o prefixo do plugin, ex.: `spec-plan:spec-functional`). Os módulos e as skills de cada um estão no `--status` (campo `modules`); na primeira chamada, omita `--modules`.
- Cada chamada imprime um JSON. Em erro, imprime `error: <mensagem>` e sai com código 1: mostre a mensagem e pare.

---

## Ação 1 — Status

Rode com `--status`. Ele não grava nada. Mostre ao usuário:

1. **Instalação**: `_sdd/` existe? `python` e `uv` disponíveis?
2. **Módulos**: para cada um, a versão e se está instalado (pelas suas skills disponíveis). `state`: `new` (ainda não passou pelo setup), `updated` (o plugin mudou de versão desde o último setup), `current`. Módulo não instalado: mostre o comando do campo `install` — **não instale**; quem instala é o usuário.
3. **Configuração**: `pending_questions` > 0 significa pergunta nova sem resposta.
4. **Scripts** em `_sdd/scripts/`: `missing` ou `stale` pedem atualização.
5. **Git**: `gitignore` = `unprotected` significa que o `config.user.toml` (pessoal) pode ir para o Git.
6. **Projetos**: rode `uv run _sdd/scripts/workspace.py` (a partir de `{workspace}`; antes do primeiro setup, use os `projects` do `--status`). Para cada projeto: fase atual (`phases.current`), Situação do `workspace.md`, um ou vários repositórios e, se houver `sprint-status.yaml`, o quadro por épico (`done`/`total`) e a próxima ação (`sprint.next`). `has_config: false` = projeto antigo sem `project-config.json` (o `discovery-init` resolve); `sprint.valid: false` = mostre os `problems`.
7. **Migrações**: rode `uv run "${CLAUDE_SKILL_DIR}/scripts/migrate.py" --workspace-root "{workspace}"`. Lista vazia = nada a migrar.

Termine com o `next`: `setup` (nunca configurado), `update` (há o que atualizar), `discovery-init` (nenhum projeto) ou nada a fazer. Se o usuário pediu setup ou atualização, siga direto para a Ação 2 sem perguntar de novo.

## Ação 2 — Setup / atualizar

Na ordem. Na primeira vez, faça tudo; numa atualização, só o que o status apontou.

1. **Perguntas.** Rode com `--list-config-questions` (com `--modules`). Ele devolve só as perguntas **sem resposta**: `[{module, key, prompt, default, scope}]`. Faça uma por vez, nesta ordem e nenhuma outra, mostrando o padrão. Quando `scope` = `user`, diga que a resposta é pessoal e não vai para o Git. Resposta vazia ou "pode ser" = o padrão, exatamente como veio. Lista vazia: pule para o passo 2.
2. **Gravar.** Com respostas, escreva-as com a ferramenta Write num JSON temporário na raiz do workspace, `{workspace}/.sdd-answers.json` (outro nome se existir):
   ```json
   { "workspace.name": "docs-time", "user.name": "Ana", "language.documents": "pt-BR" }
   ```
   Rode sem modo, com `--answers "{workspace}/.sdd-answers.json"` (o script apaga o arquivo). Sem respostas, rode sem modo e sem `--answers`: isso atualiza os scripts e as versões.
   O script cria `_sdd/`, **acrescenta** as chaves novas em `config.toml` (equipe) e `config.user.toml` (pessoal) sem alterar valores existentes, copia os scripts para `_sdd/scripts/` e grava `_sdd/version.toml`.
3. **Relatar** o JSON: `sdd` (`created`/`updated`), chaves gravadas em cada arquivo, scripts `created`/`updated`/`unchanged`, versões.
4. **Git.** Se `gitignore` = `unprotected`, ofereça acrescentar `_sdd/*.user.toml` ao `.gitignore` do workspace; com o sim, rode com `--gitignore`. Nunca faça commit.
5. **Respostas.** No primeiro setup, mostre todas as respostas (`answers`) com o arquivo de cada uma e ofereça mudar alguma.
6. **Migrações.** Rode `migrate.py` (como no Status). Para cada migração listada, mostre `title` e as versões e pergunte se aplica. Com o sim, siga o guia (`guide`) passo a passo, com as confirmações que ele pedir, e ao terminar registre com `--mark-applied <id>`. Migrações `optional` (ex.: converter um formato antigo) só aparecem com `--all` ou quando o usuário pede.
7. **Próximo passo.** Sem projetos: sugira `discovery-init`. Com projetos: siga a Ação 3.

### Mudar uma resposta

O setup nunca altera um valor existente. Para mudar (ex.: "documentos em inglês"), edite a linha da chave no arquivo certo (`scope` team → `_sdd/config.toml`; user → `_sdd/config.user.toml`) com a ferramenta Edit, mostrando antes e depois. Para valer só para você um valor da equipe, acrescente a chave no `config.user.toml`.

### Atualizar os plugins

O setup não atualiza plugins. Se o usuário quer a versão nova, mostre:
```
/plugin marketplace update claude
/reload-plugins
```
e depois rode a Ação 2 de novo (versões, perguntas novas e scripts).

## Ação 3 — Ajuda (próximo passo)

Siga `references/proximos-passos.md`: leia o estado do projeto (com `workspace.py`, quando houver `_sdd/`), recomende **uma** skill com o motivo e sugira rodá-la numa sessão nova (`/clear`) quando ela for longa. Ofereça rodar aqui. Responda só com skills instaladas; se a skill certa estiver num plugin não instalado, mostre o `/plugin install`.

---

## Regras importantes

- Tudo o que esta skill grava fica em `{workspace}/_sdd/` (e no `.gitignore`, com confirmação). Nada em `docs/`, nos repositórios de código ou no repositório de skills.
- Nunca altere um valor de configuração existente sem o usuário pedir. Nunca apague `_sdd/`.
- Faça só as perguntas que o script devolveu.
- Nunca faça commit, push ou instalação de plugin.
- Fale no idioma de `language.conversation` e chame o usuário por `user.name` quando já existirem.

## Troubleshooting

**`error: ... não é um TOML válido`** — alguém editou o arquivo à mão e quebrou a sintaxe. Mostre a linha e proponha a correção (valores entre aspas: `chave = "valor"`).

**Pasta errada** — `_sdd/` foi criado no repositório de código ou de skills. Não apague sozinho: explique e pergunte se pode mover para a pasta de documentação.

**Configuração diferente em cada máquina** — o que é do time vai no `config.toml` (versionado); o que é de cada pessoa, no `config.user.toml`.
