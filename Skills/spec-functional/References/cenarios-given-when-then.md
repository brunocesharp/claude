# Guia de Escrita de Cenários Given/When/Then

Referência baseada em *BDD in Action* — John Ferguson Smart (Manning, 2015),
capítulo 5, e *The Cucumber Book* — Matt Wynne e Aslak Hellesøy.

---

## A Estrutura Básica

```gherkin
Cenário: {título descritivo do comportamento}
  Dado {contexto / pré-condição}
  Quando {ação do ator}
  Então {resultado esperado}
```

| Palavra-chave | Papel | O que deve conter |
|---|---|---|
| **Dado** | Pré-condição | Estado do sistema antes da ação. Setup de dados em linguagem de negócio. |
| **Quando** | Ação | A única ação principal sendo testada. Uma ação por cenário. |
| **Então** | Resultado | O que o sistema faz em resposta. Verificável e específico. |
| **E / Mas** | Continuação | Extensão do passo anterior. Mesmo papel semântico. |

---

## O Título do Cenário

O título deve descrever **o comportamento**, não a ação técnica.

```
✅  Calcular pontos extras para voo em Business class
✅  Rejeitar transferência com saldo insuficiente
✅  Notificar membro quando associação está prestes a vencer

❌  Teste de cálculo de pontos
❌  Cenário de erro no saldo
❌  Verificar notificação
```

**Boas práticas para o título:**
- Use linguagem declarativa no infinitivo ou substantivo: "Calcular...", "Rejeitar...", "Notificar..."
- Inclua o contexto que diferencia este cenário dos outros da mesma feature
- Evite incluir o resultado esperado no título (ele pode mudar; o contexto é mais estável)
- Lido isoladamente, o título deve dizer o que o cenário testa

---

## Escrevendo o Dado (Given)

O Given coloca o sistema no estado certo para o teste.

**Princípios:**
- Inclua apenas as pré-condições **relevantes para este cenário**
- Use **tempo passado** para indicar que são estados já estabelecidos: "Dado que João **registrou** conta" em vez de "Dado que João **registra** conta"
- Expresse em termos de **negócio**, não de setup técnico

```gherkin
✅  Dado que Maria é cliente Gold com saldo de 500 pontos
❌  Dado que a tabela customers tem um registro com status='gold' e points=500
```

Pré-condições técnicas (banco de dados, autenticação, navegação até a página) devem
acontecer nos bastidores, fora do texto do cenário.

**Background:** quando múltiplos cenários de uma feature compartilham os mesmos
Givens, use a seção Background para evitar repetição:

```gherkin
Contexto:
  Dado que Martin é membro Frequent Flyer
  E que Martin cadastrou senha 'secreta'

Cenário: Login com senha correta
  Quando Martin faz login com senha 'secreta'
  Então ele deve ter acesso ao site

Cenário: Login com senha incorreta
  Quando Martin faz login com senha 'errada'
  Então ele deve receber mensagem de senha incorreta
```

---

## Escrevendo o Quando (When)

O When descreve a ação principal sendo testada.

**Princípios:**
- **Uma única ação por cenário.** Se houver mais de uma ação relevante, divida em cenários separados ou use um passo de alto nível que as encapsula.
- Descreva o **o quê**, não o **como**: sem referência a botões, campos ou navegação.
- Use presente ou imperativo: "Quando João solicita transferência", não "Quando João vai até a tela de transferência e preenche o campo valor e clica em confirmar"

```gherkin
✅  Quando João solicita transferência de R$200
❌  Quando João vai até a tela de transferência
    E preenche o campo valor com '200'
    E clica no botão 'Confirmar'
```

---

## Escrevendo o Então (Then)

O Then verifica o resultado esperado.

**Princípios:**
- O resultado deve ser **verificável e específico**: valores concretos, não descrições vagas
- Expresse em termos de **valor de negócio**, não de estado técnico interno
- Evite Then com múltiplos resultados não relacionados — indício de que o cenário testa mais de uma coisa

```gherkin
✅  Então o saldo de João deve ser R$300
✅  Então João deve receber email de confirmação com número do protocolo
❌  Então o sistema deve funcionar corretamente
❌  Então tudo deve estar ok
```

---

## Cenários Independentes

Cada cenário deve funcionar de forma isolada. Não crie cenários que dependem
de outro ter rodado antes para preparar o estado.

```gherkin
❌ Fluxo incorreto (cenário 2 depende do 1):

Cenário: Adicionar item ao carrinho
  Dado que o produto 'BDD in Action' está disponível
  Quando adiciono ao carrinho
  Então meu carrinho deve conter 1 item

Cenário: Finalizar compra
  Quando finalizo o pagamento    ← depende que o cenário anterior rodou
  Então devo receber o livro
```

```gherkin
✅ Fluxo correto (cada cenário é autossuficiente):

Cenário: Comprar um item
  Dado que quero comprar um bom livro
  Quando compro 'BDD in Action'
  Então devo receber o livro pelo correio
```

---

## Tabelas de Dados em Passos

Use tabelas para expressar dados de forma concisa quando um passo envolver
múltiplos registros:

```gherkin
Cenário: Transferência de pontos entre membros
  Dado as seguintes contas:
    | titular  | pontos | pontos-status |
    | Danielle | 100000 | 800           |
    | Martin   | 50000  | 50            |
  Quando Martin transfere 40000 pontos para Danielle
  Então as contas devem ser:
    | titular  | pontos | pontos-status |
    | Danielle | 140000 | 800           |
    | Martin   | 10000  | 50            |
```

---

## Esquema do Cenário (Scenario Outline)

Quando a mesma regra de negócio precisa ser verificada com múltiplas combinações
de entrada/saída, use Esquema do Cenário com tabela de Exemplos:

```gherkin
Esquema do Cenário: Calcular pontos extras por status do membro
  Dado que sou membro Frequent Flyer com status {status}
  Quando voo em um trecho que vale {base} pontos base
  Então devo ganhar {total} pontos no total

  Exemplos:
    | status   | base | total |
    | Padrão   | 439  | 439   |
    | Prata    | 439  | 659   |
    | Ouro     | 439  | 1000  |
    | Ouro     | 2040 | 3570  |
```

**Quando usar:** dois ou mais cenários que diferem apenas nos dados devem ser
consolidados em um único Esquema do Cenário.

**Vantagem adicional:** a tabela torna mais fácil identificar casos faltantes e
verificar boundary conditions (limites).

---

## Anti-padrões Comuns

### 1. Cenário como script de UI

```gherkin
❌
Cenário: Atualizar endereço
  Dado que estou logado como cliente
  Então devo ver a página inicial
  Quando seleciono o menu 'Conta'
  Então devo ver a página de conta
  Quando clico em 'Editar'
  Então devo ver o formulário de endereço
  Quando digito '100 Rua Principal' no campo rua
  E clico em 'Salvar'
  Então devo ver os dados atualizados
```

```gherkin
✅
Cenário: Atualizar endereço
  Dado que sou cliente cadastrado
  Quando atualizo meu endereço
  Então os novos dados devem aparecer no resumo da conta
```

### 2. Then vago

```gherkin
❌  Então o sistema deve funcionar corretamente
❌  Então a operação deve ser concluída com sucesso
✅  Então o saldo deve ser debitado em R$200
✅  Então deve aparecer mensagem "Transferência realizada com sucesso"
```

### 3. Múltiplos Whens no mesmo cenário

```gherkin
❌
Quando seleciono o produto
E adiciono ao carrinho
E acesso o carrinho
E clico em finalizar compra
```

```gherkin
✅
Quando finalizo a compra do produto 'BDD in Action'
```

### 4. Cenários dependentes entre si

Cada cenário deve preparar seu próprio estado inicial. Não assuma que um
cenário anterior criou dados ou colocou o sistema em um estado específico.

### 5. Regras de negócio disfarçadas de passos de implementação

```gherkin
❌  Dado que a linha 47 da tabela T_PEDIDOS tem status = 'APROVADO'
✅  Dado que o pedido de Maria está aprovado
```

---

## Checklist de Qualidade

Antes de finalizar um cenário, verifique:

- [ ] O título descreve o comportamento, não a ação técnica?
- [ ] O Given está em linguagem de negócio, sem referências a banco ou interface?
- [ ] Há apenas uma ação no When?
- [ ] O Then tem resultado específico e verificável?
- [ ] O cenário funciona de forma independente, sem depender de outro?
- [ ] Se dois cenários diferem apenas nos dados, foram consolidados em Esquema?
- [ ] Os casos de borda (mínimo, máximo, vazio, inválido) estão cobertos?
