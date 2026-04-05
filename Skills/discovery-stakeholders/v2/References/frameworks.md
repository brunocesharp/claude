# Frameworks de Referência

Este documento detalha os frameworks teóricos utilizados na skill `discovery-stakeholders`.

---

## Power-Interest Matrix (Mendelow)

### O que é

Matriz 2x2 que classifica stakeholders por seu nível de poder/influência sobre o projeto e seu interesse no resultado. Desenvolvida por Aubrey Mendelow.

### A Matriz

```
                         INTERESSE NO PROJETO
                      Baixo                Alto
                ┌─────────────────┬─────────────────┐
                │                 │                 │
        Alta    │    MANTER       │    ENGAJAR      │
                │   SATISFEITO    │   ATIVAMENTE    │
  INFLUÊNCIA    │                 │                 │
                │  "Mantenha-os   │  "Parceiros     │
                │   do seu lado"  │   estratégicos" │
                ├─────────────────┼─────────────────┤
                │                 │                 │
        Baixa   │   MONITORAR     │    MANTER       │
                │                 │   INFORMADO     │
                │                 │                 │
                │  "Esforço       │  "Comunicação   │
                │   mínimo"       │   regular"      │
                └─────────────────┴─────────────────┘
```

### Os Quadrantes

#### Engajar Ativamente (Alta Influência + Alto Interesse)

**Quem são:** Patrocinadores, decisores principais, usuários-chave com poder

**Características:**
- Podem aprovar ou vetar o projeto
- Querem estar envolvidos nas decisões
- Seu sucesso pessoal pode depender do projeto

**Estratégia:**
- Envolvimento constante em decisões
- Comunicação frequente e detalhada
- Construir relacionamento de confiança
- Co-criação de soluções

**Risco se ignorar:** Bloqueio do projeto, mudança de direção forçada

---

#### Manter Satisfeito (Alta Influência + Baixo Interesse)

**Quem são:** Executivos seniores, diretoria, áreas de governança

**Características:**
- Têm poder mas não querem detalhes
- Se interessam apenas por resultados
- Podem intervir se algo der errado

**Estratégia:**
- Comunicação executiva e concisa
- Informar apenas marcos e riscos
- Não sobrecarregar com detalhes
- Antecipar problemas antes que cheguem a eles

**Risco se ignorar:** Surpresa negativa → intervenção → perda de autonomia

---

#### Manter Informado (Baixa Influência + Alto Interesse)

**Quem são:** Usuários finais, equipes operacionais, áreas impactadas

**Características:**
- Muito interessados mas pouco poder formal
- Podem influenciar informalmente (boicote, resistência)
- São os mais afetados pelo resultado

**Estratégia:**
- Comunicação regular e transparente
- Coletar feedback frequentemente
- Fazê-los sentir ouvidos
- Transformar em embaixadores

**Risco se ignorar:** Resistência na adoção, feedback negativo tardio

---

#### Monitorar (Baixa Influência + Baixo Interesse)

**Quem são:** Áreas periféricas, stakeholders indiretos

**Características:**
- Pouca conexão com o projeto
- Podem ser afetados marginalmente
- Não demandam atenção ativa

**Estratégia:**
- Comunicação mínima (newsletters, updates gerais)
- Monitorar se interesse ou influência mudam
- Não ignorar completamente

**Risco se ignorar:** Podem ganhar influência e você não perceber

---

## Stakeholder Mapping (Freeman)

### O que é

Abordagem mais ampla que vai além da matriz 2x2, considerando relacionamentos entre stakeholders, não apenas seu poder individual. Baseada no trabalho de R. Edward Freeman.

### Conceitos-chave

#### Stakeholders Primários vs Secundários

| Tipo | Definição | Exemplos |
|------|-----------|----------|
| **Primários** | Relação direta e formal com o projeto | Patrocinador, equipe, usuários, clientes |
| **Secundários** | Relação indireta ou informal | Mídia, comunidade, reguladores, concorrentes |

#### Rede de Influência

Stakeholders não existem isolados — eles se influenciam:

```
                    ┌──────────────┐
                    │  CEO         │
                    └──────┬───────┘
                           │ influencia
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Dir. TI  │ │Dir. Prod │ │Dir. Fin  │
        └────┬─────┘ └────┬─────┘ └──────────┘
             │            │
             ▼            ▼
        ┌──────────┐ ┌──────────┐
        │ Equipe   │ │ Usuários │
        │ Técnica  │ │ Finais   │
        └──────────┘ └──────────┘
```

**Por que importa:** Convencer o CEO pode ser mais eficiente que convencer cada diretor individualmente.

#### Dinâmica de Poder

O poder dos stakeholders não é fixo:

| Fator | Como muda o poder |
|-------|-------------------|
| Fase do projeto | Técnicos têm mais poder no início, negócio no final |
| Contexto organizacional | Reorganização pode mudar tudo |
| Resultados parciais | Sucesso aumenta poder do patrocinador |
| Crises | Stakeholders de risco/compliance ganham poder |

---

## RACI Matrix

### O que é

Matriz que define responsabilidades específicas por entrega ou decisão. Complementa o mapeamento de stakeholders.

### Os Papéis

| Letra | Papel | Definição | Regra |
|-------|-------|-----------|-------|
| **R** | Responsible | Quem executa o trabalho | Pode ter vários |
| **A** | Accountable | Quem aprova/responde pelo resultado | Apenas UM por item |
| **C** | Consulted | Quem deve ser consultado (duas vias) | Pode ter vários |
| **I** | Informed | Quem deve ser informado (uma via) | Pode ter vários |

### Exemplo

| Decisão/Entrega | PM | Dev Lead | Diretor TI | Usuários |
|-----------------|----|---------:|------------|----------|
| Definir escopo | R | C | A | C |
| Arquitetura | C | R | A | I |
| Priorização de backlog | A | C | I | C |
| Go-live | R | R | A | I |

### Quando usar

- Conflitos de "quem decide o quê"
- Projetos com muitos stakeholders
- Necessidade de clareza formal de papéis

---

## Combinando os Frameworks

### Fluxo Recomendado

1. **Identificar** todos os stakeholders (primários e secundários)
2. **Classificar** na matriz Power-Interest
3. **Mapear relacionamentos** entre eles (quem influencia quem)
4. **Definir RACI** para decisões críticas
5. **Criar estratégia** de engajamento por quadrante
6. **Revisar** regularmente (stakeholders mudam)

### Perguntas-guia

| Fase | Pergunta |
|------|----------|
| Identificação | "Quem é afetado positiva ou negativamente por esse projeto?" |
| Classificação | "Essa pessoa pode vetar ou acelerar o projeto?" |
| Relacionamentos | "Quem influencia essa pessoa? Quem ela influencia?" |
| Estratégia | "O que essa pessoa precisa para apoiar o projeto?" |
