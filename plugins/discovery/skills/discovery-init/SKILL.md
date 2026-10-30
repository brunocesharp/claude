---
name: discovery-init
description: Inicia um novo projeto na pasta de documentação (workspace com vários projetos), criando docs/{projeto}/project.md, a estrutura de pastas e o registro em docs/workspace.md. Use quando o usuário disser "iniciar projeto", "novo projeto", "começar discovery", "criar projeto", "setup do projeto", "quero começar um projeto", "adicionar projeto ao workspace". NÃO use se o projeto já foi iniciado — nesses casos leia o docs/{projeto}/project.md existente.
metadata:
  version: 3.1.0
  category: discovery
  output: docs/{projeto}/project-config.json, docs/{projeto}/project.md, docs/workspace.md
---

# Discovery Init

Skill responsável por iniciar um projeto dentro da **pasta de documentação** (workspace), coletar as informações básicas, criar `docs/{projeto}/project-config.json` e `docs/{projeto}/project.md`, montar a estrutura de pastas e registrar o projeto em `docs/workspace.md`.

> **Workspace:** a raiz de trabalho é uma pasta só de documentação que reúne vários projetos. Cada projeto fica em `docs/{projeto}/` (kebab-case). O código de cada projeto continua no próprio repositório, registrado no `project.md`. Nunca crie esses arquivos no repositório de skills.

---

## Fluxo de execução

### Passo 1 — Verificar o workspace

1. Verifique se `docs/workspace.md` existe.
   - **Não existe**: este é o primeiro projeto do workspace. O arquivo será criado no Passo 5.
   - **Existe**: leia a lista de projetos.
2. Se o projeto que o usuário descreve já estiver na lista (ou já existir `docs/{projeto}/project.md`): **não sobrescreva**. Leia o arquivo, mostre os campos e pergunte se deseja atualizar algum.

---

### Passo 2 — Coletar informações do projeto

Faça as perguntas abaixo uma de cada vez, em tom conversacional:

1. **Nome do projeto**
   - "Qual é o nome do projeto?"
   - Proponha a pasta em kebab-case, sem acentos (ex.: "Gestão de Estoque" → `gestao-de-estoque`), e confirme antes de criar.

2. **Descrição resumida**
   - "Em uma frase, qual é a ideia central desse projeto?"

3. **Repositório de código**
   - "O código fica em um repositório só ou em vários (ex.: backend e frontend separados)?"
   - **Um**: "Qual é a URL do repositório? (ex.: https://github.com/org/repo)" e "Ele está clonado nesta máquina? Em qual pasta?" — o caminho local é usado por skills que leem o código (`arch-c4` em sistema existente, `business-docs`).
   - **Vários**: registre na seção Repositório o apontamento para `docs/{projeto}/repositorios.md` e, no Passo 6, ofereça cadastrar os repositórios com a skill `multi-repo`.
   - Se ainda não existir, registre `a definir` e siga.

4. **Tipo de projeto** *(opcional)*
   - "Que tipo de sistema é esse? (ex.: web app, API, mobile, integração)"

5. **Stack principal** *(opcional)*
   - "Qual é a tecnologia principal? (ex.: .NET, Angular, Java)" — ajuda as skills a escolher as skills de código.

6. **Responsável** *(opcional)*

---

### Passo 3a — Gerar `docs/{projeto}/project-config.json`

Lido pelas outras skills no Passo 0. Descrição de cada campo em `references/project-config-schema.md`.

```json
{
  "name": "{Nome do Projeto}",
  "slug": "{projeto}",
  "version": "1.0.0",
  "docs_root": "docs/{projeto}",
  "repositories": "um",
  "repository_url": "{url ou a definir}",
  "code_path": "{caminho local ou a definir}",
  "project_type": "{tipo do projeto ou a definir}",
  "tech_stack": "{stack ou a definir}",
  "responsible": "{responsável ou a definir}",
  "created_at": "{data atual no formato DD/MM/YYYY}"
}
```

Com vários repositórios: `"repositories": "varios"` e `repository_url`/`code_path` com `"ver repositorios.md"`.

### Passo 3b — Gerar `docs/{projeto}/project.md`

```markdown
# {Nome do Projeto}

## Visão Geral
{Descrição resumida fornecida pelo usuário}

## Repositório
- URL: {url ou "a definir"}
- Código local: {caminho local ou "a definir"}
- Tipo: {tipo do projeto ou "a definir"}

## Metadados
- Pasta: `docs/{projeto}/`
- Iniciado em: {data atual no formato DD/MM/YYYY}
- Responsável: {nome ou "a definir"}

## Estrutura de Documentação
- Discovery: `docs/{projeto}/discovery/`
- Escopo: `docs/{projeto}/escopo/`
- Especificação: `docs/{projeto}/especificacao/`
- Arquitetura: `docs/{projeto}/arquitetura/`
- Plano de execução: `docs/{projeto}/plano-execucao/`
- Regras de negócio: `docs/{projeto}/business/`

## Status das Fases
- [ ] Discovery
- [ ] Escopo
- [ ] Especificação
- [ ] Arquitetura
- [ ] Plano de Execução
- [ ] Homologação
- [ ] Produção
```

**Projeto com vários repositórios:** na seção Repositório, troque as linhas URL e Código local por `- Repositórios: vários, ver docs/{projeto}/repositorios.md`. O cadastro de cada repositório é feito pela skill `multi-repo`.

---

### Passo 4 — Criar a estrutura de pastas

Pergunte:

> "Deseja que eu crie agora a estrutura de pastas de documentação para este projeto?"

**Se sim**, crie as pastas com `.gitkeep`:
```
docs/{projeto}/discovery/.gitkeep
docs/{projeto}/escopo/.gitkeep
docs/{projeto}/especificacao/.gitkeep
docs/{projeto}/arquitetura/.gitkeep
docs/{projeto}/plano-execucao/.gitkeep
```

**Se não**, informe que as pastas são criadas pelas próprias skills quando forem usadas.

---

### Passo 5 — Registrar no `docs/workspace.md`

Se o arquivo não existir, crie com o template abaixo. Se existir, acrescente uma linha na tabela (mantenha a ordem alfabética) sem alterar as demais.

```markdown
# Workspace de Documentação

Pasta de documentação que reúne vários projetos. Cada projeto fica em `docs/{projeto}/`.
As skills identificam o projeto pelo nome citado na conversa ou por esta lista.

## Projetos

| Projeto | Pasta | Repositório | Código local | Situação |
|---------|-------|-------------|--------------|----------|
| {Nome} | `docs/{projeto}/` | {url ou "a definir"} | {caminho ou "a definir"} | Discovery |

## Arquitetura do conjunto

Visão de todos os sistemas e de como se relacionam (System Landscape): `docs/arquitetura/landscape.md`
(gerado pela skill `arch-c4` quando houver mais de um sistema relacionado).
```

Projeto com vários repositórios: nas colunas Repositório e Código local, registre `vários (ver docs/{projeto}/repositorios.md)`.

A coluna **Situação** acompanha a fase atual do projeto (Discovery, Escopo, Especificação, Arquitetura, Desenvolvimento, Produção). As outras skills atualizam essa coluna quando avançam de fase.

---

### Passo 6 — Sugerir próximos passos

> "O projeto **{nome}** foi iniciado em `docs/{projeto}/` e registrado no workspace. As próximas etapas do discovery são:
> - **Visão do projeto** — problema, público-alvo e proposta de valor
> - **Oportunidades** — dores e jobs to be done
> - **Hipóteses e premissas** — o que ainda precisa ser validado
> - **Stakeholders** — envolvidos e seus interesses
> - **Métricas de sucesso** — como medir o sucesso
>
> Se for um sistema que já existe, também dá para começar pela **arquitetura (C4)** a partir do código.
> {Se tiver vários repositórios:} Antes, vale cadastrar os repositórios (`multi-repo`), para as skills saberem onde está cada parte do código.
>
> Por onde quer começar?"

---

## Regras importantes

- Todos os arquivos vão para a **pasta de documentação (workspace)** — nunca para o repositório de skills nem para o repositório de código.
- Todo projeto fica em `docs/{projeto}/`, mesmo que o workspace tenha um só projeto.
- Nome de pasta em kebab-case, sem acentos, confirmado com o usuário.
- Crie sempre os dois: `project-config.json` (lido pelas skills) e `project.md` (resumo para pessoas), coerentes entre si.
- Nunca sobrescreva um `project.md` ou `project-config.json` existente sem confirmação explícita.
- Nunca reescreva o `workspace.md` inteiro: só acrescente ou atualize a linha do projeto.
- Se o usuário não souber responder algo, registre como `a definir` e siga.
- Se o workspace for um repositório Git, não faça commit nem push sem o usuário pedir.

---

## Troubleshooting

**`project.md` já existe para esse projeto**
Não sobrescreva. Leia o conteúdo atual, apresente os campos e pergunte: "Deseja atualizar algum campo?"

**Projeto tem `project.md` mas não tem `project-config.json`**
Projeto criado antes do config. Monte o config a partir dos campos do `project.md`, mostre e crie após confirmação.

**Projeto existe em `docs/` mas não está no `workspace.md`**
Acontece com projetos criados antes do workspace. Leia o `project.md` e acrescente a linha no `workspace.md`.

**Documentos antigos em `docs/` sem pasta de projeto** (ex.: `docs/project.md`, `docs/discovery/`)
Estrutura anterior, de um projeto por repositório (inclusive com `docs/project-config.json`). Proponha mover para `docs/{projeto}/` (com `git mv`, se for repositório Git) e só mova após confirmação.

**Projeto de um repositório passou a ter vários**
Use a skill `multi-repo` (Cadastrar): ela cria `docs/{projeto}/repositorios.md` com o repositório atual e os novos, e atualiza o `project.md` e o `workspace.md`.

**Nome do projeto com caracteres especiais ou acentos**
Normalize para kebab-case sem acentos (ex.: "Gestão de Estoque" → `gestao-de-estoque`) e confirme.

**Usuário quer iniciar mais de um projeto na mesma conversa**
Execute o fluxo completo para cada projeto, um de cada vez; cada um ganha a própria pasta e a própria linha no `workspace.md`.
