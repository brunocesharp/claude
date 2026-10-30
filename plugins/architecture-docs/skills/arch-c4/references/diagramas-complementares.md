# Diagramas complementares

Fonte: Simon Brown, *The C4 model for visualising software architecture*, cap. 12 ("Deployment diagrams") e 13 ("Other diagrams").

Os diagramas de contexto, contêineres e componentes costumam bastar. Os complementares mostram outros aspectos **a partir da estrutura estática**: uma vez que há vocabulário comum para a estrutura, fica fácil falar de execução, infraestrutura e deployment. Mantenha o número de diagramas no mínimo; se um diagrama não agrega, descarte.

---

## Deployment

Mostra como instâncias de **sistemas ou contêineres** são mapeadas em **nós de deployment**. Mesmo com deploy automatizado, um diagrama resumindo o mapeamento ajuda.

**Nó de deployment** — pode ser aninhado:
- infraestrutura física (servidor, dispositivo);
- virtualizada (IaaS, PaaS, máquina virtual);
- conteinerizada (container Docker, pod);
- ambiente de execução (servidor de banco, servidor web, IIS, Kestrel, navegador).

**O que incluir:**
- Um diagrama por ambiente (desenvolvimento, homologação, produção).
- Instâncias e réplicas (`api x3`), banco primário e secundário com replicação.
- Nós de infraestrutura quando ajudam a contar a história: DNS, balanceador, proxy reverso, firewall, CDN.
- Hostnames, IPs, portas expostas, se forem úteis (nunca segredos).

**Diagrama de nuvem** — não faça só o "diagrama de ícones" (Route 53, ELB, EC2, RDS). Ele mostra **quais** serviços são usados, mas não **para quê**. Mostre também os contêineres (aplicações e armazenamentos) dentro desses serviços. O mesmo vale para Docker e Kubernetes: não mostre só a infraestrutura, mostre as aplicações e os dados.

**Fontes no código (modo Levantamento)**: `docker-compose*.yml`, `Dockerfile`, manifests Kubernetes/Helm, Terraform/Bicep, `nginx*.conf`, workflows de CI/CD (`.github/workflows`), variáveis de ambiente de exemplo (`.env.example`).

---

## System Landscape

Um diagrama de contexto **sem foco em um sistema**: mostra o conjunto de sistemas de uma organização (ou do workspace), com pessoas e sistemas internos e externos e o limite da organização. Útil quando o time é responsável por vários sistemas.

Nesta skill: fica em `docs/arquitetura/landscape.md`, na raiz do workspace, e reúne os sistemas dos projetos de `docs/workspace.md` que se relacionam. Use `C4Context` com `Enterprise_Boundary` para separar interno de externo. Cada sistema do landscape aponta para o `arquitetura.md` do seu projeto.

Atualize o landscape quando um projeto ganhar ou perder uma integração com outro sistema do workspace.

---

## Dinâmico (comportamento em execução)

Aplica a ideia dos diagramas de sequência e colaboração da UML aos elementos do C4 (pessoas, sistemas, contêineres, componentes) para mostrar o que acontece em tempo de execução num cenário.

**Quando fazer** — raramente, só para cenários significativos ou complexos que **não são evidentes lendo o código**:
- interação entre aplicações durante autenticação federada;
- fluxo de mensagens/eventos assíncronos que implementa um processo de negócio;
- um padrão de baixo nível que se repete.

Não tente documentar todos os caminhos de execução.

**Formatos**:
- **Colaboração** (preferido pelo livro, mais fácil de desenhar): caixas e linhas numeradas na ordem; mesmo número indica paralelismo. No Mermaid: `C4Dynamic` (a numeração sai da ordem dos `Rel`; paralelismo vai explicado na legenda).
- **Sequência**: participantes da esquerda para a direita, tempo de cima para baixo. No Mermaid: `sequenceDiagram`, com os participantes nomeados como os elementos do C4.

Um arquivo por cenário em `docs/{projeto}/arquitetura/dinamicos/{cenario}.md`.

---

## Modelo de domínio

Se o domínio não é trivial, um diagrama com os conceitos principais ajuda (com ou sem DDD): cada classe é uma entidade do domínio, com atributos importantes e relações. No Mermaid: `classDiagram`. Se o projeto já tem documentação de modelo de dados ou regras de negócio (`docs/{projeto}/business/`), aponte para ela em vez de duplicar.

---

## Outros

- **Protótipos e wireframes** de interface: mostram o que o C4 não mostra; ficam fora desta skill.
- **Processos de negócio e fluxos de trabalho**: diagrama de atividades UML ou fluxograma (`flowchart` no Mermaid).
- **Diagramas gerados automaticamente** (ER do banco, por exemplo): se precisar de uma folha A0 para ler, provavelmente não é útil.

---

## Relação com modelos de visões

O C4 junta numa só descrição o que outros modelos separam em "visão lógica" e "visão de desenvolvimento" (4+1 de Kruchten; viewpoints de Rozanski e Woods), reduzindo a distância entre o modelo e o código. A visão física corresponde ao deployment; a visão de processos é parcialmente coberta pelos contêineres e pelos diagramas dinâmicos. Se o time usa outro modelo de visões, registre a correspondência no glossário.
