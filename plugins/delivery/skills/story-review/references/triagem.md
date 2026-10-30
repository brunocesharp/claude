# Triagem dos achados

Adaptada do `bmad-code-review` (BMAD v7). Feita pela sessão principal, depois de juntar o retorno das lentes. Nenhum achado vai para a story sem passar por aqui.

## 1. Verificar

Para cada achado, abra o código no local indicado (e além do diff, se preciso) e confirme a **consequência** alegada. Não deu para confirmar: descarte (passo 3).

## 2. Severidade (pela consequência verificada)

| Severidade | Quando |
|------------|--------|
| `high` | Critério de aceite não atendido, tarefa marcada sem implementação, dado errado ou perdido, falha de segurança, quebra de contrato, teste que não passa |
| `medium` | Caso de borda plausível que falha, erro tratado de forma errada, teste que não verifica o que diz, desvio de ADR ou de camada |
| `low` | Registro incompleto, nome fora do padrão, melhoria pequena sem impacto no usuário |

## 3. Descartar (sempre com o motivo)

Ruído, alegação refutada pela leitura do código, consequência não verificável, duplicata de outra lente, preferência de estilo sem padrão que a sustente. Os descartados ficam listados no bloco de revisão, com o motivo.

## 4. Encaminhar

| Encaminhamento | Quando | O que acontece |
|----------------|--------|----------------|
| **corrigir** | Há uma correção clara | Vira tarefa `R{n}` na story (ou é aplicada já, com confirmação) |
| **adiar** | Problema real que **já existia antes** da story | Vira story nova no `backlog` (com confirmação) ou nota no épico. Problema **causado** pela story nunca é adiado |
| **decisão** | Mais de uma correção razoável, ou exige mudar o que a story promete | Liste as opções, recomende uma e deixe a decisão com o usuário; se mudar o prometido, `correct-course` |

## 5. Resultado da revisão

| Resultado | Condição | Estado da story |
|-----------|----------|-----------------|
| **aprovada** | Nenhum `high`/`medium` em aberto e nenhuma decisão pendente (`low` pode ficar registrado) | `review → done` (com confirmação) |
| **correções** | Há `corrigir` `high`/`medium` | `review → in-progress`, com as tarefas `R{n}` — ou fica em `review` se o usuário pedir para aplicar já |
| **decisão pendente** | Há `decisão` sem resposta | Fica em `review` até decidir |

Terceira rodada de revisão com achados não triviais na mesma story: pare e procure a causa (story mal fatiada, critério ambíguo, padrão faltando) antes de outra rodada; registre para a retrospectiva.
