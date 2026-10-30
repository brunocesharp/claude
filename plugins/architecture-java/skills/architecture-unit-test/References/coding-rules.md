# Coding Rules

## Contents
- File template
- Rule 1: JUnit 5 imports only
- Rule 2: Assertions with messages
- Rule 3: Given-When-Then comments
- Rule 4: Portuguese method names

---

## File template

```java
package com.empresa.modulo;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("OrderService")
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService sut;

    @BeforeEach
    void setUp() {
        // additional setup if needed
    }

    @Test
    @DisplayName("Deve salvar pedido e retornar ID quando dados são válidos")
    void deveSalvarPedidoERetornarIdQuandoDadosSaoValidos() {
        // Given - preparação do cenário
        var order = new Order("PRODUTO-01", 2);
        when(orderRepository.save(order)).thenReturn(order.withId(1L));

        // When - execução da ação
        var result = sut.create(order);

        // Then - verificação do resultado
        assertEquals(1L, result.getId(),
            "O ID retornado deve ser o mesmo gerado pelo repositório");
        verify(orderRepository, times(1)).save(order);
    }
}
```

---

## Rule 1: JUnit 5 imports only

```java
// ✅ Correct
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

// ❌ Forbidden — JUnit 4
import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;
```

---

## Rule 2: Assertions with messages

Every assertion requires a descriptive message as its **last parameter**:

```java
// ✅ With message
assertEquals(200, response.getStatus(),
    "O status HTTP deve ser 200 para requisição válida");

assertTrue(result.isPresent(),
    "O resultado não deve ser vazio quando o usuário existe");

assertNotNull(order.getId(),
    "O ID deve ser atribuído após salvar no repositório");

assertThrows(IllegalArgumentException.class,
    () -> sut.create(null),
    "Deve lançar exceção quando o pedido for nulo");

// ❌ Without message — do not use
assertEquals(200, response.getStatus());
assertTrue(result.isPresent());
```

Available assertions:

| Assertion | Use |
|---|---|
| `assertEquals(expected, actual, msg)` | Value equality |
| `assertNotEquals(unexpected, actual, msg)` | Value difference |
| `assertTrue(condition, msg)` | True condition |
| `assertFalse(condition, msg)` | False condition |
| `assertNull(value, msg)` | Null value |
| `assertNotNull(value, msg)` | Non-null value |
| `assertThrows(Exception.class, () -> ..., msg)` | Expected exception |
| `assertAll(msg, () -> ..., () -> ...)` | Grouped assertions |

---

## Rule 3: Given-When-Then comments

Every test method must have all three blocks explicitly commented:

```java
@Test
@DisplayName("Deve lançar exceção quando produto não encontrado")
void deveLancarExcecaoQuandoProdutoNaoEncontrado() {
    // Given - o repositório não encontra o produto
    when(productRepository.findById(99L)).thenReturn(Optional.empty());

    // When / Then - a execução já lança a exceção esperada
    assertThrows(ProductNotFoundException.class,
        () -> sut.findById(99L),
        "Deve lançar ProductNotFoundException quando o produto não existe no repositório");
}
```

When `When` and `Then` merge (e.g., `assertThrows`), comment as `// When / Then`.

---

## Rule 4: Portuguese method names

Pattern: `deve<Resultado>Quando<Condição>()`

```java
// ✅ Correct
void deveSalvarPedidoQuandoDadosSaoValidos()
void deveLancarExcecaoQuandoUsuarioNaoEncontrado()
void deveRetornarListaVaziaQuandoNaoHaPedidos()

// ❌ Do not use
void shouldSaveOrder()       // English
void testSave()              // Generic
void test1()                 // Meaningless
```
