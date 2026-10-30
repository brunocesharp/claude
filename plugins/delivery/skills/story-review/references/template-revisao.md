# Bloco de revisão (seção `## Revisão` da story)

Acrescente um bloco por rodada, sem apagar os anteriores:

```markdown
### {AAAA-MM-DD} — revisão {completa | rápida} — rodada {n}

**Resultado:** {aprovada | correções | decisão pendente}
**Revisado:** {repo} `feat/{id}` contra `{base}` ({N} arquivos); suíte: {repo}: {passou | falhou (N)}

| # | Sev. | Lente | Onde | Achado | Encaminhamento |
|---|------|-------|------|--------|----------------|
| A1 | high | Aderência | api: `src/.../ListarProdutosQuery.cs:42` | Página fixa em 10, CA-1 pede 20. Consequência: lista mostra metade | corrigir → R1 |
| A2 | medium | Correção | web: `produtos-list.component.ts:31` | Última página vazia quando o total é múltiplo de 20. Consequência: botão "próxima" leva a uma tela vazia | corrigir → R2 |
| A3 | low | Registro | api | `src/Extra.cs` alterado e não declarado | corrigir → R3 |
| A4 | medium | Testes | api | Falha pré-existente em `ClientesTests` (já falhava na main) | adiar → story 1-5-... |
| A5 | — | Arquitetura | api | Paginação por offset x cursor (ADR-003 cita cursor só para > 10 mil itens) | decisão: {opções; recomendação} |

**Descartados:**
- {achado}: {motivo}

**Verificado sem achados:**
- Segurança: endpoint exige perfil Gestor; entrada validada pelo validator; sem dado sensível em log.

**Aplicado nesta rodada:** {R1 aplicado e testado | nada}
```

Tarefas de correção vão para a seção **Tarefas**, numa subseção no fim:

```markdown
### Correções da revisão {n} ({AAAA-MM-DD})

- [ ] **R1** — {correção} (CA-1)
- [ ] **R2** — {correção} (CA-1)
```

Cite o CA quando a correção for de um critério; correção que não é de critério (registro, padrão) fica sem CA.
