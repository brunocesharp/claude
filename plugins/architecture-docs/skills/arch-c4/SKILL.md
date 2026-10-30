---
name: arch-c4
description: Conduz a documentação de arquitetura de um projeto no modelo C4 (Simon Brown), gerando docs/{projeto}/arquitetura/arquitetura.md com diagramas Mermaid de contexto, contêineres, componentes e deployment. Funciona para sistema novo (a partir do escopo e da especificação) e para sistema existente (a partir do código). Use quando o usuário mencionar "arquitetura", "documentar arquitetura", "C4", "modelo C4", "diagrama de contexto", "diagrama de contêineres", "diagrama de componentes", "diagrama de deployment", "visão da arquitetura", "como o sistema está dividido", "quais sistemas se integram", "system landscape", "desenhar a arquitetura", "atualizar a arquitetura". NÃO use para gerar código (use architecture-* ou angular-*), para registrar uma decisão isolada (use arch-adr), para regras de negócio (use business-docs) ou para plano de execução (use plan-execution).
metadata:
  author: Equipe de Arquitetura
  version: 1.0.0
  category: architecture-docs
  depends-on: discovery-init
  recommended-after: spec-functional
  output: docs/{projeto}/arquitetura/arquitetura.md
---

# Arquitetura C4

Conduz a documentação da estrutura estática de um sistema em níveis de abstração (contexto, contêineres, componentes, código), mais deployment e diagramas complementares, seguindo o livro *The C4 model for visualising software architecture* (Simon Brown). Os diagramas são escritos em Mermaid C4, dentro do próprio Markdown.

Leia antes de conduzir a conversa:
- `references/vocabulario-c4.md` — o que é sistema, contêiner, componente e código (e microsserviço, serverless, biblioteca)
- `references/niveis-c4.md` — intenção, elementos, interações, público e obrigatoriedade de cada nível
- `references/notacao.md` — regras de notação (título, legenda, descrição, linhas, siglas, escopo do diagrama)
- `references/mermaid-c4.md` — sintaxe Mermaid C4, limitações e exemplos por nível

Consulte quando precisar:
- `references/levantamento-codigo.md` — como descobrir contêineres e componentes a partir do código (sistema existente)
- `references/diagramas-complementares.md` — deployment, landscape, dinâmico e modelo de domínio
- `references/template-arquitetura.md` — template do documento gerado
- `references/checklist.md` — verificação de qualidade antes de salvar

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

---

## Fluxo de Execução

Conduza em blocos, um de cada vez, esperando a resposta antes de avançar. Ao fim de cada bloco, mostre o diagrama Mermaid do nível e a tabela de elementos para o usuário confirmar. Siga o mantra de Shneiderman: **visão geral primeiro, depois zoom e filtro, detalhes sob demanda**.

### Passo 1 — Definir o modo e ler as entradas

Verifique se `docs/{projeto}/arquitetura/arquitetura.md` existe.

| Situação | Modo | O que fazer |
|----------|------|-------------|
| Não existe e o sistema ainda não foi construído | **Design** | Desenhar a partir do discovery, escopo e especificação |
| Não existe e o sistema já existe | **Levantamento** | Descobrir a arquitetura no código (`references/levantamento-codigo.md`) e confirmar com o usuário |
| Já existe | **Atualização** | Perguntar o que mudou (escopo novo, contêiner novo, integração nova) e alterar só as seções afetadas |

Leia o que existir, sem repetir perguntas já respondidas nesses documentos:
- `docs/{projeto}/project.md` — nome, repositório, **código local**
- `docs/{projeto}/repositorios.md` — se existir (código em vários repositórios): caminho, papel e contêineres de cada repositório
- `docs/{projeto}/discovery/vision.md` e `stakeholders.md` — pessoas e perfis de usuário (candidatos a *Person*)
- `docs/{projeto}/escopo/*/escopo.md` — funcionalidades, integrações e restrições
- `docs/{projeto}/especificacao/*/spec-functional.md` — atores e dependências externas citadas nos cenários
- `docs/{projeto}/arquitetura/decisoes/` — decisões já registradas
- No modo Levantamento: o código no caminho de **código local**, ou em cada repositório do `repositorios.md` (se `a definir`, pergunte onde está)

Informe o modo e o que foi lido:
> "Vou documentar a arquitetura do **{projeto}** no modo **{modo}**. Li: {lista}. Começamos pelo diagrama de contexto."

---

### Passo 2 — Vocabulário

Antes de desenhar, alinhe os termos (ver `references/vocabulario-c4.md`):

> "No C4 usamos: **sistema** (o que entrega valor aos usuários), **contêiner** (algo que precisa estar rodando para o sistema funcionar: aplicação ou armazenamento de dados, implantável separadamente — não é o contêiner do Docker), **componente** (agrupamento de funcionalidades dentro de um contêiner, atrás de uma interface) e **código**. O time já usa outros nomes para isso?"

Se o time usar outros termos, registre a equivalência no glossário do documento e use os termos do time nas conversas.

---

### Bloco 1 — Contexto do sistema (nível 1, obrigatório)

Perguntas (use as respostas já obtidas das entradas):
- "Qual é o sistema em escopo? Descreva em uma frase o que ele faz."
- "Quem usa o sistema? (perfis, papéis ou personas — com uma descrição curta de cada)"
- "Com quais outros sistemas ele se relaciona? Quem é dono de cada um?"
- "Para cada relação: o que é feito? (ex.: 'envia e-mails usando', 'consulta saldo em')"
- "Existe um limite de organização que vale mostrar (o que é interno e o que é externo)?"

**Validação:**
- Cada pessoa e cada sistema tem nome **e** descrição.
- Toda relação tem rótulo com o propósito; nada de tecnologia ou protocolo neste nível.
- Sistemas de terceiros e sistemas da própria organização que o time não constrói aparecem como externos (`_Ext`).
- O diagrama deve poder ser mostrado para pessoas não técnicas.

---

### Bloco 2 — Contêineres (nível 2, obrigatório)

Perguntas:
- "Quais aplicações e armazenamentos de dados compõem o sistema? (API, SPA, app mobile, worker, banco, fila, bucket, sistema de arquivos com dados de negócio...)"
- "Qual a tecnologia de cada um?" — se ainda não decidida, registre as opções (ex.: "PostgreSQL ou SQL Server") e um ponto em aberto.
- "Quais as principais responsabilidades de cada um?"
- "Como eles se comunicam? Para cada relação: propósito, mecanismo (REST, gRPC, fila...), estilo (síncrono/assíncrono) e protocolo."

**Validação:**
- Cada contêiner é implantável separadamente. Biblioteca ou projeto (DLL, pacote) **não** é contêiner.
- Dois schemas de banco separados são dois contêineres.
- Serviços gerenciados que o time usa e controla (bucket S3/R2, banco RDS) aparecem como contêineres; serviços de terceiros que o time só consome são sistemas externos.
- As mesmas pessoas e sistemas externos do contexto aparecem aqui, com um limite (`System_Boundary`) igual à caixa do contexto.
- Nenhuma instância física, cluster ou réplica neste nível (isso vai no deployment).

Se uma escolha de tecnologia estiver em aberto ou for relevante (ex.: banco, mensageria, autenticação), sugira registrar com `arch-adr`.

---

### Bloco 3 — Componentes (nível 3, opcional)

> "Vale detalhar os componentes de algum contêiner? Costuma valer para aplicações maiores (monólitos, APIs com muitas áreas). Para bancos, armazenamentos e serviços muito simples, não."

Para cada contêiner escolhido:
- Liste os componentes com nome, tecnologia e responsabilidade. No modo Levantamento, derive do código (controllers, serviços, repositórios, módulos) e mostre o **mapeamento para o código** (pasta/namespace).
- Inclua os contêineres, pessoas e sistemas vizinhos que se relacionam com ele, dentro de um `Container_Boundary`.
- Componentes transversais (log, autenticação, cache) entram como nota ou ficam fora, se poluírem o diagrama.

**Validação:**
- Cada componente existe de verdade no código (ou existirá do jeito desenhado): "Vocês codificariam assim?"
- Mais de ~12 componentes: divida em diagramas por área funcional, cada um contando uma parte da mesma história, no mesmo nível de abstração.

Nível 4 (código): só sugira para um componente muito complexo ou para mostrar um padrão repetido no código. Use `classDiagram` do Mermaid.

---

### Bloco 4 — Deployment (recomendado)

- "Quais ambientes vale documentar? (desenvolvimento, homologação, produção)"
- "Onde cada contêiner roda em cada ambiente? (servidor, VM, Docker, PaaS, navegador do usuário, dispositivo)"
- "Há réplicas, balanceador, proxy, CDN, firewall que importam para entender o ambiente?"

Mostre instâncias de **contêineres** dentro de nós de deployment aninhados (ver `references/diagramas-complementares.md`). Um diagrama por ambiente.

---

### Bloco 5 — Complementares (opcional)

- **Dinâmico**: só para fluxos significativos ou difíceis de entender lendo o código (autenticação federada, processamento assíncrono por eventos, integração com várias etapas). Um arquivo por cenário.
- **System Landscape**: se o workspace tem outros projetos que se relacionam com este, ofereça criar ou atualizar `docs/arquitetura/landscape.md` (visão de todos os sistemas, sem foco em um).
- **Modelo de domínio**: se o domínio não for trivial e não houver outra documentação, um `classDiagram` com as entidades principais.

---

### Passo 3 — Gerar os arquivos

Use `references/template-arquitetura.md`. Estrutura:

```
docs/{projeto}/arquitetura/
├── arquitetura.md                 # contexto, contêineres, deployment, glossário, decisões, pontos em aberto
├── componentes/{conteiner}.md     # um por contêiner detalhado (opcional)
├── dinamicos/{cenario}.md         # um por fluxo dinâmico (opcional)
└── decisoes/                      # ADRs (skill arch-adr)
```

Antes de salvar, passe o `references/checklist.md` em cada diagrama e corrija o que falhar.

No modo Atualização: altere só as seções afetadas, mantenha o resto e acrescente uma linha no **Histórico de alterações**.

---

### Passo 4 — Confirmar e informar

1. Atualize `docs/{projeto}/project.md` marcando Arquitetura como em andamento/concluída.
2. Atualize a coluna Situação do projeto em `docs/workspace.md`, se a fase mudou.
3. Informe:

> "Arquitetura do **{projeto}** documentada em `docs/{projeto}/arquitetura/arquitetura.md`:
> - Contexto: {N} pessoas, {M} sistemas externos
> - Contêineres: {K}
> - Componentes: {lista de contêineres detalhados ou "não detalhados"}
> - Deployment: {ambientes}
>
> Decisões que valem um ADR: {lista}. Pontos em aberto: {X}.
>
> Próximo passo sugerido: **plano de execução** (`plan-execution`), que vai usar os contêineres e tecnologias daqui para escolher as skills de código."

---

## Regras Importantes

### Comportamento obrigatório
- **Diagramas refletem a realidade**: no modo Levantamento, o que está desenhado precisa existir no código; no modo Design, pergunte "vocês codificariam assim?". Componente compartilhado (DLL usada por dois contêineres) aparece dentro de cada contêiner, não como contêiner separado.
- **Tecnologia explícita** em contêineres e componentes. Em design, com a decisão em aberto, liste as opções em vez de omitir.
- **Todo elemento** tem tipo, nome e descrição (contêiner e componente também tecnologia).
- **Toda relação** tem rótulo que se lê como frase, do iniciador para o receptor ("API — lê e grava em → Banco").
- **Todo diagrama** tem título com o tipo (`[Contêineres] Nome do sistema`) e uma **legenda** em tabela logo abaixo (o Mermaid C4 não desenha legenda).
- **Siglas** do domínio vão para o glossário.
- **Nunca invente** tecnologia, sistema ou integração. O que não se sabe vira "a definir" em Pontos em aberto.
- **Nunca sobrescreva** `arquitetura.md` sem confirmação.

### O que NÃO fazer
- Não misture níveis no mesmo diagrama (componentes de vários contêineres num diagrama de contêineres).
- Não coloque instâncias, réplicas ou servidores nos diagramas de contexto, contêineres ou componentes.
- Não desenhe frameworks e bibliotecas como componentes (são tecnologia do componente).
- Não force atributos de qualidade (segurança, desempenho) no diagrama: use texto curto no documento.
- Não gere diagrama de código para o sistema inteiro.

### Adaptação de tom
- **PM e stakeholders**: foque no contexto (quem usa, com o que se integra).
- **Devs e tech leads**: contêineres, componentes, tecnologias e mapeamento para o código.
- **Operação/infra**: deployment por ambiente.

---

## Exemplos de Uso

### Exemplo 1: Sistema novo, depois da especificação
**Usuário:** "Vamos documentar a arquitetura do projeto de pedidos"
**Ações:** modo Design; lê vision, escopo e spec; propõe pessoas e sistemas externos a partir dos atores dos cenários; conduz contêineres com as tecnologias das restrições do escopo; tecnologias indefinidas viram opções + ADR sugerido; pula componentes.
**Resultado:** `arquitetura.md` com contexto, contêineres, deployment de produção e 2 ADRs sugeridos.

### Exemplo 2: Sistema existente
**Usuário:** "Documenta a arquitetura do OPBH a partir do código"
**Ações:** modo Levantamento; lê `docker-compose*.yml`, `*.csproj`, `angular.json`, `nginx/*.conf`, `appsettings*.json`; encontra SPA Angular, API .NET, PostgreSQL, Redis, bucket R2, servidor de e-mail; confirma com o usuário; detalha componentes da API pelas pastas de serviços; deployment de produção e homologação a partir dos compose.
**Resultado:** documento com o que existe no código e o mapeamento componente → pasta.

### Exemplo 3: Atualização por um escopo novo
**Usuário:** "O escopo de eventos criou uma integração com o Instagram, atualiza a arquitetura"
**Ações:** modo Atualização; acrescenta o sistema externo no contexto e a relação no contêiner que integra; atualiza legendas; registra no histórico.
**Resultado:** só as seções afetadas mudam.

---

## Troubleshooting

**Usuário chama projetos/DLLs de contêineres** — explique: contêiner é o que roda e se implanta separado; projetos de uma mesma solução que geram um só executável são componentes ou camadas dentro de um contêiner.

**Diagrama de contêineres com elementos demais** — verifique se há componentes misturados ou instâncias de deployment; se o sistema for grande mesmo, considere que alguns grupos são sistemas separados (com landscape).

**Mermaid não renderiza ou fica embaralhado** — ver seção de problemas em `references/mermaid-c4.md` (aliases, aspas, ordem das declarações, `UpdateLayoutConfig`).

**Não se sabe a tecnologia** — registre as opções no elemento ("PostgreSQL ou SQL Server"), crie ponto em aberto e sugira `arch-adr`.

**Microsserviços de outro time** — são sistemas externos; os do próprio time são contêineres (cada um com seu banco como contêiner separado).
