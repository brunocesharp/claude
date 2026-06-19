# Troubleshooting — Discovery Metrics

Problemas comuns durante a definição de métricas e como resolvê-los.

---

## Problema: Usuário quer várias North Star Metrics

### Sintoma
- "Temos três métricas principais igualmente importantes"
- "Não dá pra escolher só uma"
- "Precisamos acompanhar conversão E engajamento E receita"

### Causa
- Falta de clareza sobre o valor central do produto
- Múltiplos stakeholders com objetivos diferentes
- Medo de "deixar algo de fora"

### Solução

1. **Explique o conceito:**
   > "North Star é UMA métrica que serve de bússola. Ter várias é como ter vários nortes — não ajuda a navegar."

2. **Force a priorização:**
   > "Se o projeto tivesse que escolher entre melhorar A ou B, e só pudesse uma, qual seria?"

3. **Use hierarquia:**
   > "Vamos definir uma North Star e as outras como métricas de suporte. A North Star guia a direção, as outras verificam se não estamos sacrificando algo importante."

4. **Teste com cenário:**
   > "Se a métrica A subir mas B cair, o projeto está indo bem ou mal? A resposta diz qual é a principal."

5. **Estruture assim:**
   ```
   NORTH STAR: [uma métrica]
   
   MÉTRICAS DE SUPORTE:
   - Negócio: [2-3 métricas]
   - Usuário: [2-3 métricas]
   ```

---

## Problema: Todas as métricas são de vaidade

### Sintoma
Métricas propostas não indicam valor real:
- "Número de cadastros"
- "Downloads do app"
- "Pageviews"
- "Seguidores nas redes"

### Causa
- Métricas fáceis de coletar vs. métricas significativas
- Influência de marketing/growth
- Falta de clareza sobre o que é valor

### Solução

1. **Faça o teste do "e daí?":**
   > "Tivemos 10.000 cadastros. E daí? O que isso significa para o negócio?"

2. **Empurre para ação:**
   > "Cadastros não pagam contas. Quantos desses cadastros USARAM o produto? Quantos PAGARAM?"

3. **Use o funil:**
   ```
   Cadastros (vaidade)
      ↓
   Ativados (melhor)
      ↓
   Retidos (muito melhor)
      ↓
   Pagantes (negócio real)
   ```

4. **Proponha substituições:**

   | Métrica de vaidade | Substitua por |
   |--------------------|---------------|
   | Cadastros | Taxa de ativação |
   | Downloads | D7 retention |
   | Pageviews | Ações de valor por sessão |
   | Seguidores | Engajamento rate |
   | Tempo no app | Tarefas completadas |

5. **Questione o valor:**
   > "Essa métrica subindo significa que estamos entregando mais valor para o usuário, ou só mais atividade?"

---

## Problema: Não existe baseline

### Sintoma
- "Não temos sistema atual, é tudo novo"
- "Ninguém mede isso hoje"
- "Os dados estão em planilhas espalhadas"

### Causa
- Projeto greenfield
- Falta de cultura de dados
- Sistemas legados sem instrumentação

### Solução

1. **Não trave por falta de baseline:**
   > "Vamos registrar 'a medir' e definir como primeira ação após lançamento."

2. **Crie plano de coleta:**
   ```
   Métrica: [nome]
   Baseline: A medir
   Plano:
   - Semana 1-2: Implementar coleta
   - Semana 3-4: Coletar dados iniciais
   - Semana 5: Definir baseline oficial
   - Semana 6+: Comparar contra baseline
   ```

3. **Use proxies temporários:**
   > "Enquanto não temos o dado real, podemos usar [proxy] como aproximação."

4. **Colete manualmente se necessário:**
   > "Para as primeiras semanas, alguém pode coletar manualmente? Depois automatizamos."

5. **Defina responsável:**
   > "Quem vai garantir que o baseline seja estabelecido nas primeiras 4 semanas?"

---

## Problema: Métricas de negócio conflitam com métricas de usuário

### Sintoma
- Otimizar receita prejudica experiência
- Aumentar engajamento não gera conversão
- Usuários satisfeitos mas negócio não cresce

### Causa
- Modelo de negócio desalinhado com valor para usuário
- Otimização de curto prazo vs. longo prazo
- Métricas mal definidas

### Solução

1. **Identifique o conflito:**
   > "Parece que melhorar A piora B. Vamos entender por quê."

2. **Busque a causa raiz:**
   | Conflito | Possível causa |
   |----------|----------------|
   | Mais ads = menos satisfação | Modelo de monetização agressivo |
   | Mais features = menos usabilidade | Escopo inchado |
   | Mais conversão = mais churn | Venda agressiva, produto fraco |

3. **Encontre o equilíbrio:**
   > "Qual é o nível de [métrica A] que maximiza [métrica B] no longo prazo?"

4. **Use constraints:**
   > "Vamos otimizar receita MAS com constraint de NPS > 40. Se NPS cair, paramos."

5. **Pense em longo prazo:**
   > "Forçar conversão agora pode aumentar receita Q1, mas o churn vai destruir Q2-Q4. Qual cenário preferimos?"

6. **Revise o modelo:**
   > "Se otimizar o negócio prejudica o usuário, talvez o modelo de negócio precise de ajuste."

---

## Problema: Stakeholders discordam sobre o que é sucesso

### Sintoma
- Vendas quer uma métrica, Produto quer outra
- CEO foca em receita, CPO foca em engajamento
- Cada área puxa para seu lado

### Causa
- Objetivos departamentais diferentes
- Falta de alinhamento estratégico
- Incentivos desalinhados

### Solução

1. **Escale para o patrocinador:**
   > "Temos visões diferentes sobre sucesso. Quem pode desempatar?"

2. **Volte para a visão:**
   > "O que dissemos no vision.md sobre o objetivo do projeto? Qual métrica reflete isso?"

3. **Crie hierarquia:**
   > "Vamos ter uma North Star do projeto, mas cada área pode ter métricas secundárias próprias."

4. **Mostre interdependência:**
   > "Receita depende de retenção, que depende de satisfação. Não são concorrentes, são sequenciais."

5. **Documente o acordo:**
   > "Vou registrar que a prioridade acordada é [métrica]. Todos concordam em usar essa como norte?"

---

## Problema: Métricas impossíveis de medir

### Sintoma
- "Queremos medir satisfação mas não temos como"
- "O sistema legado não tem logs"
- "Não temos orçamento para ferramenta de analytics"

### Causa
- Limitações técnicas
- Restrições de orçamento
- Falta de planejamento de instrumentação

### Solução

1. **Identifique alternativas:**
   > "Se não podemos medir X diretamente, existe algum proxy?"

2. **Proponha coleta manual:**
   > "Para começar, podemos coletar manualmente via [planilha/survey/observação]?"

3. **Use ferramentas gratuitas:**
   | Tipo | Opções gratuitas |
   |------|------------------|
   | Analytics | Google Analytics, Plausible, Umami |
   | Surveys | Google Forms, Typeform (free tier) |
   | Session recording | Hotjar (free tier), Microsoft Clarity |
   | BI | Metabase (self-hosted), Google Data Studio |

4. **Planeje instrumentação:**
   > "Vamos adicionar 'implementar tracking' como requisito do projeto."

5. **Simplifique a métrica:**
   > "Se não dá pra medir [complexo], o que seria uma versão mais simples que dá pra medir?"

---

## Problema: Métricas mudam de significado

### Sintoma
- "A definição de 'usuário ativo' mudou"
- "Antes contávamos X, agora contamos Y"
- Comparações históricas impossíveis

### Causa
- Falta de documentação da definição
- Evolução do produto
- Mudança de ferramenta

### Solução

1. **Documente definições precisamente:**
   ```
   Métrica: DAU (Daily Active Users)
   Definição: Usuários únicos que realizaram pelo menos 
              1 ação de valor no dia (login não conta)
   Ação de valor: [listar ações específicas]
   Fonte: Tabela events, filtro action_type IN (...)
   ```

2. **Versione as métricas:**
   > "DAU v1 (antes de março): incluía login. DAU v2 (março+): exclui login."

3. **Mantenha histórico:**
   > "Quando mudar a definição, calcule ambas as versões por 1-2 meses para ter overlap."

4. **Comunique mudanças:**
   > "A partir de [data], DAU será calculado de forma diferente. Motivo: [explicação]."

---

## Problema: Foco excessivo em métricas de curto prazo

### Sintoma
- Só métricas de lançamento, nada de longo prazo
- "Vamos ver como está depois que lançar"
- Sem visão de 6-12 meses

### Causa
- Pressão de entrega
- Falta de visão estratégica
- Cultura de projeto vs. produto

### Solução

1. **Exija visão de longo prazo:**
   > "Ok para métricas de lançamento. E daqui 6 meses? O que define sucesso?"

2. **Use horizontes:**
   ```
   Lançamento (Semana 1): Critérios de aceite
   Curto prazo (3 meses): Adoção e estabilização
   Médio prazo (6 meses): Engajamento e valor
   Longo prazo (12 meses): ROI e crescimento
   ```

3. **Conecte com ROI:**
   > "O projeto custou X. Em quanto tempo esperamos recuperar esse investimento? Como vamos medir?"

4. **Lembre do ciclo de produto:**
   > "Produto não acaba no lançamento. Precisamos de métricas para evolução contínua."
