# devcontainer-codex

Language: English | [Português (Brasil)](README.pt-BR.md)

`devcontainer-codex` is a monorepo boilerplate for development with Docker, VS Code Dev Containers, OpenSpec, Codex, and context-aware AI-assisted workflows.

The repository is intentionally small, but it is not just a blank container template. It provides a root development environment for cross-cutting work, runtime-specific environments for humans working on apps, durable conventions for agents and collaborators, and sample Node, PHP, and C# apps that show the expected layout.

## What This Repository Is For

Use this repository when you want a project skeleton where:

- the whole workspace can be opened in a general-purpose `dev` container;
- each runtime can also have its own focused Dev Container;
- development conventions live in versioned files instead of chat history;
- OpenSpec can be used to plan and apply larger changes;
- Codex can use `context-mode` hooks to preserve useful working context.

This README is the human entrypoint. Agent-facing operating instructions live in [AGENTS.md](AGENTS.md), and detailed project conventions live in [conventions/](conventions/).

## Quick Start

From the repository root, create the environment files:

```sh
make env
```

Then open the repository in VS Code and choose one of the Dev Container entries under [.devcontainer/](.devcontainer/).

Start with the `dev` container when you are setting up the repository, making cross-cutting changes, using Codex, working with OpenSpec, or editing shared Docker/Compose/convention files.

Use the `node`, `php`, or `csharp` containers when you want a focused human workspace for one app/runtime, including runtime-specific VS Code extensions, linting, formatting, and debugging.

## Adapting This Boilerplate

After cloning this repository for a real project, update the project identity and operating rules:

1. Edit [.env.example](.env.example) and `.env` if the project name or mounted workspace path should change.
2. Edit [openspec/config.yaml](openspec/config.yaml) to describe your real project context, source-of-truth files, and OpenSpec artifact rules.
3. Edit [conventions/language.md](conventions/language.md) to choose the default language for conversations, documentation, OpenSpec artifacts, and agent-facing context.
4. Review [AGENTS.md](AGENTS.md) if your repository entrypoints, conventions, or agent instructions change.
5. Rename, remove, or extend the sample apps under [apps/](apps/) and keep matching service files under [docker/](docker/), [.devcontainer/](.devcontainer/), and [docker-compose.yml](docker-compose.yml).

`README.md` is intentionally written in English as the default consumer-facing entrypoint. That does not have to be the operating language of your project. Choose the language you want in `conventions/language.md`, then keep `openspec/config.yaml` aligned with that decision.

## Repository Map

| Path | Purpose |
| --- | --- |
| [README.md](README.md) | Human entrypoint for understanding and using this repository. |
| [README.pt-BR.md](README.pt-BR.md) | Brazilian Portuguese localized README. |
| [AGENTS.md](AGENTS.md) | Operational entrypoint for agents and collaborators. |
| [apps/](apps/) | Runtime-specific application code. |
| [docker/](docker/) | Dockerfiles, service environment files, and container support scripts. |
| [.devcontainer/](.devcontainer/) | VS Code Dev Container entries for each workspace. |
| [docker-compose.yml](docker-compose.yml) | Shared Compose orchestration for the development services. |
| [Makefile](Makefile) | Repository bootstrap command entrypoint. |
| [bin/](bin/) | Host-side helper scripts used by Make targets. |
| [conventions/](conventions/) | Durable project conventions for language, workflow, Git, artifacts, environments, and context handling. |
| [openspec/](openspec/) | OpenSpec project configuration, specs, and change history. |
| [tmp/](tmp/) | Ignored scratch space for temporary inputs, drafts, and handoffs. |

## Bootstrap Commands

The Makefile exposes the repository bootstrap commands:

```sh
make help
make env
make env-dev
make env-node
make env-php
make env-csharp
```

`make env` invokes [bin/env](bin/env) for `dev`, `node`, `php`, and `csharp`.

Each service-specific target invokes the same script for one service:

- `make env-dev` creates the root `.env` and `docker/dev/.env` files when missing;
- `make env-node` creates the root `.env` and `docker/node/.env` files when missing;
- `make env-php` creates the root `.env` and `docker/php/.env` files when missing;
- `make env-csharp` creates the root `.env` and `docker/csharp/.env` files when missing.

The bootstrap script creates files that do not exist and leaves existing `.env` files untouched.

## Dev Containers

| Container | Service | Workspace | Use it for |
| --- | --- | --- | --- |
| `dev` | `dev` | Whole repository | Cross-cutting development, Codex, OpenSpec, Docker/Compose work, conventions, and repository-wide changes. |
| `node` | `node` | [apps/node](apps/node) | Human Node.js app development with Node 24, Corepack, and editor tooling. |
| `php` | `php` | [apps/php](apps/php) | Human PHP app development with PHP 8.5 and editor tooling. |
| `csharp` | `csharp` | [apps/csharp](apps/csharp) | Human .NET app development with .NET 10 SDK and C# editor tooling. |

All Dev Containers use the `dev` user and the Docker-outside-of-Docker feature so the workspace can interact with the host Docker daemon when needed.

The `dev` container is the main environment for AI-assisted development because it mounts the whole repository and includes general tooling such as Git, `jq`, `ripgrep`, Python, Node, OpenSpec, Codex integration, and `context-mode`.

The runtime containers are focused workspaces for humans. They intentionally mount only their matching app directory through Compose:

- `node` mounts `apps/node`;
- `php` mounts `apps/php`;
- `csharp` mounts `apps/csharp`.

## Apps

The current apps are minimal health-check examples:

- [apps/node/src/health.ts](apps/node/src/health.ts) prints `I'm healthy!`.
- [apps/php/src/health.php](apps/php/src/health.php) prints `I'm healthy!`.
- [apps/csharp/src/Health.cs](apps/csharp/src/Health.cs) prints `I'm healthy!`.

When adding a new service or app, keep the same shape:

```text
apps/<service>/             application code
docker/<service>/           Dockerfile and service environment files
.devcontainer/<service>/    VS Code Dev Container entry
docker-compose.yml          service orchestration
```

Operational services that support the whole workspace, such as `dev`, do not need a matching `apps/<service>/` directory.

## Working With OpenSpec

OpenSpec is available in the `dev` container for planning and tracking larger changes.

The expected lifecycle is:

1. Explore the problem and understand risks.
2. Propose a change with OpenSpec artifacts.
3. Apply the change to versioned files.
4. Archive the completed change.
5. Commit the reviewed result.

See [conventions/workflow.md](conventions/workflow.md) for the repository workflow and [openspec/config.yaml](openspec/config.yaml) for the current OpenSpec project context and artifact rules.

## Codex And Context-Mode

The `dev` container configures `context-mode` for Codex during `postCreateCommand`.

The script [setup-codex-context-mode](docker/dev/bin/setup-codex-context-mode):

- merges [config.toml](docker/dev/.codex/config.toml) into `~/.codex/config.toml`;
- installs hooks from [hooks.json](docker/dev/.codex/hooks.json) into `~/.codex/hooks.json`.

The `dev` Dev Container mounts `~/.codex` on the Docker volume `codex`, so Codex configuration and trust state survive container rebuilds.

The first time a new `codex` volume is created, Codex still requires a manual hook review before running those hooks.

To review the hooks from inside the `dev` container:

```sh
codex -C "$PWD" --no-alt-screen
```

Open the Hooks screen, review the hooks loaded from `~/.codex/hooks.json`, and trust them. After review, they should appear with `Active = 1`.

Repeat this only when the `codex` volume is recreated or when [hooks.json](docker/dev/.codex/hooks.json) changes.

## Next Steps

- TODO: Complete the `node`, `php`, and `csharp` human workspaces with linting, formatting, debugging, and runtime-specific VS Code extensions.
- TODO: Define the branch strategy for AI-assisted work, including model-oriented branches such as `codex` and `claude`.
- TODO: Add a messaging broker, evaluating RabbitMQ, SQS, or Kafka.
- TODO: Add more apps and runtimes, such as React, Python, and Go.
- TODO: Configure a database MCP integration.
- TODO: Configure a Chrome DevTools MCP integration.
- TODO: Add health checks for each service in [docker-compose.yml](docker-compose.yml).
