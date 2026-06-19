# BDD Mapping Guide

## Contents
- Full mapping example (Gherkin → JUnit 5)
- Handling multiple Then steps
- Handling And / But steps
- Handling Scenario Outline (parameterized)
- Handling exceptions in BDD

---

## Full mapping example — Gherkin → JUnit 5

**BDD input:**

```gherkin
Feature: Criar pedido

  Scenario: Deve salvar pedido quando dados são válidos
    Given um pedido com produto "PROD-01" e quantidade 2
    When o serviço de pedidos recebe o pedido
    Then o pedido é salvo no repositório
    And o ID gerado é retornado
```

**Generated test:**

```java
@Test
@DisplayName("Deve salvar pedido quando dados são válidos")
void deveSalvarPedidoQuandoDadosSaoValidos() {
    // Given - um pedido com produto "PROD-01" e quantidade 2
    var order = new Order("PROD-01", 2);
    when(orderRepository.save(order)).thenReturn(order.withId(1L));

    // When - o serviço de pedidos recebe o pedido
    var result = sut.create(order);

    // Then - o pedido é salvo no repositório e o ID gerado é retornado
    verify(orderRepository, times(1)).save(order);
    assertNotNull(result.getId(),
        "O ID gerado deve ser retornado após salvar o pedido");
}
```

---

## Handling multiple Then steps

Each `Then` step becomes one assertion. Keep them in the same `// Then` block.

**BDD input:**

```gherkin
Then o status do pedido é "PENDENTE"
And o total calculado é R$ 20,00
And a data de criação não é nula
```

**Generated assertions:**

```java
// Then - status, total e data de criação verificados
assertEquals("PENDENTE", result.getStatus(),
    "O status inicial do pedido deve ser PENDENTE");
assertEquals(new BigDecimal("20.00"), result.getTotal(),
    "O total deve ser R$ 20,00 para 2 itens a R$ 10,00");
assertNotNull(result.getCreatedAt(),
    "A data de criação deve ser preenchida ao criar o pedido");
```

---

## Handling And / But steps

Append `And` and `But` to the block of the step they follow.

**BDD input:**

```gherkin
Given um usuário com ID 1 existe no sistema
And o usuário está ativo
When o serviço busca o usuário por ID 1
Then o usuário é retornado
But o campo senha não é incluído na resposta
```

**Generated test:**

```java
@Test
@DisplayName("Deve retornar usuário ativo sem senha quando ID existe")
void deveRetornarUsuarioAtivoSemSenhaQuandoIdExiste() {
    // Given - usuário com ID 1 existe e está ativo
    var user = new User(1L, "Alice", true);
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    // When - serviço busca o usuário por ID 1
    var result = sut.findById(1L);

    // Then - usuário retornado sem o campo senha
    assertTrue(result.isPresent(),
        "O usuário deve ser retornado quando o ID existe");
    assertNull(result.get().getPassword(),
        "O campo senha não deve ser incluído na resposta");
}
```

---

## Handling Scenario Outline (parameterized)

Use `@ParameterizedTest` with `@MethodSource` for Scenario Outlines.

**BDD input:**

```gherkin
Scenario Outline: Deve rejeitar quantidade inválida
  Given um pedido com quantidade <quantidade>
  When o serviço tenta criar o pedido
  Then uma exceção IllegalArgumentException é lançada

  Examples:
    | quantidade |
    | 0          |
    | -1         |
    | -100       |
```

**Generated test:**

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.stream.Stream;

static Stream<Integer> quantidadesInvalidas() {
    return Stream.of(0, -1, -100);
}

@ParameterizedTest(name = "quantidade={0}")
@MethodSource("quantidadesInvalidas")
@DisplayName("Deve rejeitar quantidade inválida")
void deveRejeitarQuantidadeInvalida(int quantidade) {
    // Given - pedido com quantidade inválida
    var order = new Order("PROD-01", quantidade);

    // When / Then - exceção lançada para quantidade inválida
    assertThrows(IllegalArgumentException.class,
        () -> sut.create(order),
        "Deve rejeitar quantidade " + quantidade + " por ser inválida");
}
```

---

## Handling exceptions in BDD

When `Then` describes an error or exception, use `assertThrows`. Merge `When` and `Then` blocks.

**BDD input:**

```gherkin
Scenario: Deve lançar exceção quando produto não encontrado
  Given nenhum produto com ID 99 existe no catálogo
  When o serviço tenta buscar o produto com ID 99
  Then uma exceção ProductNotFoundException é lançada
  And a mensagem de erro contém "Produto não encontrado"
```

**Generated test:**

```java
@Test
@DisplayName("Deve lançar exceção quando produto não encontrado")
void deveLancarExcecaoQuandoProdutoNaoEncontrado() {
    // Given - nenhum produto com ID 99 existe no catálogo
    when(productRepository.findById(99L)).thenReturn(Optional.empty());

    // When / Then - exceção lançada com mensagem correta
    var exception = assertThrows(ProductNotFoundException.class,
        () -> sut.findById(99L),
        "Deve lançar ProductNotFoundException quando o produto não existe");
    assertTrue(exception.getMessage().contains("Produto não encontrado"),
        "A mensagem de erro deve informar que o produto não foi encontrado");
}
```
