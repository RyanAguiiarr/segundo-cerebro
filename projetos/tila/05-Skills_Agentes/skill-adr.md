---
name: skill-adr
trigger: "record decision" / "adr" / "decisão arquitetural"
description: "Record an Architecture Decision Record for TILA."
---

# Skill: Architecture Decision Record (ADR)

## Context
Decisões arquiteturais significativas devem ser documentadas formalmente para manter a rastreabilidade. Um ADR captura o contexto, a decisão, as alternativas consideradas e as consequências.

## Steps
1. Perguntar ao humano (ou extrair do contexto):
   - **Título**: nome curto para a decisão
   - **Contexto**: por que esta decisão foi necessária
   - **Decisão**: o que foi decidido
   - **Alternativas consideradas**: o que mais foi avaliado
   - **Consequências**: o que muda como resultado (positivo e negativo)
2. Auto-atribuir o próximo número de ADR lendo `wiki/decisions/` e encontrando o maior `NNN` existente.
3. Escrever `wiki/decisions/ADR-[NNN]-[slug].md` com o template abaixo.
4. Atualizar `index.md` — tabela de decisions.
5. Append em `log.md`:
   ```
   ## [YYYY-MM-DD HH:MM] adr | ADR-NNN: [Título]
   [Breve descrição da decisão registrada.]
   ```
6. Verificar se alguma ADR existente é **superseded** por esta nova decisão. Se sim, atualizar o status da ADR antiga para `Superseded by ADR-NNN`.

## Template ADR
```markdown
---
title: "ADR-NNN: [Título]"
type: decision
tags: [architecture, adr]
sources: []
last_updated: YYYY-MM-DD
---

# ADR-NNN: [Título]

## Status
Accepted

## Context
[Por que esta decisão foi necessária — problema, restrições, drivers.]

## Decision
[O que foi decidido — declaração clara e direta.]

## Alternatives Considered

### Alternativa 1: [Nome]
[Descrição e razão pela qual foi rejeitada.]

### Alternativa 2: [Nome]
[Descrição e razão pela qual foi rejeitada.]

## Consequences

### Positivas
- [Consequência positiva 1]
- [Consequência positiva 2]

### Negativas
- [Consequência negativa 1]
- [Consequência negativa 2]

### Riscos
- [Risco identificado]

## Backlinks
```

## Rules
- Todo ADR deve ter status: `Accepted`, `Superseded`, ou `Deprecated`.
- Se uma decisão contradiz um ADR existente, FLAGGAR o conflito antes de prosseguir.
- ADRs são imutáveis uma vez aceitos — para mudar uma decisão, criar um novo ADR que supersede o anterior.
- Sempre cross-referenciar com `context/coding-conventions.md` e `context/security-lgpd.md` quando aplicável.
- O slug deve ser kebab-case e descritivo: `ADR-002-pagination-server-side.md`.
