# Exemplos de Uso — Discovery Opportunity

Cenários detalhados de como usar a skill em diferentes situações.

---

## Exemplo 1: Produto B2B com múltiplos perfis

### Contexto
Sistema de gestão de frotas para transportadoras. Três perfis principais: gestor de frota, motorista, financeiro.

### Conversa

**Usuário:** "Quero mapear as oportunidades do nosso sistema de gestão de frotas"

**Claude:** "Ótimo! Vi que o projeto já tem um `vision.md` com três perfis identificados: gestor, motorista e financeiro. Vamos mapear os jobs de cada um. Começando pelo gestor de frota: quando ele abre o sistema, o que está tentando fazer?"

**Usuário:** "Ele quer saber onde estão os caminhões e se estão no horário"

**Claude:** "Perfeito. E o que define 'missão cumprida' para ele? Como ele sabe que conseguiu o que precisava?"

**Usuário:** "Se ele consegue responder quando um cliente liga perguntando da entrega"

**Claude:** "Então o job é algo como: 'Quando um cliente liga perguntando da entrega, quero saber a localização exata e previsão de chegada, para responder na hora sem precisar ligar para o motorista'. Correto?"

**Usuário:** "Isso, exatamente"

**Claude:** "Agora as dores. O que atrapalha ele fazer isso hoje?"

**Usuário:** "O GPS atrasa uns 15 minutos, aí ele fica sem saber onde o caminhão está de verdade. E quando o motorista entra em área sem sinal, some do mapa."

### Resultado

Documento com:
- Jobs mapeados por perfil (gestor, motorista, financeiro)
- Dores críticas: latência de GPS, perda de sinal em áreas remotas
- Contexto: uso reativo (quando cliente liga), pressão de tempo alta
- Oportunidade prioritária: "Informação de localização confiável em tempo real"

---

## Exemplo 2: Usuário começa falando de funcionalidades

### Contexto
Startup quer criar um app de produtividade. Fundador já tem ideias fortes sobre o que construir.

### Conversa

**Usuário:** "A gente precisa de um dashboard com gráficos em tempo real e notificações push"

**Claude:** "Dashboard e notificações são possíveis soluções. Antes de definir isso, me ajuda a entender: qual problema eles resolveriam? O que é difícil ou demorado hoje que o dashboard ajudaria?"

**Usuário:** "O pessoal não sabe o que priorizar no dia"

**Claude:** "Entendi. E por que eles não sabem priorizar? O que falta?"

**Usuário:** "As tarefas vêm de vários lugares — email, Slack, reuniões — e fica tudo espalhado"

**Claude:** "Então a dor é: informações fragmentadas dificultam saber o que é mais importante. O dashboard seria uma forma de consolidar isso. Existe alguma outra dor relacionada, ou essa é a principal?"

**Usuário:** "Também tem o problema de não saber se está progredindo. Fim do dia a pessoa não sabe se foi produtivo ou não"

**Claude:** "Ótimo, duas dores então: fragmentação de informações e falta de visibilidade de progresso. Agora me conta: quem sente essas dores? É todo mundo ou algum perfil específico?"

### Resultado

Documento com:
- Dores reais identificadas (fragmentação, falta de visibilidade)
- Funcionalidades originais registradas em "Ideias de Solução (para depois)"
- Jobs: "Começar o dia sabendo o que priorizar", "Terminar o dia sabendo se fui produtivo"
- Oportunidade: "Consolidar tarefas de múltiplas fontes em uma visão única"

---

## Exemplo 3: Usuário não tem acesso a usuários reais

### Contexto
PM de uma empresa fazendo discovery interno, sem orçamento para pesquisa formal.

### Conversa

**Usuário:** "Não conversei com usuários ainda, estou baseando no que ouço em reuniões"

**Claude:** "Tudo bem, podemos trabalhar com isso. Vou só marcar o que for suposição para vocês validarem depois. Me conta: o que você ouve nas reuniões sobre dores dos usuários?"

**Usuário:** "O time de vendas reclama muito que demora para gerar propostas"

**Claude:** "Ótimo ponto de partida. Você sabe quanto tempo demora hoje? Ou é uma percepção geral?"

**Usuário:** "Não tenho o número exato..."

**Claude:** "Vou registrar como 'a investigar'. Uma forma rápida de validar: pedir para 3 vendedores cronometrarem da próxima vez. Você conseguiria fazer isso?"

**Usuário:** "Consigo sim"

**Claude:** "Perfeito. E sobre o contexto: quando o vendedor precisa gerar uma proposta? É logo depois de uma reunião? Tem urgência?"

**Usuário:** "Geralmente o cliente pede 'me manda a proposta' na reunião, e o vendedor quer mandar no mesmo dia para não perder o timing"

**Claude:** "Então há pressão de tempo. Vou registrar: contexto de uso pós-reunião, expectativa de entrega no mesmo dia. Isso é observação sua ou você ouviu os vendedores falando?"

**Usuário:** "Ouvi eles falando"

**Claude:** "Ótimo, então é mais confiável. Vou marcar como 'observação de campo' em vez de suposição."

### Resultado

Documento com:
- Distinção clara entre "observação" e "suposição"
- Seção "Pontos a Investigar" com métodos de validação sugeridos
- Jobs e dores preliminares baseados em evidências parciais
- Próximo passo: validar com cronometragem real

---

## Exemplo 4: Empresa com tentativas anteriores fracassadas

### Contexto
Empresa que já tentou resolver o problema duas vezes com soluções diferentes.

### Conversa

**Usuário:** "Já tentamos duas vezes fazer um sistema de chamados e não deu certo"

**Claude:** "Isso é ouro! Entender por que não funcionou evita repetir erros. Me conta sobre a primeira tentativa: o que vocês construíram e por que não deu certo?"

**Usuário:** "Compramos um sistema de mercado, o Zendesk. Muito complexo, ninguém usava"

**Claude:** "Complexidade foi a barreira. O que era complexo especificamente? Muitas opções? Interface confusa? Treinamento necessário?"

**Usuário:** "Tinha que categorizar o chamado em 15 campos antes de enviar. O pessoal desistia"

**Claude:** "Entendi — fricção alta no cadastro. E a segunda tentativa?"

**Usuário:** "Fizemos interno, uma planilha Google compartilhada. Funcionou por 2 meses, depois virou bagunça"

**Claude:** "O que causou a bagunça? Muita gente editando? Falta de estrutura? Informação desatualizada?"

**Usuário:** "Ninguém atualizava o status. Não dava para saber o que estava resolvido ou pendente"

**Claude:** "Então duas lições: (1) cadastro precisa ser simples, poucos campos, (2) atualização de status precisa ser fácil ou automática. Essas são restrições importantes para qualquer solução futura. Tem mais alguma tentativa ou workaround atual?"

### Resultado

Documento com:
- Seção "Tentativas Anteriores" rica em aprendizados
- Restrições derivadas: simplicidade de cadastro, status com baixa fricção
- Oportunidades enquadradas pelos aprendizados passados
- Evitação de erros já cometidos

---

## Exemplo 5: Discovery para feature, não produto novo

### Contexto
Produto já existe, equipe quer adicionar uma feature de relatórios.

### Conversa

**Usuário:** "Queremos adicionar relatórios ao nosso sistema de vendas"

**Claude:** "Relatórios é a solução proposta. Antes de desenhar os relatórios, vamos entender a oportunidade. Quem está pedindo relatórios e por quê?"

**Usuário:** "Os gerentes de vendas. Eles querem acompanhar performance da equipe"

**Claude:** "Entendi o job: acompanhar performance. O que é difícil nisso hoje? Como eles fazem atualmente?"

**Usuário:** "Eles exportam dados para Excel e montam na mão"

**Claude:** "Quanto tempo leva isso?"

**Usuário:** "Umas 2 horas por semana"

**Claude:** "E durante essa montagem, quais são as partes mais chatas ou propensas a erro?"

**Usuário:** "Cruzar dados de diferentes telas. Às vezes os números não batem"

**Claude:** "Então duas dores: tempo gasto (2h/semana) e inconsistência de dados. Qual é mais crítica?"

**Usuário:** "A inconsistência, porque o gerente perde credibilidade se apresenta número errado"

**Claude:** "Interessante — a dor emocional (credibilidade) é mais forte que a funcional (tempo). Isso muda a prioridade do que resolver primeiro. Algum relatório específico que é mais problemático?"

### Resultado

Documento focado em feature:
- Job: "Apresentar dados de performance confiáveis para a diretoria"
- Dor crítica: inconsistência de dados (impacto em credibilidade)
- Dor secundária: tempo de montagem manual
- Contexto: apresentação semanal para diretoria
- Oportunidade: "Fonte única de verdade para métricas de vendas"

---

## Anti-exemplo: O que NÃO fazer

### Conversa problemática

**Usuário:** "Quero mapear oportunidades para um sistema de RH"

**Claude:** ❌ "Ok! Para um sistema de RH, as principais oportunidades geralmente são: gestão de folha de pagamento, controle de férias, recrutamento e seleção, avaliação de desempenho. Qual dessas vocês querem focar?"

### Por que está errado

- Claude assumiu oportunidades genéricas de mercado
- Não perguntou sobre os usuários específicos
- Não investigou dores reais
- Sugeriu soluções (funcionalidades) em vez de mapear problemas
- Ignorou o contexto específico da empresa

### Como deveria ser

**Claude:** ✅ "Ótimo! Antes de mapear oportunidades, me ajuda a entender: quem são os usuários principais desse sistema? E qual é a dor que motivou vocês a pensarem nisso agora?"

---

## Checklist de qualidade do documento

Antes de finalizar o `opportunity.md`, verifique:

- [ ] Pelo menos 1 job claramente definido por perfil principal
- [ ] Jobs seguem a fórmula "Quando [situação], quero [ação], para [resultado]"
- [ ] Dores estão separadas entre críticas e secundárias
- [ ] Desejos estão separados de dores
- [ ] Contexto de uso está detalhado (frequência, ambiente, pressão)
- [ ] Tentativas anteriores estão documentadas (ou indicado que não houve)
- [ ] Oportunidades estão priorizadas (A/B/C)
- [ ] Pontos incertos estão em "a investigar"
- [ ] Nenhuma solução/funcionalidade aparece como oportunidade
- [ ] Ideias de solução estão separadas para fase posterior
