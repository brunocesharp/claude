# Especificação Funcional: Gestão de Produtos

## Feature 1: Cadastro de produtos

### Regras de Negócio

- **RN-1.1** — O nome do produto é obrigatório e único
- **RN-1.2** — O preço deve ser maior que zero

### Cenários

#### Cenário 1.1: Criar produto válido

Dado que estou na tela de cadastro
Quando informo nome e preço válidos
Então o produto é criado

#### Cenário 1.2: Recusar produto com nome repetido

Dado que existe o produto "Caneta"
Quando cadastro outro produto "Caneta"
Então vejo "Já existe um produto com esse nome"

#### Cenário 1.3: Listar produtos com paginação

Dado que existem 25 produtos
Quando abro a lista
Então vejo os 20 primeiros e a paginação

#### Cenário 1.4: Exportar para PDF (removido)

Removido: a exportação saiu do escopo em 20/10.

## Feature 2: Estoque

- **RN-2.1** — O estoque nunca fica negativo

#### Cenário 2.1: Registrar entrada de estoque

Dado um produto com estoque 5
Quando registro entrada de 3
Então o estoque fica 8
