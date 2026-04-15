---
name: discovery-init
description: Inicia o discovery de um novo projeto de software criando o project.md e a estrutura de pastas. Use quando o usuário disser "iniciar projeto", "novo projeto", "começar discovery", "criar projeto", "setup do projeto", "quero começar um projeto". NÃO use se o projeto já foi iniciado — nesses casos leia o project.md existente.
metadata:
  version: 2.1.0
  category: discovery
---

# Discovery Init

Skill responsável por inicializar um novo projeto, coletar informações básicas, criar o arquivo `project.md`, montar a estrutura de pastas de documentação e publicar tudo no repositório Git do projeto.

> **Importante:** todos os arquivos e pastas criados por esta skill vão para o **repositório do projeto alvo** (informado pelo usuário), nunca para o repositório de skills onde esta skill está instalada.

---

## Fluxo de execução

### Passo 1 — Verificar se o projeto já existe

Antes de qualquer pergunta, verifique se já existe um `project.md` que corresponda ao que o usuário está descrevendo:

- **Com repositório clonado**: procure em `docs/project.md`
- **Sem repositório** (local): procure em `{nome-do-projeto}/docs/project.md`

- **Se existir**: não sobrescreva. Leia o arquivo, informe o usuário e pergunte se deseja atualizar algum campo.
- **Se não existir**: siga para o Passo 2.

---

### Passo 2 — Coletar informações do projeto

Faça as perguntas abaixo uma de cada vez, em tom conversacional:

1. **Nome do projeto**
   - "Qual é o nome do projeto?"
   - Use esse nome para nomear a pasta em kebab-case (ex: "Meu Projeto" → `meu-projeto`). Confirme o nome da pasta com o usuário antes de criar arquivos.

2. **Descrição resumida**
   - "Em uma frase, qual é a ideia central desse projeto?"

3. **Repositório Git**
   - "Qual é a URL do repositório Git? (ex: https://github.com/org/repo)"
   - Se não tiver ainda, registre como `"a definir"` e siga para o Passo 3 sem executar nenhum comando git.

4. **Tipo de projeto** *(opcional)*
   - "Que tipo de sistema é esse? (ex: web app, API, mobile, integração, etc.)"

---

### Passo 3 — Clonar o repositório alvo

> **Execute apenas se uma URL de repositório válida foi informada. Pule este passo se a URL for "a definir".**

Execute os comandos abaixo via Bash:

```bash
# Clona o repositório alvo em um diretório temporário
git clone {url-do-repositorio} /tmp/{nome-do-projeto}
```

Se o clone falhar (repo privado, credenciais, URL inválida), informe o erro ao usuário e pergunte se deseja corrigir a URL ou continuar sem repositório (registrando como "a definir").

Após o clone bem-sucedido, confirme a branch padrão:

```bash
cd /tmp/{nome-do-projeto} && git branch --show-current
```

Guarde o nome da branch para usar no push (Passo 6).

---

### Passo 4 — Gerar o arquivo `project.md` no repositório alvo

O caminho do arquivo depende se há repositório ou não:

| Situação | Caminho do arquivo |
|---|---|
| Com repositório clonado | `/tmp/{nome-do-projeto}/docs/project.md` |
| Sem repositório (local) | `{nome-do-projeto}/docs/project.md` |

O repositório já é exclusivo do projeto — o nome do projeto está no nome do repositório, não na pasta `docs/`.

Template:

```markdown
# {Nome do Projeto}

## Visão Geral
{Descrição resumida fornecida pelo usuário}

## Repositório
- URL: {url ou "a definir"}
- Tipo: {tipo do projeto ou "a definir"}

## Metadados
- Iniciado em: {data atual no formato DD/MM/YYYY}
- Responsável: {perguntar ao usuário ou deixar "a definir"}

## Estrutura de Documentação
- Discovery: `docs/discovery/`
- Escopo: `docs/escopo/`

## Status das Fases
- [ ] Discovery
- [ ] Escopo
- [ ] Especificação
- [ ] Refinamento
- [ ] Plano de Execução
- [ ] Homologação
- [ ] Produção
```

---

### Passo 5 — Criar estrutura de pastas no repositório alvo

Crie as pastas com `.gitkeep` para que o Git as versione.

**Com repositório clonado** (`/tmp/{nome-do-projeto}/`):
```bash
mkdir -p /tmp/{nome-do-projeto}/docs/discovery
mkdir -p /tmp/{nome-do-projeto}/docs/escopo
touch /tmp/{nome-do-projeto}/docs/discovery/.gitkeep
touch /tmp/{nome-do-projeto}/docs/escopo/.gitkeep
```

**Sem repositório** (local, pule o Passo 6):
```bash
mkdir -p {nome-do-projeto}/docs/discovery
mkdir -p {nome-do-projeto}/docs/escopo
touch {nome-do-projeto}/docs/discovery/.gitkeep
touch {nome-do-projeto}/docs/escopo/.gitkeep
```

---

### Passo 6 — Commit e push no repositório alvo

> **Execute apenas se o clone foi realizado com sucesso no Passo 3.**

```bash
cd /tmp/{nome-do-projeto}
git add docs/
git commit -m "docs: inicializa estrutura de documentação do projeto"
git push origin {branch}
```

Após o push, confirme ao usuário:

> "Estrutura de documentação criada e publicada no repositório! Branch: `{branch}`
> - `docs/project.md`
> - `docs/discovery/`
> - `docs/escopo/`"

---

### Passo 7 — Sugerir próximos passos

> "O projeto **{nome}** foi iniciado! As próximas etapas do discovery são:
> - **Visão do projeto** — definir o problema, público-alvo e proposta de valor
> - **Mapeamento de oportunidades** — identificar dores e jobs to be done
> - **Hipóteses e premissas** — levantar o que ainda precisa ser validado
> - **Stakeholders** — mapear os envolvidos e seus interesses
> - **Métricas de sucesso** — definir como vamos medir o sucesso
>
> Por onde quer começar?"

---

## Regras importantes

- Todos os arquivos vão para o **repositório alvo** — nunca para o repositório de skills.
- **Com repositório**: a pasta `docs/` fica na raiz do repo — o nome do projeto está no nome do repositório, não dentro de `docs/`.
- **Sem repositório**: crie a pasta `{nome-do-projeto}/` em kebab-case no diretório atual — confirme o nome com o usuário antes de criar.
- Nunca sobrescreva um `project.md` existente sem confirmação explícita.
- Se o usuário não souber responder algo, registre como `"a definir"` e siga.
- O diretório temporário `/tmp/{nome-do-projeto}` pode ser descartado após o push — o usuário pode clonar o repo localmente depois.

---

## Troubleshooting

**`project.md` já existe para esse projeto**
Não sobrescreva. Leia o conteúdo atual, apresente os campos existentes ao usuário e pergunte: "Deseja atualizar algum campo?"

**Clone falha (repositório privado ou credenciais ausentes)**
Informe o erro exato. Oriente o usuário a configurar autenticação (SSH key ou token) e tente novamente. Se não for possível resolver, registre a URL como "a definir" e continue sem git.

**Push rejeitado (sem permissão ou branch protegida)**
Informe o erro. Pergunte se o usuário deseja usar outra branch:
```bash
git checkout -b docs/init-discovery
git push origin docs/init-discovery
```

**Nome do projeto com caracteres especiais ou acentos**
Normalize para kebab-case sem acentos (ex: "Gestão de Estoque" → `gestao-de-estoque`). Confirme com o usuário antes de usar.

**Usuário não tem repositório Git ainda**
Registre a URL como `"a definir"` no `project.md`. Crie os arquivos localmente. Não bloqueie o fluxo — o repositório pode ser adicionado depois atualizando o arquivo.

**Usuário quer iniciar mais de um projeto na mesma conversa**
Execute o fluxo completo para cada projeto separadamente, um de cada vez. Use diretórios temporários diferentes (`/tmp/{nome-projeto-1}`, `/tmp/{nome-projeto-2}`).
