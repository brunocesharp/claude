# Técnica de Extração de Exemplos

Referência baseada em *BDD in Action* — John Ferguson Smart (Manning, 2015),
capítulo 4, e *Specification by Example* — Gojko Adzic (Manning, 2011).

---

## Por que Conversar em Torno de Exemplos

Usuários e stakeholders raramente expressam o que precisam em termos de valor
de negócio puro. Eles tendem a pedir soluções técnicas específicas porque é o que
conhecem. O problema é duplo:

1. Eles não são especialistas em software — a solução que pedem pode não ser a ideal
2. Se você não entende o **porquê** de uma feature, não consegue adaptá-la quando
   as circunstâncias mudam

A técnica de conversas em torno de exemplos resolve isso: ao invés de discutir a
solução abstrata, você discute casos concretos do mundo real. Isso força a
clareza — exemplos não permitem ambiguidade.

---

## O Ciclo de Aprendizado pelo Exemplo

Baseado nas Teorias de Aprendizagem Experimental de David Kolb:

```
1. Experiência    → Discutir um exemplo concreto de como a feature deve funcionar
2. Reflexão       → Pensar sobre o exemplo e procurar inconsistências
3. Conceitualizar → Construir modelo mental do requisito a partir dos exemplos
4. Testar         → Buscar novos exemplos que confirmem ou invalidem o modelo
```

Na prática, cada exemplo que você levanta é como uma peça de quebra-cabeça:
- Se se encaixa, confirma sua compreensão
- Se não se encaixa, revelou uma premissa errada — ótimo, melhor descobrir agora

---

## Como Conduzir a Conversa

### Comece sempre pelo exemplo mais simples

> "Me dá um exemplo concreto. Se eu usasse essa funcionalidade hoje,
> o que eu faria e o que esperaria ver?"

O caso mais comum (happy path) é o ponto de partida. Ele ancora a conversa
em algo real antes de explorar variações.

### Use números e valores reais

Especificações com valores concretos são mais úteis que regras abstratas.

```
❌  "Membros ganham pontos por quilômetro voado"
✅  "Se você voa Sydney–Melbourne (878 km) em Economy, ganha 439 pontos"
```

O segundo exemplo imediatamente levanta a pergunta: e em Business? e para
membros Gold? — revelando requisitos que a versão abstrata escondia.

### A técnica "Popping the Why Stack"

Quando um stakeholder pede uma feature específica, pergunte "por quê?" até
chegar a um objetivo de negócio mensurável. Geralmente 3 a 5 porquês bastam.

Exemplo:
- **Stakeholder:** "Quero que as pessoas possam postar anúncios classificados online"
- **Você:** "Por quê?" → "Porque as pessoas não leem mais o jornal impresso"
- **Você:** "Por quê isso é um problema?" → "A receita dos classificados está caindo"
- **Você:** "Como anúncios online vai aumentar a receita?" → "Mais visibilidade = mais vendas = mais comissão"

Resultado: o objetivo real é **aumentar receita de comissão**, não "ter anúncios online".
Isso abre espaço para outras soluções que talvez sejam mais baratas ou eficazes.

---

## O Formato "Três Amigos"

A forma mais eficiente de levantar exemplos envolve três perfis ao mesmo tempo:

| Perfil | Contribuição principal |
|---|---|
| **Analista / PO** | Conhece o negócio, valida relevância dos exemplos |
| **Desenvolvedor** | Aponta implicações técnicas, custo de cada abordagem |
| **Testador / QA** | Levanta casos de borda, exceções, casos que "quebram" a regra |

O testador é especialmente valioso nesta fase: seu instinto natural é perguntar
"e se...?" — exatamente o que transforma um exemplo simples em uma especificação robusta.

---

## Tipos de Exemplos a Levantar

Para cobrir uma feature com qualidade, você precisa de pelo menos:

### 1. Caso padrão (happy path)
O fluxo mais comum, onde tudo funciona como esperado.
> "Dado que Pedro tem saldo suficiente, quando solicita transferência de R$100, então..."

### 2. Variações válidas
Casos que seguem a regra mas com dados diferentes.
> "E se Pedro for cliente Gold? E se a transferência for para outro banco?"

### 3. Limites (boundary conditions)
O comportamento exatamente nos limites das regras.
> "E se o saldo for exatamente igual ao valor da transferência? E se for R$0,01 a menos?"

### 4. Casos inválidos
O que acontece quando a entrada está errada ou incompleta.
> "E se o CPF do destinatário não existir? E se o valor for negativo?"

### 5. Casos de exceção
Falhas externas ou situações fora do controle do usuário.
> "E se o banco destinatário estiver indisponível? E se a sessão expirar durante a operação?"

---

## Sinais de que um Exemplo Revelou uma Lacuna

Durante a conversa, preste atenção nestes sinais:

- **Stakeholder hesita antes de responder** — provavelmente não pensou nesse caso ainda
- **Resposta contradiz algo dito antes** — pode haver conflito de regras ou entendimento incorreto
- **"Depende"** — sempre que ouvir isso, pergunte "depende de quê?" e documente as condições
- **"Nunca vai acontecer"** — documente o caso de qualquer forma; se nunca vai acontecer, o teste é barato; se acontecer, você estava preparado

---

## Transformando Exemplos em Cenários

Depois da conversa, organize os exemplos em cenários estruturados:

**Exemplo bruto da conversa:**
> "Se você voa Sydney–Melbourne em Economy como membro Prata, ganha 50% a mais,
> então 659 pontos no total"

**Cenário formalizado:**
```gherkin
Cenário: Membro Prata ganha bônus de status em voos Economy
  Dado que a distância Sydney–Melbourne é 878 km
  E que sou membro Frequent Flyer com status Prata
  Quando voo de Sydney para Melbourne em Economy
  Então devo ganhar 659 pontos no total
```

**Quando há múltiplas variações, consolide em tabela:**
```gherkin
Esquema do Cenário: Calcular pontos por status do membro
  Dado que sou membro com status {status}
  Quando voo em trecho de {base} pontos base
  Então devo ganhar {total} pontos no total

  Exemplos:
    | status  | base | total |
    | Padrão  | 439  | 439   |
    | Prata   | 439  | 659   |
    | Ouro    | 439  | 1000  |
```

---

## O que Fazer com Lacunas

Quando não houver resposta clara para um exemplo:

1. **Não invente** — especificações incorretas custam mais do que lacunas explícitas
2. **Documente como "Ponto em Aberto"** com a pergunta específica a ser respondida
3. **Identifique quem pode responder** — nome do stakeholder ou área responsável
4. **Estime o impacto** — essa lacuna bloqueia o desenvolvimento ou é periférica?

Exemplo de ponto em aberto bem documentado:
```
- [ ] Qual é o comportamento quando o membro Ouro voa em Business class?
      A regra do mínimo garantido (1000 pts) se aplica? Ou há um mínimo diferente?
      Responsável: equipe de marketing do programa Frequent Flyer
```
