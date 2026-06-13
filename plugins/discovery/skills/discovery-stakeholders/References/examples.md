# Exemplos de Uso — Discovery Stakeholders

Cenários detalhados de como usar a skill em diferentes situações.

---

## Exemplo 1: Projeto corporativo com múltiplas áreas

### Contexto
Sistema de gestão de contratos para empresa de médio porte. Envolve Jurídico, Comercial, Financeiro e TI.

### Conversa

**Usuário:** "Preciso mapear stakeholders do projeto de gestão de contratos"

**Claude:** "Vamos mapear todos os envolvidos. Começando pelo básico: quem solicitou esse projeto?"

**Usuário:** "O diretor jurídico, Dr. Mendes"

**Claude:** "Ele é o patrocinador então. E quem vai usar o sistema no dia a dia?"

**Usuário:** "Os advogados do jurídico e os vendedores que precisam ver status de contratos"

**Claude:** "Dois grupos de usuários com necessidades diferentes. Vamos detalhar: os advogados têm algum líder ou coordenador que os representa?"

**Usuário:** "Tem a Dra. Silva, coordenadora jurídica"

**Claude:** "E do lado comercial, quem representa os vendedores?"

**Usuário:** "O gerente comercial, Carlos"

**Claude:** "Ótimo. Agora áreas que não usam mas são afetadas: o financeiro vai precisar de dados desse sistema? TI vai dar suporte?"

**Usuário:** "Sim, financeiro precisa dos dados para faturamento, e TI vai integrar com o ERP"

**Claude:** "Então temos stakeholders no financeiro e TI também. Quem são os pontos focais lá?"

**Usuário:** "Marina é a gerente financeira, e Pedro é o coordenador de TI"

**Claude:** "Agora vamos classificar. Dr. Mendes como patrocinador tem alta influência e provavelmente alto interesse. Você diria que ele está muito envolvido ou delega?"

**Usuário:** "Muito envolvido, ele mesmo solicitou por causa de um problema grave em um contrato"

**Claude:** "Então é 'Engajar Ativamente'. E a Dra. Silva?"

**Usuário:** "Ela que vai sofrer se não funcionar, então muito interessada, e tem autonomia no jurídico"

**Claude:** "Alta influência + Alto interesse = Engajar também. E o Carlos do comercial?"

**Usuário:** "Ele quer o sistema mas não vai brigar muito se atrasar. Interesse médio, influência baixa"

**Claude:** "Manter Informado então. E financeiro e TI?"

**Usuário:** "Marina precisa dos dados, vai reclamar se não tiver. Pedro só quer que a integração não dê problema"

**Claude:** "Marina: alto interesse, influência média — vou colocar como Manter Informado com atenção extra. Pedro: baixo interesse, média influência — Manter Satisfeito para garantir a integração."

### Resultado

Documento com:
- 6 stakeholders mapeados
- 2 críticos (Dr. Mendes, Dra. Silva)
- Matriz de comunicação diferenciada por área
- Identificação de possível tensão: Comercial pode se sentir menos prioritário

---

## Exemplo 2: Startup com poucos stakeholders mas críticos

### Contexto
Startup de 15 pessoas desenvolvendo novo produto. Fundadores muito envolvidos.

### Conversa

**Usuário:** "Somos uma startup pequena, acho que não temos muitos stakeholders"

**Claude:** "Em startups, cada pessoa costuma ter múltiplos papéis. Vamos mapear quem está envolvido no projeto. Quem decidiu que esse projeto é prioridade?"

**Usuário:** "Os dois fundadores, João e Maria"

**Claude:** "Eles são co-patrocinadores. Têm visões alinhadas ou diferentes?"

**Usuário:** "João foca no produto, Maria no comercial. Às vezes divergem"

**Claude:** "Isso é importante — potencial conflito entre stakeholders críticos. Quem desempata quando divergem?"

**Usuário:** "Geralmente o João, mas a Maria tem maioria societária"

**Claude:** "Interessante dinâmica. Vou registrar os dois como 'Engajar Ativamente' com nota sobre possível divergência. Quem mais?"

**Usuário:** "Tem o CTO, Ricardo, que vai implementar"

**Claude:** "Ricardo tem alta influência técnica e provavelmente alto interesse. Engajar também. Investidores acompanham o projeto?"

**Usuário:** "Temos um investidor anjo, Carlos, que pergunta todo mês sobre progresso"

**Claude:** "Carlos: alta influência (pode afetar próxima rodada), interesse médio (acompanha mas não no dia a dia). Manter Satisfeito — comunicação executiva mensal. Mais alguém?"

**Usuário:** "Os 5 desenvolvedores que vão construir"

**Claude:** "Eles são stakeholders de alto interesse mas baixa influência individual. Vou tratar como grupo 'Time de Desenvolvimento'. Quem os representa?"

**Usuário:** "O Ricardo mesmo"

**Claude:** "Então o Ricardo acumula: stakeholder individual E representante do time. Vou destacar isso. Clientes atuais serão afetados?"

**Usuário:** "Sim, temos 10 clientes que vão receber a nova feature"

**Claude:** "Clientes: alto interesse, podem ter influência indireta (churn, feedback negativo). Sugiro identificar 2-3 clientes-chave para acompanhar de perto."

### Resultado

Documento com:
- 5 stakeholders (2 fundadores, CTO, investidor, clientes-chave)
- Alerta sobre dinâmica João vs Maria
- Ricardo com papel duplo destacado
- Recomendação de identificar clientes-chave para beta

---

## Exemplo 3: Projeto com stakeholders externos

### Contexto
Integração com sistema de parceiro de negócios. Envolve stakeholders de duas empresas.

### Conversa

**Usuário:** "Vamos integrar com o sistema da empresa parceira TechCorp"

**Claude:** "Projetos com stakeholders externos têm complexidade adicional. Vamos mapear os dois lados. Internamente, quem patrocina?"

**Usuário:** "Nossa diretora de operações, Ana"

**Claude:** "E do lado da TechCorp, quem é o ponto focal?"

**Usuário:** "O gerente de parcerias deles, Bruno"

**Claude:** "Bruno tem poder de decisão ou precisa escalar?"

**Usuário:** "Para coisas técnicas ele decide, para contrato precisa da diretoria"

**Claude:** "Então Bruno é influência média — importante para o dia a dia mas não para decisões críticas. Quem na diretoria da TechCorp devemos mapear?"

**Usuário:** "Não sei, não temos contato direto"

**Claude:** "Isso é um risco. Stakeholder com poder que não conhecemos. Sugiro: peça ao Bruno para nos apresentar ou pelo menos saber quem é. Tecnicamente, quem do lado deles vai trabalhar na integração?"

**Usuário:** "Eles têm um time de APIs, mas não sei nomes"

**Claude:** "Outro ponto a investigar. Vou registrar como 'Time de APIs TechCorp — a mapear'. E do nosso lado técnico?"

**Usuário:** "Nosso arquiteto, Carlos, e dois desenvolvedores"

**Claude:** "Carlos é stakeholder técnico crítico — alta influência no 'como', alto interesse porque vai implementar. E há algum contrato ou SLA envolvido?"

**Usuário:** "Sim, o jurídico das duas empresas precisa aprovar termos"

**Claude:** "Stakeholders jurídicos dos dois lados. Geralmente alta influência (podem bloquear), baixo interesse (só querem aprovar e seguir). Manter Satisfeitos — comunicação clara sobre o que precisam revisar."

### Resultado

Documento com:
- Stakeholders mapeados por empresa (internos vs TechCorp)
- Alerta sobre stakeholders desconhecidos na TechCorp
- Plano de ação: identificar contatos faltantes
- Matriz de comunicação considerando duas organizações

---

## Exemplo 4: Situação com patrocinador fraco

### Contexto
Projeto de modernização de sistema legado. Patrocinador nominal não demonstra interesse.

### Conversa

**Usuário:** "Nosso patrocinador é o diretor de TI, mas ele mal responde emails"

**Claude:** "Patrocinador desengajado é um risco sério. Vamos entender melhor: ele foi designado ou se voluntariou?"

**Usuário:** "Foi designado pelo CEO porque o projeto é de TI"

**Claude:** "Isso explica. Ele não 'comprou' o projeto. Ele tem outras prioridades que competem?"

**Usuário:** "Sim, ele está tocando uma migração de datacenter que é prioridade"

**Claude:** "Então o projeto é secundário para ele. Algumas opções: 1) Encontrar um proxy que possa decidir no dia a dia; 2) Engajar um stakeholder de negócio que tenha interesse; 3) Escalar para o CEO. Qual parece mais viável?"

**Usuário:** "Ele tem uma gerente, Paula, que responde mais rápido"

**Claude:** "Paula pode ser a proxy operacional. Mas ela tem autonomia para decidir ou só executa?"

**Usuário:** "Ela pode decidir coisas operacionais, mas escopo e orçamento são com ele"

**Claude:** "Então vou mapear: Diretor de TI como sponsor formal (Manter Satisfeito — comunicação mínima, só decisões críticas), Paula como proxy operacional (Engajar Ativamente — ela que vai destrancar o dia a dia). Existe algum stakeholder de negócio que realmente PRECISA desse sistema?"

**Usuário:** "A gerente de operações, Carla, reclama todo dia do sistema atual"

**Claude:** "Carla pode ser uma co-patrocinadora informal. Alto interesse, pode ter influência indireta. Se ela pressionar o CEO, o projeto ganha prioridade. Sugiro engajá-la como aliada."

### Resultado

Documento com:
- Patrocinador formal mapeado mas com nota de baixo engajamento
- Paula como proxy operacional — stakeholder chave real
- Carla como potencial aliada/co-patrocinadora
- Plano de contingência: escalar para CEO se decisões críticas travarem

---

## Exemplo 5: Projeto com histórico de conflitos

### Contexto
Substituição de sistema em área que já teve projeto fracassado há 2 anos.

### Conversa

**Usuário:** "Vamos refazer um projeto que fracassou antes. O clima está tenso"

**Claude:** "Projetos com histórico negativo têm stakeholders 'marcados'. Vamos entender quem foi afetado. O que aconteceu no projeto anterior?"

**Usuário:** "Gastaram 6 meses, não entregou, culparam o time de TI"

**Claude:** "Então TI é stakeholder com trauma. Eles vão ser resistentes ou defensivos. Quem de TI esteve envolvido e ainda está na empresa?"

**Usuário:** "O gerente de desenvolvimento, Roberto. Ele 'levou a culpa'"

**Claude:** "Roberto é stakeholder crítico por razões emocionais, não só funcionais. Ele precisa ser reconquistado. Se ele não comprar o projeto, vai sabotar — consciente ou inconscientemente. Qual a melhor forma de engajá-lo?"

**Usuário:** "Ele é técnico, gosta de ser consultado"

**Claude:** "Sugiro: envolva-o nas decisões técnicas desde o início. Peça a opinião dele sobre o que deu errado antes. Faça sentir que dessa vez será diferente. E do lado de negócio, quem patrocinou o projeto anterior?"

**Usuário:** "O diretor comercial, que foi trocado. Agora é outro"

**Claude:** "Novo diretor pode ser aliado — não carrega o peso do fracasso. Mas ele sabe do histórico?"

**Usuário:** "Provavelmente ouviu fofocas"

**Claude:** "Sugiro uma conversa franca com ele sobre o que aconteceu e por que dessa vez será diferente. Antecipe-se às fofocas. Mais alguém marcado pelo projeto anterior?"

**Usuário:** "Os usuários foram prometidos um sistema e nunca chegou. Estão céticos"

**Claude:** "Ceticismo dos usuários. Eles são 'Manter Informado' mas com comunicação especial — precisa ser honesta, sem promessas exageradas, com marcos visíveis para reconstruir confiança."

### Resultado

Documento com:
- Mapa normal + seção especial "Histórico e Dinâmicas"
- Roberto como stakeholder de recuperação crítica
- Plano de comunicação especial para usuários céticos
- Estratégia de "fresh start" com novo diretor

---

## Anti-exemplo: O que NÃO fazer

### Conversa problemática

**Usuário:** "Preciso mapear stakeholders"

**Claude:** ❌ "Ok! Os stakeholders típicos de um projeto são:
1. Patrocinador
2. Usuários
3. Time técnico
4. Gerente de projeto

Pronto, está mapeado!"

### Por que está errado

- Usou lista genérica em vez de perguntar sobre o projeto específico
- Não classificou por influência e interesse
- Não explorou relacionamentos ou conflitos
- Não criou estratégia de engajamento
- Não identificou nomes ou papéis reais

### Como deveria ser

**Claude:** ✅ "Para mapear bem, preciso entender o contexto. Me conta: quem solicitou ou patrocina esse projeto?"

---

## Checklist de qualidade do documento

Antes de finalizar o `stakeholders.md`, verifique:

- [ ] Pelo menos 5-7 stakeholders identificados
- [ ] Todos classificados por influência e interesse
- [ ] Pelo menos 1 stakeholder por quadrante (ou justificativa)
- [ ] Stakeholders críticos têm detalhamento completo
- [ ] Matriz de comunicação com canal e frequência
- [ ] Responsável definido para stakeholders de alta influência
- [ ] Conflitos ou tensões identificados (se houver)
- [ ] Linguagem neutra e profissional
- [ ] Plano de ação imediato com próximos passos
