---
id: language
title: Convenção de idioma
when: Sempre ao atuar neste repositório; esta convenção define o idioma padrão da conversa, do contexto do projeto e dos artefatos.
---

# Convenção de idioma

## Regra padrão

Use PT-BR como idioma padrão para:

- artefatos de mudanças OpenSpec;
- handoffs;
- documentos do projeto;
- prompts e notas internas versionadas;
- rascunhos de conteúdo profissional, salvo quando o objetivo declarado for outro idioma.

## Exceções

Use outro idioma quando:

- o usuário pedir explicitamente;
- a change OpenSpec definir que o artefato final deve estar em outro idioma;
- o conteúdo for uma versão localizada, como currículo ou perfil em inglês;
- nomes próprios, termos técnicos, APIs, comandos ou sintaxe de ferramentas exigirem o idioma original.

A exceção vale para o artefato específico pedido. Ela não altera o idioma padrão do repositório.

## Conteúdo e sintaxe de ferramenta

Idioma do conteúdo e sintaxe obrigatória são coisas diferentes. O texto explicativo pode estar em PT-BR, mas a estrutura exigida por ferramentas deve permanecer no formato esperado.

Em OpenSpec:

- preserve headings estruturais como `## Why`, `## What Changes`, `## ADDED Requirements` e `#### Scenario`;
- preserve palavras normativas exigidas, como `MUST` e `SHALL`;
- preserve marcadores de cenário, blocos de código, caminhos, comandos e identificadores;
- não traduza nomes de arquivos, comandos, flags, schemas ou IDs.

Quando houver dúvida, mantenha a sintaxe da ferramenta intacta e escreva apenas o conteúdo humano em PT-BR.
