---
id: git
title: Convenção de Git
when: Sempre que trabalhar com estado versionado, diff, staging, branch, commit, push, histórico ou revisão de alterações.
---

# Convenção de Git

## Estado de trabalho

Antes de editar, verifique o estado do repositório quando a tarefa envolver commit, branch, push ou revisão de alterações. Não reverta alterações de outra pessoa sem pedido explícito.

## Branches

Quando uma branch for necessária, use nomes curtos e descritivos, preferencialmente ligados a change OpenSpec:

```text
change/define-project-conventions
```

Se o usuário ou o repositório já tiverem uma convenção mais específica, siga a convenção existente.

## Commits

Commits devem ser pequenos, revisáveis e conectados ao objetivo da mudança. Prefira mensagens em PT-BR, salvo instrução contrária.

Formato sugerido:

```text
docs: define convenções do projeto
```

Inclua no commit apenas arquivos relacionados ao trabalho. Não misture handoffs temporários, ajustes de ambiente e conteúdo durável sem necessidade.

## Push

Só faça push quando o usuário pedir explicitamente ou quando o fluxo combinado exigir. Antes do push, valide o que for relevante para a mudança e revise o diff.
