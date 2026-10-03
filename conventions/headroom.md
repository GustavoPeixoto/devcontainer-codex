---
id: headroom
title: Convenção de Headroom
when: Sempre que usar ou configurar Headroom, sua CLI, ferramentas MCP de compressão e recuperação, o proxy ou o roteamento de inferência do Codex pelo Headroom.
---

# Convenção de Headroom

> [!WARNING]
> **Integração em acompanhamento: recuperação de conteúdo pelo Codex**
>
> A integração permanece na branch `headroom`, com a versão
> `headroom-ai[proxy]==0.39.1` fixada no Dockerfile. Resultados de
> `headroom_retrieve` chamados por `functions.exec` podem ser comprimidos
> novamente pelo proxy, fazendo o agente receber outro marcador CCR em vez do
> conteúdo original recuperado.
>
> Estamos acompanhando o [repositório do Headroom](https://github.com/headroomlabs-ai/headroom),
> a [issue #3563](https://github.com/headroomlabs-ai/headroom/issues/3563) e o
> [PR #3915](https://github.com/headroomlabs-ai/headroom/pull/3915). Em
> **2026-10-03**, ambos estavam abertos e o PR ainda não havia sido incorporado.
> Aguardamos uma correção oficial publicada e validada neste ambiente antes de
> integrar estas alterações à branch principal. A atualização deverá manter
> uma versão exata no Dockerfile e confirmar que o conteúdo recuperado chega
> integralmente ao agente em uma nova conversa. Revise este alerta após essa
> validação.

## Regra geral

Use Headroom para compressão, recuperação de conteúdo original e estatísticas
de consumo de tokens durante desenvolvimento assistido por IA no serviço `dev`.

Quando o conteúdo comprimido omitir informações necessárias à tarefa, use
`headroom_retrieve` para recuperar o original. Não interprete uma informação
omitida pela compressão como ausente no conteúdo original.

O setup do ambiente `dev` deve configurar automaticamente o MCP e o roteamento
de inferência pelo proxy Headroom. Preserve a configuração anterior para
restauração com `--disable`, sem migrar conversas existentes.

Esta convenção é a fonte durável para uso e configuração do Headroom. Use
[AGENTS.md](../AGENTS.md) como índice operacional e os READMEs da raiz como
entradas humanas, com resumos e referências a esta convenção.

## Convivência com context-mode

Use [context-mode](context-mode.md) para pesquisa, indexação, processamento de
saídas extensas e memória da sessão. Use as ferramentas MCP do Headroom quando
precisar comprimir conteúdo ou recuperar originais armazenados por ele.

O proxy atua sobre o tráfego de inferência do cliente configurado para usá-lo.
Essa integração complementa as ferramentas `ctx_*`; as regras de coleta e
preservação de contexto continuam em [context-mode.md](context-mode.md).

## Configuração operacional

A imagem instala `headroom-ai[proxy]==0.39.1` em um virtualenv isolado em
`/opt/headroom`. O extra `proxy` inclui as dependências do MCP. O executável
`/usr/local/bin/headroom` está no `PATH` do usuário `dev`.

As fontes operacionais da integração são:

- [docker/dev/Dockerfile](../docker/dev/Dockerfile): instalação da CLI e das dependências;
- [docker/dev/bin/setup-codex-headroom](../docker/dev/bin/setup-codex-headroom): configuração do MCP e ativação ou restauração do provider;
- [docker/dev/bin/start-headroom-proxy](../docker/dev/bin/start-headroom-proxy): inicialização e readiness do proxy;
- [.devcontainer/dev/devcontainer.json](../.devcontainer/dev/devcontainer.json): execução dos setups e inicialização do proxy;
- [docker/dev/.env.example](../docker/dev/.env.example): opções de runtime usadas como modelo para `docker/dev/.env`;
- [docker/dev/tests/test_headroom.py](../docker/dev/tests/test_headroom.py): validação da integração.

Consulte [environment.md](environment.md) para a topologia dos ambientes e
[README.md](../README.md) para o bootstrap do repositório.

## Relação com o upstream

Esta integração foi baseada no
[commit de referência](https://github.com/GustavoPeixoto/php-qa-scope/commit/11c33eee7c2c2fc7539f741e0853294c453eae9f).
Documentação upstream: [instalação](https://docs.headroomlabs.ai/docs/installation),
[proxy](https://docs.headroomlabs.ai/docs/proxy) e
[MCP](https://docs.headroomlabs.ai/docs/mcp).

## Inicialização e escopo

O Dev Container `dev`:

1. Executa `setup-codex-context-mode` e `setup-codex-headroom` no
   `postCreateCommand`. O segundo configura o MCP Headroom e seleciona o proxy
   como provider do Codex, salvando a configuração anterior e preservando a
   autenticação, os hooks e o histórico.
2. Executa `start-headroom-proxy` no `postStartCommand`, inclusive ao reiniciar um
   container existente. Aguarda readiness antes de concluir a inicialização.

Após a criação ou o rebuild, o roteamento já está configurado. Não há etapa
adicional de ativação manual.

O proxy escuta em `127.0.0.1:8787` dentro de `dev`; nenhuma porta é publicada no
host. O MCP é um processo stdio iniciado pelo Codex com
`headroom mcp serve --proxy-url http://127.0.0.1:8787`. A opção `--proxy-url`
permite recuperar originais comprimidos pelo proxy, além daqueles do próprio
MCP.

Após atualizar um clone existente, faça **Dev Containers: Rebuild Container**.
Arquivos `.env` existentes são preservados pelo bootstrap. O Compose carrega as
variáveis de `docker/dev/.env`; os scripts mantêm os defaults abaixo como
fallback quando essas variáveis estão ausentes ou vazias.

## Uso da CLI e do MCP

Dentro de `dev`:

```sh
headroom --version
headroom --help
headroom doctor
codex mcp list
```

O MCP oferece `headroom_compress`, `headroom_retrieve` e `headroom_stats`. A
compressão pelo MCP ocorre quando o agente chama essas ferramentas. O setup
configura separadamente o provider que redireciona as chamadas de inferência.

## Ativar e desativar o roteamento do Codex

O `postCreateCommand` executa o setup sem argumentos para usar o proxy na CLI
e na extensão Codex. Para reaplicar a configuração em um container existente:

```sh
start-headroom-proxy
setup-codex-headroom
```

O setup detecta login ChatGPT usando o helper da versão instalada do Headroom.
Quando não identifica esse login, usa `OPENAI_API_KEY` se essa variável estiver
exportada. Em um volume novo sem credenciais, prepara o provider para login
ChatGPT, que continua sendo feito pelo Codex. A escolha também pode ser explícita:

```sh
# Use depois de autenticar o Codex com sua conta ChatGPT.
setup-codex-headroom --auth chatgpt

# Exporte OPENAI_API_KEY no ambiente que iniciará a CLI/extensão.
setup-codex-headroom --auth api-key
```

O provider usa Responses API e anuncia suporte a WebSockets. Para login ChatGPT,
configura `requires_openai_auth=true`; para API key, configura
`env_key="OPENAI_API_KEY"`. A chave não é gravada pelo setup. Consulte também a
[configuração oficial do Codex](https://developers.openai.com/codex/config-advanced).

O setup salva o estado anterior em `~/.codex/config.toml.before-headroom`, com
permissões `0600`. Para desativar:

```sh
setup-codex-headroom --disable
```

A desativação restaura apenas os campos de roteamento que ainda pertencem à
integração, preservando configurações adicionadas depois. O MCP e o proxy
continuam disponíveis. Reiniciar o container executa apenas o start e mantém a
desativação. Criar ou reconstruir o container executa novamente o setup e reativa
o roteamento, assim como executar `setup-codex-headroom` sem argumentos.

O argumento `--enable` permanece como alias do setup padrão por compatibilidade;
ele não é necessário para ativar a integração.

Depois de ativar ou desativar, recarregue a extensão Codex e inicie uma nova
conversa. O setup não migra providers de conversas existentes nem altera os
bancos de histórico. Perfis que selecionam outro provider continuam usando
esse provider. O volume Docker `codex` é compartilhado e persistente: alterações
na configuração do usuário podem afetar outros workspaces que montam o mesmo
volume.

## Opções de runtime

Copie as opções desejadas de [.env.example](../docker/dev/.env.example) para `docker/dev/.env`
e recrie o container para atualizar seu ambiente:

| Variável | Default | Efeito |
| --- | --- | --- |
| `HEADROOM_SAVINGS_PROFILE` | `coding` | Perfil de compressão. |
| `HEADROOM_MODE` | `cache` | Modo do proxy; `token` prioriza remoção de tokens. |
| `HEADROOM_BEACON` | `off` | Desativa por padrão o beacon de upload anônimo no proxy e no MCP. |
| `HEADROOM_STARTUP_TIMEOUT` | `120` | Tempo máximo de inicialização, em segundos. |

Ao executar a imagem diretamente com `docker run`, passe
`--env-file docker/dev/.env` para carregar a mesma configuração de runtime.

O host e a porta são escolhas fixas desta integração. `HEADROOM_PYTHON` e
`HEADROOM_CLI` permitem usar outro executável nos testes. `CODEX_HOME` permite
configurar e testar um diretório isolado.

O setup do MCP copia `HEADROOM_BEACON` para o ambiente do servidor. Após mudar
essa opção em um container existente, execute `setup-codex-headroom` e recarregue
o Codex. Alterar opções do proxy exige reiniciar seu processo; executar o script
com um proxy pronto apenas reutiliza o processo atual.

## Diagnóstico e validação

```sh
curl --fail http://127.0.0.1:8787/readyz
curl --fail http://127.0.0.1:8787/stats
tail -n 50 "${CODEX_HOME:-/home/dev/.codex}/headroom/proxy.log"
/opt/headroom/bin/python docker/dev/tests/test_headroom.py
```

O script de inicialização usa `flock`, valida a identidade e readiness do serviço
e recusa uma porta ocupada por outro processo. Logs e PID ficam em
`${CODEX_HOME:-/home/dev/.codex}/headroom/`. Em caso de falha, consulte o log e
corrija a causa antes de repetir `start-headroom-proxy`.

Os testes usam um `CODEX_HOME` temporário e exercitam configuração, restauração,
autenticação, convivência com context-mode, inicialização concorrente e
compressão com recuperação via MCP. O teste de proxy exige a porta 8787 livre;
rode em um container de teste separado quando o proxy do workspace estiver em
execução. Nenhuma chamada de inferência paga é necessária. Para validar a conta
real, abra uma nova conversa depois do setup e confira streaming e aumento
dos contadores em `/stats`.
