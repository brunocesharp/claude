# Comandos Git

Use sempre `git -C "{caminho}"` em vez de entrar na pasta: cada comando diz em qual repositório roda, e o diretório de trabalho do terminal não muda. Os comandos valem para Bash e PowerShell.

---

## Somente leitura (podem rodar sem confirmação)

### Detecção, no cadastro

| Informação | Comando |
|------------|---------|
| É repositório Git? | `git -C "{caminho}" rev-parse --is-inside-work-tree` |
| URL do remoto | `git -C "{caminho}" remote get-url origin` |
| Branch principal do remoto | `git -C "{caminho}" symbolic-ref --short refs/remotes/origin/HEAD` (resposta `origin/main` → `main`) |
| Branch principal, se o comando acima falhar | `git -C "{caminho}" remote show origin` (linha "HEAD branch"; precisa de rede) |
| Raiz do repositório | `git -C "{caminho}" rev-parse --show-toplevel` |
| Submódulos | `git -C "{caminho}" submodule status` |

**URL com credencial** (`https://usuario:token@github.com/org/repo.git`): registre só `https://github.com/org/repo.git`.

**Stack**: liste os arquivos da raiz e de um nível abaixo com a ferramenta de busca de arquivos (Glob), não com o Git.

### Panorama

| Informação | Comando |
|------------|---------|
| Branch atual | `git -C "{caminho}" branch --show-current` (vazio = HEAD destacado) |
| Alterações não commitadas | `git -C "{caminho}" status --porcelain` (conte as linhas) |
| Atrás / à frente do remoto | `git -C "{caminho}" rev-list --left-right --count "@{upstream}...HEAD"` (primeiro número = atrás, segundo = à frente; erro = branch sem upstream) |
| Último commit | `git -C "{caminho}" log -1 --format="%cd|%s" --date=format:%d/%m/%Y` |
| Branch existe localmente? | `git -C "{caminho}" rev-parse --verify --quiet "refs/heads/{branch}"` |
| Branch existe no remoto? | `git -C "{caminho}" rev-parse --verify --quiet "refs/remotes/origin/{branch}"` |
| Commits da branch sobre a principal | `git -C "{caminho}" rev-list --count "origin/{principal}..{branch}"` |

### Atualizar referências remotas (pedir uma vez)

`git -C "{caminho}" fetch --prune` — baixa as referências do remoto e não mexe nos arquivos nem nas branches locais. Precisa de rede e pode pedir autenticação: pergunte uma vez por execução do panorama.

---

## Alteram o repositório (somente com confirmação)

Mostre o comando, o repositório e o efeito, e espere o "sim". Execute um repositório por vez e mostre o resultado.

### Clonar

```
git clone "{url}" "{destino}"
```

Pré-condições: o destino não existe (ou é uma pasta vazia) e não fica dentro da pasta de documentação.

### Criar a branch da entrega

Pré-condições, todas verificadas antes:
1. `status --porcelain` vazio (sem alterações pendentes). Se houver, **pare naquele repositório** e avise.
2. A branch ainda não existe (local nem remota). Se existir, não recrie: pergunte se a entrega usa a existente.
3. Referências atualizadas (`fetch --prune`, com a confirmação de rede).

Criar a partir da principal do remoto, sem mexer na branch principal local:

```
git -C "{caminho}" switch -c "{branch}" "origin/{principal}"
```

Não publique a branch (`push -u`) sem o usuário pedir.

### Trocar de branch

```
git -C "{caminho}" switch "{branch}"
```

Só com a pasta sem alterações pendentes.

### Atualizar a branch atual

```
git -C "{caminho}" pull --ff-only
```

Só com a pasta sem alterações pendentes. `--ff-only` falha em vez de criar merge: se falhar, avise e pare (a branch divergiu do remoto).

---

## Nunca, a menos que o usuário peça aquela ação

`commit`, `push`, `merge`, `rebase`, `reset`, `stash`, `clean`, `checkout -- .`/`restore`, `branch -d/-D`, `push --force`. Se o usuário pedir, faça só no repositório citado e mostre o resultado.
