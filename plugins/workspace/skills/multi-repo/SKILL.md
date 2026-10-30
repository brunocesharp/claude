---
name: multi-repo
description: Organiza projetos cujo código está em vários repositórios (backend, frontend, mobile, infraestrutura, bibliotecas), a partir da pasta de documentação. Cadastra os repositórios de cada projeto em docs/{projeto}/repositorios.md, mostra o panorama do Git em todos eles (branch, alterações, atrás/à frente), clona os que faltam, indica em qual repositório cada tarefa roda e coordena mudanças que atravessam repositórios (mesma branch, ordem de merge e de deploy, compatibilidade de contratos). Use quando o usuário mencionar "vários repositórios", "multi repo", "multirepo", "repositórios do projeto", "cadastrar repositório", "adicionar repositório", "status dos repositórios", "como estão os repositórios", "clonar os repositórios", "preparar o ambiente", "criar branch em todos", "feature em mais de um repositório", "em qual repositório fica", "ordem de deploy entre repositórios". NÃO use para iniciar um projeto (use discovery-init), documentar a arquitetura (use arch-c4), planejar as tarefas (use plan-execution) ou gerar código (use architecture-* ou angular-*).
metadata:
  version: 1.0.0
  category: workspace
  depends-on: discovery-init
  output: docs/{projeto}/repositorios.md, docs/{projeto}/plano-execucao/{escopo}/mudanca-multi-repo.md
---

# Multi-repo

Mantém o mapa **projeto → repositórios** dentro da pasta de documentação e ajuda a trabalhar com o código espalhado por vários repositórios: saber onde está cada parte, ver a situação de todos de uma vez e fazer uma mudança que atravessa repositórios sem quebrar a integração entre eles.

Leia antes de executar:
- `references/template-repositorios.md` — template do `repositorios.md` e do `mudanca-multi-repo.md`
- `references/comandos-git.md` — comandos de detecção e de panorama (somente leitura) e os comandos que alteram algo, com as pré-condições
- `references/coordenacao-mudancas.md` — ordem entre repositórios, compatibilidade de contratos e checklist de mudança coordenada

---

## Pré-requisito

### Passo 0 — Identificar o projeto

A raiz de trabalho é uma pasta de documentação com vários projetos, cada um em `docs/{projeto}/`.

1. Se o usuário citou o projeto, use a pasta dele.
2. Senão, leia `docs/workspace.md`: com um único projeto, use-o e avise; com vários, liste e pergunte qual.
3. Sem `docs/workspace.md`, procure `docs/*/project.md`.
4. Se o projeto não existir, ofereça iniciá-lo com `discovery-init`.
5. Leia `docs/{projeto}/project-config.json` (nome, stack, repositório; ver o schema em `discovery-init/references/project-config-schema.md`). Se não existir, use o `project.md` e ofereça criar o config a partir dele.

`{projeto}` é a pasta escolhida; todos os caminhos abaixo são relativos à raiz de trabalho.

**Exceção:** no **Panorama** o usuário pode pedir o workspace inteiro ("como estão todos os repositórios"). Nesse caso percorra todos os projetos do `workspace.md`.

---

## Onde ficam os repositórios

| Situação do projeto | Onde está registrado |
|---------------------|----------------------|
| Um repositório | `repository_url` e `code_path` do `docs/{projeto}/project-config.json` e seção **Repositório** do `project.md` |
| Dois ou mais | `docs/{projeto}/repositorios.md`; o `project.md` aponta para ele e o `workspace.md` mostra "vários" |

Quando um projeto de um repositório ganha o segundo, esta skill cria o `repositorios.md` com os dois e troca a seção do `project.md` pelo apontamento (ver o template). O `repositorios.md` é a fonte única dali em diante: as outras skills (`arch-c4`, `business-docs`, `plan-execution`) leem os caminhos de lá.

---

## Fluxo de execução

### Passo 1 — Escolher a operação

Pela frase do usuário, escolha a operação. Se não estiver claro, pergunte:

> "O que você quer fazer com os repositórios do **{projeto}**?
> 1. **Cadastrar** ou atualizar a lista de repositórios
> 2. **Panorama**: ver branch, alterações pendentes e sincronia de todos
> 3. **Preparar**: clonar os que ainda não estão nesta máquina
> 4. **Mudança coordenada**: uma entrega que mexe em mais de um repositório
> 5. **Onde fica**: em qual repositório está (ou vai ficar) uma parte do sistema"

---

### Operação 1 — Cadastrar

1. Leia o `repositorios.md` (ou a seção Repositório do `project.md`). Mostre o que já está cadastrado.
2. Para cada repositório novo, peça a **URL** ou o **caminho local** (o que o usuário tiver). Com o caminho local, detecte o resto com os comandos de leitura de `references/comandos-git.md`:
   - URL do `origin` (remova usuário e token da URL antes de registrar);
   - branch principal;
   - stack, pelos arquivos da raiz (`*.sln`, `*.csproj`, `angular.json`, `package.json`, `pom.xml`, `go.mod`, `Dockerfile`, `*.tf`, `docker-compose*.yml`...).
3. Pergunte o que não dá para detectar:
   - **Papel** (backend, frontend, mobile, worker, infraestrutura, biblioteca, contratos, documentação);
   - **Contêineres C4** que o repositório implementa. Se `docs/{projeto}/arquitetura/arquitetura.md` existir, ofereça a lista de contêineres de lá. Um repositório pode implementar vários contêineres, e um contêiner deve estar em um único repositório;
   - **Contratos** que ele expõe ou consome (API HTTP com OpenAPI, pacote NuGet/npm, eventos/filas, schema de banco compartilhado);
   - **Deploy**: como e para onde publica (pipeline, ambiente), se o usuário souber.
4. Mostre a tabela montada e peça confirmação antes de gravar.
5. Grave `docs/{projeto}/repositorios.md` pelo template. Se era projeto de um repositório, atualize a seção Repositório do `project.md` para apontar para o arquivo e, no `project-config.json`, mude `repositories` para `"varios"` e `repository_url`/`code_path` para `"ver repositorios.md"`. Atualize as colunas Repositório e Código local do `docs/workspace.md` para `vários (ver docs/{projeto}/repositorios.md)`.
6. Se algum repositório for usado por mais de um projeto do workspace (biblioteca, contratos), cadastre-o em cada projeto com a mesma URL e marque **Compartilhado com** {projetos}.

---

### Operação 2 — Panorama

Somente leitura. Para cada repositório do projeto (ou do workspace):

1. Verifique se o caminho local existe e é um repositório Git.
2. Pergunte uma vez se pode rodar `git fetch` (atualiza só as referências remotas, não mexe nos arquivos; precisa de rede). Sem fetch, avise que "atrás/à frente" usa a última informação baixada.
3. Colete: branch atual, alterações não commitadas, commits atrás/à frente do remoto, data e assunto do último commit, branches locais da entrega em andamento (se houver `mudanca-multi-repo.md` aberto).
4. Mostre no chat (não grave arquivo):

> | Repositório | Papel | Branch | Alterações | Atrás / À frente | Último commit |
> |-------------|-------|--------|------------|------------------|---------------|
> | opbh-api | backend | feat/eventos | 3 arquivos | 0 / 2 | 28/10 "feat: agenda" |
> | opbh-web | frontend | master | nenhuma | 4 / 0 | 20/10 "fix: menu" |

5. Termine com os **pontos de atenção**: repositório não clonado, branch diferente da esperada para a entrega, alterações paradas, branch atrás do remoto, entrega com branch faltando em algum repositório. Sugira a ação, mas não execute.

---

### Operação 3 — Preparar (clonar os que faltam)

1. Liste os repositórios sem caminho local ou cujo caminho não existe.
2. Proponha o destino de cada um. Padrão: a mesma pasta-mãe dos repositórios já clonados (ex.: `D:\repos\{nome}`); pergunte se não houver referência.
3. Mostre os comandos `git clone` e **só execute após confirmação**. Nunca clone para dentro da pasta de documentação, nem por cima de pasta que já existe.
4. Grave os caminhos no `repositorios.md`.
5. Explique como dar ao Claude Code acesso aos repositórios a partir do workspace (ver "Trabalhar no código a partir do workspace").

---

### Operação 4 — Mudança coordenada

Para uma entrega (escopo, item do plano de execução ou pedido avulso) que mexe em mais de um repositório. Siga `references/coordenacao-mudancas.md`.

1. **Entradas**: leia `docs/{projeto}/plano-execucao/{escopo}/execution-plan.md` (se existir), `docs/{projeto}/arquitetura/arquitetura.md` e o `repositorios.md`. Sem plano, pergunte o que a entrega muda.
2. **Repositórios afetados**: cruze os contêineres que a entrega toca com a coluna Contêineres C4 do cadastro. Mostre a lista e o motivo de cada um.
3. **Contratos que mudam**: endpoints, DTOs, eventos, pacotes, schema. Para cada um, classifique: compatível (só acrescenta) ou incompatível (remove, renomeia, muda tipo ou obrigatoriedade).
4. **Ordem**: provedor antes do consumidor (contratos/biblioteca → backend → frontend/mobile), com a estratégia de compatibilidade de cada contrato incompatível (expandir e depois contrair, versão nova do endpoint, feature flag).
5. **Branch**: proponha o mesmo nome em todos os repositórios afetados (padrão `feat/{escopo}`; siga a convenção do repositório se houver). Para criar, confira as pré-condições de `references/comandos-git.md` (sem alterações pendentes, branch principal atualizada) e **só crie após confirmação**, repositório por repositório, mostrando o resultado.
6. **Registro**: grave `docs/{projeto}/plano-execucao/{escopo}/mudanca-multi-repo.md` pelo template (repositórios, branch, contratos, ordem de merge e de deploy, PRs a preencher, checklist). Se a entrega for avulsa, use `{escopo}` = nome curto da mudança em kebab-case.
7. **Execução das tarefas**: para cada tarefa do plano, diga em qual repositório ela roda e qual skill de código usar. As skills de código (`architecture-*`, `angular-*`) rodam dentro do repositório certo.

Rodando de novo para a mesma entrega, atualize o `mudanca-multi-repo.md` (PRs abertos, mergeados, ambientes publicados) em vez de criar outro.

---

### Operação 5 — Onde fica

Responda pelo cadastro: qual repositório implementa o contêiner ou a área citada, o caminho local e, se o `arch-c4` tiver o mapeamento componente → código, a pasta dentro do repositório. Se a parte ainda não existe, diga em qual repositório ela deveria nascer pelo papel de cada um e pela arquitetura; se não houver um repositório adequado, aponte que é uma decisão de arquitetura (sugira `arch-adr`).

---

## Trabalhar no código a partir do workspace

O Claude Code só lê e edita arquivos do diretório onde foi aberto e dos diretórios adicionados. Para trabalhar no código sem sair do workspace de documentação:

- na sessão: `/add-dir D:\repos\opbh-api` (um por repositório);
- ao abrir: `claude --add-dir D:\repos\opbh-api --add-dir D:\repos\opbh-web`;
- fixo para o time: `permissions.additionalDirectories` no `.claude/settings.json` do workspace (caminhos variam por máquina: prefira o `settings.local.json`).

Para gerar muito código num só repositório, abrir o Claude Code dentro dele costuma ser melhor: as instruções (`CLAUDE.md`) e as configurações daquele repositório passam a valer. Os documentos continuam no workspace.

---

## Regras importantes

- **Somente leitura por padrão.** Detectar, listar e mostrar o panorama não alteram nada nos repositórios.
- **Nada que altera um repositório sem confirmação**: `clone`, criar branch, `checkout`, `pull`. Peça confirmação mostrando o comando e o repositório.
- **Nunca** faça commit, push, merge, rebase, reset, stash, exclusão de branch ou descarte de alterações, a menos que o usuário peça explicitamente aquela ação. Repositório com alterações pendentes: avise e pare naquele repositório.
- Uma falha num repositório não interrompe os outros no panorama, mas interrompe a criação de branches da mudança coordenada (para não deixar a entrega pela metade sem avisar). Mostre o que já foi feito.
- Nunca registre credenciais: remova `usuario:token@` das URLs e não copie segredos de configuração.
- Todo arquivo desta skill fica na pasta de documentação, em `docs/{projeto}/`. Nada é escrito nos repositórios de código.
- Nunca sobrescreva o `repositorios.md` sem mostrar o que muda. Nunca reescreva o `workspace.md` inteiro: só a linha do projeto.
- Se o usuário não souber algo (papel, deploy, contratos), registre `a definir` e siga.

---

## Troubleshooting

**Caminho cadastrado não existe nesta máquina**
Cada pessoa clona onde quer. Pergunte o caminho certo; se o workspace for compartilhado no Git, sugira manter os caminhos no `repositorios.md` como "sugeridos" e cada um ajustar o seu, ou usar a mesma pasta-mãe no time.

**A pasta não é um repositório Git**
Registre o caminho, marque a URL como `a definir` e avise que o panorama não funciona para ela.

**Repositório com submódulos ou monorepo com vários contêineres**
Um monorepo é um único repositório: cadastre uma linha só e liste todos os contêineres que ele implementa. Submódulos entram como repositórios próprios, com papel e observação "submódulo de {repo}".

**Branch da entrega já existe em algum repositório**
Não recrie. Mostre de onde ela partiu e quantos commits tem, e pergunte se a entrega deve usá-la.

**Contrato incompatível sem estratégia definida**
Não siga com a ordem de merge. Explique as opções de `references/coordenacao-mudancas.md` e, se o time escolher uma que vale para as próximas entregas, sugira registrar com `arch-adr`.

**Projeto antigo com só o campo Código local**
Funciona como projeto de um repositório. Só crie o `repositorios.md` quando o usuário cadastrar o segundo.

---

## Exemplos de uso

**Usuário:** "O OPBH agora tem o front num repositório separado, cadastra os dois"
**Ação:** Cadastrar. Lê o `project.md`, detecta URL, branch e stack nos dois caminhos, pergunta papel e contêineres, cria `docs/opbh/repositorios.md` e atualiza `project.md` e `workspace.md`.

**Usuário:** "Como estão os repositórios de todos os projetos?"
**Ação:** Panorama do workspace inteiro, agrupado por projeto, com os pontos de atenção.

**Usuário:** "Vamos implementar o escopo de eventos, prepara os repositórios"
**Ação:** Mudança coordenada. Lê o plano e a arquitetura, lista os repositórios afetados, contratos e ordem, propõe `feat/eventos` em cada um, cria após confirmação e grava `mudanca-multi-repo.md`.
