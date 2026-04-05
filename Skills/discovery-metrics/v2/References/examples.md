# Exemplos de Uso — Discovery Metrics

Cenários detalhados de como usar a skill em diferentes situações.

---

## Exemplo 1: Produto B2C com foco em engajamento

### Contexto
App de meditação guiada. Modelo freemium com assinatura mensal.

### Conversa

**Usuário:** "Preciso definir métricas de sucesso para o nosso app de meditação"

**Claude:** "Ótimo! Vi no `vision.md` que o objetivo é ajudar pessoas a criar o hábito de meditar. Vamos definir como medir isso. Se o projeto der certo, qual é a principal mudança que queremos ver?"

**Usuário:** "Queremos que as pessoas meditem regularmente"

**Claude:** "'Regularmente' é vago. O que significa para vocês? Todo dia? 3x por semana?"

**Usuário:** "Pelo menos 3x por semana seria ótimo"

**Claude:** "Então uma possível North Star seria: 'Usuários que meditam 3+ vezes por semana'. Isso captura o hábito que vocês querem criar. Faz sentido?"

**Usuário:** "Sim, perfeito"

**Claude:** "Qual é o baseline? Quantos usuários fazem isso hoje?"

**Usuário:** "Hoje só 15% dos usuários ativos meditam 3x ou mais"

**Claude:** "Ótimo baseline. Qual seria uma meta realista para 6 meses?"

**Usuário:** "Dobrar para 30%?"

**Claude:** "Ambicioso mas factível. Agora métricas de negócio: como isso se conecta com receita?"

**Usuário:** "Quanto mais meditam, mais convertem para premium"

**Claude:** "Então métricas de negócio seriam: taxa de conversão free→premium e MRR. Qual o baseline de conversão hoje?"

**Usuário:** "2% convertem para premium"

**Claude:** "E vocês esperam que aumentar meditação aumente conversão? Essa é uma hipótese do `assumptions.md` que podemos validar. Meta de conversão?"

**Usuário:** "Chegar em 5% em 6 meses"

**Claude:** "Perfeito. Agora métricas de usuário usando HEART: para Happiness, como medir satisfação?"

**Usuário:** "NPS após 30 dias de uso"

**Claude:** "Retention é crítico para hábito. Quais cohorts acompanhar?"

**Usuário:** "D7 e D30 são os mais importantes"

**Claude:** "Task Success: qual é a tarefa principal que o usuário precisa completar?"

**Usuário:** "Completar uma sessão de meditação"

**Claude:** "Taxa de conclusão de sessão então. Quantos começam vs. quantos terminam?"

### Resultado

Documento com:
- **North Star:** Usuários que meditam 3+ vezes por semana (15% → 30%)
- **Negócio:** Conversão free→premium (2% → 5%), MRR
- **HEART:** NPS (Happiness), D7/D30 retention, Session completion rate
- **Conexão:** Hipótese de que engajamento leva a conversão

---

## Exemplo 2: Sistema interno B2B com foco em eficiência

### Contexto
Sistema de aprovação de despesas para empresa de 500 funcionários. Substituindo processo manual.

### Conversa

**Usuário:** "Precisamos definir métricas para o sistema de aprovação de despesas"

**Claude:** "Sistemas internos geralmente focam em eficiência. Qual é o problema atual que vocês estão resolvendo?"

**Usuário:** "O processo atual demora 5 dias em média e tem muitos erros"

**Claude:** "Perfeito, já temos baseline! Tempo de aprovação = 5 dias. E erros?"

**Usuário:** "Cerca de 20% das despesas precisam de correção manual"

**Claude:** "Então a North Star poderia ser 'Tempo médio de aprovação' ou 'Taxa de aprovação sem intervenção'. Qual captura melhor o valor?"

**Usuário:** "Tempo é mais visível para a diretoria"

**Claude:** "Ok, North Star = Tempo médio de aprovação. Baseline 5 dias, meta?"

**Usuário:** "1 dia seria ideal"

**Claude:** "80% de redução é agressivo. Vamos escalonar: meta 3 meses = 3 dias, meta 6 meses = 1 dia. Faz sentido?"

**Usuário:** "Sim"

**Claude:** "Métricas de negócio: além do tempo, o que mais a empresa ganha?"

**Usuário:** "Economia de horas do time financeiro"

**Claude:** "Quantas horas gastam hoje?"

**Usuário:** "Uma pessoa dedica 20h por semana só para isso"

**Claude:** "Então podemos medir 'Horas de trabalho manual por semana'. Baseline 20h, meta?"

**Usuário:** "Reduzir para 5h"

**Claude:** "E a taxa de erro de 20%?"

**Usuário:** "Queremos reduzir para menos de 5%"

**Claude:** "Agora métricas de usuário: os funcionários vão usar bem? Como medir adoção?"

**Usuário:** "Queremos que todos usem o novo sistema em 30 dias"

**Claude:** "Métrica: '% funcionários usando novo sistema' com meta 100% em 30 dias. Task Success: taxa de envio de despesa sem erro?"

**Usuário:** "Sim, queremos que 95% dos envios estejam corretos de primeira"

### Resultado

Documento com:
- **North Star:** Tempo médio de aprovação (5 dias → 1 dia)
- **Negócio:** Horas manuais por semana (20h → 5h), Taxa de erro (20% → 5%)
- **Usuário:** Adoção (100% em 30 dias), Envio correto de primeira (95%)
- **Critérios de lançamento:** Sistema funcional, treinamento completo, 50 funcionários piloto

---

## Exemplo 3: Projeto de redução de custos

### Contexto
Automação de atendimento com chatbot para reduzir volume no call center.

### Conversa

**Usuário:** "Precisamos definir métricas para o projeto de chatbot"

**Claude:** "Projetos de redução de custo têm métricas claras de ROI. Qual é o custo atual do call center?"

**Usuário:** "Gastamos R$500k por mês com a operação"

**Claude:** "E qual % do volume o chatbot deveria absorver?"

**Usuário:** "Esperamos que resolva 40% dos atendimentos"

**Claude:** "Se 40% for resolvido pelo chatbot, a economia seria de ~R$200k/mês. Essa é a North Star de negócio: 'Economia mensal com automação'. Mas precisamos de uma métrica de produto também."

**Usuário:** "Que tal taxa de resolução do chatbot?"

**Claude:** "Perfeito. 'Taxa de resolução sem humano' = % de conversas que o chatbot resolve sozinho. Meta 40%. Mas e a satisfação? Se resolver mal, os clientes vão reclamar."

**Usuário:** "Boa observação"

**Claude:** "Sugiro acompanhar CSAT do chatbot vs. CSAT do humano. A meta deveria ser: resolução de 40% com CSAT pelo menos igual ao atendimento humano."

**Usuário:** "Qual é o CSAT humano hoje?"

**Claude:** "Você sabe? Se não, precisamos medir antes de lançar o chatbot."

**Usuário:** "Acho que está em torno de 4.2 de 5"

**Claude:** "'Acho' não é baseline. Vamos confirmar isso como ação. Agora, métricas de risco: o que pode dar errado?"

**Usuário:** "O chatbot pode frustrar clientes e aumentar reclamações"

**Claude:** "Então precisamos de anti-métricas: 'Escalações para humano após frustração' e 'Reclamações sobre o chatbot'. Se subirem, paramos."

**Usuário:** "Boa ideia"

**Claude:** "Critérios de lançamento: o que precisa funcionar no dia 1?"

**Usuário:** "Resolver pelo menos os 10 tipos de dúvida mais comuns"

**Claude:** "Cobertura de 10 intents principais com taxa de acerto > 90%. E rollback?"

**Usuário:** "Se o CSAT cair mais de 0.3 pontos, voltamos para humano"

### Resultado

Documento com:
- **North Star:** Taxa de resolução sem humano (0% → 40%)
- **Negócio:** Economia mensal (R$0 → R$200k), Custo por atendimento
- **Usuário:** CSAT do chatbot (meta: ≥ 4.2), Tempo de resolução
- **Anti-métricas:** Escalações frustradas, Reclamações sobre chatbot
- **Critérios de rollback:** CSAT cair > 0.3 pontos

---

## Exemplo 4: MVP precisando validar hipóteses

### Contexto
Startup testando conceito de delivery de refeições saudáveis para escritórios.

### Conversa

**Usuário:** "Estamos lançando um MVP e precisamos saber o que medir"

**Claude:** "MVP é sobre aprendizado. Quais são as hipóteses críticas do `assumptions.md`?"

**Usuário:** "Que empresas pagariam por delivery de almoço saudável para funcionários"

**Claude:** "Essa é a hipótese de demanda. Como validar? Qual seria a evidência de que empresas PAGARIAM?"

**Usuário:** "Se fechássemos alguns contratos"

**Claude:** "Quantos contratos seriam suficientes para validar?"

**Usuário:** "Se conseguíssemos 5 empresas no piloto, já seria validação"

**Claude:** "Primeira métrica: 'Empresas contratantes'. Meta: 5 no primeiro mês. E os funcionários dessas empresas, vão usar?"

**Usuário:** "Essa é outra hipótese"

**Claude:** "Métrica: 'Taxa de adesão por empresa'. Se a empresa contrata, qual % dos funcionários deveria usar?"

**Usuário:** "Pelo menos 30% para valer a pena"

**Claude:** "E eles vão continuar usando ou é só curiosidade inicial?"

**Usuário:** "Precisamos de recompra"

**Claude:** "Métrica: 'Taxa de pedido recorrente'. Funcionário que pediu semana 1, pediu semana 2? Meta?"

**Usuário:** "50% de recompra semanal seria ótimo"

**Claude:** "Agora a unidade econômica: quanto custa entregar vs. quanto cobram?"

**Usuário:** "Ainda não sabemos exatamente"

**Claude:** "Isso é crítico. Vocês podem estar validando demanda de algo que dá prejuízo. Métrica: 'Margem por pedido'. Mesmo que negativa no MVP, precisam saber."

**Usuário:** "Verdade, não tinha pensado nisso"

**Claude:** "E satisfação? Se não gostarem da comida, não adianta ter demanda."

**Usuário:** "NPS após primeira semana"

**Claude:** "Perfeito. Resumindo as métricas de validação, não de crescimento ainda."

### Resultado

Documento com:
- **Hipótese → Métrica:**
  - Empresas pagariam → Contratos fechados (meta: 5)
  - Funcionários usariam → Taxa de adesão (meta: 30%)
  - Usariam de novo → Recompra semanal (meta: 50%)
  - Gostam → NPS (meta: > 40)
  - É lucrativo → Margem por pedido (baseline: a medir)
- **Decisão:** Se atingir 4 de 5 métricas, prosseguir

---

## Exemplo 5: Projeto sem baseline disponível

### Contexto
Primeiro app mobile de um banco tradicional. Não há histórico digital.

### Conversa

**Usuário:** "Estamos lançando o primeiro app do banco. Não temos baseline de nada digital"

**Claude:** "Projeto greenfield! Não temos baseline digital, mas podemos usar proxy do mundo físico. Quantas transações acontecem nas agências por mês?"

**Usuário:** "Cerca de 500 mil"

**Claude:** "Esse é um proxy. A pergunta é: quantas dessas poderiam migrar para o app?"

**Usuário:** "Estimamos que 60% são simples o suficiente para app"

**Claude:** "Então 300 mil transações potenciais. North Star poderia ser 'Transações no app' com meta de capturar X% disso. Mas sem histórico digital, como definir meta?"

**Usuário:** "Olhar benchmarks de outros bancos?"

**Claude:** "Boa ideia. Bancos digitais têm 80%+ no app. Bancos tradicionais migrando, 30-40% no primeiro ano. Meta: 30% das transações elegíveis no app em 12 meses?"

**Usuário:** "Parece realista"

**Claude:** "Isso dá 90 mil transações/mês no app em 12 meses. Quebrando em metas intermediárias: 3 meses = 20 mil, 6 meses = 50 mil."

**Usuário:** "E as métricas de usuário?"

**Claude:** "Adoção: quantos correntistas baixaram e ativaram? Vocês têm 200 mil correntistas?"

**Usuário:** "Sim, aproximadamente"

**Claude:** "Meta de ativação: 30% em 12 meses = 60 mil usuários ativos. Retention: D30 de apps de banco costuma ser 40-50%. Vamos mirar 40%."

**Usuário:** "E se não tivermos os dados para medir essas coisas?"

**Claude:** "Ação prioritária: implementar analytics antes do lançamento. Ferramenta escolhida?"

**Usuário:** "Ainda não decidimos"

**Claude:** "Vou registrar como blocker. Sem analytics, não temos como medir nada. Firebase Analytics é gratuito e suficiente para começar."

### Resultado

Documento com:
- **North Star:** Transações no app (0 → 90k/mês em 12 meses)
- **Proxy usado:** Volume de agências (500k) × Elegibilidade (60%)
- **Benchmarks:** Bancos tradicionais migrando (30-40% em 1 ano)
- **Usuário:** Downloads/Ativação (60k em 12m), D30 Retention (40%)
- **Blocker:** Implementar analytics antes do lançamento
- **Plano de baseline:** Coletar 4 semanas pós-lançamento

---

## Anti-exemplo: O que NÃO fazer

### Conversa problemática

**Usuário:** "Quais métricas devo usar para meu projeto?"

**Claude:** ❌ "As métricas mais comuns são:
- DAU/MAU para engajamento
- NPS para satisfação
- Conversão para negócio
- Churn para retenção

Essas métricas servem para a maioria dos projetos!"

### Por que está errado

- Não perguntou sobre o projeto específico
- Métricas genéricas que podem ser irrelevantes
- Não definiu baseline ou metas
- Não conectou com o objetivo do projeto
- Não identificou a North Star

### Como deveria ser

**Claude:** ✅ "Para definir métricas que fazem sentido, preciso entender o contexto. Me conta: qual é o objetivo principal desse projeto? O que muda se ele der certo?"

---

## Checklist de qualidade do documento

Antes de finalizar o `success-metrics.md`, verifique:

- [ ] Objetivo central claro e conectado à visão
- [ ] UMA North Star Metric definida
- [ ] North Star tem definição precisa de cálculo
- [ ] Baseline definido ou plano para definir
- [ ] Metas com números específicos e prazos
- [ ] Métricas de negócio (2-3)
- [ ] Métricas de usuário usando HEART (2-3)
- [ ] Critérios de aceitação do lançamento
- [ ] Responsáveis definidos
- [ ] Fontes de dados identificadas
- [ ] Anti-métricas consideradas
- [ ] Nenhuma métrica de vaidade sem justificativa
