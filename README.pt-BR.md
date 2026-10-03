# devcontainer-codex

Idioma: [English](README.md) | Português (Brasil)

`devcontainer-codex` é um boilerplate de monorepo para desenvolvimento com Docker, VS Code Dev Containers, OpenSpec, Codex e fluxos de trabalho assistidos por IA com contexto preservado.

O repositório é intencionalmente pequeno, mas não é apenas um template vazio de container. Ele fornece um ambiente raiz para trabalho transversal, ambientes específicos de runtime para pessoas trabalhando em apps, convenções duráveis para agentes e colaboradores, e apps de exemplo em Node, PHP e C# que mostram a estrutura esperada.

## Para Que Este Repositório Serve

Use este repositório quando você quiser uma base de projeto onde:

- o workspace inteiro possa ser aberto em um container `dev` de uso geral;
- cada runtime também possa ter seu próprio Dev Container focado;
- convenções de desenvolvimento vivam em arquivos versionados em vez de histórico de chat;
- OpenSpec possa ser usado para planejar e aplicar mudanças maiores;
- Codex possa usar hooks de `context-mode` para preservar contexto útil de trabalho.

Este README é a entrada humana. Instruções operacionais para agentes vivem em [AGENTS.md](AGENTS.md), e convenções detalhadas do projeto vivem em [conventions/](conventions/).

## Começo Rápido

A partir da raiz do repositório, crie os arquivos de ambiente:

```sh
make env
```

Depois, abra o repositório no VS Code e escolha uma das entradas de Dev Container em [.devcontainer/](.devcontainer/).

Comece pelo container `dev` quando estiver configurando o repositório, fazendo mudanças transversais, usando Codex, trabalhando com OpenSpec ou editando arquivos compartilhados de Docker, Compose e convenções.

Use os containers `node`, `php` ou `csharp` quando quiser um workspace humano focado em um app/runtime, incluindo extensões específicas do VS Code, linting, formatting e debugging.

## Adaptando Este Boilerplate

Depois de clonar este repositório para um projeto real, atualize a identidade do projeto e as regras operacionais:

1. Edite [.env.example](.env.example) e `.env` se o nome do projeto ou o caminho montado do workspace precisar mudar.
2. Edite [openspec/config.yaml](openspec/config.yaml) para descrever o contexto real do seu projeto, os arquivos de fonte de verdade e as regras de artefatos OpenSpec.
3. Edite [conventions/language.md](conventions/language.md) para escolher o idioma padrão de conversas, documentação, artefatos OpenSpec e contexto voltado a agentes.
4. Revise [AGENTS.md](AGENTS.md) se as entradas do repositório, convenções ou instruções para agentes mudarem.
5. Renomeie, remova ou estenda os apps de exemplo em [apps/](apps/) e mantenha os arquivos de serviço correspondentes em [docker/](docker/), [.devcontainer/](.devcontainer/) e [docker-compose.yml](docker-compose.yml).

`README.md` é escrito intencionalmente em inglês como a entrada padrão voltada a consumidores. Isso não precisa ser o idioma operacional do seu projeto. Escolha o idioma desejado em `conventions/language.md` e mantenha `openspec/config.yaml` alinhado com essa decisão.

## Mapa do Repositório

| Caminho | Propósito |
| --- | --- |
| [README.md](README.md) | Entrada humana principal, em inglês, para entender e usar este repositório. |
| [README.pt-BR.md](README.pt-BR.md) | Versão localizada em português brasileiro. |
| [AGENTS.md](AGENTS.md) | Entrada operacional para agentes e colaboradores. |
| [apps/](apps/) | Código de aplicações específicas por runtime. |
| [docker/](docker/) | Dockerfiles, arquivos de ambiente de serviços e scripts de suporte a containers. |
| [.devcontainer/](.devcontainer/) | Entradas de VS Code Dev Container para cada workspace. |
| [docker-compose.yml](docker-compose.yml) | Orquestração Compose compartilhada para os serviços de desenvolvimento. |
| [Makefile](Makefile) | Entrada de comandos de bootstrap do repositório. |
| [bin/](bin/) | Scripts auxiliares executados no host pelos targets do Make. |
| [conventions/](conventions/) | Convenções duráveis do projeto para idioma, workflow, Git, artefatos, ambientes e contexto. |
| [openspec/](openspec/) | Configuração do projeto OpenSpec, specs e histórico de mudanças. |
| [tmp/](tmp/) | Espaço ignorado para insumos temporários, rascunhos e handoffs. |

## Comandos de Bootstrap

O Makefile expõe os comandos de bootstrap do repositório:

```sh
make help
make env
make env-dev
make env-node
make env-php
make env-csharp
```

`make env` invoca [bin/env](bin/env) para `dev`, `node`, `php` e `csharp`.

Cada target específico invoca o mesmo script para um serviço:

- `make env-dev` cria o `.env` da raiz e `docker/dev/.env` quando ausentes;
- `make env-node` cria o `.env` da raiz e `docker/node/.env` quando ausentes;
- `make env-php` cria o `.env` da raiz e `docker/php/.env` quando ausentes;
- `make env-csharp` cria o `.env` da raiz e `docker/csharp/.env` quando ausentes.

O script de bootstrap cria arquivos que ainda não existem e preserva arquivos `.env` existentes.

## Dev Containers

| Container | Serviço | Workspace | Use para |
| --- | --- | --- | --- |
| `dev` | `dev` | Repositório inteiro | Desenvolvimento transversal, Codex, OpenSpec, trabalho em Docker/Compose, convenções e mudanças no repositório inteiro. |
| `node` | `node` | [apps/node](apps/node) | Desenvolvimento humano de app Node.js com Node 24, Corepack e tooling de editor. |
| `php` | `php` | [apps/php](apps/php) | Desenvolvimento humano de app PHP com PHP 8.5 e tooling de editor. |
| `csharp` | `csharp` | [apps/csharp](apps/csharp) | Desenvolvimento humano de app .NET com .NET 10 SDK e tooling de C#. |

Todos os Dev Containers usam o usuário `dev` e a feature Docker-outside-of-Docker para que o workspace possa interagir com o Docker daemon do host quando necessário.

O container `dev` é o ambiente principal para desenvolvimento assistido por IA porque monta o repositório inteiro e inclui ferramentas gerais como Git, `jq`, `ripgrep`, Python, Node, integração com Codex, OpenSpec e `context-mode`.

Os containers de runtime são workspaces focados para humanos. Eles montam intencionalmente apenas o diretório do app correspondente via Compose:

- `node` monta `apps/node`;
- `php` monta `apps/php`;
- `csharp` monta `apps/csharp`.

## Apps

Os apps atuais são exemplos mínimos de health check:

- [apps/node/src/health.ts](apps/node/src/health.ts) imprime `I'm healthy!`.
- [apps/php/src/health.php](apps/php/src/health.php) imprime `I'm healthy!`.
- [apps/csharp/src/Health.cs](apps/csharp/src/Health.cs) imprime `I'm healthy!`.

Ao adicionar um novo serviço ou app, mantenha a mesma estrutura:

```text
apps/<service>/             código da aplicação
docker/<service>/           Dockerfile e arquivos de ambiente do serviço
.devcontainer/<service>/    entrada de VS Code Dev Container
docker-compose.yml          orquestração do serviço
```

Serviços operacionais que apoiam o workspace inteiro, como `dev`, não precisam de um diretório `apps/<service>/` correspondente.

## Trabalhando Com OpenSpec

OpenSpec está disponível no container `dev` para planejar e acompanhar mudanças maiores.

O ciclo de vida esperado é:

1. Explorar o problema e entender riscos.
2. Propor uma mudança com artefatos OpenSpec.
3. Aplicar a mudança em arquivos versionados.
4. Arquivar a mudança concluída.
5. Commitar o resultado revisado.

Veja [conventions/workflow.md](conventions/workflow.md) para o workflow do repositório e [openspec/config.yaml](openspec/config.yaml) para o contexto atual do projeto OpenSpec e regras de artefatos.

## Codex E Context-Mode

O container `dev` configura `context-mode` para o Codex durante o `postCreateCommand`.

O script [setup-codex-context-mode](docker/dev/bin/setup-codex-context-mode):

- mescla [config.toml](docker/dev/.codex/config.toml) em `~/.codex/config.toml`;
- instala hooks de [hooks.json](docker/dev/.codex/hooks.json) em `~/.codex/hooks.json`.

O Dev Container `dev` monta `~/.codex` no volume Docker `codex`, então a configuração do Codex e o estado de confiança sobrevivem a rebuilds do container.

Na primeira vez que um novo volume `codex` for criado, o Codex ainda exige revisão manual dos hooks antes de executá-los.

Para revisar os hooks dentro do container `dev`:

```sh
codex -C "$PWD" --no-alt-screen
```

Abra a tela de Hooks, revise os hooks carregados de `~/.codex/hooks.json` e confie neles. Depois da revisão, eles devem aparecer com `Active = 1`.

Repita esse passo apenas quando o volume `codex` for recriado ou quando [hooks.json](docker/dev/.codex/hooks.json) mudar.

## Headroom

A imagem `dev` inclui a CLI Headroom, um servidor MCP para Codex e um proxy local
iniciado junto com o Dev Container. O setup configura automaticamente o MCP e o
roteamento de inferência do Codex pelo proxy na criação ou no rebuild do
container. Para reaplicar o setup ou restaurar o provider anterior:

```sh
start-headroom-proxy
setup-codex-headroom
# Restaura o provider anterior e mantém o MCP disponível:
setup-codex-headroom --disable
```

Recarregue a extensão Codex e inicie uma nova conversa depois de alterar o
roteamento. Conversas existentes não são migradas. Faça rebuild do Dev Container
para instalar a integração em um clone existente. Veja a
[convenção de Headroom](conventions/headroom.md) para regras de uso, autenticação,
opções de runtime, diagnóstico e testes.

## Próximos Passos

- TODO: Completar os workspaces humanos `node`, `php` e `csharp` com linting, formatting, debugging e extensões específicas do VS Code.
- TODO: Definir a estratégia de branches para trabalho assistido por IA, incluindo branches por modelo como `codex` e `claude`.
- TODO: Adicionar um broker de mensageria, avaliando RabbitMQ, SQS ou Kafka.
- TODO: Adicionar mais apps e runtimes, como React, Python e Go.
- TODO: Configurar uma integração MCP para banco de dados.
- TODO: Configurar uma integração MCP para Chrome DevTools.
- TODO: Adicionar health checks para cada serviço em [docker-compose.yml](docker-compose.yml).
