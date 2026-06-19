# Layer Patterns

## Contents
- @Service — business logic
- Domain classes — entities and value objects
- @Repository — data access
- @RestController — HTTP layer

---

## @Service — business logic

Mock all repositories and external services. Verify orchestration.

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderService")
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private OrderService sut;

    @Test
    @DisplayName("Deve criar pedido e notificar cliente quando dados são válidos")
    void deveCriarPedidoENotificarClienteQuandoDadosSaoValidos() {
        // Given - dados válidos e repositório configurado
        var order = new Order("PROD-01", 2);
        when(orderRepository.save(order)).thenReturn(order.withId(1L));

        // When - criação do pedido
        var result = sut.create(order);

        // Then - pedido salvo e notificação enviada
        assertNotNull(result.getId(),
            "O pedido deve ter um ID após ser salvo");
        verify(orderRepository, times(1)).save(order);
        verify(notificationService, times(1)).notifyCustomer(any());
    }

    @Test
    @DisplayName("Deve lançar exceção quando pedido for nulo")
    void deveLancarExcecaoQuandoPedidoForNulo() {
        // Given - pedido nulo

        // When / Then - exceção esperada na criação
        assertThrows(IllegalArgumentException.class,
            () -> sut.create(null),
            "Deve lançar IllegalArgumentException quando o pedido for nulo");
    }
}
```

---

## Domain classes — entities and value objects

No mocks needed. Test pure business rules, invariants, and calculations.
Do not use `@ExtendWith` unless needed.

```java
@DisplayName("Order")
class OrderTest {

    @Test
    @DisplayName("Deve calcular total corretamente para quantidade e preço informados")
    void deveCalcularTotalCorretamenteParaQuantidadeEPrecoInformados() {
        // Given - pedido com 3 itens a R$10
        var order = new Order("PROD-01", 3, BigDecimal.valueOf(10.0));

        // When - cálculo do total
        var total = order.getTotal();

        // Then - total é quantidade x preço unitário
        assertEquals(BigDecimal.valueOf(30.0), total,
            "O total deve ser quantidade x preço unitário");
    }

    @Test
    @DisplayName("Deve rejeitar quantidade negativa na criação")
    void deveRejeitarQuantidadeNegativaNaCriacao() {
        // Given - quantidade inválida

        // When / Then - exceção ao criar com valor negativo
        assertThrows(IllegalArgumentException.class,
            () -> new Order("PROD-01", -1, BigDecimal.valueOf(10.0)),
            "Deve rejeitar quantidade negativa ao criar pedido");
    }
}
```

---

## @Repository — data access

Mock `EntityManager`, `JdbcTemplate`, or similar infrastructure.
Use only for custom mapping logic. Standard Spring Data queries require `@DataJpaTest` (integration test — out of scope for this skill).

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderRepositoryImpl")
class OrderRepositoryImplTest {

    @Mock
    private EntityManager entityManager;

    @InjectMocks
    private OrderRepositoryImpl sut;

    @Test
    @DisplayName("Deve retornar Optional vazio quando pedido não encontrado")
    void deveRetornarOptionalVazioQuandoPedidoNaoEncontrado() {
        // Given - EntityManager não retorna resultado
        when(entityManager.find(Order.class, 99L)).thenReturn(null);

        // When - busca por ID inexistente
        var result = sut.findById(99L);

        // Then - resultado vazio
        assertFalse(result.isPresent(),
            "Deve retornar Optional vazio quando o pedido não existe");
    }
}
```

---

## @RestController — HTTP layer

Mock the `@Service` dependency. For `MockMvc` slice tests (`@WebMvcTest`), inform the user that this requires an integration test setup — out of scope here.

```java
@ExtendWith(MockitoExtension.class)
@DisplayName("OrderController")
class OrderControllerTest {

    @Mock
    private OrderService orderService;

    @InjectMocks
    private OrderController sut;

    @Test
    @DisplayName("Deve retornar pedido criado quando requisição for válida")
    void deveRetornarPedidoCriadoQuandoRequisicaoForValida() {
        // Given - serviço retorna pedido com ID
        var order = new Order("PROD-01", 2);
        when(orderService.create(any())).thenReturn(order.withId(1L));

        // When - chamada ao controller
        var result = sut.create(order);

        // Then - retorno com ID gerado
        assertNotNull(result.getId(),
            "O pedido retornado deve conter o ID gerado pelo serviço");
    }
}
```
