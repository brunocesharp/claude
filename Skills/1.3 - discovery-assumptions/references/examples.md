# Exemplos de Uso — Discovery Assumptions

Cenários detalhados de como usar a skill em diferentes situações.

---

## Exemplo 1: Startup em fase inicial (tudo é hipótese)

### Contexto
Startup quer criar um app de gestão financeira pessoal. Não há produto ainda, apenas uma ideia.

### Conversa

**Usuário:** "Quero mapear as hipóteses do nosso app de finanças pessoais"

**Claude:** "Ótimo! Em projetos novos, quase tudo é hipótese — o que é saudável. Vamos começar pelos usuários. Quem vocês imaginam usando esse app?"

**Usuário:** "Jovens de 25-35 anos que querem controlar gastos"

**Claude:** "Essa já é uma hipótese: 'Nosso público-alvo são jovens de 25-35 anos'. Qual a evidência de que esse público específico tem esse problema?"

**Usuário:** "Bom, a gente vê muita gente reclamando nas redes sociais..."

**Claude:** "Reclamação em redes sociais é um sinal, mas fraco. Vou registrar como baixa certeza. Outra hipótese implícita: vocês assumem que esses jovens QUEREM uma solução de app. Já usam algo hoje? Planilha, outro app?"

**Usuário:** "Não pesquisamos isso ainda"

**Claude:** "Então é mais uma hipótese de baixa certeza: 'Usuários estão dispostos a substituir a solução atual por um app novo'. Isso é crítico — se eles já têm algo que funciona, convencê-los a mudar é difícil. Vamos para negócio: qual o modelo de receita?"

**Usuário:** "Assinatura de R$15/mês"

**Claude:** "Hipótese de negócio: 'Usuários pagarão R$15/mês por esse app'. Impacto altíssimo se estiver errado — sem receita, não há negócio. Certeza?"

**Usuário:** "Baixa, não testamos pricing"

**Claude:** "Essa vai para o quadrante crítico. Sugiro um smoke test antes de desenvolver — landing page com opção de pré-cadastro e indicação de preço."

### Resultado

Documento com:
- 8 hipóteses mapeadas (maioria baixa certeza)
- 4 hipóteses críticas: público-alvo, disposição de trocar solução atual, willingness to pay, tamanho de mercado
- Plano de validação: 5 entrevistas + landing page com pricing
- Timeline: 3 semanas antes de começar desenvolvimento

---

## Exemplo 2: Feature em produto existente

### Contexto
Empresa de SaaS quer adicionar módulo de relatórios ao produto atual.

### Conversa

**Usuário:** "Precisamos mapear hipóteses para o novo módulo de relatórios"

**Claude:** "Vi que vocês já têm `vision.md` e `opportunity.md`. Lá menciona que gestores pedem relatórios há 6 meses. Isso é evidência forte — vou registrar como alta certeza que existe demanda. Mas ainda há hipóteses. Por exemplo: vocês assumem que relatórios VÃO resolver a dor. Como sabem?"

**Usuário:** "Os clientes pediram relatórios..."

**Claude:** "Clientes pedem relatórios, mas o que eles realmente PRECISAM? Às vezes pedem uma coisa e o problema é outro. Já investigaram o job to be done por trás?"

**Usuário:** "Eles querem acompanhar performance da equipe"

**Claude:** "Ok, a hipótese então é: 'Relatórios são a melhor forma de acompanhar performance da equipe'. Pode haver outras: dashboards em tempo real, alertas automáticos, ranking gamificado. Vocês testaram alternativas?"

**Usuário:** "Não, assumimos que relatórios é o que eles querem"

**Claude:** "Vou registrar como média certeza — tem demanda, mas a solução específica não foi validada. E sobre o técnico: o sistema atual tem os dados necessários para os relatórios?"

**Usuário:** "Temos os dados, mas não sei se a performance aguenta relatórios pesados"

**Claude:** "Hipótese técnica crítica: 'O sistema atual suporta consultas de relatórios com performance aceitável'. Sugiro um spike antes de comprometer escopo."

### Resultado

Documento com:
- Hipóteses de usuário parcialmente validadas (demanda existe)
- Hipótese crítica: solução específica (relatórios vs alternativas)
- Hipótese técnica crítica: performance de consultas
- Plano: spike técnico (3 dias) + 3 entrevistas de validação de solução

---

## Exemplo 3: Projeto com histórico de dados

### Contexto
E-commerce quer otimizar checkout. Têm dados de 2 anos de operação.

### Conversa

**Usuário:** "Queremos mapear hipóteses para a otimização do checkout"

**Claude:** "Com 2 anos de dados, várias hipóteses podem ser validadas por análise. Vamos começar: qual é a hipótese principal do projeto?"

**Usuário:** "Que simplificar o checkout vai aumentar conversão"

**Claude:** "Boa. Vocês têm dados de onde as pessoas abandonam o funil atual?"

**Usuário:** "Sim, 40% abandona na página de pagamento"

**Claude:** "Isso é evidência forte de que há problema na página de pagamento. A hipótese 'há atrito no checkout' tem alta certeza. Mas 'simplificar vai resolver' ainda é hipótese. Pode ser preço de frete, falta de opção de pagamento, desconfiança... Vocês sabem por que abandonam?"

**Usuário:** "Não temos essa informação"

**Claude:** "Então a hipótese real é: 'A causa do abandono é complexidade, não outros fatores'. Isso é crítico — se for frete caro, simplificar não resolve nada."

**Usuário:** "Como validamos?"

**Claude:** "Duas opções: survey de exit intent ('por que você não completou?') ou análise de comportamento (session recording). Qual é mais viável?"

**Usuário:** "Já temos Hotjar instalado"

**Claude:** "Perfeito. A validação pode ser feita com dados existentes. Sugiro: 20 sessões de abandono analisadas antes de definir escopo."

### Resultado

Documento com:
- Hipóteses validadas por dados: problema existe, localização identificada
- Hipótese crítica: causa do abandono (complexidade vs outros fatores)
- Método de validação: análise de session recordings
- Sem necessidade de pesquisa externa — dados internos suficientes

---

## Exemplo 4: Stakeholder que não aceita incertezas

### Contexto
Projeto patrocinado por executivo que quer ir direto para desenvolvimento.

### Conversa

**Usuário:** "O diretor quer que a gente comece a desenvolver semana que vem. Não quer esperar validações"

**Claude:** "Entendo a pressão. Vamos ser estratégicos: mapear as hipóteses rapidamente e identificar quais PRECISAM de validação e quais podemos aceitar como risco."

**Usuário:** "Ele acha que já sabe tudo sobre o mercado"

**Claude:** "A experiência dele é valiosa. Podemos registrar o conhecimento dele como evidência para aumentar a certeza de algumas hipóteses. Quais coisas ele tem certeza?"

**Usuário:** "Que o mercado quer essa solução porque concorrentes estão crescendo"

**Claude:** "Isso é evidência de mercado — concorrentes crescendo sugere demanda. Vou registrar como média-alta certeza. Mas há uma hipótese implícita: 'Nosso produto vai ser escolhido em vez do concorrente'. O que nos diferencia?"

**Usuário:** "Preço menor"

**Claude:** "Hipótese: 'Clientes vão escolher a gente por preço'. Se errada, perdemos mercado. Qual a certeza?"

**Usuário:** "Média, acho..."

**Claude:** "Essa pode ser validada em paralelo ao desenvolvimento. Sugiro: enquanto o time desenvolve, fazemos 5 entrevistas com prospects perguntando sobre critérios de escolha. 2 semanas, não atrasa nada."

**Usuário:** "Isso ele pode aceitar"

**Claude:** "Perfeito. Vou registrar as hipóteses críticas com plano de validação em paralelo. Assim entregamos velocidade E reduzimos risco."

### Resultado

Documento com:
- Hipóteses priorizadas por criticidade
- Validações paralelas ao desenvolvimento (não bloqueantes)
- Premissas aceitas baseadas na experiência do executivo (documentadas)
- Risk register claro para decisão consciente

---

## Exemplo 5: Hipóteses técnicas complexas

### Contexto
Projeto envolve machine learning e integrações com sistemas legados.

### Conversa

**Usuário:** "Temos hipóteses técnicas complexas: usar ML para previsão de demanda"

**Claude:** "ML é rico em hipóteses. Vamos mapear: primeiro, vocês têm dados suficientes para treinar um modelo?"

**Usuário:** "Temos 18 meses de histórico de vendas"

**Claude:** "Ok, hipótese: '18 meses de dados são suficientes para treinar modelo com acurácia útil'. Qual a certeza?"

**Usuário:** "Média. O cientista de dados acha que sim, mas não testou"

**Claude:** "Próxima hipótese: 'Os dados disponíveis têm qualidade suficiente'. Dados de vendas costumam ter problemas — promoções, sazonalidade, dados faltantes. Já analisaram?"

**Usuário:** "Não em profundidade"

**Claude:** "Hipótese crítica então. E sobre a integração: o modelo vai precisar de dados do ERP?"

**Usuário:** "Sim, em tempo real"

**Claude:** "Hipótese técnica: 'O ERP suporta integração em tempo real com latência aceitável'. ERPs legados frequentemente são gargalos. Já testaram?"

**Usuário:** "O fornecedor disse que tem API"

**Claude:** "'Fornecedor disse' não é validação. Vou registrar como baixa certeza. Sugiro spike de integração antes de comprometer arquitetura ML."

**Usuário:** "E sobre a acurácia do modelo?"

**Claude:** "Hipótese: 'O modelo terá acurácia suficiente para decisões de negócio'. O que é 'suficiente'? 80%? 95%? E qual o custo de errar?"

**Usuário:** "Se prever errado, compramos estoque demais ou de menos"

**Claude:** "Alto impacto. Sugiro: definir threshold de acurácia aceitável ANTES de começar, e PoC com dados históricos para validar se é atingível."

### Resultado

Documento com:
- 6 hipóteses técnicas mapeadas
- 3 críticas: qualidade de dados, integração ERP, acurácia mínima
- Plano de validação em fases:
  1. Análise exploratória de dados (1 semana)
  2. Spike de integração ERP (3 dias)
  3. PoC de modelo com dados históricos (2 semanas)
- Critérios de go/no-go definidos para cada fase

---

## Anti-exemplo: O que NÃO fazer

### Conversa problemática

**Usuário:** "Quero mapear hipóteses do projeto"

**Claude:** ❌ "Ok! As hipóteses são:
1. Usuários vão querer o produto
2. A tecnologia vai funcionar
3. O negócio vai ser viável

Pronto! Essas são as hipóteses principais de qualquer projeto."

### Por que está errado

- Hipóteses genéricas demais
- Não perguntou sobre o projeto específico
- Não usou documentos anteriores (vision.md, opportunity.md)
- Não classificou impacto/certeza
- Não sugeriu validações específicas

### Como deveria ser

**Claude:** ✅ "Antes de mapear, deixa eu ver o contexto. Vi que vocês têm `vision.md` com público definido como X e `opportunity.md` com dores Y e Z. Vamos partir daí: a primeira hipótese implícita é que X realmente é o público certo. Qual a evidência que vocês têm disso?"

---

## Checklist de qualidade do documento

Antes de finalizar o `assumptions.md`, verifique:

- [ ] Pelo menos 2-3 hipóteses de cada tipo (usuário, negócio, técnica)
- [ ] Todas classificadas por impacto e certeza
- [ ] Pelo menos 1 hipótese no quadrante crítico (se não, questione se o projeto tem risco suficiente para valer a pena)
- [ ] Hipóteses críticas têm plano de validação
- [ ] Critérios de sucesso/falha definidos para validações
- [ ] Conexão com oportunidades do opportunity.md
- [ ] Premissas aceitas estão documentadas com justificativa
- [ ] Não há hipóteses vagas ("vai dar certo")
- [ ] Todas são afirmações testáveis
