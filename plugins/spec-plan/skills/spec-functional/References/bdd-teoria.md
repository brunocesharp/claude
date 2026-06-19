# BDD — Teoria e Fundamentos

Referência baseada em *BDD in Action* — John Ferguson Smart (Manning, 2015),
capítulos 1, 3 e 4.

---

## O que é BDD

Behavior-Driven Development (BDD) é um conjunto de práticas de engenharia de
software projetado para ajudar times a construir e entregar software de maior valor
e qualidade mais rapidamente.

BDD parte de dois problemas centrais em projetos de software:
- **Não construir o software certo** — entregar features que o negócio não precisa
- **Não construir o software de forma certa** — código frágil, difícil de manter

A resposta do BDD: usar conversas em torno de **exemplos concretos** para
construir um entendimento compartilhado dos requisitos antes de escrever qualquer
código.

---

## A Hierarquia de Abstrações

```
Objetivo de Negócio (Business Goal)
    └── Capacidade (Capability)
            └── Feature
                    └── User Story  ← artefato de planejamento, descartável
                            └── Cenários (Given/When/Then)
                                    └── Exemplos Concretos
```

### Objetivo de Negócio (Business Goal)
Declaração de alto nível de como o projeto beneficiará a organização.
Sempre mensurável: aumentar receita, reduzir custo, proteger receita, evitar custo futuro.

Formato recomendado:
```
In order to {impacto mensurável no negócio}
As {papel executivo ou área responsável}
I want {comportamento ou estratégia esperada}
```

Exemplo:
```
In order to increase ticket sales by 5% over the next year
As the Flying High Sales Manager
I want to encourage travellers to fly with Flying High rather than rivals
```

### Capacidade (Capability)
O que o sistema precisa ser capaz de fazer para realizar o objetivo de negócio.
Não implica implementação específica. Pode ser prefixada com "to be able to".

Exemplo: "the ability to book a flight online"

### Feature
Funcionalidade concreta entregável que suporta uma capacidade. É o que aparece
no manual do usuário. Deve ser testável pelos usuários em isolamento.

Formato recomendado (Feature Injection):
```
Feature: {nome}
  In order to {objetivo de negócio}
  As {ator principal}
  I want {o que o sistema faz}
```

### User Story
Ferramenta de planejamento para quebrar uma feature em partes implementáveis.
**Artefato temporário** — pode ser descartado após a feature ser entregue.
O que persiste são os cenários, não as histórias.

### Cenários (Given/When/Then)
Exemplos concretos e executáveis que ilustram como a feature se comporta.
São a especificação viva do sistema.

---

## Por que Exemplos Concretos?

Especificações em linguagem natural são ambíguas por natureza. Exemplos concretos
eliminam ambiguidade porque não permitem interpretação: ou o sistema faz
exatamente aquilo, ou não faz.

Exemplo de especificação vaga:
> "Members will earn Frequent Flyer points from Flying High flights."

Exemplo de especificação concreta:
> **Dado** que a distância Sydney–Melbourne é 878 km
> **Quando** eu voo de Sydney para Melbourne em Economy como membro padrão
> **Então** eu devo ganhar 439 pontos

A segunda versão responde perguntas que a primeira levanta: quantos pontos? por
qual critério? varia conforme a classe? — sem precisar escrever uma linha a mais.

---

## Feature Injection

Técnica de análise de requisitos baseada em três passos (Kent McDonald e Chris Matts):

1. **Caçar o valor** — entender como o sistema deve entregar valor ao negócio antes
   de decidir quais features construir
2. **Injetar as features** — identificar as features que melhor entregam esse valor,
   partindo dos outputs/outcomes e trabalhando de trás para frente
3. **Identificar os exemplos** — usar exemplos concretos para expandir o entendimento
   de como cada feature deve se comportar

O princípio fundamental: **o valor vem dos outputs, não dos inputs**. Para saber
quais features têm maior ROI, comece pelos resultados que entregam mais valor e
trabalhe de trás para frente até encontrar o mínimo necessário para produzi-los.

---

## Impact Mapping

Mapa visual que conecta objetivos de negócio a features através de 4 perguntas:

```
Por quê? (Why)   → Objetivo de negócio
Quem? (Who)      → Stakeholders e atores afetados
Como? (How)      → Como esses atores contribuem ou impedem o objetivo
O quê? (What)    → Features que habilitam os comportamentos desejados
```

Útil para: priorizar features, tornar premissas visíveis, conectar backlog a objetivos.

---

## Deliberate Discovery

Princípio proposto por Dan North: a maior restrição em projetos de software é a
**ignorância**. Quanto mais você sabe sobre o problema antes de comprometer-se
com uma solução, menor o risco.

Aplicado à especificação: identifique ativamente as áreas de incerteza e trate-as
antes de especificar os cenários. Exemplos concretos são a principal ferramenta
para reduzir ignorância — cada exemplo levantado ou confirmado reduz o espaço
de interpretação possível.

---

## Real Options

Princípio proposto por Chris Matts: não se comprometa com uma solução antes de
ter informação suficiente para escolher bem.

Na especificação funcional isso se traduz em: quando uma regra de negócio ainda
não está clara, **não invente** — marque como "Ponto em Aberto" e mantenha a
opção em aberto até ter a resposta do stakeholder. Comprometer-se com uma
especificação errada é mais custoso do que deixar o ponto explicitamente em aberto.
