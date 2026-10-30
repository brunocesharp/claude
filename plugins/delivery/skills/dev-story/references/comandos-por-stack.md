# Build e testes por stack

Use o que o repositório já define antes destes padrões: scripts do `package.json`, `Makefile`, `README`/`CLAUDE.md` do repositório, pipeline de CI (`.github/workflows`, `azure-pipelines.yml`). Os comandos abaixo são o padrão quando nada disso existe.

| Stack (arquivo na raiz) | Build | Testes de um alvo | Suíte completa |
|-------------------------|-------|-------------------|----------------|
| .NET (`*.sln`, `*.csproj`) | `dotnet build` | `dotnet test --filter "FullyQualifiedName~{Classe}"` | `dotnet test` |
| Angular (`angular.json`) | `npx ng build` | `npx ng test --watch=false --include="**/{arquivo}.spec.ts"` | `npx ng test --watch=false` |
| Node/TS (`package.json`) | `npm run build` (se existir) | `npx jest {arquivo}` / `npx vitest run {arquivo}` | `npm test` |
| Java Maven (`pom.xml`) | `mvn -q compile` | `mvn -q test -Dtest={Classe}` | `mvn -q verify` |
| Java Gradle (`build.gradle*`) | `./gradlew build -x test` | `./gradlew test --tests {Classe}` | `./gradlew test` |
| Python (`pyproject.toml`) | — | `pytest {arquivo}::{teste}` | `pytest` |

Regras:
- Rode os testes **sem modo watch** (`--watch=false`), para o comando terminar.
- Testes que precisam de serviço externo (banco, fila) e não sobem localmente: registre no Registro do desenvolvimento como "não executado: {motivo}" — nunca marque como passando.
- Lint/format do repositório (se houver script) rodam antes de mover para `review`.
- Angular em ambiente sem navegador: use o `--browsers=ChromeHeadless` se o projeto tiver o Karma configurado para isso.
