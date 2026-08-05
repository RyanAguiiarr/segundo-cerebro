---
id: dec-2026-08-04-arquitetura-segundo-cerebro
type: decision
subtype: ""
area:
  - carreira
  - estudos
created: 2026-08-04
updated: 2026-08-04
freshness: atemporal
confidence: alta
source: conversa
tags:
  - decision
  - arquitetura
  - segundo-cerebro
contexto: "Necessidade de estruturar um cérebro pessoal abrangendo toda a vida (saúde, finanças, carreira, estudos) integrando o sub-cérebro técnico Tila de forma leve sem refatorar seu acervo pré-existente."
decisao: "Adotar a arquitetura baseada no motor open-source obsidian-second-brain com organização por tipos em wiki/, hubs MOCs em mocs/ e sub-vault isolado em projetos/tila/."
alternativas_consideradas:
  - "Usar presets padrão do skill (executivo/construtor) — rejeitado por não cobrir vida inteira + sub-cérebro aninhado."
  - "Reconstruir/refatorar o Tila Brain na mesma estrutura do cérebro raiz — rejeitado para evitar churn desnecessário."
consequencias: "Garantia de zero notas duplicadas por tipo, preservação da estrutura histórica do Tila e controle estrito de frescor OKM."
reversivel: sim
revisitar_em: 2026-11-04
formal: true
relations:
  - type: gerou
    target: "[[mocs/tila]]"
  - type: referencia
    target: "[[GOVERNANCA]]"
---

## Para o Claude futuro
Esta nota de decisão documenta a escolha arquitetural de construção do Segundo Cérebro Pessoal com IA e a integração do sub-vault Tila Brain em `projetos/tila/`. Consulte esta nota ao planejar novas integrações de sub-vaults ou alterações na taxonomia por tipo em `wiki/`.

## Contexto & Problema
O usuário precisava de um sistema de conhecimento persistente para a vida inteira (cobrindo saúde, finanças, carreira, compromissos, relacionamentos e estudos) que também permitisse integrar de forma nativa o seu cérebro técnico pré-existente (Tila Brain).

## Decisão Tomada
Adotou-se o motor open-source `obsidian-second-brain` com uma arquitetura customizada em 11 fases:
1. **Organização por Tipos em `wiki/`:** Existence check pré-criação único por tipo de nota para eliminar duplicatas.
2. **Hubs por Área em `mocs/`:** MOCs atuam como agregadores de área.
3. **Sub-Vault Aninhado `projetos/tila/`:** Encaixe leve sem refatorar as notas pré-existentes do Tila.
4. **Governança OKM & Frescor:** Fatos voláteis mantidos obrigatoriamente como ponteiros com carimbo de recência.

## Alternativas Consideradas
- **Usar os 4 Presets de Bootstrap Padrão do Skill:** Rejeitado pois nenhum cobria a combinação de vida inteira + sub-cérebro aninhado.
- **Refatorar o Tila Brain para o Schema Raiz:** Rejeitado para evitar reescrita destrutiva de notas funcionais.

## Consequências & Trade-offs
- **Positivo:** Zero duplicação de entidades por grafia, histórico preservado e rastreabilidade bitemporal.
- **Trade-off:** Exige manutenção de ponteiros limpos no MOC raiz [`mocs/tila.md`](file:///c:/Users/ryanc/Second_brain/mocs/tila.md).
