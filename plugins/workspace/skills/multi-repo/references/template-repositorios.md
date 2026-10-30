# Templates

## 1. `docs/{projeto}/repositorios.md`

```markdown
# Repositórios — {Nome do Projeto}

O código do **{Nome do Projeto}** está em {N} repositórios. Este arquivo é a fonte única dos caminhos: as skills que leem código (`arch-c4`, `business-docs`, `plan-execution`) usam esta lista.

## Repositórios

| Repositório | Papel | URL | Código local | Branch principal | Stack | Contêineres C4 |
|-------------|-------|-----|--------------|------------------|-------|----------------|
| {nome} | backend | {url} | {caminho ou "a definir"} | main | .NET 9, EF Core | API, Worker |
| {nome} | frontend | {url} | {caminho ou "a definir"} | main | Angular 20 | SPA |

Os caminhos locais são os desta máquina; em outra máquina, ajuste a coluna Código local.

## Contratos entre repositórios

| Contrato | Tipo | Provedor | Consumidores | Onde está a definição |
|----------|------|----------|--------------|-----------------------|
| API REST | HTTP + OpenAPI | {repo backend} | {repo frontend} | `/swagger/v1/swagger.json` |
| {pacote} | NuGet / npm | {repo biblioteca} | {repos} | {feed} |
| {evento} | Fila / evento | {repo} | {repos} | {arquivo do schema} |

## Deploy

| Repositório | Pipeline | Ambientes | Depende de |
|-------------|----------|-----------|------------|
| {nome} | {ex.: GitHub Actions, deploy.yml} | homolog, produção | — |
| {nome} | {pipeline} | homolog, produção | API publicada antes |

## Observações

- {Compartilhado com: {outro-projeto}} (repositórios usados por mais de um projeto)
- {Convenção de branch, se houver: ex.: feat/{nome}, fix/{nome}}

## Histórico

| Data | Alteração |
|------|-----------|
| {DD/MM/YYYY} | Cadastro inicial |
```

### Seção Repositório do `project.md` depois do cadastro

```markdown
## Repositório
- Repositórios: vários, ver `docs/{projeto}/repositorios.md`
- Tipo: {tipo do projeto}
```

### Linha do `docs/workspace.md`

```markdown
| {Nome} | `docs/{projeto}/` | vários (ver `docs/{projeto}/repositorios.md`) | vários | {Situação} |
```

---

## 2. `docs/{projeto}/plano-execucao/{escopo}/mudanca-multi-repo.md`

```markdown
# Mudança em vários repositórios — {Nome da entrega}

- Projeto: {Nome do Projeto}
- Plano de execução: `docs/{projeto}/plano-execucao/{escopo}/execution-plan.md` {ou "avulsa"}
- Branch: `feat/{escopo}` (mesmo nome em todos os repositórios)
- Situação: Em andamento | Em homologação | Em produção | Concluída
- Iniciada em: {DD/MM/YYYY}

## Repositórios afetados

| Ordem | Repositório | Por quê | Tarefas do plano | Branch criada | PR |
|-------|-------------|---------|------------------|---------------|----|
| 1 | {repo backend} | novo endpoint de eventos | 1.1 a 1.6 | Sim | {link ou "a abrir"} |
| 2 | {repo frontend} | tela de eventos consome o endpoint | 1.7 a 1.10 | Sim | {link ou "a abrir"} |

## Contratos que mudam

| Contrato | Mudança | Compatível? | Estratégia |
|----------|---------|-------------|------------|
| `GET /api/eventos` | endpoint novo | Sim (só acrescenta) | — |
| `EventoDto.data` | vira `dataInicio` + `dataFim` | Não | expandir e contrair: manter `data` até o front publicar |

## Ordem de merge e de deploy

1. {repo backend}: merge e deploy em homolog
2. {repo frontend}: merge e deploy em homolog, apontando para o backend já publicado
3. Validação em homolog
4. Produção na mesma ordem
5. {Contração: remover `EventoDto.data` numa entrega seguinte}

## Checklist

- [ ] Branch criada em todos os repositórios afetados
- [ ] Contratos incompatíveis com estratégia definida
- [ ] Provedor publicado antes do consumidor em cada ambiente
- [ ] PRs com link cruzado (cada PR cita os outros)
- [ ] Arquitetura C4 atualizada, se mudou contêiner, integração ou componente (`arch-c4`)
- [ ] Contração agendada (se houve expansão)

## Histórico

| Data | Evento |
|------|--------|
| {DD/MM/YYYY} | Branches criadas |
```
