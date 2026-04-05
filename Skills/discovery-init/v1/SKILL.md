---
name: discovery-init
description: Inicia o processo de discovery de um novo projeto de software. Use esta skill sempre que o usuário mencionar "iniciar projeto", "novo projeto", "começar discovery", "criar projeto", "setup do projeto" ou qualquer variação que indique o início de um ciclo de desenvolvimento. Esta skill é o ponto de entrada obrigatório para todas as outras skills de discovery — ela cria o arquivo project.md e a estrutura de pastas necessária. Use proativamente sempre que parecer que um projeto está sendo iniciado do zero.
---

# Discovery Init

Skill responsável por inicializar um novo projeto, coletar informações básicas, criar o arquivo `project.md` e (opcionalmente) montar a estrutura de pastas de documentação.

---

## Fluxo de execução

### Passo 1 — Coletar informações do projeto

Faça as seguintes perguntas ao usuário, uma de cada vez, em tom conversacional:

1. **Nome do projeto**
   - "Qual é o nome do projeto?"
   - Use esse nome para nomear a pasta e o documento.

2. **Descrição resumida**
   - "Em uma frase, qual é a ideia central desse projeto?"

3. **Repositório Git**
   - "Qual é a URL do repositório Git?"
   - Se o usuário disser que ainda não tem, registre como `"a definir"` e siga normalmente.

4. **Tipo de projeto** *(opcional, mas útil)*
   - "Que tipo de sistema é esse? (ex: web app, API, mobile, integração, etc.)"

---

### Passo 2 — Gerar o arquivo `project.md`

Salve o arquivo em:
```
docs/{nome-do-projeto}/project.md
```

Use o template abaixo, preenchido com as respostas coletadas:

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

### Passo 3 — Perguntar sobre estrutura de pastas

Após salvar o `project.md`, pergunte:

> "Deseja que eu crie agora a estrutura de pastas de documentação para este projeto?"

**Se sim**, crie as seguintes pastas (com um `.gitkeep` dentro de cada uma para que o Git as versione):
```
docs/{nome-do-projeto}/discovery/.gitkeep
docs/{nome-do-projeto}/escopo/.gitkeep
```

Confirme ao usuário:
> "Estrutura criada! Os documentos de discovery serão salvos em `docs/{nome-do-projeto}/discovery/` e o escopo em `docs/{nome-do-projeto}/escopo/`."

**Se não**, informe:
> "Tudo bem! Quando quiser criar a estrutura, é só pedir. O `project.md` foi salvo em `docs/{nome-do-projeto}/project.md`."

---

### Passo 4 — Sugerir próximos passos

Ao final, apresente as próximas skills disponíveis:

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

- Se o usuário já tiver um `project.md` existente para esse projeto, **não sobrescreva** — leia o arquivo e pergunte se deseja atualizar algum campo.
- O nome da pasta deve ser gerado em **kebab-case** a partir do nome do projeto (ex: "Meu Projeto" → `meu-projeto`).
- Sempre confirme o nome da pasta antes de criar os arquivos.
- Se o repositório já existir e o usuário quiser clonar, apenas registre a URL — não execute `git clone` automaticamente sem confirmação explícita.
