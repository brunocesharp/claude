# Levantamento a partir do código (modo Levantamento)

Para sistemas existentes. O objetivo é que o diagrama reflita o código, e não a memória do time. Tudo que for encontrado é **confirmado com o usuário** antes de entrar no documento.

O código fica no caminho de **Código local** do `docs/{projeto}/project.md`. Se estiver `a definir`, pergunte onde está e registre.

**Código em vários repositórios:** os caminhos estão em `docs/{projeto}/repositorios.md` (skill `multi-repo`). Faça o levantamento em cada repositório e:
- some os contêineres de todos; as chamadas entre repositórios (URL da API no `environment.ts` do front, cliente HTTP, filas) são as relações entre contêineres;
- na evidência de cada elemento, cite o repositório (`opbh-api: src/X.API/X.API.csproj`);
- no mapeamento componente → código, use `{repositório}/{pasta}`;
- se um contêiner não tem repositório no cadastro, ou um repositório não implementa nenhum contêiner, registre em Pontos em aberto e ofereça atualizar a coluna Contêineres C4 do `repositorios.md`.

---

## 1. Pessoas e sistemas externos (contexto)

| Onde procurar | O que indica |
|---------------|--------------|
| Perfis/roles de autorização, guards de rota, menus por perfil | Tipos de usuário (pessoas) |
| `appsettings*.json`, `.env.example`, `environment*.ts` | URLs e chaves de serviços externos (e-mail, pagamento, armazenamento, APIs de terceiros) |
| Clientes HTTP, adapters, gateways (`HttpClient`, `IHttpClientFactory`, SDKs `AWSSDK.*`, `Stripe`, `SendGrid`...) | Integrações com sistemas externos |
| SMTP, filas e webhooks recebidos | Sistemas que enviam ou recebem dados |
| Discovery do projeto (`vision.md`, `stakeholders.md`) | Perfis de usuário |

## 2. Contêineres

| Onde procurar | O que indica |
|---------------|--------------|
| `docker-compose*.yml` | Serviços em execução: cada serviço próprio é candidato a contêiner; imagens de banco, cache e fila são contêineres de dados |
| `Dockerfile*` | Unidades implantáveis |
| `*.sln` + `*.csproj` com `Sdk="Microsoft.NET.Sdk.Web"` ou `OutputType Exe` | Aplicações .NET executáveis (API, worker, console). Projetos `classlib` **não** são contêineres |
| `angular.json`, `package.json` com build de app, `vite.config.*`, `next.config.*` | Aplicações front-end (SPA rodando no navegador) |
| `Program.cs` com `AddHostedService`/`BackgroundService` | Processamento em segundo plano (pode ser componente da API, se roda no mesmo processo) |
| Connection strings e `DbContext` | Bancos e schemas (um schema = um contêiner) |
| Redis, RabbitMQ, Kafka, buckets S3/R2 | Cache, filas e armazenamento como contêineres |
| Pasta de arquivos com dados de negócio (uploads, dumps) | Contêiner "Sistema de arquivos" |
| MCP servers, CLIs, ferramentas de importação | Contêineres próprios, se o time os executa como parte do sistema |

Para cada contêiner, anote: nome, tecnologia com versão (do `csproj`, `package.json`, imagem Docker), responsabilidades (das pastas e do README) e com quem se comunica (URLs, connection strings, chamadas HTTP).

**Cuidados:**
- Um `BackgroundService` dentro da API roda no mesmo processo: é componente da API, não contêiner separado.
- Proxy reverso (nginx) que só serve estáticos e repassa requisições: aparece no deployment. Só é contêiner se tiver lógica própria do sistema.
- Ferramentas de desenvolvimento (Swagger, pgAdmin) não entram.

## 3. Componentes

Para cada contêiner escolhido para detalhar:

| Estrutura | Candidatos a componente |
|-----------|-------------------------|
| .NET em camadas (Clean Architecture) | Controllers (ou grupos por área), serviços de aplicação por domínio, repositórios, adapters externos, serviços em segundo plano, middleware relevante |
| .NET por feature (vertical slices) | Uma feature (pasta) = um componente |
| Angular | Áreas/features com rota própria (lazy loaded), serviços core (auth, http, interceptors), bibliotecas compartilhadas |
| Banco relacional | Agrupamentos lógicos de tabelas por área |

Agrupe classes pelo que faz sentido em uma conversa de arquitetura: interface + implementação são um componente; DTOs, entidades e utilitários **não** são componentes. Se a API tiver dezenas de controllers, agrupe por área funcional ou divida em vários diagramas.

Monte a tabela **componente → caminho no código**. Se um componente não tem um lugar claro no código, isso é um achado: registre em Pontos em aberto (distância entre modelo e código).

## 4. Deployment

Ver `diagramas-complementares.md`, seção "Deployment" (compose por ambiente, Dockerfile, nginx, workflows de CI/CD).

## 5. Confirmação

Apresente o que foi encontrado em tabela antes de gerar o diagrama:

> "Encontrei no código:
> | Elemento | Tipo | Tecnologia | Evidência |
> |----------|------|------------|-----------|
> | API | Contêiner | ASP.NET Core 9 | `backend/src/X.API/X.API.csproj` |
> | ... |
>
> Falta algo? Algum desses não deveria aparecer?"

Nunca inclua segredos (senhas, chaves, tokens) encontrados em arquivos de configuração.
