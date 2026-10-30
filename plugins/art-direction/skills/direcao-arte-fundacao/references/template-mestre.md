# Template Mestre — Skills do Sistema de Direção de Arte

Estrutura padrão que orienta todas as skills do sistema de direção de arte.

**Regra fundamental:**
- PASTAS organizam conhecimento
- ARTEFATOS preservam o estado do conhecimento
- SKILLS operam sobre os artefatos
- TROUBLESHOOTING decide se a operação deve acontecer
- HANDOFF transfere formalmente o resultado para a próxima operação

---

## Seções Obrigatórias de Toda Skill

### 0. Identificação
- Nome: `Direcao-arte_[nome-fase]_[nome-topico]` ou `Direcao-arte_[nome-fase]`
- Campos: nome, fase, tópico, pasta de atuação, tipo (tópico ou geral de fase)

### 1. Troubleshooting (gate de entrada)

Execute antes de qualquer processamento. Determina se a skill deve ser utilizada.

**1.1 Pertinência** — A solicitação pertence ao domínio desta skill?
→ Não pertence: retorne NAO EXECUTAR + identifique o domínio responsável.

**1.2 Existência** — O artefato solicitado já existe?
→ Se existir: avalie seu estado antes de gerar nova versão.

**1.3 Validade** — O artefato existente está aprovado, atualizado e sem conflitos?
→ Se inválido: ofereça revisão ao invés de sobrescrever.

**1.4 Pré-requisitos** — As entradas obrigatórias estão disponíveis?
→ Ausência de pré-requisito indispensável: BLOQUEADA.

**1.5 Redundância** — Outra skill já produziu ou é responsável pelo mesmo resultado?
→ Evitar duplicação salvo revisão, auditoria ou consolidação explícita.

**Estados do gate:**
- `EXECUTAR` — skill adequada, necessária e com condições suficientes
- `NAO EXECUTAR` — skill desnecessária, inadequada ou redundante
- `BLOQUEADA` — skill adequada e necessária, mas sem entradas suficientes

### 2. Identidade
Especialidade, função no sistema, domínio de conhecimento, relação com a fase, responsabilidade principal e limites.
Declare explicitamente o que **não** é responsabilidade desta skill.

### 3. Objetivo
Formato: "transformar [entradas] em [resultado], produzindo [artefatos] que possam ser utilizados por [destino]."

### 4. Escopo
Atividades dentro e fora do escopo. Limites de autoridade:
- Decisões autônomas
- Propostas que exigem aprovação
- Decisões herdadas (não modificáveis)

### 5. Entradas
- **Obrigatórias** — ausência pode bloquear a execução
- **Condicionais** — exigidas apenas em determinados cenários
- **Opcionais** — melhoram o resultado, mas não bloqueiam

### 6. Leitura de Artefatos
Reconstrói contexto a partir de artefatos persistentes.

**Ordem de autoridade:**
```
decisão aprovada > especificação vigente > artefato de trabalho > referência > hipótese
```

### 7. Procedimento
1. Diagnóstico
2. Análise
3. Desenvolvimento
4. Decisão
5. Formalização
6. Verificação
7. Registro

### 8. Regras de Decisão
Critérios objetivos, prioridades, tratamento de decisões herdadas, conflitos e incertezas.

**Prioridade genérica:**
```
função > legibilidade > consistência > tema > estética ornamental
```

Hipóteses não devem ser convertidas em decisões aprovadas.

### 9. Outputs
Artefato principal e auxiliares. Para cada output: nome, tipo, destino, status inicial, consumidores.

### 10. Critérios de Conclusão
- `CONCLUÍDA` — todos os critérios obrigatórios atendidos
- `CONCLUÍDA COM PENDÊNCIAS` — resultado utilizável com questões registradas
- `NÃO CONCLUÍDA` — execução iniciada sem resultado utilizável

### 11. Handoff
Transferência formal para outras skills/fases: artefatos, localização, status, decisões consolidadas, pendências, dependências, consumidores, restrições de uso.

---

## Fluxo Padrão

```
CHAMADA DA SKILL
      |
      v
TROUBLESHOOTING
   |      |      |
   |      |      +--> BLOQUEADA → informa dependências
   |      +---------> NÃO EXECUTAR → encerra
   +----------------> EXECUTAR
                         |
                    IDENTIDADE
                         |
                     OBJETIVO
                         |
                      ESCOPO
                         |
                     ENTRADAS
                         |
              LEITURA DE ARTEFATOS
                         |
                   PROCEDIMENTO
                         |
               REGRAS DE DECISÃO
                         |
                      OUTPUTS
                         |
            CRITÉRIOS DE CONCLUSÃO
                         |
                      HANDOFF
                         |
                         v
               PRÓXIMA SKILL / FASE
```

---

## Convenção de Nomenclatura

```
Skill de tópico:   Direcao-arte_[nome-fase]_[nome-topico]
                   Ex: Direcao-arte_Sistema-visual_Iconografia

Skill geral:       Direcao-arte_[nome-fase]
                   Ex: Direcao-arte_Fundacao
```

A numeração das pastas (F01, T01 etc.) não precisa fazer parte do nome da skill.

---

## Princípios Globais

- **Persistência:** decisões relevantes devem ser registradas em artefatos
- **Não redundância:** verificar existência de resultado válido antes de produzir algo novo
- **Propriedade:** cada artefato possui um tópico responsável por sua versão autoritativa
- **Rastreabilidade:** deve ser possível identificar entradas e decisões que originaram um artefato
- **Modularidade:** cada skill atua dentro de seu domínio
- **Preservação:** artefatos aprovados não são sobrescritos silenciosamente
- **Handoff explícito:** resultados destinados a processos posteriores informam status, localização, dependências e restrições
- **Validação:** produzir um arquivo não é suficiente; o resultado deve atender aos critérios de conclusão
