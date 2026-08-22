---
id: context-mode
title: Convenção de context-mode
when: Sempre que usar context-mode, ferramentas `ctx_*`, hooks do Codex, retomada após compactação ou investigação com saídas potencialmente grandes.
---

# Convenção de context-mode

## Regra geral

Use context-mode para preservar a janela de contexto durante desenvolvimento assistido por IA.

Quando a intenção for analisar, filtrar, contar, comparar, resumir, buscar, transformar ou agregar dados, prefira executar a análise em ferramenta `ctx_*` e retornar apenas o resultado derivado. Evite despejar saídas extensas, HTML bruto, logs longos, dumps ou arquivos grandes diretamente na conversa.

Shell comum continua apropriado para comandos curtos, mutações de estado, validações locais, servidores, instalações, Git e leituras feitas especificamente para editar um trecho de arquivo.

## Relação com o upstream

Esta convenção é baseada nas regras de roteamento do context-mode para Codex em <https://github.com/mksglu/context-mode/blob/main/configs/codex/AGENTS.md>, mas não é uma cópia literal do upstream. Ao atualizar o context-mode, compare com esse arquivo e incorpore apenas regras compatíveis com este repositório.

## Retomada de contexto

Ao retomar uma sessão, continuar depois de compactação ou precisar lembrar decisões anteriores, pesquise a base do context-mode antes de perguntar novamente ao usuário.

Use `ctx_search` com `sort: "timeline"` para recuperar decisões, planos, bloqueios, erros, abordagens rejeitadas e guias de compactação já capturados.

Depois de `/clear` ou `/compact`, trate a base de conhecimento do context-mode como preservada. Use `ctx purge` apenas quando o usuário pedir explicitamente para limpar a base.

## Coleta e análise

Use `ctx_batch_execute` quando precisar rodar múltiplos comandos de investigação relacionados. Dê labels descritivos aos comandos e inclua as queries necessárias no mesmo round trip quando possível.

Use `ctx_execute` ou `ctx_execute_file` quando a tarefa for processar dados ou arquivos e o conteúdo bruto não precisar entrar na conversa. O código deve imprimir somente a resposta necessária.

Use busca textual comum, como `rg`, quando a saída esperada for pequena e diretamente observável. Se a saída crescer ou exigir sumarização, redirecione para context-mode.

## Rede e conteúdo externo

Evite `curl`, `wget` e fetches inline que tragam respostas grandes diretamente para o contexto. Para páginas, APIs ou documentos externos, prefira ferramentas de busca, indexação ou processamento que devolvam apenas trechos relevantes ou sínteses verificáveis.

Quando a resposta depender de fonte externa recente ou instável, verifique a informação com fonte apropriada e registre links usados na resposta.

## Comandos de manutenção

Quando o usuário pedir:

- `ctx stats`: chame a ferramenta de estatísticas do context-mode e mostre a saída;
- `ctx doctor`: chame o diagnóstico do context-mode e apresente o checklist;
- `ctx upgrade`: chame a ferramenta de upgrade, execute o comando retornado e oriente reinício da sessão;
- `ctx purge`: confirme o escopo antes de limpar, porque a ação é destrutiva.

## Configuração operacional

A configuração operacional do context-mode para Codex neste projeto vive no ambiente `dev`:

- `docker/dev/.codex/config.toml` declara hooks e servidor MCP;
- `docker/dev/.codex/hooks.json` declara os hooks do Codex;
- `docker/dev/bin/setup-codex-context-mode` mescla a configuração em `~/.codex`;
- `.devcontainer/dev/devcontainer.json` executa o setup no `postCreateCommand`;
- `README.md` documenta o review manual dos hooks quando um volume novo é criado.

Não duplique essa configuração em `AGENTS.md`. Use `AGENTS.md` como índice operacional e esta convenção como fonte durável para as regras de uso.
