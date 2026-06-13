# Template — Arquivo de Regras de Negócio

Use este template ao criar ou atualizar qualquer arquivo em `docs/business/`.

---

## Frontmatter obrigatório

```markdown
---
area: {nome da área — ex: Fila, Projetos, Encontros, Participantes}
ultima_atualizacao: {YYYY-MM-DD}
regras: [RN-001, RN-002, RN-003]
status: completo | parcial | rascunho
---
```

---

## Estrutura do arquivo

```markdown
# Regras de Negócio — {Área}

> Gerado a partir do código em: {lista de arquivos analisados}

## Visão Geral

{Parágrafo curto descrevendo o propósito desta área e suas principais responsabilidades.}

---

## RN-{número}: {Nome curto da regra}

**Descrição:** {O que a regra garante ou impede — uma frase clara.}

**Trigger:** {Quando a regra é avaliada — ex: "Ao registrar presença", "Ao criar projeto".}

**Pré-condições:**
- {condição 1}
- {condição 2}

**Comportamento:**
```
{pseudocódigo ou descrição das ações}
```

**Implementação:**
- Arquivo: `{caminho/relativo/ao/arquivo.cs}` linha {N}
- Método: `{NomeDoMetodo}`

**Exceção lançada:** `{TipoDeExcecao}` — "{mensagem de erro}"

**Testes relacionados:** `{caminho/do/teste.cs}` — `{NomeDoTeste}`

---

{repetir bloco acima para cada regra}

---

## Fluxo Consolidado

{Diagrama ASCII ou lista ordenada mostrando como as regras interagem entre si nesta área.}

---

## Regras relacionadas em outras áreas

| Regra | Área | Relação |
|-------|------|---------|
| RN-{X} | {Área} | {Como se relaciona} |
```

---

## Convenções de numeração

- Regras são numeradas globalmente com 3 dígitos: `RN-001`, `RN-002`, ...
- Consulte todos os arquivos em `docs/business/` antes de atribuir um número novo
- O próximo número disponível é o maior existente + 1
- **Nunca reutilize um número** de uma regra removida

## Convenções de nomes de arquivo

| Área | Arquivo |
|------|---------|
| Sistema de Fila | `docs/business/fila.md` |
| Participantes | `docs/business/participantes.md` |
| Projetos e Autorias | `docs/business/projetos.md` |
| Encontros | `docs/business/encontros.md` |
| Apresentações | `docs/business/apresentacoes.md` |
| Pontuação (detalhado) | `docs/business/pontuacao.md` |
| Códigos Sequenciais | `docs/business/codigos-sequenciais.md` |
| Autenticação e Acesso | `docs/business/auth.md` |
| Validações de Formato | `docs/business/validacoes.md` |

Se uma área nova for identificada, use kebab-case: `docs/business/nome-da-area.md`.
