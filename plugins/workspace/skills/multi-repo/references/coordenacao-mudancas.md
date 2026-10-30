# Coordenação de mudanças entre repositórios

Com o código em vários repositórios, uma entrega vira vários PRs que são mergeados e publicados em momentos diferentes. Entre um deploy e outro, as versões antiga e nova convivem. A regra que evita quebra: **em qualquer ordem em que as publicações aconteçam, o que está no ar continua funcionando**.

---

## 1. Repositórios afetados

Parta dos contêineres C4 que a entrega toca (plano de execução ou `arquitetura.md`) e use a coluna Contêineres C4 do `repositorios.md`.

| A entrega muda... | Repositórios afetados |
|-------------------|-----------------------|
| Regra de negócio só no backend | backend |
| Tela nova consumindo endpoint existente | frontend |
| Tela nova com endpoint novo | backend e frontend |
| Modelo compartilhado (pacote, contratos) | biblioteca/contratos e todos os consumidores que vão usar a versão nova |
| Infraestrutura (variável de ambiente, fila nova, bucket) | infraestrutura e os que leem a configuração |

Repositório que só precisa "atualizar o pacote" também entra na lista, com o motivo.

---

## 2. Contratos compatíveis e incompatíveis

| Mudança | Compatível? |
|---------|-------------|
| Endpoint, campo opcional de resposta, evento novo | Sim |
| Campo opcional novo na requisição | Sim |
| Campo obrigatório novo na requisição | **Não** |
| Remover ou renomear endpoint, campo ou evento | **Não** |
| Mudar tipo, formato ou significado de um campo | **Não** |
| Validação mais restritiva no provedor | **Não** (consumidores antigos podem passar a falhar) |
| Pacote com versão maior (major) | **Não** |

Contratos compatíveis seguem a ordem natural. Os incompatíveis precisam de uma estratégia.

---

## 3. Estratégias para mudança incompatível

| Estratégia | Como funciona | Quando usar |
|------------|---------------|-------------|
| **Expandir e contrair** | 1) o provedor passa a aceitar/devolver o formato novo **e** o antigo; 2) os consumidores migram; 3) numa entrega seguinte, o provedor remove o antigo | Padrão para renomear campo, trocar formato, separar campo em dois |
| **Versão nova do endpoint/evento** | `v2` ao lado da `v1`; consumidores migram; `v1` é desligada depois | Mudança grande, vários consumidores, consumidores de outros times |
| **Feature flag** | código novo publicado desligado nos dois lados; liga quando todos estão no ar | Comportamento novo que precisa entrar ao mesmo tempo em vários repositórios |
| **Janela de deploy conjunto** | publica todos juntos, aceitando a indisponibilidade curta | Último recurso: sistema interno, sem usuários no horário, combinado com o time |

Banco de dados segue a mesma ideia: coluna nova anulável primeiro, preencher, passar a usar, remover a antiga numa entrega seguinte. Nunca renomeie coluna numa migration que roda antes do código que a usa estar no ar.

A estratégia escolhida para cada contrato vai para o `mudanca-multi-repo.md`. A contração é uma tarefa real: registre no checklist e no plano da entrega seguinte.

---

## 4. Ordem de merge e de deploy

Regra geral: **provedor antes do consumidor**, em cada ambiente.

```
contratos / biblioteca  ->  backend (provedor)  ->  frontend, mobile, workers (consumidores)
```

- Biblioteca: publicar a versão do pacote antes de mergear quem a consome.
- Banco: a migration roda com o backend; ela precisa ser compatível com o código antigo que ainda está no ar durante o deploy.
- Homologação primeiro, na mesma ordem; produção só depois da validação, na mesma ordem.
- Com feature flag, a ordem dos merges importa menos: a flag só liga quando todos estiverem no ar.

---

## 5. Branch e PRs

- O mesmo nome de branch em todos os repositórios (`feat/{escopo}`): fica fácil achar as partes da entrega e o panorama mostra quem está fora dela.
- Siga a convenção de cada repositório se houver (ex.: `feature/`, número da tarefa no nome).
- Cada PR cita os outros PRs da entrega e a ordem de merge na descrição.
- O `mudanca-multi-repo.md` guarda os links dos PRs e o andamento.

---

## 6. Checklist da mudança coordenada

- [ ] Todos os repositórios afetados identificados, com o motivo
- [ ] Cada contrato que muda classificado (compatível ou não)
- [ ] Estratégia definida para cada contrato incompatível
- [ ] Ordem de merge e de deploy registrada, provedor antes do consumidor
- [ ] Migrations compatíveis com o código anterior
- [ ] Branch com o mesmo nome em todos os repositórios afetados
- [ ] PRs com links cruzados
- [ ] Contração (remoção do antigo) registrada para a entrega seguinte
- [ ] C4 atualizado se a entrega mudou contêiner, integração ou componente (`arch-c4`)
