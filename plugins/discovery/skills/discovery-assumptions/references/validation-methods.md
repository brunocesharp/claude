# Métodos de Validação de Hipóteses

Este documento lista técnicas práticas para validar diferentes tipos de hipóteses.

---

## Hipóteses sobre Usuários (Desirability)

### Entrevistas Exploratórias

**O que é:** Conversas semi-estruturadas com usuários potenciais

**Quando usar:**
- Validar se o problema existe
- Entender contexto e motivações
- Descobrir nuances não mapeadas

**Como fazer:**
- 5-8 entrevistas geralmente bastam para padrões
- Use perguntas abertas, não direcionadas
- Foque no comportamento passado, não em intenções futuras
- Grave (com permissão) para análise posterior

**Custo:** Baixo (tempo)
**Tempo:** 1-2 semanas
**Confiança:** Média (qualitativo)

**Dica:** Leia "The Mom Test" de Rob Fitzpatrick para técnicas de entrevista.

---

### Teste de Usabilidade com Protótipo

**O que é:** Observar usuários tentando completar tarefas em um protótipo

**Quando usar:**
- Validar se a solução proposta é usável
- Identificar pontos de fricção
- Testar fluxos antes de desenvolver

**Como fazer:**
- Crie protótipo em Figma, Maze ou similar
- Defina 3-5 tarefas específicas
- Observe 5-7 usuários (suficiente para 80% dos problemas)
- Não ajude — observe e anote

**Custo:** Baixo-Médio (ferramenta + tempo)
**Tempo:** 1-2 semanas
**Confiança:** Média-Alta

---

### Survey Quantitativo

**O que é:** Questionário estruturado com amostra maior

**Quando usar:**
- Validar se padrões qualitativos se confirmam em escala
- Medir intensidade de dores
- Priorizar entre opções

**Como fazer:**
- Use Typeform, Google Forms ou similar
- Mantenha curto (5-10 perguntas)
- Inclua perguntas de filtro para garantir amostra relevante
- Busque N>30 para significância estatística básica

**Custo:** Baixo (ferramenta) + Médio (distribuição)
**Tempo:** 1-3 semanas
**Confiança:** Alta (se amostra adequada)

---

### Análise de Dados Existentes

**O que é:** Examinar comportamento real em produto ou sistema existente

**Quando usar:**
- Validar hipóteses sobre comportamento atual
- Identificar padrões de uso
- Medir frequência de problemas

**Como fazer:**
- Defina métricas que comprovam/refutam a hipótese
- Extraia dados relevantes (analytics, logs, CRM)
- Analise tendências e segmentos

**Custo:** Baixo (se dados existem)
**Tempo:** Dias a 1 semana
**Confiança:** Alta (comportamento real)

---

## Hipóteses sobre Negócio (Viability)

### Smoke Test / Landing Page

**O que é:** Página que apresenta proposta de valor e mede interesse real

**Quando usar:**
- Validar interesse antes de construir
- Testar diferentes propostas de valor
- Coletar leads para validações futuras

**Como fazer:**
- Crie landing page com proposta clara
- Inclua CTA específico (cadastro, lista de espera, etc.)
- Direcione tráfego (ads, email, redes sociais)
- Meça conversão

**Custo:** Baixo-Médio
**Tempo:** 1-2 semanas
**Confiança:** Média-Alta

**Métricas de sucesso:**
- Taxa de conversão > 5% (lista de espera)
- Taxa de conversão > 2% (pré-venda)

---

### Pré-venda ou Carta de Intenção

**O que é:** Solicitar compromisso financeiro antes de construir

**Quando usar:**
- Validar disposição real de pagar
- Produtos B2B com ticket alto
- Quando smoke test não é suficiente

**Como fazer:**
- Apresente proposta detalhada para prospects
- Solicite depósito, assinatura de contrato ou carta de intenção
- Defina condições claras (reembolso se não entregar, etc.)

**Custo:** Baixo (tempo de vendas)
**Tempo:** 2-4 semanas
**Confiança:** Muito Alta (dinheiro é a validação mais forte)

---

### Benchmark de Mercado

**O que é:** Análise de concorrentes e mercado para validar viabilidade

**Quando usar:**
- Validar tamanho de mercado
- Entender pricing praticado
- Identificar gaps de mercado

**Como fazer:**
- Pesquise concorrentes diretos e indiretos
- Analise pricing, features, posicionamento
- Estime TAM, SAM, SOM
- Identifique diferenciais possíveis

**Custo:** Baixo (pesquisa)
**Tempo:** 1-2 semanas
**Confiança:** Média

---

### Análise Financeira

**O que é:** Modelagem de custos, receitas e break-even

**Quando usar:**
- Validar se o modelo de negócio fecha
- Identificar premissas financeiras críticas
- Definir pricing mínimo viável

**Como fazer:**
- Modele custos fixos e variáveis
- Projete receita com diferentes cenários
- Calcule break-even e payback
- Teste sensibilidade a variações

**Custo:** Baixo (tempo)
**Tempo:** Dias a 1 semana
**Confiança:** Média (depende das premissas)

---

## Hipóteses Técnicas (Feasibility)

### Spike Técnico

**O que é:** Investigação timeboxada para validar viabilidade técnica

**Quando usar:**
- Validar se uma integração funciona
- Testar performance de uma abordagem
- Explorar tecnologia nova

**Como fazer:**
- Defina pergunta específica a responder
- Timebox curto (2-5 dias)
- Foque em responder a pergunta, não em código de produção
- Documente aprendizados

**Custo:** Médio (tempo de dev)
**Tempo:** 2-5 dias
**Confiança:** Alta

**Template de spike:**
```
Pergunta: [O que queremos descobrir?]
Timebox: [Quantos dias?]
Critério de sucesso: [Como sabemos que funciona?]
Resultado: [O que aprendemos?]
Recomendação: [Seguir, ajustar ou abandonar?]
```

---

### Prova de Conceito (PoC)

**O que é:** Implementação mínima que demonstra viabilidade

**Quando usar:**
- Validar arquitetura proposta
- Demonstrar para stakeholders
- Testar integração end-to-end

**Como fazer:**
- Implemente o caminho crítico apenas
- Ignore edge cases e tratamento de erros
- Foque em provar que funciona, não em produção

**Custo:** Médio-Alto (tempo de dev)
**Tempo:** 1-3 semanas
**Confiança:** Alta

---

### Teste de Performance

**O que é:** Validar se o sistema aguenta a carga esperada

**Quando usar:**
- Validar hipóteses de escalabilidade
- Testar antes de lançamento
- Comparar abordagens técnicas

**Como fazer:**
- Defina cenários de carga (usuários simultâneos, requests/segundo)
- Use ferramentas como k6, JMeter, Locust
- Meça latência, throughput, erros
- Identifique gargalos

**Custo:** Médio (ferramentas + tempo)
**Tempo:** 1-2 semanas
**Confiança:** Alta

---

### Consulta com Especialista

**O que é:** Validar com alguém que já enfrentou desafio similar

**Quando usar:**
- Tecnologia desconhecida pela equipe
- Decisões arquiteturais críticas
- Validar estimativas de esforço

**Como fazer:**
- Identifique especialista (interno, comunidade, consultor)
- Prepare perguntas específicas
- Documente recomendações
- Valide com segunda opinião se crítico

**Custo:** Baixo a Alto (depende do especialista)
**Tempo:** Dias
**Confiança:** Média-Alta (depende da fonte)

---

## Matriz de Seleção de Método

| Tipo de Hipótese | Método Rápido | Método Robusto |
|------------------|---------------|----------------|
| Usuário quer isso? | Entrevistas (5-8) | Survey (N>100) + Pré-venda |
| Usuário consegue usar? | Teste com protótipo | Teste com MVP real |
| Resolve o problema? | Concierge | MVP funcional |
| Negócio é viável? | Benchmark | Análise financeira + Pré-venda |
| Tecnicamente possível? | Spike (2-5 dias) | PoC (1-3 semanas) |
| Escala funciona? | Consulta especialista | Teste de performance |

---

## Critérios de Sucesso

Antes de validar, defina o critério de sucesso:

| Tipo | Exemplo de Critério |
|------|---------------------|
| Entrevistas | "7 de 8 mencionaram essa dor espontaneamente" |
| Survey | "NPS > 40" ou "% concordando > 70%" |
| Landing page | "Taxa de conversão > 5%" |
| Pré-venda | "3 contratos assinados" |
| Spike | "Integração funciona com latência < 200ms" |
| PoC | "Fluxo completo funciona sem erros críticos" |

**Importante:** Defina ANTES de validar para evitar racionalização post-hoc.
