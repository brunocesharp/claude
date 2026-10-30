# Checklist de prontidão (antes de fatiar)

Adaptado do `check-implementation-readiness` do BMAD v6. Responda cada item com **ok**, **lacuna** ou **não se aplica**, mostre ao usuário e pergunte se segue. Lacuna não bloqueia: vira ponto em aberto (resolver agora, spike ou decidir na story).

## Especificação (`especificacao/{escopo}/spec-functional.md`)

- [ ] Existe e foi lida por inteiro.
- [ ] Toda feature tem pelo menos um cenário `#### Cenário N.M` (sem cenário não há o que cobrir).
- [ ] Os cenários têm resultado verificável (o "Então" diz o que se observa).
- [ ] Os pontos em aberto da spec estão listados (viram pontos em aberto do épico).

## Escopo (`escopo/{escopo}/escopo.md`)

- [ ] O que está **fora** do escopo está claro (vira "Não entra" dos épicos).
- [ ] Restrições (prazo, tecnologia, regulação) conhecidas.

## Arquitetura (`arquitetura/arquitetura.md` e `arquitetura/decisoes/`)

- [ ] Os contêineres que o escopo toca existem no C4 (API, SPA, banco, worker...).
- [ ] Sistema externo ou contêiner novo exigido pela spec → lacuna: sugerir `arch-c4` (ou spike).
- [ ] ADRs aceitos que afetam o escopo foram lidos (as stories os respeitam).
- [ ] Sem arquitetura documentada: avisar que o plano supõe a arquitetura e sugerir `arch-c4`.

## Código e repositórios

- [ ] Sabe-se onde o código fica: `project-config.json` (um repositório) ou `repositorios.md` (vários).
- [ ] Vários repositórios: cada contêiner tocado tem um repositório responsável.
- [ ] Contratos entre repositórios que vão mudar foram identificados.

## Planejamento existente

- [ ] Épicos já existentes em `implementacao/epicos/` (de outro escopo ou desta mesma rodada): o próximo número vem de `epics.py validate`.
- [ ] Existe `plano-execucao/{escopo}/execution-plan.md`: perguntar se ele deve ser a base (modo Migrar) ou só referência.
