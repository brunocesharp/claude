# Checklist dos diagramas

Passe em cada diagrama antes de salvar. Item que falhar: corrija ou registre em Pontos em aberto com o motivo.

## Todo diagrama

- [ ] Título com o tipo: `[Contexto]`, `[Contêineres]`, `[Componentes]`, `[Deployment]`, `[Dinâmico]`, `[Landscape]`
- [ ] Tabela de legenda logo abaixo (formas, cores, bordas, estilos de linha, siglas usadas)
- [ ] Um só nível de abstração no diagrama
- [ ] Todo elemento tem nome e descrição; contêiner e componente também tecnologia
- [ ] Toda relação tem rótulo que se lê como frase, do iniciador para o receptor
- [ ] Direção das setas consistente (dependência) em todos os diagramas
- [ ] Siglas do domínio estão no glossário
- [ ] Até ~12 elementos; acima disso, avaliado se vale dividir
- [ ] Posições consistentes entre diagramas (pessoas em cima, externos embaixo)
- [ ] O Mermaid renderiza (aliases sem hífen/acento, textos entre aspas)
- [ ] Nenhum segredo (senha, chave, token, IP interno sensível)

## Contexto

- [ ] Pode ser mostrado a uma pessoa não técnica
- [ ] Sem tecnologia, protocolo ou formato de dados
- [ ] Sistemas que o time não constrói estão como externos
- [ ] Todo perfil de usuário relevante do discovery aparece (ou foi omitido de propósito)

## Contêineres

- [ ] Cada contêiner é implantável separadamente (nenhuma DLL, pacote ou camada)
- [ ] Bancos e armazenamentos aparecem como contêineres; cada schema é um contêiner
- [ ] As mesmas pessoas e sistemas do contexto; `System_Boundary` igual à caixa do contexto
- [ ] Relações com mecanismo, estilo (síncrono/assíncrono) e protocolo
- [ ] Sem instâncias, réplicas ou servidores
- [ ] Tecnologias em aberto aparecem como opções e estão em Pontos em aberto

## Componentes

- [ ] Um contêiner por diagrama, dentro de `Container_Boundary`
- [ ] Cada componente existe no código (modo Levantamento) ou seria codificado assim (modo Design)
- [ ] Tabela componente → caminho no código
- [ ] Frameworks e bibliotecas aparecem como tecnologia, não como componente
- [ ] Transversais (log, auth, cache) tratados por nota ou omitidos de propósito
- [ ] Componente compartilhado aparece dentro de cada contêiner que o usa, marcado como compartilhado

## Deployment

- [ ] Um diagrama por ambiente
- [ ] Mostra os contêineres dentro dos nós, não só a infraestrutura
- [ ] Nós aninhados até o ambiente de execução
- [ ] Réplicas e replicação de dados indicadas quando existem

## Dinâmico

- [ ] O cenário não é evidente lendo o código
- [ ] Ordem dos `Rel` corresponde à ordem dos passos
- [ ] Tabela de passos abaixo do diagrama
