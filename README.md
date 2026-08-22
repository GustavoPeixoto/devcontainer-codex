# devcontainer-codex

## Hooks do context-mode

O devcontainer configura o `context-mode` para o Codex durante o `postCreateCommand`.

O script [setup-codex-context-mode](docker/dev/bin/setup-codex-context-mode):

- mescla a configuração de [config.toml](docker/dev/.codex/config.toml) em `~/.codex/config.toml`;
- instala os hooks de [hooks.json](docker/dev/.codex/hooks.json) em `~/.codex/hooks.json`.

A pasta `~/.codex` é montada no volume Docker `codex`, então a configuração e o estado de trust sobrevivem a rebuilds do container.

Na primeira vez que um volume novo for criado, o Codex ainda exige review manual dos hooks antes de executá-los.

Para revisar:

```sh
codex -C /devcontainer-codex --no-alt-screen
```

Abra a tela de Hooks, revise e confie nos hooks vindos de `~/.codex/hooks.json`.

Após o review, eles devem aparecer com `Active = 1`.

Repita esse passo apenas quando o volume `codex` for recriado ou quando `hooks.json` mudar.
