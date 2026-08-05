---
name: skill-capture-feature
trigger: "capture feature" / "feature done" / "/capture"
description: "Called after every completed feature. Reads the new/changed code, extracts reusable patterns and decisions into the wiki, updates the TILA skill file, and logs the change. This is the mechanism that keeps the brain synchronized with the living codebase."
---

# Skill: Capture Feature

## When to invoke
Invoke this skill every time a feature, fix, or refactor is completed in TILA — regardless of size.
The dev assistant skill (`skill-dev-assistant.md`) calls this automatically on completion.

## Steps
1. Perguntar ao humano: "Qual foi a feature? Quais arquivos mudaram?" (ou ler o git diff se disponível).
2. Ler os arquivos modificados de `c:\Tila\Tila_BackEnd` ou `c:\Tila\Tila_Frontend`.
3. Escrever uma entrada de changelog em `raw/codebase/changelog/[YYYY-MM-DD]-[feature-slug].md`:
   - Nome e intenção da feature
   - Arquivos criados ou modificados (com descrição de uma linha para cada)
   - Padrões introduzidos (novo padrão de endpoint, novo formato de DTO, novo tipo de componente Angular, etc.)
   - Qualquer desvio das convenções existentes — flaggar claramente
4. Atualizar páginas em `wiki/concepts/` afetadas pela feature:
   - Se um novo endpoint foi adicionado → atualizar `wiki/concepts/api-endpoints.md`
   - Se uma nova entidade foi criada → criar `wiki/entities/[entity-name].md`
   - Se um novo padrão de componente Angular foi usado → atualizar `wiki/concepts/angular-patterns.md`
   - Se uma decisão de segurança foi feita → atualizar `wiki/concepts/security.md` e `context/security-lgpd.md`
5. Se a feature envolveu uma escolha arquitetural significativa, acionar `skill-adr.md`.
6. Atualizar `context/roadmap.md`: marcar o item completado, anotar novos blockers descobertos.
7. Acionar `skill-update-tila-skill.md` para manter o skill file do projeto atualizado.
8. Atualizar `index.md` e append em `log.md`:
   ```
   ## [YYYY-MM-DD HH:MM] capture | Feature: [nome]
   [Breve descrição da feature capturada e quais páginas wiki foram atualizadas.]
   ```
9. Perguntar: "Desejo sincronizar com Git agora? (`/salve`)"

## Rules
- Nunca copiar-colar código bruto na wiki — extrair apenas padrões e decisões.
- Se a feature introduziu uma mudança sensível à segurança (novo endpoint, nova role, novo campo de dados), SEMPRE atualizar `context/security-lgpd.md` e flaggar para review.
- Se uma convenção foi quebrada (e.g. `@Autowired` usado ao invés de constructor injection), registrar em `wiki/decisions/` como nota de desvio, não silenciosamente.
- O arquivo de changelog em `raw/codebase/changelog/` é imutável uma vez escrito — criar um novo arquivo para correções ao invés de editar.
- Se o git diff estiver disponível, usá-lo preferencialmente à descrição verbal do humano.
- Changelog deve ser escrito em formato técnico conciso, não prosa longa.
