# Schema: docs/project-config.json

Arquivo de configuração central do projeto. Criado pela skill `discovery-init` e lido por todas as demais skills para resolver caminhos e obter contexto do projeto.

## Localização

Sempre em `docs/project-config.json` a partir da **raiz do projeto** (diretório onde o usuário executa as skills).

- **Setup git**: raiz do repositório clonado
- **Setup local**: dentro da pasta `{slug}/` criada por discovery-init

> Regra: execute sempre as skills a partir da pasta que contém `docs/`.

---

## Campos

```json
{
  "name": "Nome do Projeto",
  "slug": "nome-do-projeto",
  "version": "1.0.0",
  "setup": "git",
  "docs_root": "docs",
  "repository_url": "https://github.com/org/repo",
  "project_type": "web-api",
  "tech_stack": "dotnet",
  "responsible": "a definir",
  "created_at": "15/04/2026"
}
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | string | Nome legível do projeto |
| `slug` | string | Nome em kebab-case (usado como nome de pasta em setup local) |
| `version` | string | Versão do projeto (semver) |
| `setup` | `"git"` \| `"local"` | `"git"` — repositório Git existe; `"local"` — sem repositório ainda |
| `docs_root` | string | Pasta raiz de documentação. Padrão: `"docs"`. Altere se quiser usar outro nome |
| `repository_url` | string | URL do repositório Git ou `"a definir"` |
| `project_type` | string | Tipo do sistema: `web-api`, `mobile`, `integração`, `frontend`, etc. |
| `tech_stack` | string | Tecnologia principal: `dotnet`, `nodejs`, `python`, `java`, etc. |
| `responsible` | string | Responsável pelo projeto ou `"a definir"` |
| `created_at` | string | Data de criação no formato `DD/MM/YYYY` |

---

## Como usar em outras skills

Ao iniciar qualquer skill, leia `docs/project-config.json`:

```
1. Leia docs/project-config.json
2. Extraia docs_root (padrão: "docs" se o campo não existir)
3. Use {docs_root} como prefixo em todos os caminhos de documentação
```

Exemplos de caminhos derivados:

| Documento | Caminho |
|-----------|---------|
| project.md | `{docs_root}/project.md` |
| vision.md | `{docs_root}/discovery/vision.md` |
| opportunity.md | `{docs_root}/discovery/opportunity.md` |
| assumptions.md | `{docs_root}/discovery/assumptions.md` |
| stakeholders.md | `{docs_root}/discovery/stakeholders.md` |
| success-metrics.md | `{docs_root}/discovery/success-metrics.md` |
| escopo.md | `{docs_root}/escopo/{titulo-kebab}/escopo.md` |
| spec-functional.md | `{docs_root}/especificacao/{escopo}/spec-functional.md` |

---

## Evolução do arquivo

O `project-config.json` pode ser atualizado manualmente ou por skills ao longo do projeto:

- `version` — incremente a cada entrega ou fase concluída
- `setup` — pode mudar de `"local"` para `"git"` quando o repositório for criado
- `repository_url` — preencha quando disponível (substituindo `"a definir"`)
- `tech_stack` — preencha quando a tecnologia for definida
