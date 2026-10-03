# Guia operacional do projeto

Este repositório é um boilerplate de mono repo usando devcontainers e agentes de desenvolvimento assistido por IA.

## Entradas do repositório

[README.md](README.md) é a entrada humana da raiz do repositório.

Este [AGENTS.md](AGENTS.md) é a entrada operacional para agentes e colaboradores. Ele funciona como índice das convenções do projeto e orienta quais fontes canônicas consultar.

## Convenções

Convenções são documentos duráveis em `conventions/` que definem regras transversais do projeto. Cada convenção declara no front matter `when` quando deve ser lida.

| Convenção | Escopo |
| --- | --- |
| [conventions/language.md](conventions/language.md) | Idioma padrão da conversa, contexto do projeto e artefatos. |
| [conventions/workflow.md](conventions/workflow.md) | Exploração, planejamento, proposta e aplicação de mudanças. |
| [conventions/git.md](conventions/git.md) | Estado versionado, diff, branch, commit, push e revisão de alterações. |
| [conventions/environment.md](conventions/environment.md) | Ambientes, infraestrutura local, Docker, Compose, devcontainers, `dev` e serviços/apps. |
| [conventions/artifacts.md](conventions/artifacts.md) | Artefatos duráveis e transitórios, insumos, handoffs, rascunhos, `tmp/` e fontes de verdade. |
| [conventions/context-mode.md](conventions/context-mode.md) | Uso de context-mode, ferramentas `ctx_*`, hooks do Codex e preservação da janela de contexto. |
| [conventions/headroom.md](conventions/headroom.md) | Uso e configuração da CLI, MCP e proxy Headroom, compressão, recuperação de conteúdo e roteamento de inferência do Codex. |
