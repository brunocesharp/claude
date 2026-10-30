---
name: direcao-arte-fundacao
description: >
  Conduz a fundação da direção de arte de um projeto digital, estabelecendo e documentando
  a identidade visual completa. Use quando o usuário mencionar "direção de arte", "identidade visual",
  "criar guia visual", "definir estilo visual", "briefing visual", "paleta de cores do projeto",
  "tipografia do projeto", "sistema visual", "pilares visuais", "style guide", "design system",
  "padrão visual", "linguagem visual", "visual identity" ou pedir para definir como o produto deve parecer.
  NÃO use para especificação de componentes individuais (use architecture-angular),
  nem para validação de acessibilidade/legibilidade (use direcao-arte-validacao).
metadata:
  version: 1.0.0
  category: design
  output: "{docs_root}/direcao-arte/fundacao.md"
---

# Direção de Arte — Fundação

Skill que conduz a fundação da identidade visual de um projeto digital, gerando `fundacao.md`.

Antes de iniciar, consulte os arquivos de referência:
- `references/guia-processo.md` — etapas, perguntas-chave e entregáveis por fase
- `references/template-mestre.md` — estrutura padrão do Sistema de Direção de Arte
- `references/fontes.md` — Poulin: Layout, Type, Language of Graphic Design

---

## Troubleshooting

Execute este gate antes de qualquer processamento.

**1.1 Pertinência** — A solicitação envolve decisões de identidade visual ou sistema visual do projeto? Se não, retorne **NÃO EXECUTAR** e identifique a skill adequada.

**1.2 Existência** — Verifique se `{docs_root}/direcao-arte/fundacao.md` já existe.
- Existe e está aprovado: pergunte se é revisão, atualização ou consulta — não sobrescreva silenciosamente.
- Existe como rascunho: ofereça continuar de onde parou.
- Não existe: prossiga normalmente.

**1.3 Pré-requisitos** — Leia `docs/project-config.json` e extraia `docs_root`, `name`, `project_type`, `tech_stack`. Se não existir, solicite as informações mínimas: nome do projeto, tipo e público-alvo.

**1.4 Estado:** EXECUTAR / NÃO EXECUTAR / BLOQUEADA (se não houver informações mínimas do projeto).

---

## Pré-requisito

Leia `docs/project-config.json` e extraia:
- `docs_root` (padrão: `"docs"`)
- `name` — nome do projeto
- `project_type` — tipo de produto (web-app, mobile, dashboard, etc.)
- `tech_stack` — tecnologia principal

Se `{docs_root}/direcao-arte/fundacao.md` já existir, leia-o completamente e extraia todas as decisões aprovadas. **Não repita perguntas já respondidas.**

---

## Fluxo de Execução

A arquitetura funcional precede qualquer escolha estética.
Nenhum bloco começa sem que o anterior esteja confirmado.

---

### Bloco 0 — Fundamentos do Projeto

Apresente o objetivo:

> "Vou conduzir a fundação da direção de arte de **{name}**. Trabalharemos em blocos temáticos — cada um tem perguntas e um entregável que precisa de aprovação antes de avançarmos.
>
> **Bloco 0: Fundamentos**
>
> 1. Qual é o conceito central do produto? (gênero, tom, público-alvo principal)
> 2. O que o produto **não** deve parecer? (referências visuais a evitar)
> 3. Quais fontes de projeto existem? (wireframes, briefings, documentos de marca)
> 4. Qual o escopo completo da direção de arte? (telas, componentes, documentação)"

Aguarde as respostas. Registre como **Briefing Consolidado** e confirme:

> "Briefing consolidado:
> - Conceito: {conceito}
> - Tom: {tom}
> - Público: {publico}
> - O que evitar: {evitar}
> - Escopo: {escopo}
>
> Correto? Podemos avançar?"

---

### Bloco 1 — Auditoria e Arquitetura Visual

> "**Bloco 1: Arquitetura Visual**
>
> 1. Quais sistemas funcionais a arte precisa preservar sem alterar? (navegação, estados, dados)
> 2. Qual a hierarquia de leitura? O que o usuário deve ver primeiro, segundo, terceiro?
> 3. Quais informações são críticas e **não podem depender só de cor**? (ex: status de erro, alertas)
> 4. Quais são os principais riscos de leitura? (baixo contraste, densidade, responsividade)
> 5. Qual o inventário de componentes? (listagem das telas/seções principais)"

Formalize a hierarquia funcional obrigatória:

```
FUNÇÃO → DIREÇÃO → ESTADO → IDENTIDADE → INTERAÇÃO → TEMA → DECORAÇÃO
```

Confirme com o usuário o **Mapa Visual Mestre** antes de avançar.

---

### Bloco 2 — Conceito e Direção de Arte

> "**Bloco 2: Conceito Visual**
>
> 1. **Formas:** O produto usa formas orgânicas ou geométricas? Suaves ou angulosas?
> 2. **Acabamento:** Flat, ilustrativo, fotográfico, minimalista, expressivo?
> 3. **Densidade:** Interface densa com muita informação ou arejada e espaçosa?
> 4. **Direção cromática:** Que personalidade as cores devem transmitir? (não é a paleta final — é a intenção: seriedade, energia, confiança, criatividade...)
> 5. **Caminhos excluídos:** Que estilos visuais estão explicitamente fora? Por quê?"

Confirme o **Styleframe Conceitual** (descrição textual aprovada) antes de avançar.

---

### Bloco 3 — Sistema Visual

> "**Bloco 3: Sistema Visual**
>
> Vou detalhar cada dimensão:"

**3.1 Paleta Cromática**

> "Quais as cores principais separadas por função?
> - Orientação (navegação, menus, localização)
> - Identidade (marca, destaque principal)
> - Correspondência (categorias, tipos de conteúdo)
> - Ação (CTAs, botões primários)
> - Estado (sucesso, erro, aviso, neutro)
>
> Para cada grupo: cor principal + variação clara + variação escura."

Regra: informação crítica nunca depende só de cor — exija redundância (ícone, forma, texto).

**3.2 Tipografia**

> "Defina as tipografias por função:
> - Display: títulos de alto impacto (uso decorativo, força visual)
> - Funcional: corpo de texto, interface, labels (legibilidade máxima)
>
> Para cada uma: família, peso(s) usados, tamanho base, line-height."

Consulte `references/fontes.md` — Poulin Design School Type para classificações e critérios.

**3.3 Grid e Composição**

> "Como o grid organiza o conteúdo?
> - Número de colunas (mobile / tablet / desktop)
> - Gutter e margem lateral
> - Unidade base de espaçamento (ex: 8px)
> - Proporções usadas (ex: razão áurea, regra dos terços)"

Consulte `references/fontes.md` — Poulin Design School Layout para sistemas proporcionais.

**3.4 Iconografia**

> "Como os ícones se comportam no sistema?
> - Estilo: outline, filled, duotone, custom?
> - Tamanhos padrão: 16, 20, 24, 32px?
> - Biblioteca base ou custom? (ex: Heroicons, Lucide, Material)
> - Regra de redundância: ícone acompanha sempre texto ou pode ser solo?"

**3.5 Estados e Interações**

> "Como os estados visuais são comunicados?
> - Hover, active, focus, disabled, loading
> - Animações: presentes? Duração padrão? (ex: 150ms ease)
> - Transições entre telas: fade, slide, nenhuma?"

Confirme o **Guia Visual v1** (decisões de sistema aprovadas) antes de fechar.

---

### Bloco 4 — Fechamento e Validação

Liste todas as decisões consolidadas e pergunte:

> "Cobrimos toda a fundação visual. Antes de gerar o documento:
> 1. Há algum componente ou tela com regra visual especial não mencionada?
> 2. Existe conflito entre alguma decisão tomada e o tech_stack ({tech_stack})?
> 3. Há restrição técnica que limita alguma escolha visual? (ex: biblioteca de componentes já instalada)"

---

## Gerar o Documento

Crie `{docs_root}/direcao-arte/fundacao.md` com a estrutura abaixo.

Se a pasta não existir, crie-a antes de escrever.

```markdown
# Direção de Arte — Fundação
**Projeto:** {name}
**Versão:** 1.0.0
**Data:** {data}
**Status:** rascunho | aprovado

---

## Briefing Consolidado
- **Conceito:** {conceito}
- **Tom:** {tom}
- **Público-alvo:** {publico}
- **Escopo:** {escopo}
- **O que evitar:** {evitar}

---

## Arquitetura Visual

### Hierarquia de Leitura
{hierarquia priorizada}

### Hierarquia Funcional
FUNÇÃO → DIREÇÃO → ESTADO → IDENTIDADE → INTERAÇÃO → TEMA → DECORAÇÃO

### Riscos Identificados e Respostas
| Risco | Resposta |
|-------|----------|
| {risco} | {resposta} |

### Inventário de Componentes
{lista de telas/seções}

---

## Conceito Visual
- **Formas:** {formas}
- **Acabamento:** {acabamento}
- **Densidade:** {densidade}
- **Direção cromática:** {intencao_cores}
- **Caminhos excluídos:** {exclusoes}

---

## Sistema Visual

### Paleta Cromática
| Função | Cor Principal | Clara | Escura |
|--------|--------------|-------|--------|
| Orientação | {cor} | {cor} | {cor} |
| Identidade | {cor} | {cor} | {cor} |
| Correspondência | {cor} | {cor} | {cor} |
| Ação | {cor} | {cor} | {cor} |
| Sucesso | {cor} | — | — |
| Erro | {cor} | — | — |
| Aviso | {cor} | — | — |
| Neutro | {cor} | {cor} | {cor} |

> Regra: informação crítica nunca depende exclusivamente de cor.

### Tipografia
| Função | Família | Pesos | Tamanho base | Line-height |
|--------|---------|-------|--------------|-------------|
| Display | {familia} | {pesos} | {tamanho} | {lh} |
| Funcional | {familia} | {pesos} | {tamanho} | {lh} |

### Grid e Composição
- **Colunas:** mobile {n} / tablet {n} / desktop {n}
- **Gutter:** {valor}
- **Margem lateral:** {valor}
- **Unidade base:** {valor}px
- **Proporções:** {sistemas usados}

### Iconografia
- **Estilo:** {estilo}
- **Tamanhos:** {tamanhos}
- **Biblioteca:** {biblioteca}
- **Regra de uso:** {regra redundancia}

### Estados e Interações
| Estado | Tratamento visual |
|--------|------------------|
| Hover | {descricao} |
| Active | {descricao} |
| Focus | {descricao} |
| Disabled | {descricao} |
| Loading | {descricao} |

- **Animações:** {presentes/ausentes}
- **Duração padrão:** {ms} {easing}

---

## Decisões Registradas
| # | Decisão | Alternativa descartada | Motivo |
|---|---------|----------------------|--------|
| D-01 | {decisao} | {alternativa} | {motivo} |

---

## Pontos em Aberto
| # | Questão | Responsável | Prazo |
|---|---------|-------------|-------|
| P-01 | {questao} | {responsavel} | {prazo} |
```

---

## Após Gerar o Documento

> "Documento salvo em `{docs_root}/direcao-arte/fundacao.md`.
>
> **Resumo:**
> - {N} dimensões visuais definidas
> - {N} decisões registradas
> - {N} pontos em aberto
>
> **Próximos passos:**
> - Criar componentes-piloto aplicando o sistema visual
> - Usar `architecture-angular` para gerar os componentes com o padrão definido aqui
> - Ao questionar qualquer decisão visual no projeto, consulte este documento primeiro"

---

## Regras de Decisão

- **Arquitetura funcional antes de estética:** função → legibilidade → consistência → tema → estética ornamental
- **Redundância obrigatória:** informação crítica nunca depende só de cor (exige ícone, forma ou texto)
- **Decisões aprovadas não são sobrescritas silenciosamente** — qualquer revisão exige confirmação explícita
- **Hipóteses não viram decisões aprovadas** — registre como "Ponto em Aberto" com responsável
- **Rastreabilidade:** toda decisão deve ter alternativa descartada e motivo registrado

---

## Critérios de Conclusão

- [ ] Briefing consolidado aprovado
- [ ] Hierarquia funcional definida e confirmada
- [ ] Conceito visual aprovado
- [ ] Paleta cromática com funções definidas
- [ ] Tipografias definidas com pesos e tamanhos
- [ ] Grid e composição especificados
- [ ] Iconografia especificada com regra de uso
- [ ] Estados e interações documentados
- [ ] Documento salvo em `{docs_root}/direcao-arte/fundacao.md`
- [ ] Pontos em aberto registrados com responsáveis

**CONCLUÍDA** — todos os critérios atendidos.
**CONCLUÍDA COM PENDÊNCIAS** — documento gerado com pontos em aberto registrados.
**NÃO CONCLUÍDA** — execução iniciada sem documento gerado.

---

## Handoff

Ao concluir, informe:

> "**Handoff — Fundação Visual**
>
> Artefato: `{docs_root}/direcao-arte/fundacao.md`
> Status: {CONCLUÍDA | CONCLUÍDA COM PENDÊNCIAS}
>
> Este documento é a referência autoritativa para todas as decisões visuais do projeto.
> Skills que o consomem: `architecture-angular` (geração de componentes), `direcao-arte-validacao` (validação de consistência).
>
> Restrição: não modifique decisões marcadas como 'aprovado' sem revisão explícita."

---

## Troubleshooting

**Usuário não sabe definir a direção cromática**
Ofereça referências de personalidade: "Seria algo como: confiança/seriedade (azuis, tons frios), energia/criatividade (laranjas, gradientes), sustentabilidade (verdes, terrosos), luxo (pretos, dourados)?"

**Usuário quer definir a paleta antes da hierarquia**
Redirecione: "Ótimo ponto — vamos garantir que a hierarquia funcional esteja clara primeiro, para que a paleta sirva a ela, não o contrário. Voltamos às cores no Bloco 3."

**Projeto já tem design system instalado (ex: Material, Tailwind, Shadcn)**
Adapte o Bloco 3: em vez de definir do zero, mapeie as decisões dentro das opções que o sistema permite. Registre como restrição herdada.

**Conflito entre decisão estética e tech_stack**
Registre como Ponto em Aberto com a questão: "Essa escolha é realizável com {tech_stack}? Confirme com o desenvolvedor antes de aprovar."
