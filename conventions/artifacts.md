---
id: artifacts
title: Convenção de artefatos
when: Sempre que precisar entender, criar, usar, mover, versionar, referenciar ou destilar artefatos, insumos, handoffs, rascunhos, `tmp/` ou fontes de verdade.
---

# Convenção de artefatos

## Definição

Artefatos são insumos, documentos, specs, convenções, decisões, handoffs, rascunhos e entregáveis usados para conduzir o trabalho do projeto.

Esta convenção separa artefatos duráveis e versionáveis de artefatos transitórios. Essa separação evita que decisões importantes dependam de memória conversacional, arquivos temporários ou contexto externo ao repositório.

## Artefatos duráveis

Artefatos duráveis são fontes de verdade versionadas. Eles devem conter o contexto necessário para que outra pessoa ou agente consiga continuar o trabalho sem depender de arquivos temporários.

Exemplos:

- `README.md`;
- `AGENTS.md`;
- `conventions/`;
- `openspec/`;
- documentação final;
- decisões consolidadas;
- specs, propostas, designs e tarefas OpenSpec.

## Artefatos transitórios

Artefatos transitórios são materiais de apoio. Eles podem orientar exploração, revisão e implementação, mas não devem ser tratados como fonte de verdade durável.

Use `tmp/` para insumos temporários, como:

- handoffs;
- rascunhos;
- notas de exploração;
- dumps;
- arquivos de apoio;
- materiais ainda não destilados.

Conteúdo em `tmp/` deve permanecer ignorado pelo Git, exceto marcadores estruturais como `tmp/.gitkeep`.

## Destilação de insumos

Quando um artefato transitório for necessário para entender escopo, decisão, requisito, risco ou tarefa, destile o conteúdo relevante para um artefato durável.

Referências a arquivos transitórios podem permanecer como proveniência, mas o entendimento principal deve estar no artefato durável correspondente.

## Uso em mudanças OpenSpec

Artefatos de change devem ser autossuficientes. `proposal.md`, `design.md`, specs e `tasks.md` não devem depender de handoffs, rascunhos ou arquivos temporários para serem compreendidos.

Antes de considerar uma change pronta, revise se insumos transitórios relevantes foram incorporados aos artefatos OpenSpec aplicáveis.
