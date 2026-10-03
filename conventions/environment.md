---
id: environment
title: Convenção de ambiente
when: Sempre que precisar entender ou alterar ambientes, infraestrutura local, Docker, Compose, devcontainers, serviço `dev`, serviços/apps do monorepo ou desenvolvimento assistido por IA.
---

# Convenção de ambiente

## Regra geral

Use o serviço `dev` como ambiente macro do repositório para desenvolvimento assistido por IA, especificação, automação e tarefas transversais.

Use os ambientes específicos de serviços ou apps do monorepo quando o objetivo for trabalhar com ferramentas próprias daquele serviço, como editor, lint, formatting, debug ou runtime local.

## Serviço `dev`

O serviço `dev` representa o ambiente de desenvolvimento transversal do monorepo. Ele deve enxergar o repositório inteiro e concentrar ferramentas gerais de apoio ao desenvolvimento, como OpenSpec, ferramentas de contexto, CLIs auxiliares, automações e bibliotecas úteis.

O serviço inclui context-mode para preservação de contexto e Headroom para compressão e recuperação de conteúdo. Consulte [context-mode.md](context-mode.md) e [headroom.md](headroom.md) para suas regras de uso e configuração operacional.

Desenvolvimento assistido por IA deve acontecer a partir do serviço `dev`. O agente precisa operar com visão macro do repositório, porque uma alteração em um serviço ou app pode impactar outros serviços, `docker-compose.yml`, devcontainers, convenções, documentação ou artefatos OpenSpec.

Não use ambientes isolados de serviços ou apps como contexto principal para desenvolvimento assistido por IA, salvo decisão explícita e justificada para uma tarefa muito restrita.

## Serviços e apps do monorepo

Cada serviço ou app do monorepo deve manter sua estrutura previsível:

- código do app em `apps/<service>/`, quando o serviço representar uma aplicação ou runtime do monorepo;
- imagem, variáveis de ambiente e suporte de container em `docker/<service>/`;
- entrada de desenvolvimento em `.devcontainer/<service>/`;
- orquestração declarada em `docker-compose.yml`.

Serviços operacionais que apoiam o workspace inteiro, como `dev`, não precisam ter uma pasta correspondente em `apps/`.

## Escopo das convenções

Esta convenção descreve a topologia e o uso dos ambientes. Ela não deve documentar detalhes internos de cada serviço ou app.

Detalhes específicos de runtime, extensões, comandos, portas, debuggers, linters ou ferramentas locais devem ficar perto do serviço ou app correspondente, ou em documentação própria quando se tornarem fonte de verdade durável.
