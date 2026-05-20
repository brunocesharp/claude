# Exemplos de Uso — Scope Generate

Cenários detalhados de como usar a skill em diferentes situações.

---

## Exemplo 1: Escopo geral de projeto novo

### Contexto
Primeiro escopo de um sistema de gestão de pedidos. Discovery completo disponível.

### Conversa

**Usuário:** "Quero gerar o escopo do projeto de gestão de pedidos"

**Claude:** "Encontrei o projeto 'gestao-pedidos' com os seguintes documentos de discovery:
- vision.md ✓
- opportunity.md ✓
- assumptions.md ✓
- stakeholders.md ✓
- success-metrics.md ✓

Nenhum escopo existente ainda. Este será o primeiro.

Qual será o título desse escopo?"

**Usuário:** "Escopo Geral do Sistema"

**Claude:** "Esse escopo cobre o projeto inteiro ou apenas uma parte?"

**Usuário:** "O projeto inteiro, é o escopo geral"

**Claude:** "Entendido. Para o escopo 'Escopo Geral do Sistema', vou utilizar todos os documentos de discovery. Confirma?"

**Usuário:** "Sim, pode gerar"

**Claude:** *[Gera o escopo consolidando todos os documentos]*

> "Escopo **'Escopo Geral do Sistema'** criado com sucesso!
>
> 📄 `docs/gestao-pedidos/escopo/escopo-geral-do-sistema/escopo.md`
> 📁 Discovery copiado para `docs/gestao-pedidos/escopo/escopo-geral-do-sistema/discovery/`
>
> **Situação:** Rascunho
>
> O escopo inclui:
> - 12 funcionalidades (8 Must, 3 Should, 1 Could)
> - 3 stakeholders aprovadores
> - North Star: Tempo médio de processamento de pedido
> - 2 hipóteses críticas a validar
>
> Próximos passos:
> - Revise o documento e ajuste se necessário
> - Envie para os aprovadores quando estiver pronto"

### Resultado

- Escopo completo com todas as informações do discovery
- Pasta `escopo-geral-do-sistema/` criada com cópias dos documentos
- Situação: Rascunho

---

## Exemplo 2: Escopo de módulo específico

### Contexto
Projeto já tem escopo geral aprovado. Agora criando escopo para módulo de relatórios.

### Conversa

**Usuário:** "Preciso criar um escopo para o módulo de relatórios"

**Claude:** "Encontrei o projeto com os seguintes escopos existentes:
- **Escopo Geral do Sistema** — Situação: Aprovado

E os documentos de discovery completos.

O novo escopo será para o módulo de relatórios. Qual será o título?"

**Usuário:** "Módulo de Relatórios Gerenciais"

**Claude:** "Este módulo foi mencionado no escopo geral como 'out of scope'. Confirmo que agora está sendo desenvolvido separadamente?"

**Usuário:** "Exato, estava planejado para a fase 2"

**Claude:** "Perfeito. Para o 'Módulo de Relatórios Gerenciais', quais documentos de discovery são relevantes? Pelo que vi no opportunity.md, as oportunidades relacionadas são:
- O3: 'Gestores não têm visibilidade dos dados'
- O5: 'Tomada de decisão baseada em intuição'

E no success-metrics.md:
- N2: 'Tempo para obter relatório'

Devo focar nesses pontos ou há outros?"

**Usuário:** "Esses são os principais. Pode focar neles"

**Claude:** *[Gera escopo focado nas oportunidades e métricas relevantes]*

> "Escopo **'Módulo de Relatórios Gerenciais'** criado!
>
> 📄 `docs/gestao-pedidos/escopo/modulo-de-relatorios-gerenciais/escopo.md`
>
> **Situação:** Rascunho
>
> Observações:
> - Vinculado como evolução do 'Escopo Geral do Sistema'
> - Focado nas oportunidades O3 e O5
> - 6 funcionalidades (4 Must, 2 Should)
>
> Adicionei referência cruzada para o escopo geral na seção 'Escopos Relacionados'."

### Resultado

- Escopo focado no módulo específico
- Conexão clara com escopo geral (relacionados)
- Apenas oportunidades e métricas relevantes incluídas

---

## Exemplo 3: Escopo de MVP/Fase 1

### Contexto
Projeto novo, discovery completo, mas querem começar com MVP antes de tudo.

### Conversa

**Usuário:** "Quero criar um escopo só do MVP, não do projeto inteiro"

**Claude:** "Entendido, escopo parcial focado no MVP. Li o discovery do projeto 'app-delivery'.

No opportunity.md há 8 oportunidades mapeadas. Para um MVP, quais são as essenciais?"

**Usuário:** "As três primeiras: cadastro de restaurantes, cardápio digital e pedido básico"

**Claude:** "Essas três oportunidades correspondem a 12 funcionalidades no total. Para MVP, vou classificar como Must apenas as indispensáveis para validar o modelo. As demais ficam como Should para fase 2.

Qual será o título? Sugiro 'Fase 1 — MVP' ou 'MVP — Fluxo Básico de Pedido'"

**Usuário:** "Fase 1 — MVP"

**Claude:** "E as hipóteses críticas do assumptions.md — quais precisam ser validadas no MVP?"

**Usuário:** "H1 (restaurantes vão aderir) e H3 (usuários preferem pedir pelo app)"

**Claude:** "Vou destacar essas hipóteses no escopo com plano de validação. 

Para métricas, do success-metrics.md a North Star é 'Pedidos completados por dia'. Para MVP, qual seria a meta mínima para considerar validado?"

**Usuário:** "Se tivermos 50 pedidos por dia em 1 mês, está validado"

**Claude:** *[Gera escopo de MVP com funcionalidades filtradas e foco em validação]*

> "Escopo **'Fase 1 — MVP'** criado!
>
> 📄 `docs/app-delivery/escopo/fase-1-mvp/escopo.md`
>
> **Características do MVP:**
> - 7 funcionalidades Must (mínimo viável)
> - 5 funcionalidades Should (fase 2)
> - 2 hipóteses críticas a validar
> - Meta de validação: 50 pedidos/dia em 30 dias
>
> Seção especial adicionada: 'Critérios de Validação do MVP' com go/no-go para fase 2."

### Resultado

- Escopo reduzido para MVP
- Funcionalidades priorizadas para validação rápida
- Critérios claros para decidir se avança para fase 2
- Hipóteses críticas em destaque

---

## Exemplo 4: Escopo que complementa outro existente

### Contexto
Escopo de integração com sistema externo, complementando escopo core já em execução.

### Conversa

**Usuário:** "Preciso criar o escopo da integração com o ERP"

**Claude:** "Encontrei o projeto 'sistema-vendas' com:
- **Escopo Core do Sistema** — Situação: Em execução
- **Módulo de Comissões** — Situação: Aprovado

A integração com ERP está listada como 'out of scope' no escopo core. Você quer criar um escopo separado para ela?"

**Usuário:** "Sim, vai rodar em paralelo com o core"

**Claude:** "Entendido. Preciso entender as fronteiras:

O escopo core menciona que 'dados de clientes virão de fonte manual'. A integração vai mudar isso?"

**Usuário:** "Sim, os dados vão vir do ERP automaticamente"

**Claude:** "Então há uma mudança no escopo core quando a integração ficar pronta. Vou documentar isso como dependência.

Quais dados serão integrados?"

**Usuário:** "Clientes, produtos e pedidos"

**Claude:** "E qual a direção? Só leitura do ERP ou vai enviar dados de volta?"

**Usuário:** "Bidirecional: lê clientes e produtos, envia pedidos confirmados"

**Claude:** *[Gera escopo de integração com fronteiras claras]*

> "Escopo **'Integração com ERP SAP'** criado!
>
> 📄 `docs/sistema-vendas/escopo/integracao-erp-sap/escopo.md`
>
> **Destaques:**
> - Fluxos de leitura: Clientes, Produtos (6 funcionalidades)
> - Fluxos de escrita: Pedidos confirmados (3 funcionalidades)
> - Dependência: Escopo Core deve estar em produção antes
> 
> **Seção especial:** 'Impacto em Escopos Existentes'
> - Escopo Core: Funcionalidade de cadastro manual de clientes será desativada
> - Módulo de Comissões: Dados de vendas virão da integração"

### Resultado

- Escopo de integração com fronteiras claras
- Dependências com outros escopos documentadas
- Impacto em escopos existentes explicitado

---

## Exemplo 5: Escopo sem discovery completo

### Contexto
Projeto urgente com discovery parcial. Apenas vision.md existe.

### Conversa

**Usuário:** "Preciso gerar o escopo do projeto de chat interno"

**Claude:** "Encontrei o projeto 'chat-interno' com apenas:
- vision.md ✓
- opportunity.md ✗
- assumptions.md ✗
- stakeholders.md ✗
- success-metrics.md ✗

O discovery está incompleto. Posso gerar o escopo, mas ficará superficial em relação a oportunidades, hipóteses e métricas.

Opções:
1. Conduzir discovery rápido agora (30-40 min)
2. Gerar escopo parcial e complementar depois
3. Gerar escopo coletando informações mínimas agora

Qual prefere?"

**Usuário:** "Opção 3, preciso do escopo hoje"

**Claude:** "Ok, vou coletar o mínimo necessário. 

**Stakeholders:** Quem precisa aprovar este escopo?"

**Usuário:** "O CTO e a gerente de RH"

**Claude:** "**Métricas:** Como vamos saber se o chat interno deu certo?"

**Usuário:** "Se 80% dos funcionários usarem em 30 dias"

**Claude:** "**Hipóteses críticas:** O que precisa ser verdade para isso funcionar?"

**Usuário:** "Que as pessoas larguem o WhatsApp pessoal para trabalho"

**Claude:** "Isso é uma hipótese de alto risco. Como validar?"

**Usuário:** "Podemos fazer uma pesquisa interna antes de lançar"

**Claude:** *[Gera escopo com informações coletadas na conversa]*

> "Escopo **'Chat Interno Corporativo'** criado!
>
> 📄 `docs/chat-interno/escopo/chat-interno-corporativo/escopo.md`
>
> ⚠️ **Atenção:** Discovery incompleto
> - Informações de stakeholders e métricas foram coletadas nesta conversa
> - Recomendo complementar o discovery posteriormente
> - Hipótese crítica identificada: migração do WhatsApp
>
> **Adicionado ao escopo:**
> - Seção 'Informações Coletadas Durante Geração' com registro do que foi discutido
> - Plano de validação para hipótese de migração do WhatsApp"

### Resultado

- Escopo gerado mesmo com discovery incompleto
- Informações coletadas na conversa documentadas
- Alerta sobre limitações do escopo
- Recomendação de complementar discovery

---

## Anti-exemplo: O que NÃO fazer

### Conversa problemática

**Usuário:** "Gera o escopo do projeto X"

**Claude:** ❌ *[Lê os documentos de discovery e gera escopo automaticamente sem interação]*

> "Escopo criado!
> 
> Incluí todas as 47 funcionalidades do opportunity.md como Must.
> Copiei todas as métricas do success-metrics.md.
> Todos os stakeholders do stakeholders.md precisam aprovar."

### Por que está errado

- Não perguntou sobre título e abrangência
- Não filtrou funcionalidades por relevância
- Não priorizou (tudo como Must)
- Não verificou escopos existentes
- Não solicitou confirmação antes de gerar
- Copiou mecanicamente sem curadoria

### Como deveria ser

**Claude:** ✅ "Encontrei o projeto X com discovery completo. Antes de gerar:
1. Qual será o título desse escopo?
2. Cobre o projeto inteiro ou uma parte específica?
3. Existe algum escopo anterior que devo considerar?"

---

## Checklist de qualidade da geração

Antes de finalizar a geração, verifique:

- [ ] Usuário confirmou título e abrangência
- [ ] Escopos existentes foram verificados
- [ ] Sobreposições foram tratadas
- [ ] Documentos relevantes foram filtrados (não copiou tudo cegamente)
- [ ] Funcionalidades foram priorizadas (MoSCoW)
- [ ] Usuário confirmou antes de gerar
- [ ] Pasta criada com nome em kebab-case
- [ ] Discovery copiado (não modificado)
- [ ] Escopo criado como Rascunho
- [ ] project.md foi atualizado
- [ ] Próximos passos foram comunicados
