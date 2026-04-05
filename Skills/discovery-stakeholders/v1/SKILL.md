---
name: discovery-stakeholders
description: Conduz o mapeamento de stakeholders durante o discovery de um projeto. Use esta skill sempre que o usuário mencionar "stakeholders", "partes interessadas", "quem aprova o projeto", "quem é afetado", "mapa de envolvidos", "quem financia", "quem decide", "patrocinador do projeto", "quem precisa ser consultado" ou qualquer variação que indique a necessidade de identificar e classificar os envolvidos no projeto. Use proativamente sempre que o usuário estiver descrevendo conflitos de interesse, dependências organizacionais ou precisar entender quem influencia o sucesso do projeto.
---

# Discovery Stakeholders

Skill responsável por conduzir o mapeamento de stakeholders e gerar o documento `stakeholders.md`.

---

## Pré-requisito

Verifique se `docs/{nome-do-projeto}/project.md` existe.
- **Se não existir**: sugira iniciar com `discovery-init`.
- **Se existir**: leia o arquivo e também `vision.md` se disponível — ele ajuda a contextualizar quem pode ser afetado.

---

## Fluxo de execução

### Bloco 1 — Identificação dos Envolvidos

> "Vamos mapear todas as pessoas e grupos que têm alguma relação com esse projeto. Não precisa ser perfeito agora — vamos refinando."

Perguntas iniciais:
- "Quem vai usar o sistema no dia a dia?"
- "Quem solicitou ou patrocina esse projeto?"
- "Quem precisa aprovar decisões importantes?"
- "Quem vai ser afetado pelo projeto mas não vai usar o sistema diretamente?"
- "Existe alguma área ou equipe que depende dos resultados desse sistema?"
- "Há algum cliente externo, parceiro ou fornecedor envolvido?"

---

### Bloco 2 — Classificação por Interesse e Influência

Para cada stakeholder identificado, pergunte:

> "Para cada pessoa ou grupo, me ajude a entender: **qual o interesse deles no projeto** e **quanta influência têm sobre ele**?"

Use a matriz de classificação:

```
              ALTA INFLUÊNCIA
                    |
  Manter satisfeito |  Engajar ativamente
  (consultar sempre)|  (parceiro estratégico)
                    |
BAIXO INTERESSE ----+---- ALTO INTERESSE
                    |
  Monitorar         |  Manter informado
  (baixa prioridade)|  (comunicar regularmente)
                    |
              BAIXA INFLUÊNCIA
```

---

### Bloco 3 — Expectativas e Preocupações

Para os stakeholders de alta influência ou alto interesse:

> "O que cada um deles espera do projeto? E o que poderia fazê-los resistir ou dificultar o andamento?"

Perguntas de aprofundamento:
- "Existe algum stakeholder que pode ser um bloqueador?"
- "Existe alguma tensão ou conflito de interesse entre stakeholders?"
- "Quem precisa ser envolvido nas decisões de escopo para evitar problemas depois?"

---

### Bloco 4 — Estratégia de Comunicação

> "Como vamos manter cada grupo informado e engajado ao longo do projeto?"

Perguntas:
- "Qual o canal preferido de cada grupo? (reunião, e-mail, dashboard, relatório...)"
- "Com que frequência cada grupo precisa de atualizações?"
- "Quem do time é responsável por cada relação?"

---

## Gerar o documento `stakeholders.md`

Salve em:
```
docs/{nome-do-projeto}/discovery/stakeholders.md
```

Template:

```markdown
# Mapa de Stakeholders — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}

---

## Mapa de Envolvidos

| Stakeholder | Papel | Interesse | Influência | Classificação |
|---|---|---|---|---|
| {nome/grupo} | {papel} | {alto/médio/baixo} | {alta/média/baixa} | {engajar/satisfazer/informar/monitorar} |

---

## Detalhamento por Stakeholder

### {Nome do Stakeholder 1}
- **Papel:** {descrição do papel}
- **O que espera do projeto:** {expectativas}
- **Preocupações / possíveis resistências:** {riscos de relacionamento}
- **Como engajar:** {estratégia}
- **Frequência de comunicação:** {diária / semanal / por marco}
- **Canal preferido:** {reunião / e-mail / Slack / relatório}
- **Responsável pelo relacionamento:** {nome ou área}

---

## Stakeholders Críticos ⚠️

> Stakeholders de alta influência que precisam de atenção especial.

- **{Nome}** — {por que é crítico e qual a estratégia}

---

## Tensões e Conflitos Identificados

{Liste eventuais conflitos de interesse entre stakeholders, ou "Nenhum identificado neste momento"}

---

## Matriz de Comunicação

| Stakeholder | Canal | Frequência | Responsável |
|---|---|---|---|
| {nome} | {canal} | {frequência} | {responsável} |
```

---

## Após gerar o documento

> "O `stakeholders.md` foi salvo em `docs/{nome-do-projeto}/discovery/`. Com os stakeholders mapeados, fica mais fácil tomar decisões de escopo com as pessoas certas. Quer continuar com:
> - **Métricas de sucesso** — definir como vamos medir o sucesso do projeto
> - **Escopo** — consolidar tudo em um documento de escopo"

---

## Regras importantes

- Trate stakeholders como pessoas com motivações reais — não os reduza a caixinhas em uma matriz.
- Se o usuário identificar um stakeholder bloqueador, explore isso: "O que precisaria acontecer para que essa pessoa se tornasse um aliado?"
- Nunca registre opiniões negativas sobre stakeholders de forma que possa ser embaraçoso se o documento for compartilhado — use linguagem neutra e profissional.
- Se o usuário não souber o nome de alguém, registre pelo papel: "Diretor de TI", "Equipe de Compliance", etc.
