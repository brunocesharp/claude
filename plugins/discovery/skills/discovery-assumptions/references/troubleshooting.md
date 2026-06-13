# Troubleshooting — Discovery Assumptions

Problemas comuns durante o mapeamento de hipóteses e como resolvê-los.

---

## Problema: Usuário confunde hipótese com fato

### Sintoma
Usuário apresenta suposições como certezas:
- "Os usuários querem isso"
- "Sabemos que funciona"
- "Todo mundo faz assim"

### Causa
Viés de confirmação — tendemos a tratar nossas crenças como fatos, especialmente quando investimos emocionalmente na ideia.

### Solução

1. **Peça a evidência:**
   > "Qual foi a última vez que você viu isso acontecer? Quantas vezes?"

2. **Separe crença de dado:**
   > "Isso é algo que você observou diretamente ou é uma suposição baseada em experiência?"

3. **Use a técnica do advogado do diabo:**
   > "Se alguém quisesse provar que isso está errado, que argumento usaria?"

4. **Registre com ressalva:**
   - Se não houver evidência, registre como hipótese de baixa certeza
   - Anote: "Baseado em percepção da equipe, sem validação formal"

---

## Problema: Todas as hipóteses parecem "óbvias"

### Sintoma
Usuário resiste a listar hipóteses:
- "Isso é óbvio, não precisa validar"
- "Todo mundo sabe"
- "É senso comum"

### Causa
- Viés do especialista (curse of knowledge)
- Medo de parecer inseguro
- Pressão para parecer que sabe o que está fazendo

### Solução

1. **Mostre exemplos de "óbvios" que falharam:**
   > "Muitos produtos falharam porque assumiram coisas 'óbvias'. O Segway era 'obviamente' revolucionário. O Google+ era 'obviamente' melhor que o Facebook."

2. **Faça a pergunta do impacto:**
   > "Mesmo que seja óbvio, se estiver errado, o que acontece com o projeto?"

3. **Transforme em hipótese testável:**
   > "Ok, é óbvio. Então deve ser fácil validar rapidamente. Qual seria a evidência que provaria isso?"

4. **Use a técnica do alienígena:**
   > "Se alguém que nunca viu esse mercado perguntasse 'por que você acredita nisso?', o que você diria?"

---

## Problema: Usuário não consegue pensar em hipóteses

### Sintoma
- "Não temos hipóteses"
- "Já sabemos tudo que precisamos"
- Silêncio prolongado quando perguntado

### Causa
- Falta de prática em pensar em incertezas
- Documentos anteriores (vision.md, opportunity.md) não foram feitos
- Projeto muito inicial ou muito maduro

### Solução

1. **Extraia de documentos anteriores:**
   > "No vision.md vocês disseram que o público é X. Qual a evidência de que X realmente tem esse problema?"

2. **Use categorias como gatilho:**
   > "Vamos por partes: sobre os USUÁRIOS, o que estamos assumindo? Sobre a TECNOLOGIA? Sobre o NEGÓCIO?"

3. **Inverta a pergunta:**
   > "O que precisaria ser verdade para esse projeto dar certo?"

4. **Liste hipóteses comuns e pergunte:**
   > "Vocês estão assumindo que:
   > - Usuários vão adotar a ferramenta?
   > - A integração com X funciona?
   > - O mercado é grande o suficiente?
   > Alguma dessas se aplica?"

5. **Use o exercício do "pré-mortem":**
   > "Imagine que é daqui a um ano e o projeto fracassou. O que aconteceu? Qual foi a causa?"

---

## Problema: Hipóteses muito vagas

### Sintoma
Hipóteses formuladas de forma genérica:
- "Vai dar certo"
- "Os usuários vão gostar"
- "É viável tecnicamente"

### Causa
Falta de especificidade ou medo de se comprometer com algo mensurável.

### Solução

1. **Peça para quantificar:**
   > "'Usuários vão gostar' — quantos? O que significa 'gostar'? Como vamos medir?"

2. **Use a fórmula de hipótese testável:**
   ```
   Acreditamos que [público específico]
   vai [comportamento específico]
   porque [razão]
   Saberemos que estamos certos quando [métrica mensurável]
   ```

3. **Dê exemplos de hipóteses bem formuladas:**
   > "Em vez de 'usuários vão adotar', tente: 'Vendedores do time comercial vão registrar pelo menos 80% das visitas no mesmo dia usando o app, porque é mais rápido que o processo atual de email'"

4. **Pergunte o critério de sucesso:**
   > "Se formos validar isso, o que precisa acontecer para você dizer 'confirmado'?"

---

## Problema: Conflito sobre certeza

### Sintoma
Stakeholders discordam sobre o nível de certeza:
- "Eu tenho certeza, você que não"
- "Isso é fato, não hipótese"
- Debates improdutivos

### Causa
- Diferentes níveis de experiência com o problema
- Informações assimétricas
- Ego ou política

### Solução

1. **Separe percepção de evidência:**
   > "Vocês dois têm perspectivas válidas. Vamos separar: qual é a EVIDÊNCIA concreta que cada um tem?"

2. **Use votação de confiança:**
   > "De 1 a 10, qual a confiança de cada um? Se houver diferença grande, vale investigar por quê."

3. **Documente ambas as visões:**
   > "Vou registrar que há divergência sobre essa hipótese. Isso por si só já indica que vale validar."

4. **Proponha validação rápida:**
   > "A melhor forma de resolver é testar. Qual seria o experimento mais rápido para tirar a dúvida?"

---

## Problema: Hipóteses técnicas ignoradas

### Sintoma
- Foco apenas em hipóteses de usuário/negócio
- "A parte técnica a gente resolve"
- Dev team ausente da discussão

### Causa
- Discovery feito apenas por PMs/negócio
- Confiança excessiva na capacidade técnica
- Falta de integração entre times

### Solução

1. **Inclua dev na conversa:**
   > "Para mapear hipóteses técnicas completas, seria bom ter alguém do time de engenharia. Podemos incluir?"

2. **Use perguntas específicas:**
   > - "Existe alguma integração com sistema externo?"
   > - "Estamos assumindo alguma performance ou escala específica?"
   > - "Tem alguma tecnologia nova que o time nunca usou?"
   > - "Existe dependência de terceiros (API, fornecedor, parceiro)?"

3. **Lembre de dívidas técnicas:**
   > "O sistema atual tem alguma limitação que pode afetar esse projeto?"

4. **Pergunte sobre o não-funcional:**
   > "E quanto a segurança, performance, disponibilidade? Estamos assumindo algo?"

---

## Problema: Muitas hipóteses críticas

### Sintoma
- Tudo é "alto impacto + baixa certeza"
- Lista enorme de coisas a validar
- Paralisia por excesso

### Causa
- Falta de priorização relativa
- Aversão a risco excessiva
- Projeto realmente muito arriscado

### Solução

1. **Force ranking:**
   > "Se só pudéssemos validar UMA hipótese antes de começar, qual seria?"

2. **Agrupe hipóteses relacionadas:**
   > "Essas três hipóteses são sobre o mesmo tema. Podemos validar juntas com um experimento?"

3. **Questione o impacto:**
   > "Se essa hipótese estiver errada, o projeto falha completamente ou só precisa de ajuste?"

4. **Separe por fase:**
   > "Quais hipóteses precisam ser validadas ANTES de começar? Quais podem ser validadas DURANTE o desenvolvimento?"

5. **Aceite algum risco:**
   > "Todo projeto tem risco. A questão é: qual risco estamos dispostos a correr?"

---

## Problema: Stakeholder quer pular validações

### Sintoma
- "Não temos tempo para isso"
- "Vamos construir e ver o que acontece"
- Pressão para ir direto ao desenvolvimento

### Causa
- Pressão de prazo
- Cultura de "fazer primeiro, pensar depois"
- Desconhecimento do custo de errar

### Solução

1. **Mostre o custo de estar errado:**
   > "Se construirmos e essa hipótese estiver errada, perdemos X meses e Y reais. A validação custaria Z dias. Qual é o melhor investimento?"

2. **Proponha validação mínima:**
   > "Entendo a pressa. Qual seria a validação mais rápida possível? 3 entrevistas de 30 minutos? Um spike de 2 dias?"

3. **Documente a decisão:**
   > "Ok, vamos seguir sem validar essa hipótese. Vou registrar que é uma decisão consciente de aceitar o risco."

4. **Sugira validação em paralelo:**
   > "Podemos começar o desenvolvimento E validar ao mesmo tempo. Se a hipótese falhar cedo, ajustamos rápido."
