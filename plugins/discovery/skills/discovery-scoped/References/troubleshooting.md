# Troubleshooting — Scope Generate

Problemas comuns durante a geração de escopo e como resolvê-los.

---

## Problema: Discovery incompleto ou inexistente

### Sintoma
- Faltam arquivos em `docs/{projeto}/discovery/`
- Arquivos existem mas estão superficiais
- Usuário quer gerar escopo "do zero"

### Causa
- Pressa para começar desenvolvimento
- Discovery feito informalmente
- Projeto herdado sem documentação

### Solução

1. **Avalie a gravidade:**
   
   | Arquivos disponíveis | Recomendação |
   |----------------------|--------------|
   | Nenhum | Conduzir discovery mínimo primeiro |
   | 1-2 arquivos | Gerar com aviso + complementar |
   | 3-4 arquivos | Gerar normalmente |
   | Todos | Ideal |

2. **Se nenhum arquivo:**
   > "Nenhum documento de discovery encontrado. Posso gerar o escopo com base nas informações que você fornecer agora, mas recomendo fazer pelo menos `discovery-vision` e `discovery-opportunity` antes. Quer que eu conduza um discovery rápido?"

3. **Se parcialmente:**
   > "Encontrei apenas vision.md e opportunity.md. O escopo pode ficar incompleto em relação a hipóteses e métricas. Quer prosseguir assim ou complementar o discovery primeiro?"

4. **Discovery mínimo express:**
   Se o usuário insistir em prosseguir, colete:
   - Qual o problema? (vision)
   - Quem é afetado? (stakeholders)
   - Como saber se deu certo? (metrics)
   
   Registre no próprio escopo como "informações coletadas durante geração do escopo".

---

## Problema: Sobreposição com escopo existente

### Sintoma
- Funcionalidades do novo escopo já estão em outro
- Usuário quer "refazer" algo já aprovado
- Áreas de responsabilidade confusas

### Causa
- Falta de visibilidade dos escopos existentes
- Mudança de requisitos
- Diferentes stakeholders solicitando coisas similares

### Solução

1. **Identifique o tipo de sobreposição:**

   | Situação do escopo existente | Ação |
   |------------------------------|------|
   | Rascunho | Sugerir consolidar |
   | Em revisão | Sugerir consolidar ou esperar |
   | Aprovado | Bloquear + sugerir extensão |
   | Em execução | Bloquear + aguardar |
   | Concluído | Permitir evolução |

2. **Se o escopo existente está em Rascunho/Revisão:**
   > "O escopo '{outro}' já cobre '{área}' e está em {situação}. Sugestões:
   > 1. Consolidar os dois em um único escopo
   > 2. Delimitar claramente a fronteira entre eles
   > 3. Aguardar aprovação do primeiro para então criar o segundo
   > 
   > Qual prefere?"

3. **Se o escopo existente está Aprovado/Em execução:**
   > "A funcionalidade '{funcionalidade}' já está no escopo '{outro}' que está {situação}. Não posso duplicar.
   > 
   > Opções:
   > 1. Remover essa funcionalidade do novo escopo
   > 2. Criar uma extensão/evolução do escopo existente
   > 3. Aguardar conclusão do escopo existente"

4. **Delimitar fronteiras:**
   Se decidirem manter separados, documente explicitamente:
   ```markdown
   ### Fronteiras com Outros Escopos
   
   | Escopo | O que ele cobre | O que este escopo cobre |
   |--------|-----------------|------------------------|
   | {outro} | {descrição} | {descrição} |
   ```

---

## Problema: Escopo muito grande

### Sintoma
- Lista enorme de funcionalidades
- Prazo não-realista
- Muitos "Must have"
- Stakeholders com expectativas diferentes

### Causa
- Tentativa de resolver tudo de uma vez
- Falta de priorização
- Múltiplos stakeholders empurrando demandas

### Solução

1. **Identifique o tamanho:**
   
   | Indicador | Escopo normal | Escopo grande demais |
   |-----------|---------------|---------------------|
   | Funcionalidades Must | 5-15 | 20+ |
   | Estimativa | 1-3 meses | 6+ meses |
   | Stakeholders aprovadores | 2-4 | 8+ |

2. **Sugira divisão:**
   > "Este escopo tem {N} funcionalidades Must, o que geralmente indica que deveria ser dividido.
   > 
   > Sugestões de divisão:
   > 1. **Por fase:** MVP (Must) → Fase 2 (Should) → Fase 3 (Could)
   > 2. **Por módulo:** {módulo A} → {módulo B} → {módulo C}
   > 3. **Por usuário:** Fluxo do {perfil A} → Fluxo do {perfil B}"

3. **Aplique MoSCoW rigoroso:**
   Para cada funcionalidade "Must", pergunte:
   > "Se essa funcionalidade não existir no lançamento, o projeto falha completamente ou só fica pior?"
   
   Se "só fica pior" → downgrade para Should.

4. **Crie escopo de MVP:**
   > "Vamos criar primeiro o escopo do MVP com apenas as funcionalidades que tornam o sistema viável. As demais entram em escopos de evolução."

---

## Problema: Escopo muito vago

### Sintoma
- "Inclui" com itens genéricos ("melhorar a experiência")
- Funcionalidades sem critérios de aceite
- Métricas como "aumentar satisfação"
- Ninguém consegue explicar o que será feito

### Causa
- Discovery superficial
- Pressão para "ter um documento"
- Falta de expertise técnica

### Solução

1. **Identifique vaguidão:**

   | Exemplo vago | Versão específica |
   |--------------|-------------------|
   | "Melhorar o cadastro" | "Reduzir campos de cadastro de 15 para 5" |
   | "Aumentar performance" | "Tempo de carregamento < 2s" |
   | "Integrar com ERP" | "Ler pedidos do SAP via API REST" |
   | "Dashboard de dados" | "Gráfico de vendas por região com filtro de período" |

2. **Questione cada item:**
   > "Quando você diz '{item vago}', o que exatamente você quer dizer? O que eu veria na tela?"

3. **Exija critérios verificáveis:**
   > "Como vamos saber se '{funcionalidade}' está pronta? Qual é o critério de aceite que permite dizer 'sim, está funcionando'?"

4. **Conecte a oportunidades:**
   > "Essa funcionalidade resolve qual dor específica do discovery? Se não conecta a nenhuma oportunidade, por que está no escopo?"

---

## Problema: Stakeholders não alinhados sobre abrangência

### Sintoma
- Diferentes pessoas têm diferentes expectativas
- "Eu achei que incluía X"
- Conflitos sobre o que é "in scope"

### Causa
- Comunicação insuficiente
- Discovery feito com grupo parcial
- Mudanças não documentadas

### Solução

1. **Documente as divergências:**
   > "Percebo que há visões diferentes sobre o escopo:
   > - {Stakeholder A} espera que inclua {X}
   > - {Stakeholder B} entende que {X} está fora
   > 
   > Vamos resolver isso antes de prosseguir."

2. **Use a seção "Não inclui" explicitamente:**
   Cada item "fora" deve ter justificativa:
   ```markdown
   ### Não Inclui (Out of Scope)
   
   - Integração com sistema X — será feito em escopo separado após validação do MVP
   - Relatórios gerenciais — dependem de definição de métricas pela diretoria
   ```

3. **Proponha reunião de alinhamento:**
   > "Sugiro uma reunião de 30 minutos com {stakeholders} para alinhar a abrangência antes de finalizar o escopo."

4. **Registre decisões:**
   ```markdown
   ### Decisões de Abrangência
   
   | Item | Decisão | Quem decidiu | Data |
   |------|---------|--------------|------|
   | {X} | Fora deste escopo | {nome} | {data} |
   ```

---

## Problema: Funcionalidades sem oportunidade correspondente

### Sintoma
- Funcionalidades que "apareceram" no escopo
- Não conectam com discovery
- Stakeholder pediu mas não justificou

### Causa
- Demandas de stakeholders não passaram pelo discovery
- "Gold plating" — adicionar mais do que o necessário
- Confusão sobre o que o sistema deve fazer

### Solução

1. **Questione a necessidade:**
   > "A funcionalidade '{F}' não aparece no discovery. Qual oportunidade ou dor ela resolve?"

2. **Avalie se é mesmo necessária:**

   | Resposta | Ação |
   |----------|------|
   | "É óbvio que precisa" | Pergunte qual evidência suporta isso |
   | "O stakeholder X pediu" | Volte ao stakeholder e pergunte o porquê |
   | "Todo sistema tem isso" | Não é justificativa — remova ou justifique |
   | Conecta a oportunidade real | Documente a conexão |

3. **Adicione ao discovery retroativamente:**
   Se for legítima mas faltou no discovery:
   > "Vou adicionar essa oportunidade ao opportunity.md para manter a rastreabilidade."

4. **Marque como "Could" se não justificada:**
   Se não houver justificativa forte, não deveria ser Must/Should.

---

## Problema: Métricas impossíveis de medir

### Sintoma
- "Aumentar satisfação" sem forma de medir
- "Melhorar eficiência" sem baseline
- Sistema legado não tem dados

### Causa
- Métricas definidas sem considerar viabilidade
- Falta de instrumentação
- Discovery não explorou como medir

### Solução

1. **Identifique o bloqueio:**

   | Bloqueio | Solução |
   |----------|---------|
   | Não tem baseline | Definir coleta como primeira ação |
   | Sistema não tem dados | Planejar instrumentação |
   | Métrica não mensurável | Substituir por proxy |

2. **Proponha instrumentação:**
   > "Para medir '{métrica}', vamos precisar de:
   > - {ferramenta/código/processo}
   > 
   > Isso deveria estar no escopo ou é pré-requisito?"

3. **Sugira proxies:**
   > "Se não podemos medir '{ideal}' diretamente, podemos usar '{proxy}' como aproximação?"

4. **Registre como risco:**
   ```markdown
   | Risco | Não conseguiremos medir a métrica X |
   | Probabilidade | Média |
   | Impacto | Alto — não saberemos se deu certo |
   | Mitigação | Implementar tracking na primeira sprint |
   ```

---

## Problema: Estimativa muito incerta

### Sintoma
- "Não sei quanto tempo leva"
- Estimativa varia de 2 semanas a 6 meses
- Dependências não resolvidas

### Causa
- Escopo ainda vago
- Tecnologia desconhecida
- Dependências externas

### Solução

1. **Aceite incerteza inicial:**
   > "Estimativa de alto nível com confiança {baixa/média}. Será refinada na especificação."

2. **Use ranges:**
   ```markdown
   | Fase | Melhor caso | Provável | Pior caso |
   |------|-------------|----------|-----------|
   | Dev | 4 semanas | 6 semanas | 10 semanas |
   ```

3. **Identifique o que gera incerteza:**
   ```markdown
   ### Fatores de Incerteza na Estimativa
   
   - Integração com sistema X: nunca fizemos, pode ter surpresas
   - Definição de regras de negócio: stakeholder ainda não confirmou
   ```

4. **Proponha spike técnico:**
   > "Para reduzir incerteza, sugiro um spike de {N} dias antes de comprometer prazo."
