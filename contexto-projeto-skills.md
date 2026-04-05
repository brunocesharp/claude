# Contexto do Projeto — Skills de Escopo para Claude Code

## Objetivo Geral

Criar um conjunto de skills para o Claude Code com o objetivo de guiar equipes de desenvolvimento através do ciclo completo de um projeto de software, desde a ideação até a publicação em produção.

---

## Visão do Ciclo Completo

O projeto cobre as seguintes fases, cada uma com suas skills e documentos de saída:

| Fase | Objetivo | Saída |
|---|---|---|
| **Discovery** | Construção da ideia do projeto | Documentos com conceitos importantes do projeto |
| **Especificação** | Detalhamento das regras de negócio | Documentos de especificações |
| **Refinamento** | Detalhamento técnico do sistema | Documento com descrição técnica, telas, API, estrutura de dados |
| **Plano de Execução** | Detalhamento das tarefas | Documento com tarefas e estimativa de conclusão |
| **Artefato Homologação** | Gerar e publicar artefato de homologação | Pull Request publicado no ambiente de homologação |
| **Artefato Produção** | Gerar e publicar artefato de produção | Pull Request publicado no ambiente de produção |

**Status atual:** apenas as fases de Discovery e Escopo foram desenvolvidas. As demais fases estão mapeadas mas ainda não implementadas.

---

## Decisões de Design

- **Skills modulares** — uma skill por documento, em vez de uma skill única end-to-end. Isso permite usar peças isoladas conforme a necessidade.
- **Interação conversacional + geração de documentos** — Claude conduz perguntas por blocos temáticos e ao final gera os arquivos `.md`.
- **Formato de saída** — Markdown (`.md`).
- **Público-alvo** — múltiplos perfis: Product Manager, Tech Lead, Desenvolvedor, Analista de Sistemas.
- **Armazenamento** — as skills ficam em `.claude/skills/` dentro do projeto; os documentos gerados ficam em `docs/`.
- **Repositório Git** — cada projeto deve ter uma URL de repositório, que é coletada na skill de init (pode ser "a definir" se ainda não existir).

---

## Estrutura de Pastas

```
seu-projeto/
├── CLAUDE.md
├── .claude/
│   └── skills/
│       ├── discovery-init/
│       │   └── SKILL.md
│       ├── discovery-vision/
│       │   └── SKILL.md
│       ├── discovery-opportunity/
│       │   └── SKILL.md
│       ├── discovery-assumptions/
│       │   └── SKILL.md
│       ├── discovery-stakeholders/
│       │   └── SKILL.md
│       ├── discovery-metrics/
│       │   └── SKILL.md
│       └── scope-generate/
│           └── SKILL.md
│
└── docs/
    └── {nome-do-projeto}/
        ├── project.md
        ├── discovery/
        │   ├── vision.md
        │   ├── opportunity.md
        │   ├── assumptions.md
        │   ├── stakeholders.md
        │   └── success-metrics.md
        └── escopo/
            └── {titulo-do-escopo}/
                ├── escopo.md
                └── discovery/
                    └── (cópias dos arquivos de discovery relevantes)
```

---

## Skills Implementadas

### 1. `discovery-init`
**Gatilho:** "iniciar projeto", "novo projeto", "começar discovery", "criar projeto"
**O que faz:**
- Coleta nome do projeto, descrição resumida, URL do repositório Git e tipo de projeto
- Gera o arquivo `docs/{nome-do-projeto}/project.md` com metadados e status das fases
- Pergunta se o usuário quer criar a estrutura de pastas `discovery/` e `escopo/`
- Sugere as próximas skills de discovery disponíveis
- É o ponto de entrada recomendado para todas as outras skills

---

### 2. `discovery-vision`
**Gatilho:** "visão do projeto", "definir visão", "proposta de valor", "público-alvo", "qual o problema"
**O que faz:**
- Conduz conversa em blocos: O Problema → Público-Alvo → Proposta de Valor → Contexto → Restrições
- Gera `docs/{nome-do-projeto}/discovery/vision.md`
- Documento inclui: descrição do problema, perfis de usuário, proposta de valor, motivação, restrições e declaração de visão

---

### 3. `discovery-opportunity`
**Gatilho:** "oportunidades do projeto", "mapear dores", "jobs to be done", "dores dos usuários"
**O que faz:**
- Baseada no framework Opportunity Solution Tree (Teresa Torres) e Jobs to Be Done (Christensen/Ulwick)
- Conduz conversa em blocos: Jobs to Be Done → Dores → Desejos → Contexto de Uso → Tentativas Anteriores
- Gera `docs/{nome-do-projeto}/discovery/opportunity.md`
- Nunca sugere soluções durante essa etapa — foco total no problema

---

### 4. `discovery-assumptions`
**Gatilho:** "hipóteses do projeto", "premissas", "o que ainda não sabemos", "validações necessárias"
**O que faz:**
- Baseada no Assumption Mapping (David Bland & Alex Osterwalder) e Lean Startup (Eric Ries)
- Conduz conversa em blocos: Hipóteses sobre Usuários → Hipóteses de Negócio → Hipóteses Técnicas → Priorização
- Usa matriz de priorização: alto impacto + baixa certeza = validar primeiro
- Gera `docs/{nome-do-projeto}/discovery/assumptions.md`
- Sugere formas concretas de validar hipóteses críticas

---

### 5. `discovery-stakeholders`
**Gatilho:** "stakeholders", "partes interessadas", "quem aprova", "quem é afetado", "mapa de envolvidos"
**O que faz:**
- Conduz conversa em blocos: Identificação → Classificação por Interesse/Influência → Expectativas → Estratégia de Comunicação
- Usa matriz poder/interesse para classificar stakeholders
- Gera `docs/{nome-do-projeto}/discovery/stakeholders.md`
- Inclui matriz de comunicação com canal, frequência e responsável

---

### 6. `discovery-metrics`
**Gatilho:** "métricas do projeto", "como medir sucesso", "KPIs", "OKRs", "critérios de sucesso"
**O que faz:**
- Baseada nos frameworks OKR, North Star Metric e HEART (Google)
- Conduz conversa em blocos: Objetivo Central → North Star Metric → Métricas de Negócio → Métricas de Produto/Usuário → Critérios de Aceitação → Baseline e Metas
- Gera `docs/{nome-do-projeto}/discovery/success-metrics.md`
- Empurra métricas vagas para métricas mensuráveis com baseline e meta

---

### 7. `scope-generate`
**Gatilho:** "gerar escopo", "criar escopo", "montar escopo", "definir escopo", "escopo do projeto", "escopo do módulo"
**O que faz:**
- Lê todos os arquivos de `discovery/` do projeto
- Lê todos os escopos já existentes em `escopo/` para evitar duplicidade
- Um escopo pode cobrir o projeto inteiro ou uma parte (módulo, feature, fase)
- Cria a pasta `docs/{nome-do-projeto}/escopo/{titulo-kebab-case}/`
- Copia os arquivos de discovery relevantes para `escopo/{titulo}/discovery/`
- Gera `escopo.md` consolidando as informações

**Campos obrigatórios no `escopo.md`:**
- Título do escopo
- Situação: `Rascunho → Em revisão → Aprovado → Em execução → Concluído`
- Data de criação
- Histórico de situação

**Conteúdo do `escopo.md`:**
- Contexto
- Abrangência (inclui / não inclui)
- Usuários afetados
- Oportunidades endereçadas
- Funcionalidades e comportamentos esperados
- Hipóteses críticas associadas
- Stakeholders envolvidos
- Métricas de sucesso
- Restrições e dependências
- Escopos relacionados
- Histórico de situação

**Proteção contra duplicidade:**
- Nunca repete funcionalidades de escopos `Aprovado` ou `Em execução`
- Avisa sobre sobreposição com escopos em `Rascunho` ou `Em revisão`, mas não bloqueia

---

## Skills Mapeadas para Fases Futuras (não implementadas)

| Fase | Skills previstas |
|---|---|
| **Especificação** | `spec-business-rules`, `spec-functional`, `spec-nonfunctional` |
| **Refinamento** | `refinement-screens`, `refinement-api`, `refinement-data-model` |
| **Plano de Execução** | `plan-tasks`, `plan-estimation` |
| **Homologação** | `deploy-homolog` |
| **Produção** | `deploy-production` |

---

## Próximos Passos Sugeridos

1. Instalar as 7 skills no `.claude/skills/` de um projeto real
2. Testar o fluxo completo: `discovery-init` → skills de discovery → `scope-generate`
3. Validar os documentos gerados e ajustar os templates se necessário
4. Iniciar o desenvolvimento das skills de **Especificação**
