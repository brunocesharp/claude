# 🎯 Skills de Escopo para Claude Code

Um conjunto de skills conversacionais para guiar equipes de desenvolvimento através do ciclo completo de um projeto de software — da ideação à produção.

## O que é isso?

Este repositório contém **skills modulares** para o Claude Code que ajudam a construir documentação de projeto de forma estruturada e conversacional. Cada skill conduz uma conversa focada em um aspecto específico do projeto e gera documentos `.md` padronizados.

**Por que usar?**
- Garante que nenhum aspecto importante seja esquecido
- Cria documentação consistente entre projetos
- Funciona como um facilitador de discovery e escopo
- Permite usar apenas as peças que você precisa

## 🚀 Quick Start

### 1. Copie as skills para seu projeto

```bash
# Clone este repositório
git clone <url-do-repositorio> claude-skills

# Copie a pasta de skills para seu projeto
cp -r claude-skills/skills/* seu-projeto/.claude/skills/
```

### 2. Inicie um novo projeto

No Claude Code, dentro do seu projeto:

```
> iniciar projeto
```

O Claude vai guiar você pelo setup inicial.

### 3. Siga o fluxo de discovery

Após o init, siga as skills de discovery na ordem que fizer sentido:

```
> definir visão do projeto
> mapear oportunidades
> levantar hipóteses
> identificar stakeholders
> definir métricas de sucesso
```

### 4. Gere o escopo

Com o discovery completo (ou parcialmente completo):

```
> gerar escopo
```

## 📦 Skills Disponíveis

### Fase: Discovery

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `discovery-init` | "iniciar projeto", "novo projeto" | `project.md` |
| `discovery-vision` | "visão do projeto", "proposta de valor" | `vision.md` |
| `discovery-opportunity` | "mapear oportunidades", "jobs to be done" | `opportunity.md` |
| `discovery-assumptions` | "hipóteses", "premissas" | `assumptions.md` |
| `discovery-stakeholders` | "stakeholders", "partes interessadas" | `stakeholders.md` |
| `discovery-metrics` | "métricas", "KPIs", "como medir sucesso" | `success-metrics.md` |

### Fase: Escopo

| Skill | Gatilho | Saída |
|-------|---------|-------|
| `scope-generate` | "gerar escopo", "criar escopo" | `escopo.md` + cópia do discovery |

## 📁 Estrutura de Pastas Gerada

Após usar as skills, seu projeto terá esta estrutura:

```
seu-projeto/
├── .claude/
│   └── skills/           # Skills copiadas para cá
│       ├── discovery-init/
│       ├── discovery-vision/
│       ├── discovery-opportunity/
│       ├── discovery-assumptions/
│       ├── discovery-stakeholders/
│       ├── discovery-metrics/
│       └── scope-generate/
│
└── docs/
    └── nome-do-projeto/
        ├── project.md              # Metadados do projeto
        ├── discovery/
        │   ├── vision.md
        │   ├── opportunity.md
        │   ├── assumptions.md
        │   ├── stakeholders.md
        │   └── success-metrics.md
        └── escopo/
            └── titulo-do-escopo/
                ├── escopo.md       # Documento consolidado
                └── discovery/      # Snapshot do discovery usado
```

## 🎭 Para quem é isso?

- **Product Managers** — para conduzir discovery estruturado
- **Tech Leads** — para garantir alinhamento antes de codar
- **Desenvolvedores** — para entender o contexto completo
- **Analistas de Sistemas** — para documentação consistente

## 🔧 Como funciona cada skill

### discovery-init

Ponto de entrada. Coleta informações básicas:
- Nome do projeto
- Descrição resumida
- URL do repositório Git
- Tipo de projeto

### discovery-vision

Baseada em **Lean Canvas** e **Value Proposition Canvas**. Explora:
- Qual problema estamos resolvendo?
- Para quem?
- Qual a proposta de valor?
- Quais as restrições?

### discovery-opportunity

Baseada em **Opportunity Solution Tree** (Teresa Torres) e **Jobs to Be Done**. Mapeia:
- Jobs que o usuário quer realizar
- Dores atuais
- Desejos e expectativas
- Tentativas anteriores de resolver

### discovery-assumptions

Baseada em **Assumption Mapping** (Bland & Osterwalder) e **Lean Startup**. Identifica:
- Hipóteses sobre usuários
- Hipóteses de negócio
- Hipóteses técnicas
- Priorização por impacto × certeza

### discovery-stakeholders

Mapeia todas as partes interessadas:
- Quem aprova?
- Quem é afetado?
- Matriz poder × interesse
- Estratégia de comunicação

### discovery-metrics

Baseada em **OKRs**, **North Star Metric** e **HEART Framework**. Define:
- Métrica principal (North Star)
- KPIs de negócio
- KPIs de produto/usuário
- Baseline e metas

### scope-generate

Consolida tudo em um documento de escopo:
- Lê todo o discovery existente
- Verifica escopos já criados (evita duplicidade)
- Gera documento com funcionalidades, restrições, métricas
- Copia snapshot do discovery usado

## 🛣️ Roadmap

| Fase | Status | Skills |
|------|--------|--------|
| Discovery | ✅ Implementado | 6 skills |
| Escopo | ✅ Implementado | 1 skill |
| Especificação | 🔜 Planejado | `spec-business-rules`, `spec-functional`, `spec-nonfunctional` |
| Refinamento | 🔜 Planejado | `refinement-screens`, `refinement-api`, `refinement-data-model` |
| Plano de Execução | 🔜 Planejado | `plan-tasks`, `plan-estimation` |
| Deploy | 🔜 Planejado | `deploy-homolog`, `deploy-production` |

## 💡 Dicas de Uso

**Não precisa fazer tudo**
Use só as skills que fazem sentido para seu contexto. Um projeto pequeno pode precisar só de `vision` e `scope-generate`.

**Itere**
Os documentos são vivos. Rode as skills novamente quando tiver novas informações.

**Escopo parcial**
Um escopo pode cobrir só uma feature ou módulo, não precisa ser o projeto inteiro.

**Múltiplos escopos**
Projetos grandes podem ter vários escopos, cada um com seu ciclo de vida independente.

## 🤝 Contribuindo

1. Fork este repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-skill`)
3. Commit suas mudanças (`git commit -m 'Adiciona skill X'`)
4. Push para a branch (`git push origin feature/nova-skill`)
5. Abra um Pull Request

### Estrutura de uma skill

```
nome-da-skill/
└── SKILL.md    # Arquivo único com instruções para o Claude
```

O `SKILL.md` deve conter:
- Descrição e gatilhos
- Fluxo conversacional
- Template do documento de saída
- Regras e validações

## 📄 Licença

MIT

---

**Feito para times que querem parar de começar projetos no escuro.**
