# Template — arquitetura.md

Salvar em `docs/{projeto}/arquitetura/arquitetura.md`. Seções opcionais que não forem feitas ficam com "Não documentado" e o motivo, em vez de sumir: assim quem lê sabe que a ausência é intencional.

Os diagramas seguem a sintaxe de `mermaid-c4.md`; cada um tem título com o tipo e tabela de legenda logo abaixo.

````markdown
# Arquitetura — {Nome do Projeto}

> Modelo: C4 (contexto, contêineres, componentes, código) + deployment
> Modo: {Design | Levantamento a partir do código}
> Atualizado em: {DD/MM/AAAA}
> Versão: {1.0}

## Sumário

1. [Contexto do sistema](#1-contexto-do-sistema)
2. [Contêineres](#2-contêineres)
3. [Componentes](#3-componentes)
4. [Deployment](#4-deployment)
5. [Diagramas dinâmicos](#5-diagramas-dinâmicos)
6. [Decisões de arquitetura](#6-decisões-de-arquitetura)
7. [Glossário](#7-glossário)
8. [Pontos em aberto](#8-pontos-em-aberto)
9. [Histórico de alterações](#9-histórico-de-alterações)

---

## 1. Contexto do sistema

{Uma ou duas frases: o que o sistema faz, para quem, e com o que se integra.}

```mermaid
C4Context
  title [Contexto] {Nome do Sistema}
  ...
```

| Legenda | Significado |
|---------|-------------|
| Pessoa | {perfil de usuário} |
| Caixa azul | Sistema em escopo |
| Caixa cinza | Sistema externo (outro dono) |
| Seta | Dependência, do iniciador para o receptor |

### Pessoas

| Pessoa | Descrição |
|--------|-----------|
| {nome} | {papel e responsabilidades} |

### Sistemas externos

| Sistema | Descrição | Dono | Relação |
|---------|-----------|------|---------|
| {nome} | {o que faz} | {time/fornecedor} | {propósito da relação} |

---

## 2. Contêineres

{Forma geral do sistema e como as responsabilidades se distribuem.}

```mermaid
C4Container
  title [Contêineres] {Nome do Sistema}
  ...
```

| Legenda | Significado |
|---------|-------------|
| ... | ... |

| Contêiner | Tecnologia | Responsabilidades | Código |
|-----------|------------|-------------------|--------|
| {nome} | {tecnologia e versão, ou opções em aberto} | {lista curta} | {pasta no repositório} |

### Comunicação

| De | Para | Propósito | Mecanismo | Estilo | Protocolo |
|----|------|-----------|-----------|--------|-----------|
| {contêiner} | {contêiner/sistema} | {lê e grava em...} | {REST, EF Core, fila...} | {síncrono/assíncrono} | {HTTPS, TCP 5432...} |

---

## 3. Componentes

| Contêiner | Diagrama |
|-----------|----------|
| {nome} | [componentes/{conteiner}.md](componentes/{conteiner}.md) |

{Ou: "Não documentado — {motivo, ex.: contêineres simples; detalhe disponível no código}."}

---

## 4. Deployment

### Produção

```mermaid
C4Deployment
  title [Deployment] {Nome do Sistema} — Produção
  ...
```

| Legenda | Significado |
|---------|-------------|
| ... | ... |

### Homologação

{Diagrama ou diferenças em relação à produção.}

---

## 5. Diagramas dinâmicos

| Cenário | Diagrama |
|---------|----------|
| {nome do fluxo} | [dinamicos/{cenario}.md](dinamicos/{cenario}.md) |

{Ou: "Nenhum — os fluxos são evidentes no código."}

---

## 6. Decisões de arquitetura

| ADR | Título | Situação |
|-----|--------|----------|
| [ADR-001](decisoes/ADR-001-{titulo}.md) | {título} | {Proposta/Aceita/Substituída} |

Decisões que ainda precisam de ADR: {lista ou "nenhuma"}.

---

## 7. Glossário

| Termo | Significado |
|-------|-------------|
| Contêiner | Unidade implantável separadamente (aplicação ou armazenamento de dados). Não confundir com container Docker. |
| {sigla do domínio} | {significado} |

---

## 8. Pontos em aberto

- [ ] {decisão de tecnologia pendente, integração a confirmar, componente sem lugar claro no código}

---

## 9. Histórico de alterações

| Data | Alteração | Origem |
|------|-----------|--------|
| {DD/MM/AAAA} | Versão inicial | {escopo, especificação ou levantamento do código} |
````

---

## Template — componentes/{conteiner}.md

````markdown
# Componentes — {Nome do Contêiner}

> Sistema: {Nome do Sistema} · Voltar para [arquitetura.md](../arquitetura.md)
> Atualizado em: {DD/MM/AAAA}

{O que o contêiner faz e como está organizado (camadas, features, hexagonal...).}

```mermaid
C4Component
  title [Componentes] {Nome do Sistema} — {Nome do Contêiner}
  ...
```

| Legenda | Significado |
|---------|-------------|
| ... | ... |

## Componentes

| Componente | Tecnologia | Responsabilidade | Código |
|------------|------------|------------------|--------|
| {nome} | {tecnologia} | {responsabilidade} | `{caminho}` |

## Transversais

{Log, autenticação, cache: como são tratados e por que não aparecem no diagrama.}
````

---

## Template — dinamicos/{cenario}.md

````markdown
# Dinâmico — {Cenário}

> Sistema: {Nome do Sistema} · Voltar para [arquitetura.md](../arquitetura.md)

{Por que este fluxo merece um diagrama (não é evidente no código).}

```mermaid
C4Dynamic
  title [Dinâmico] {Nome do Sistema} — {Cenário}
  ...
```

| Passo | Descrição |
|-------|-----------|
| 1 | {o que acontece} |
````

---

## Template — docs/arquitetura/landscape.md (raiz do workspace)

````markdown
# Landscape — {Organização ou Workspace}

> Atualizado em: {DD/MM/AAAA}

```mermaid
C4Context
  title [Landscape] {Organização}
  Enterprise_Boundary(org, "{Organização}") {
    ...
  }
  ...
```

| Sistema | Projeto | Arquitetura |
|---------|---------|-------------|
| {nome} | {projeto} | [docs/{projeto}/arquitetura/arquitetura.md](../{projeto}/arquitetura/arquitetura.md) |
````
