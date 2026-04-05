# Template: opportunity.md

Use este template para gerar o documento de mapeamento de oportunidades.

Salve em: `docs/{nome-do-projeto}/discovery/opportunity.md`

---

## Template

```markdown
# Mapeamento de Oportunidades — {Nome do Projeto}

> Gerado em: {data no formato DD/MM/YYYY}
> Versão: 1.0

---

## Jobs to Be Done

> O que os usuários estão tentando realizar ao usar esse sistema?

| Perfil | Job Principal | Situação de Uso | Critério de Sucesso |
|--------|---------------|-----------------|---------------------|
| {perfil 1} | {job} | {quando/onde ocorre} | {como sabe que completou} |
| {perfil 2} | {job} | {quando/onde ocorre} | {como sabe que completou} |

### Jobs Secundários

{Liste jobs menos frequentes mas relevantes, se houver}

---

## Dores e Fricções

### Dores Críticas

> Problemas de alto impacto que precisam ser resolvidos.

| # | Dor | Perfis Afetados | Frequência | Impacto |
|---|-----|-----------------|------------|---------|
| 1 | {descrição da dor} | {perfis} | {diária/semanal/eventual} | {alto/médio} |
| 2 | {descrição da dor} | {perfis} | {frequência} | {impacto} |

### Dores Secundárias

> Problemas menores mas que valem atenção.

| # | Dor | Perfis Afetados | Frequência | Impacto |
|---|-----|-----------------|------------|---------|
| 1 | {descrição} | {perfis} | {frequência} | {baixo/médio} |

---

## Desejos e Ganhos Esperados

> O que o usuário espera ganhar além da resolução das dores.

| Tipo | Desejo | Perfis | Por que importa |
|------|--------|--------|-----------------|
| Funcional | {o que quer fazer} | {perfis} | {benefício} |
| Emocional | {como quer se sentir} | {perfis} | {benefício} |
| Social | {como quer ser visto} | {perfis} | {benefício} |

---

## Contexto de Uso

| Aspecto | Descrição |
|---------|-----------|
| **Frequência** | {diário / semanal / pontual / variável} |
| **Ambiente** | {escritório / campo / home office / misto} |
| **Dispositivo principal** | {desktop / mobile / ambos} |
| **Conectividade** | {sempre online / offline frequente / variável} |
| **Pressão de tempo** | {alta / média / baixa / depende do contexto} |
| **Interrupções** | {frequentes / raras / contexto específico} |

### Observações sobre o contexto

{Outros aspectos relevantes do contexto de uso}

---

## Tentativas Anteriores

| Solução Tentada | Tipo | Por Que Não Funcionou | Aprendizado |
|-----------------|------|----------------------|-------------|
| {nome/descrição} | {interna/mercado/workaround} | {motivo da falha} | {o que aprendemos} |
| {nome/descrição} | {tipo} | {motivo} | {aprendizado} |

### Workarounds Atuais

{Descreva soluções improvisadas que os usuários usam hoje, se houver}

---

## Mapa de Oportunidades

> Oportunidades são lacunas entre o que o usuário precisa e o que existe hoje.

| # | Oportunidade | Jobs Relacionados | Dores Endereçadas | Frequência | Impacto | Prioridade |
|---|--------------|-------------------|-------------------|------------|---------|------------|
| 1 | {descrição} | {jobs} | {dores #} | {freq} | {alto/médio/baixo} | {A/B/C} |
| 2 | {descrição} | {jobs} | {dores #} | {freq} | {impacto} | {prioridade} |
| 3 | {descrição} | {jobs} | {dores #} | {freq} | {impacto} | {prioridade} |

### Legenda de Prioridade

- **A** = Alta frequência + Alto impacto → resolver primeiro
- **B** = Alta frequência OU alto impacto → considerar no roadmap
- **C** = Baixa frequência + Baixo impacto → avaliar depois ou descartar

---

## Pontos a Investigar

> Itens que precisam de validação com usuários reais ou mais pesquisa.

| # | Ponto | Como Validar | Responsável | Prazo |
|---|-------|--------------|-------------|-------|
| 1 | {descrição do ponto incerto} | {método sugerido} | {a definir} | {a definir} |
| 2 | {descrição} | {método} | {responsável} | {prazo} |

---

## Ideias de Solução (para depois)

> Funcionalidades ou soluções mencionadas durante o mapeamento. NÃO são o foco desta fase.

| Ideia | Oportunidade Relacionada | Origem |
|-------|-------------------------|--------|
| {funcionalidade sugerida} | {oportunidade #} | {quem sugeriu} |

---

## Próximos Passos Recomendados

Com base neste mapeamento, sugerimos:

1. **Validar pontos incertos** — priorizar investigação dos itens marcados
2. **Priorizar oportunidades A** — foco nas de maior impacto e frequência  
3. **Continuar discovery:**
   - [ ] Hipóteses — transformar oportunidades em hipóteses testáveis
   - [ ] Stakeholders — mapear quem influencia essas oportunidades
   - [ ] Métricas — definir como medir sucesso

---

## Histórico de Versões

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | {data} | Versão inicial |
```

---

## Instruções de Uso

### Campos obrigatórios

- Jobs to Be Done (pelo menos 1)
- Dores críticas (pelo menos 1)
- Contexto de uso
- Mapa de oportunidades (pelo menos 1)

### Campos opcionais

- Jobs secundários
- Dores secundárias
- Tentativas anteriores (se não houver, indicar)
- Pontos a investigar
- Ideias de solução

### Quando marcar como "a definir" ou "a investigar"

- Usuário não soube responder com certeza
- Informação baseada em suposição, não observação
- Precisa de validação com usuários reais
- Dado conflitante ou ambíguo

### Priorização de oportunidades

Use a matriz:

```
                    IMPACTO
                 Baixo    Alto
           ┌─────────┬─────────┐
    Alta   │    B    │    A    │
FREQUÊNCIA ├─────────┼─────────┤
    Baixa  │    C    │    B    │
           └─────────┴─────────┘
```

- **A** = Fazer primeiro
- **B** = Considerar
- **C** = Avaliar depois
