# Template Completo: spec-functional.md

Este arquivo contém o template do documento de especificação funcional com
exemplos preenchidos para facilitar o entendimento do formato esperado.

---

## Template Vazio

```markdown
# Especificação Funcional — {Título do Escopo}

> Gerado em: {DD/MM/YYYY}
> Versão: 1.0
> Status: Rascunho
> Referência: docs/{projeto}/escopo/{escopo}/escopo.md

---

## Contexto

{2 a 4 linhas resumindo o escopo que originou esta especificação.
Copie ou parafraseie do campo "Contexto" do escopo.md.}

---

## Features Especificadas

- [Feature 1: {nome}](#feature-1-nome)
- [Feature 2: {nome}](#feature-2-nome)

---

## Feature {N}: {Nome}

### Narrativa

Feature: {nome}
  In order to {objetivo de negócio mensurável}
  As {ator principal — quem se beneficia ou usa a feature}
  I want {o que o sistema deve ser capaz de fazer}

### Regras de Negócio

Declarações que governam o comportamento desta feature.
Escreva em linguagem declarativa — o que DEVE ser verdade, não como implementar.

- **RN-{N}.1** — {descrição da regra}
- **RN-{N}.2** — {descrição da regra}

### Cenários

---

#### Cenário {N}.1: {Título — happy path}

Dado {contexto em termos de negócio}
  E {contexto adicional, se necessário}
Quando {ação do ator — única ação principal}
Então {resultado verificável e específico}
  E {resultado adicional, se necessário}

---

#### Cenário {N}.2: {Título — caso alternativo}

Dado {contexto diferente do happy path}
Quando {mesma ação ou ação alternativa}
Então {resultado diferente — inclusive mensagens de erro}

---

#### Cenário {N}.3: {Título — tabela de exemplos quando há múltiplas combinações}

Esquema do Cenário: {título genérico que cobre todos os casos}
  Dado {contexto com variavel}
  Quando {ação}
  Então {resultado com resultado}

  Exemplos:
    | variavel | resultado |
    | {valor1} | {saida1}  |
    | {valor2} | {saida2}  |
    | {valor3} | {saida3}  |

### Pontos em Aberto

- [ ] {Pergunta específica a ser respondida + quem pode responder}

---

## Próximos Passos Sugeridos

- **spec-usecases** — para fluxos com múltiplos atores ou ramificações complexas
- **spec-nonfunctional** — para requisitos de performance, segurança ou disponibilidade
- **refinement-screens** — para detalhar as interfaces que suportam estes cenários
- **refinement-api** — para detalhar os contratos de API necessários

---

## Histórico

| Data | Versão | Alteração | Autor |
|------|--------|-----------|-------|
| {DD/MM/YYYY} | 1.0 | Versão inicial | — |
```

---

## Exemplo Preenchido — Módulo de Pontuação Frequent Flyer

```markdown
# Especificação Funcional — Cálculo de Pontos por Voo

> Gerado em: 06/04/2026
> Versão: 1.0
> Status: Rascunho
> Referência: docs/flying-high/escopo/pontuacao-voos/escopo.md

---

## Contexto

Este escopo define o comportamento do cálculo de pontos Frequent Flyer para voos
da Flying High Airlines. O objetivo é incentivar a fidelidade dos clientes,
recompensando mais quem tem status mais alto no programa.

---

## Features Especificadas

- [Feature 1: Ganhar pontos base por distância voada](#feature-1-ganhar-pontos-base)
- [Feature 2: Aplicar bônus de status](#feature-2-aplicar-bonus-de-status)

---

## Feature 1: Ganhar Pontos Base por Distância Voada

### Narrativa

Feature: Ganhar pontos base por distância voada
  In order to incentivar membros a voar mais com a Flying High
  As o gerente do programa Frequent Flyer
  I want que membros ganhem pontos proporcionais à distância voada

### Regras de Negócio

- **RN-1.1** — Pontos base são calculados à razão de 0,5 ponto por quilômetro voado
- **RN-1.2** — A distância usada é a distância entre os aeroportos de origem e destino
- **RN-1.3** — Pontos são creditados após confirmação do embarque

### Cenários

---

#### Cenário 1.1: Calcular pontos para voo doméstico em Economy

Dado que a distância Sydney–Melbourne é 878 km
  E que sou membro Frequent Flyer padrão
Quando voo de Sydney para Melbourne em Economy
Então devo ganhar 439 pontos

---

#### Cenário 1.2: Não creditar pontos se o membro não embarcou

Dado que tenho reserva confirmada no voo Sydney–Melbourne
  E que não realizei o check-in
Quando o voo parte
Então não devo receber pontos por este voo

---

## Feature 2: Aplicar Bônus de Status

### Narrativa

Feature: Aplicar bônus de status
  In order to recompensar clientes mais fiéis e incentivar upgrade de categoria
  As o gerente do programa Frequent Flyer
  I want que membros Prata e Ouro recebam pontos extras além dos pontos base

### Regras de Negócio

- **RN-2.1** — Membro Padrão recebe apenas os pontos base, sem bônus
- **RN-2.2** — Membro Prata recebe 50% de bônus sobre os pontos base
- **RN-2.3** — Membro Ouro recebe 75% de bônus sobre os pontos base
- **RN-2.4** — Membro Ouro tem garantia mínima de 1.000 pontos por viagem

### Cenários

---

#### Cenário 2.1: Calcular pontos por status do membro

Esquema do Cenário: Calcular pontos por status do membro Frequent Flyer
  Dado que sou membro Frequent Flyer com status {status}
  Quando voo em trecho que vale {base} pontos base
  Então devo ganhar {total} pontos no total

  Exemplos:
    | status  | base | total | notas                          |
    | Padrão  | 439  | 439   | sem bônus                      |
    | Prata   | 148  | 500   | mínimo garantido Prata         |
    | Prata   | 439  | 659   | 50% de bônus                   |
    | Ouro    | 439  | 1000  | mínimo garantido Ouro          |
    | Ouro    | 2040 | 3570  | 75% de bônus acima do mínimo   |

---

#### Cenário 2.2: Garantir mínimo de pontos para membro Ouro em voo curto

Dado que sou membro Ouro
  E que voo em trecho curto que vale apenas 200 pontos base
Quando o voo é concluído
Então devo ganhar 1000 pontos (garantia mínima Ouro, não 350 do bônus de 75%)

### Pontos em Aberto

- [ ] O mínimo garantido para membro Prata é de quanto? (Referência: equipe marketing)
- [ ] O bônus de status se aplica a voos de parceiros? (Referência: gerente do programa)

---

## Próximos Passos Sugeridos

- **spec-nonfunctional** — verificar requisitos de disponibilidade do serviço de pontuação
- **refinement-api** — detalhar o contrato do endpoint de registro de voo

---

## Histórico

| Data | Versão | Alteração | Autor |
|------|--------|-----------|-------|
| 06/04/2026 | 1.0 | Versão inicial | Sarah (BA) |
```
