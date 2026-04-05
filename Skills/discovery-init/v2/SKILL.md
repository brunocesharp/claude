---
name: discovery-init
description: Inicia o discovery de um novo projeto de software criando o project.md e a estrutura de pastas. Use quando o usuário disser "iniciar projeto", "novo projeto", "começar discovery", "criar projeto", "setup do projeto", "quero começar um projeto". NÃO use se o projeto já foi iniciado — nesses casos leia o project.md existente.
metadata:
  version: 1.1.0
  category: discovery
---

# Discovery Init

Skill responsável por inicializar um novo projeto, coletar informações básicas, criar o arquivo `project.md` e (opcionalmente) montar a estrutura de pastas de documentação.

---

## Fluxo de execução

### Passo 1 — Verificar se o projeto já existe

Antes de qualquer pergunta, verifique se já existe um arquivo `docs/*/project.md` que corresponda ao que o usuário está descrevendo.

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
   - "Qual é a URL do repositório Git?"
   - Se não tiver ainda, registre como `"a definir"` e siga normalmente. Não execute `git clone` automaticamente — apenas registre a URL.

4. **Tipo de projeto** *(opcional)*
   - "Que tipo de sistema é esse? (ex: web app, API, mobile, integração, etc.)"

---

### Passo 3 — Gerar o arquivo `project.md`

Salve o arquivo em:
```
docs/{nome-do-projeto}/project.md
```

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
- Discovery: `docs/{nome-do-projeto}/discovery/`
- Escopo: `docs/{nome-do-projeto}/escopo/`

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

### Passo 4 — Perguntar sobre estrutura de pastas

Após salvar o `project.md`, pergunte:

> "Deseja que eu crie agora a estrutura de pastas de documentação para este projeto?"

**Se sim**, crie as pastas com `.gitkeep` para que o Git as versione:
```
docs/{nome-do-projeto}/discovery/.gitkeep
docs/{nome-do-projeto}/escopo/.gitkeep
```

Confirme:
> "Estrutura criada! Discovery em `docs/{nome-do-projeto}/discovery/` e escopo em `docs/{nome-do-projeto}/escopo/`."

**Se não**, informe:
> "Tudo bem! O `project.md` foi salvo em `docs/{nome-do-projeto}/project.md`. Quando quiser criar a estrutura de pastas, é só pedir."

---

### Passo 5 — Sugerir próximos passos

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

- O nome da pasta deve ser sempre em **kebab-case** — confirme com o usuário antes de criar.
- Nunca sobrescreva um `project.md` existente sem confirmação explícita.
- Nunca execute `git clone` automaticamente — apenas registre a URL.
- Se o usuário não souber responder algo, registre como `"a definir"` e siga.

---

## Troubleshooting

**`project.md` já existe para esse projeto**
Não sobrescreva. Leia o conteúdo atual, apresente os campos existentes ao usuário e pergunte: "Deseja atualizar algum campo?"

**Nome do projeto com caracteres especiais ou acentos**
Normalize para kebab-case sem acentos (ex: "Gestão de Estoque" → `gestao-de-estoque`). Confirme com o usuário antes de usar.

**Usuário não tem repositório Git ainda**
Registre a URL como `"a definir"` no `project.md`. Não bloqueie o fluxo — o repositório pode ser adicionado depois atualizando o arquivo.

**Usuário quer iniciar mais de um projeto na mesma conversa**
Execute o fluxo completo para cada projeto separadamente, um de cada vez.
