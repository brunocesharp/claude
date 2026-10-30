# 01 — Instalação no estilo BMAD v7 e hub `sdd`

- **Pedido:** "Instalação da v7, quero seguir o mesmo conceito do BMAD" (linha 3)
- **Tamanho:** M
- **Depende de:** 02 (perguntas do setup) — fazer junto
- **Situação:** [x] implementada em 30/10/2026 — plugin `sdd`, skill `sdd-setup` (o nome decidido estava escrito "ssd-setup"; usei `sdd-setup`, igual ao plugin). Skills CLI testado: `npx skills add <repo> --list` encontra todas as skills no layout atual. Falta testar a instalação real pelo marketplace num workspace.

## Contexto

### Como o BMAD v7 faz
- Instala as skills com o Skills CLI: `npx skills add bmad-code-org/BMAD-METHOD --skill '*'` (ou seletivo, por nome), ou pelo marketplace de plugins do Claude Code (`/plugin marketplace add bmad-code-org/bmad-plugins`).
- Instalação e configuração são **dois passos**: instalar as skills e depois pedir à skill hub `bmad` para rodar `bmad setup`, que cria `_bmad/` (configuração, scripts, `custom/`) na raiz do projeto ou do workspace.
- O hub também tem `bmad status` (verifica instalação e versões) e responde "o que vem agora?".
- Atualização: `bmad setup` de novo, que compara versões, roda `npx skills update`, faz perguntas novas e migrações (renomeação de skills, mover customizações).
- Para vários repositórios, o setup é feito **na raiz do workspace**.

### Como está hoje
- Só o marketplace de plugins (`/plugin marketplace add brunocesharp/claude` + `/plugin install <plugin>@claude`), documentado no README.
- Não existe passo de setup: o primeiro contato é o `discovery-init`, que já cria arquivos de projeto.
- Não há skill de ajuda/estado geral.

## Objetivo

Ter um ponto de entrada único — a skill **`sdd`** — que instala/configura o workspace, mostra o estado e diz qual é o próximo passo, no mesmo papel do hub `bmad`.

## Proposta

1. **Plugin novo `sdd`** com a skill `sdd` (hub). Comandos por linguagem natural:
   - `sdd setup` — primeira configuração ou atualização do workspace (perguntas no 02; cria `_sdd/` do 03).
   - `sdd status` — versões dos plugins instalados x versão gravada no `_sdd/config.toml`, projetos do workspace e, por projeto, a fase e o resumo do `sprint-status.yaml` (quando existir).
   - `sdd ajuda` / "o que faço agora?" — lê o estado e recomenda a próxima skill (ex.: escopo sem spec → `spec-functional`; story `ready-for-dev` → `dev-story` numa sessão nova).
2. **Dois caminhos de instalação**, documentados no README:
   - Marketplace de plugins (o atual) — continua sendo o principal.
   - Skills CLI (`npx skills add brunocesharp/claude --skill '*'`) — avaliar se o repositório funciona com o Skills CLI no layout atual (`plugins/*/skills/*`). Se não funcionar sem mudar a estrutura, registrar como fora de escopo.
3. **Setup no workspace**, não no repositório de skills: `_sdd/` fica na raiz da pasta de documentação, ao lado de `docs/`.
4. **Atualização**: `sdd setup` detecta que `_sdd/config.toml` existe, compara a versão gravada com a dos plugins, faz só as perguntas novas e roda migrações declaradas (ver 03, `migrations/`).
5. **`discovery-init`** passa a verificar se o setup foi feito: sem `_sdd/config.toml`, oferece rodar `sdd setup` antes (sem bloquear).

## Decisões em aberto

- Nome do plugin e da skill (`sdd`? `sdd-full`?). O nome da skill é como o usuário a chama. nome: ssd-setup
- Manter o Skills CLI como segundo caminho ou só o marketplace. manter como segundo caminho
- O hub deve instalar plugins que faltam (como o BMAD instala skills ausentes) ou só avisar com o comando? Recomendação: só avisar e mostrar o comando `/plugin install`. Faça o recomendado

## Critérios de aceite

- [ ] `plugins/sdd/.claude-plugin/plugin.json` e `plugins/sdd/skills/sdd/SKILL.md` com frontmatter válido; plugin registrado no `marketplace.json`.
- [ ] `sdd setup` num workspace vazio cria `_sdd/` e termina sugerindo `discovery-init`.
- [ ] `sdd setup` num workspace já configurado não sobrescreve nada sem confirmação e só pergunta o que é novo.
- [ ] `sdd status` funciona com e sem `uv` instalado.
- [ ] README: seção de instalação com os dois passos (instalar plugins → `sdd setup`); `0.0 - contexto-projeto-skills.md` e `CLAUDE.md` atualizados.

## Arquivos impactados

`.claude-plugin/marketplace.json`, `plugins/sdd/**` (novo), `plugins/discovery/skills/discovery-init/SKILL.md`, `README.md`, `CLAUDE.md`, `0.0 - contexto-projeto-skills.md`.

## Fora do escopo

Publicar em skills.sh ou em outro registro; suporte a outras ferramentas (Codex etc.).
