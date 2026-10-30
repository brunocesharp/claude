# Fatiamento vertical: épicos e stories

## Épico

Um épico é **um resultado coerente para o usuário** que precisa de várias sessões de implementação. Teste: dá para explicar o épico a um usuário sem citar camada, tabela ou tecnologia?

| Bom | Ruim (por quê) |
|-----|----------------|
| Cadastro de produtos | Backend de produtos (camada) |
| Controle de estoque | Banco de dados do estoque (camada) |
| Login com conta corporativa | Configurar autenticação (tarefa técnica, a menos que seja o épico habilitador) |

Tamanho: de 2 a ~8 stories. Mais que isso, divida pelo resultado (ex.: "Cadastro" e "Busca e filtros"). Um épico com uma story só é uma story.

## Story

Uma story é uma **fatia vertical**: atravessa as camadas necessárias (domínio → persistência → API → tela) para entregar **um comportamento testável** de ponta a ponta, e **cabe numa sessão** de implementação.

| Bom | Ruim (por quê) |
|-----|----------------|
| Criar produto com validação de nome único (cenários 1.1, 1.2) | Criar entidade Produto (horizontal: só uma camada, nada testável pelo usuário) |
| Listar produtos com paginação (1.3) | Criar todas as telas de produto (grande demais, vários comportamentos) |
| Registrar entrada de estoque (2.1) | Endpoints de estoque + tela de estoque + relatórios (vários resultados) |
| Spike: medir concorrência no estoque | Pesquisar tecnologias (sem pergunta, sem fim) |

### Como fatiar (em ordem de preferência)

1. **Por cenário ou grupo de cenários** da especificação: o happy path primeiro, depois as variações.
2. **Por regra de negócio**: o caso simples numa story, as regras de exceção em outra.
3. **Por operação**: criar, consultar, alterar, remover.
4. **Por variação de dado ou de interface**: um tipo de produto primeiro; importar por planilha depois.
5. **Esqueleto andante**: em sistema novo, a primeira story atravessa todas as camadas com o mínimo (vira o checkpoint que define os padrões).

### Tamanho relativo

| Tamanho | Referência |
|---------|------------|
| **P** | Um comportamento simples, poucos arquivos, normalmente um repositório |
| **M** | Uma fatia vertical completa (API + tela) de um comportamento com algumas regras |
| **G** | No limite de uma sessão: várias regras ou dois repositórios. Pergunte se dá para dividir |

Maior que G **não** é story: divida. Sinais: mais de ~4 cenários, mais de um ator, "e" no título, depende de decisão ainda em aberto.

### Tipos

| `kind` | Quando | `covers` |
|--------|--------|----------|
| `story` | Comportamento para o usuário | Obrigatório |
| `spike` | Pergunta técnica ou de negócio que bloqueia o fatiamento ou a estimativa (resultado: uma decisão, um protótipo descartável, um ADR) | Opcional |
| `enabler` | Habilitador técnico sem comportamento visível (pipeline, autenticação base, migração de dados), só quando não cabe dentro da primeira story que precisa dele | Opcional |

### Ordem de build

- Dependências antes de quem depende (`depends_on` só aponta para trás).
- **Vários repositórios:** provedor antes do consumidor dentro da mesma story (API antes da tela) e, entre stories, contrato novo antes de quem o consome. Mudança incompatível de contrato vira story própria com a estratégia (expandir e depois contrair, versão nova, feature flag) ou ponto em aberto para `arch-adr`. Prefira stories de um repositório só quando o fatiamento vertical permitir.
- Risco primeiro: o que pode mudar o plano (integração externa, regra incerta) vem cedo, com `checkpoint`.
- Valor cedo: o primeiro épico entrega algo que o usuário consegue usar.

### Checkpoint

Marque `checkpoint: true` na story que pede atenção humana antes de seguir: a primeira de um padrão (as próximas vão copiar), a que toca integração externa, segurança ou dados existentes, e a que resolve um spike. A implementação para no fim dela para alguém revisar com calma, antes de automatizar as seguintes.
