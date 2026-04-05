---
name: discovery-stakeholders
description: Conduz o mapeamento de stakeholders durante o discovery, gerando o documento stakeholders.md. Use quando o usuário mencionar "stakeholders", "partes interessadas", "quem aprova", "quem é afetado", "mapa de envolvidos", "quem financia", "quem decide", "patrocinador", "sponsor", "quem consultar", "RACI", "matriz de responsabilidades", "conflitos de interesse", "quem bloqueia", "quem influencia", "dependências organizacionais", "áreas envolvidas". Requer discovery-init. NÃO use para visão geral (use discovery-vision), dores e oportunidades (use discovery-opportunity), hipóteses (use discovery-assumptions) ou métricas (use discovery-metrics). Esta skill foca em PESSOAS e RELACIONAMENTOS, não em problemas ou soluções.
metadata:
  author: Equipe de Discovery
  version: 1.1.0
  category: discovery
  depends-on: discovery-init
  recommended-after: discovery-assumptions
  output: docs/{projeto}/discovery/stakeholders.md
  frameworks: Power-Interest Matrix, Stakeholder Mapping
---

# Discovery Stakeholders

Conduz o mapeamento de stakeholders e gera o documento `stakeholders.md`.

Para detalhes sobre os frameworks (Power-Interest Matrix, Stakeholder Mapping), consulte `references/frameworks.md`.

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.

- **Se não existir**: pergunte "Quer que eu inicie o projeto agora usando a skill discovery-init?"
- **Se existir**: leia também `vision.md` se disponível — ajuda a identificar quem pode ser afetado.

---

## Fluxo de Execução

Conduza a conversa em blocos temáticos. Espere a resposta de cada bloco antes de avançar.

### Bloco 1 — Identificação dos Envolvidos

> "Vamos mapear todas as pessoas e grupos que têm alguma relação com esse projeto. Não precisa ser perfeito — vamos refinando."

Perguntas:
- "Quem vai usar o sistema no dia a dia?"
- "Quem solicitou ou patrocina esse projeto?"
- "Quem precisa aprovar decisões importantes?"
- "Quem será afetado mas não usa o sistema diretamente?"
- "Existe área ou equipe que depende dos resultados?"
- "Há cliente externo, parceiro ou fornecedor envolvido?"

**Validação:**
- Pelo menos 5-7 stakeholders devem ser identificados
- Deve incluir: 1 patrocinador, 1 usuário final, 1 decisor
- Se lista curta, pergunte sobre áreas adjacentes (TI, Jurídico, Compliance, RH)

---

### Bloco 2 — Classificação por Interesse e Influência

Para cada stakeholder identificado:

> "Para cada pessoa ou grupo: qual o interesse deles no projeto e quanta influência têm?"

Para detalhes da matriz de classificação, consulte `references/classification.md`.

Resumo rápido:
- **Engajar ativamente** = Alta influência + Alto interesse
- **Manter satisfeito** = Alta influência + Baixo interesse
- **Manter informado** = Baixa influência + Alto interesse
- **Monitorar** = Baixa influência + Baixo interesse

**Validação:**
- Todos os stakeholders devem ser classificados
- Se todos forem "alta influência", questione: "Quem realmente pode vetar decisões?"

---

### Bloco 3 — Expectativas e Preocupações

Para stakeholders de alta influência ou alto interesse:

> "O que cada um espera do projeto? E o que poderia fazê-los resistir ou dificultar?"

Perguntas:
- "Existe stakeholder que pode ser um bloqueador?"
- "Há tensão ou conflito de interesse entre stakeholders?"
- "Quem precisa ser envolvido em decisões de escopo?"

**Validação:**
- Stakeholders críticos devem ter expectativas documentadas
- Bloqueadores potenciais devem ter estratégia de mitigação

---

### Bloco 4 — Estratégia de Comunicação

> "Como vamos manter cada grupo informado e engajado?"

Perguntas:
- "Qual o canal preferido de cada grupo?"
- "Com que frequência cada grupo precisa de atualizações?"
- "Quem do time é responsável por cada relação?"

Para estratégias específicas por tipo, consulte `references/engagement-strategies.md`.

**Validação:**
- Stakeholders de alta influência devem ter responsável definido
- Frequência deve ser realista (não prometer reuniões semanais com 15 pessoas)

---

## Gerar o Documento

Após coletar as informações, gere `docs/{nome-do-projeto}/discovery/stakeholders.md` usando o template em `references/template-stakeholders.md`.

---

## Após Gerar o Documento

1. **Salve o arquivo** em `docs/{nome-do-projeto}/discovery/stakeholders.md`

2. **Informe o usuário:**

> "O `stakeholders.md` foi salvo. Com os stakeholders mapeados, fica mais fácil tomar decisões com as pessoas certas. Próximos passos:
>
> - **Métricas de sucesso** — definir como medir o sucesso do projeto
> - **Escopo** — consolidar tudo em um documento de escopo
>
> Qual faz mais sentido agora?"

---

## Regras Importantes

### Comportamento Obrigatório

- **Trate como pessoas** — stakeholders têm motivações reais, não são caixinhas em matriz
- **Linguagem neutra** — nunca registre opiniões negativas que possam constranger
- **Explore bloqueadores** — "O que precisaria para essa pessoa se tornar aliada?"
- **Aceite papéis** — se não souber o nome, registre pelo papel ("Diretor de TI")

### O Que NÃO Fazer

- Não reduza pessoas a rótulos simplistas
- Não ignore stakeholders de "baixa influência" — podem ganhar poder
- Não registre política organizacional sensível no documento
- Não assuma que influência é fixa — ela muda ao longo do projeto
- Não foque só em stakeholders óbvios — pergunte sobre áreas adjacentes

### Adaptação de Tom

- **Para PMs:** Foque em expectativas e comunicação
- **Para devs/tech leads:** Destaque decisores técnicos e dependências
- **Para founders:** Mapeie investidores, advisors, parceiros estratégicos

---

## Troubleshooting

Para problemas comuns, consulte `references/troubleshooting.md`.

Resumo dos mais frequentes:
- **Stakeholder oculto descoberto tarde** → revisite mapa regularmente
- **Conflito entre stakeholders de alta influência** → escalate para patrocinador
- **Patrocinador desengajado** → identifique proxy ou renegocie apoio
- **Muitos stakeholders** → priorize por impacto no projeto

---

## Exemplos

Para exemplos detalhados de uso, consulte `references/examples.md`.
