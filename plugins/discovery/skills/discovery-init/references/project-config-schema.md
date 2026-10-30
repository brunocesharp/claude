# Schema: docs/{projeto}/project-config.json

Configuração do projeto em formato estruturado. Criado pela skill `discovery-init` junto com o `project.md` e lido pelas demais skills no Passo 0, depois de identificar o projeto.

## Localização

Um arquivo por projeto, dentro da pasta do projeto no workspace de documentação:

```
docs/
├── workspace.md
├── projeto-a/
│   ├── project-config.json
│   └── project.md
└── projeto-b/
    ├── project-config.json
    └── project.md
```

O `project.md` é o resumo para pessoas (visão geral, status das fases); o `project-config.json` é para as skills (caminhos, stack, repositório). Os dois são criados juntos e devem ser mantidos coerentes.

---

## Campos

```json
{
  "name": "Nome do Projeto",
  "slug": "nome-do-projeto",
  "version": "1.0.0",
  "docs_root": "docs/nome-do-projeto",
  "repositories": "um",
  "repository_url": "https://github.com/org/repo",
  "code_path": "D:\\repos\\repo",
  "project_type": "web-api",
  "tech_stack": "dotnet",
  "responsible": "a definir",
  "created_at": "15/04/2026"
}
```

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `name` | string | Nome legível do projeto |
| `slug` | string | Nome da pasta do projeto em kebab-case (igual à pasta em `docs/`) |
| `version` | string | Versão do projeto (semver) |
| `docs_root` | string | Pasta de documentação do projeto: sempre `docs/{slug}` |
| `repositories` | `"um"` \| `"varios"` | `"varios"`: os repositórios estão em `docs/{slug}/repositorios.md` (skill `multi-repo`) e os dois campos seguintes ficam `"ver repositorios.md"` |
| `repository_url` | string | URL do repositório de código ou `"a definir"` |
| `code_path` | string | Caminho local do código nesta máquina ou `"a definir"` |
| `project_type` | string | Tipo do sistema: `web-api`, `web-app`, `mobile`, `integração`, `frontend`... |
| `tech_stack` | string | Tecnologia principal: `dotnet`, `angular`, `java`, `nodejs`, `python`... ou `"a definir"` |
| `responsible` | string | Responsável pelo projeto ou `"a definir"` |
| `created_at` | string | Data de criação no formato `DD/MM/YYYY` |

---

## Como as skills usam

1. Identificam o projeto pelo Passo 0 (projeto citado na conversa ou lista do `docs/workspace.md`).
2. Leem `docs/{projeto}/project-config.json`.
3. Usam `name` e `tech_stack` para personalizar perguntas e escolher skills de código; `repository_url`/`code_path` (ou o `repositorios.md`) para achar o código.
4. Se o arquivo não existir (projeto criado antes do config), seguem com o `project.md` e oferecem criar o config a partir dele.

---

## Evolução do arquivo

- `version`: incremente a cada entrega ou fase concluída
- `repository_url` e `code_path`: preencha quando disponíveis (substituindo `"a definir"`)
- `repositories`: muda para `"varios"` quando a skill `multi-repo` cadastra o segundo repositório
- `tech_stack`: preencha quando a tecnologia for definida (a `arch-c4` pode sugerir a partir dos contêineres)

O caminho local (`code_path`) varia por máquina. Se o workspace é compartilhado no Git, combine com o time uma pasta-mãe comum ou deixe cada pessoa ajustar o seu.
