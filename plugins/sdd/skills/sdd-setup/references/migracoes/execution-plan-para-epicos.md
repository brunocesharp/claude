# Migração opcional: `execution-plan.md` → épicos e stories

- **id:** `execution-plan-para-epicos`
- **Módulo:** `spec-plan` (a partir da 1.1.0)
- **Tipo:** opcional — o `plan-execution` continua funcionando; migre só os planos que vão ser implementados pelo fluxo de stories.

## O que muda

Antes: `docs/{projeto}/plano-execucao/{escopo}/execution-plan.md` com Entregas e tarefas por camada, estimadas em horas.
Depois: `docs/{projeto}/implementacao/epicos/epic-N-slug.md` com stories verticais (P/M/G) e `implementacao/sprint-status.yaml`. O plano antigo **fica** no lugar, com uma linha apontando para os épicos.

## Passos

1. **Encontrar** os planos: `docs/*/plano-execucao/*/execution-plan.md`. Mostre a lista e pergunte quais migrar (pode ser nenhum).
2. **Para cada plano escolhido**, rode a skill `plan-epics` no modo **Migrar** com o projeto e o escopo do plano. Ela converte, valida a cobertura e gera o quadro, com confirmação em cada etapa.
3. **Conferir**: `uv run _sdd/scripts/epics.py --project docs/{projeto} validate` sem `problems` e `status.py ... show` com as stories esperadas.
4. **Registrar**: depois que todos os planos escolhidos estiverem migrados (ou se o usuário decidir não migrar nenhum e não quiser ser lembrado de novo), rode
   `uv run "${CLAUDE_SKILL_DIR}/scripts/migrate.py" --workspace-root "{workspace}" --mark-applied execution-plan-para-epicos`.

Se o `plan-epics` não estiver instalado (`/plugin install spec-plan@claude` na versão 1.1.0 ou mais nova), pare e mostre o comando.
