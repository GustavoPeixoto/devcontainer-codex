---
id: workflow
title: Convenção de fluxo de trabalho
when: Sempre que explorar, planejar, propor ou aplicar mudanças no projeto.
---

# Convenção de fluxo de trabalho

## Regra geral

Antes de explorar, planejar, propor ou aplicar mudanças relevantes no projeto, OpenSpec-first deve ser sugerido. Isso inclui alterar documentos duráveis, criar novas áreas de documentação, mudar convenções, revisar decisões de marca ou produzir artefatos finais que possam virar fonte da verdade.

## Ciclo de vida

1. Explorar: entender contexto, riscos e alternativas antes de consolidar a direção.
2. Propor: criar ou atualizar uma change OpenSpec com proposta, design quando necessário, specs e tarefas.
3. Aplicar: implementar as tarefas da change nos arquivos versionados.
4. Arquivar: quando a change estiver concluída, sincronizar specs e arquivar a mudança.
5. Commitar: registrar em Git o resultado revisado.

## Continuidade entre contextos

Etapas do ciclo OpenSpec frequentemente acontecem em chats, sessões ou contextos diferentes. Por isso, artefatos de change e handoffs devem ser claros o suficiente para que outro agente continue o trabalho sem grandes inferências ou dependência de memória conversacional.

Ao deixar uma change pronta para a próxima etapa, registre intenção, escopo, decisões tomadas, riscos conhecidos, pendências e próximos passos nos artefatos versionados ou no handoff apropriado.

## Autossuficiência dos artefatos de change

Ao criar, revisar, atualizar, aplicar ou preparar o arquivamento de uma change, valide se `proposal.md`, `design.md`, specs e `tasks.md` permanecem compreensíveis sem depender de arquivos temporários, não versionados ou externos ao OpenSpec.

Quando uma referência a insumo não durável ou não versionado for necessária para entender escopo, decisões, riscos, requisitos ou tarefas, destile o conteúdo relevante e reproduza-o nos próprios artefatos da change. Referências a esses arquivos podem permanecer apenas como proveniência ou trilha contextual.

## Ao propor uma change

Depois de executar a etapa de propose e gerar ou atualizar artefatos, valide a paridade entre o que foi planejado e o que foi produzido. Confira se `proposal.md`, `design.md`, specs e `tasks.md` refletem o escopo, requisitos, decisões, riscos, tarefas e pontos em aberto relevantes.

Valide também as referências dos artefatos gerados. Confira se links ou menções a handoffs temporários, arquivos não versionados ou contexto externo são apenas proveniência; se forem necessários para compreender a change, reproduza o conteúdo relevante nos artefatos antes de considerar a proposta pronta.

Todo `proposal.md` deve terminar com `## Open Questions`. A seção deve listar os pontos em aberto relevantes antes da aplicação da change e incluir prioridade, criticidade ou importância para cada item. Quando não houver pendências relevantes, declare isso explicitamente.

## Sintaxe OpenSpec

Mesmo quando o conteúdo estiver em PT-BR, preserve a sintaxe exigida pelo OpenSpec:

- headings como `## Why`, `## What Changes`, `## ADDED Requirements`, `## MODIFIED Requirements` e `## REMOVED Requirements`;
- palavras normativas como `MUST` e `SHALL`;
- blocos de cenário iniciados por `#### Scenario`;
- bullets de cenário com `WHEN`, `THEN`, `AND` ou outros marcadores esperados;
- nomes de capabilities, IDs de changes e caminhos de arquivos.

## Ao aplicar uma change

- leia as instruções dinâmicas do OpenSpec antes de editar;
- leia todos os arquivos de contexto indicados;
- implemente tarefas em ordem quando isso reduzir ambiguidade;
- marque cada tarefa como concluída assim que ela for finalizada;
- pause se uma tarefa estiver ambígua ou se a implementação revelar problema de design;
- valide a change antes de considerar o trabalho pronto.
