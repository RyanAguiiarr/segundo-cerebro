# CLAUDE.md â€” Tila_Brain v2
> Rewritten: 2026-06-09
> This file governs all agent behavior in Tila_Brain.
> Read it completely before every session. No exceptions.

## On session start
1. Read this file completely
2. Read 00-Index/SOUL.md â€” internalize before doing anything
3. Read index.md â€” understand current state of the brain
4. Read log.md last 10 entries â€” understand what happened recently
5. Read 01-Negocio/contexto/roadmap.md â€” understand current priorities
6. Announce: "Tila_Brain v2 loaded. [N] permanent notes. [N] patterns. Last: [date]."

---

## Â§1 â€” Identity
You are the Tila agent. Read 00-Index/SOUL.md now.
Your non-negotiables are defined there. They override everything else.

---

## Â§2 â€” Business knowledge layer (Breno method)

### Where knowledge lives
- `01-Negocio/inbox/` â€” raw, unvalidated notes. Agent NEVER reads these as truth.
- `01-Negocio/permanent/` â€” validated knowledge. Agent trusts these.
- `00-Index/mocs/` â€” navigation maps. Read before exploring a cluster.

### Rules for this layer
- NEVER write to 01-Negocio/permanent/ without running skill-gate-validacao first
- Titles must be theses (assertions), never labels
- Every permanent note must link to at least one other permanent note
- AI writes DRAFTS. Human promotes drafts to permanent after review.
- "The density of the graph is not intelligence." â€” Breno Vieira

### Writing a new permanent note
1. Write draft in 01-Negocio/inbox/[slug]-DRAFT.md
2. Run skill-gate-validacao
3. If gate passes: move to appropriate permanent/ subfolder, update index.md
4. If gate fails: append ## Gate Failures section with specific fixes needed
5. Run skill-moc-update after any batch of new permanent notes

---

## Â§3 â€” Code knowledge layer (Breno method)

### Where code knowledge lives
- `03-Codebase/snapshots/` â€” point-in-time audits. Immutable once written.
- `03-Codebase/patterns/` â€” verified coding patterns as permanent thesis notes.
- `03-Codebase/changelog/` â€” feature capture log (written by /capture).

### Rules for this layer
- ALWAYS run skill-graphify-query before ANY interaction with code (creating, modifying, diagnosing, refactoring, migrating)
- The Graphify is OMNIPRESENT — it guides feature creation, bug diagnosis, refactoring, migration AND blast radius
- NEVER suggest modifying a class without knowing its dependents
- Patterns in 03-Codebase/patterns/ must be verified in real files — no assumptions
- After every feature: /capture → gate on extracted patterns → graphify rebuild (`graphify . --update`)
- Read 00-Index/manual-contexto-graphify.md for the full Graphify Knowledge Base

### Code query protocol (Graphify-first)
Any question about code → skill-graphify-query → context from graph → then answer
New feature or idea → skill-graphify-query (find optimal coupling point) → then propose
Bug or diagnostic → skill-graphify-query (trace end-to-end flow) → then diagnose
Refactor or migration → skill-graphify-query (map dependencies) → then plan
Code change → skill-graphify-query (blast radius) → report → await human confirmation → then implement
Architecture question → read relevant ADR in 02-Arquitetura_ADRs/
What exists question → read 03-Codebase/snapshots/ most recent audit

---

## §4 — Operation layer (Okamoto method)

### Skills (how I act)
See 05-Skills_Agentes/ for all available skills.

#### Session Pipeline (Fluxo do Programador)
The programmer workflow follows a strict pipeline. EVERY coding session MUST follow this flow:

```
/boot → [programação com recorder ativo] → /arch-review → [codificar] → /capture → /close (organiza + commit + push)
```

| Phase | Skill | Trigger | What it does |
|---|---|---|---|
| 🟢 START | skill-session-boot | `/boot` or session start | Loads SOUL, index, logs, roadmap, pipeline, snapshots, last session, pending items. Creates session file. |
| 🔵 DURING | skill-session-recorder | automatic | Records EVERYTHING: ideas, features, bugs, decisions, code changes, UI changes. Nothing escapes. |
| 🔵 DURING | skill-arch-review | before coding any idea | Analyzes idea via arch-thinker + Graphify + ADRs. Produces APPROVE/ADJUST/REJECT verdict. |
| 🔵 DURING | skill-dev-assistant | while coding | Governance layer: checklists, conventions, anti-patterns, security. |
| 🔵 DURING | skill-graphify-query | before ANY code interaction | **Omnipresent context engine.** Diagnoses bugs, finds optimal coupling for features, maps refactoring/migration paths, AND calculates blast radius. MANDATORY for everything. |
| 🔴 END | skill-session-close | `/close` or `/salve` | Processes session, runs organizer, verifies links, generates report, **auto git add + commit + push**. |

#### External Skills (used during coding)
- `arch-thinker` (Tila_Frontend/.agent/skills/) — Architecture thinking framework
- `java-spring-modern-reviewer` (.claude/skills/) — Java/Spring Boot code review
- `angular-modern-reviewer` (.claude/skills/) — Angular code review

#### Knowledge Skills
- skill-gate-validacao — before ANY permanent note
- skill-capture-feature (/capture) — after every feature
- skill-ingest (/ingest) — to ingest new knowledge sources
- skill-generate-laudo — for pré-laudo generation
- skill-adr — for architectural decisions
- skill-moc-update — after new permanent notes
- skill-query — to answer questions against the wiki

### Crons (when I act autonomously)
See 06-Automacoes/crons/_cron-registry.md for the full schedule.
Key crons: weekly-digest (Monday), lint-wiki (Sunday), gate-inbox (Monday)

### Session rhythm (MANDATORY)
```
1. /boot        → Load brain state, create session file, announce briefing
2. [work]       → Code, discuss, decide — recorder captures EVERYTHING
3. /arch-review → Before implementing any non-trivial idea (uses arch-thinker + graphify)
4. [code]       → Write code following dev-assistant checklists and graphify blast radius
5. /capture     → After each feature is done
6. /close       → End session: organize brain, verify links, auto commit + push
```

> ⚠️ RULE: /close is the FINAL step. It automatically runs brain-organizer,
> presents a summary, asks for confirmation, and then executes `git add . && git commit && git push` on Tila_Brain.
> The programmer does NOT need to commit manually.

> ⚠️ RULE: If a programmer starts coding without /boot, silently execute boot first.
> ⚠️ RULE: If a programmer tries to close without /close, alert them.

---

## Â§5 â€” Learning layer (Karpathy method)

### Where raw knowledge lives
- `07-Raw/` â€” immutable source documents. Agent reads, never modifies.
  - 07-Raw/articles/ â€” web articles
  - 07-Raw/videos/ â€” YouTube transcripts
  - 07-Raw/laudos/ â€” anonymized medical reports
  - 07-Raw/assets/ â€” images
  - 07-Raw/sessions/ — programming session logs (created by skill-session-boot)

### Ingest protocol (/ingest [source])
1. Read the source in 07-Raw/
2. Discuss 2-3 key takeaways with the human BEFORE writing anything
3. Propose draft notes for 01-Negocio/inbox/ (human approves)
4. Run skill-gate-validacao on each proposed note
5. Update index.md and log.md after any promotion to permanent/

### Index and log conventions
index.md â€” catalog of ALL permanent notes + patterns + ADRs + snapshots
log.md â€” append-only. Format: ## [YYYY-MM-DD HH:MM] action | description

---

## Â§6 â€” Core constraints (never violate)

1. Never modify files in 07-Raw/ â€” immutable source truth
2. Never write to 01-Negocio/permanent/ without gate passing
3. Never suggest code changes without checking blast radius first
4. Never expose real patient data â€” always synthetic in examples
5. Never invent medical facts â€” mark as "âš ï¸ Unverified â€” source needed"
6. Never ignore an ADR â€” if a decision conflicts with an existing ADR, flag it
7. Always update index.md and log.md after any wiki change
8. LGPD is a hard constraint â€” flag every violation, never rationalize it

---

## §7 — Hermes Autonomy Mode (Agente Autônomo)

Quando o Hermes estiver operando (agente autônomo), as seguintes regras se aplicam, tornando automáticas as rotinas que para o programador são manuais:
1. **Boot Inicial Automático**: Ao iniciar o trabalho, o Hermes já lê o cérebro (SOUL, index, log, roadmap) para carregar seu contexto inicial.
2. **Consultas Proativas**: `skill-graphify-query` e `skill-dev-assistant` rodam automaticamente durante o trabalho — o agente não espera ser instruído a usá-las.
3. **Critério de Registro**: 
   - **Sempre registrar**: decisões arquiteturais (`skill-adr`) e features completas (`skill-capture-feature`).
   - **Registrar se relevante**: ideias descartadas com razão, correções de rumo, novos padrões identificados (se for importar no futuro).
   - **Não registrar**: passos intermediários, tentativas/erros de sintaxe ou ruído inútil.
4. **Fechamento Automático de Ciclo**: Ao finalizar uma funcionalidade ou correção, o Hermes executa as rotinas de fechamento autonomamente (cria/edita/linka notas, roda `skill-gate-validacao`, atualiza `index.md`, e finaliza com `skill-session-close` e commit/push via `brain-sync.ps1`). 
O ciclo só termina quando o cérebro está atualizado e sincronizado.

---

## TILA-Specific Coding Rules (quick reference)

### Backend
- All responses: `ResponseEntity<GenericResult<T>>`
- DTOs: Java records with Bean Validation
- Services: constructor injection only (no @Autowired field)
- Write operations: @Transactional required
- Read operations: @Transactional(readOnly=true)
- Passwords: BCryptPasswordEncoder
- Secrets: environment variables only â€” NEVER in application.properties

### Frontend
- All components: standalone (no NgModule)
- State: Angular Signals (via stores)
- DI: inject() function
- Guards/interceptors: functional
- CSS: vanilla only â€” never Tailwind
- API calls: withCredentials=true (cookie transport)

### Medical domain
- AI generates DRAFTS â€” human always reviews
- Never store real patient data in examples
- Laudos must include "human review required" disclaimer
- LGPD compliance is non-negotiable

## Paths (verified 2026-06-18)

| Repo | Path |
|---|---|
| Brain root | `c:\Users\ryanc\Second_brain\projetos\tila` |
| Backend | `c:\Tila\Tila_BackEnd` |
| Frontend | `c:\Tila\Tila_Frontend` |
| Graphify Manual | `c:\Users\ryanc\Second_brain\projetos\tila\00-Index\manual-contexto-graphify.md` |

---

## §8 — Integração com o Segundo Cérebro Raiz (Governança Extendida)

A partir da integração ao Segundo Cérebro Pessoal:
1. **Extensão de Regras para Conteúdo NOVO:** Qualquer nota **nova** criada no Tila Brain deve seguir as regras globais de captura (_CLAUDE.md raiz - Fase 2), frescor OKM (Fase 3) e vínculo (Fase 4). Estas regras **não se aplicam retroativamente** ao acervo pré-existente.
2. **Tag de Área Obrigatória em Novas Notas:** Toda nova nota deve conter `area: [tila]` no frontmatter para indexação pelo ponteiro central em [`mocs/tila.md`](file:///c:/Users/ryanc/Second_brain/mocs/tila.md).
3. **Cofre por Projeto (`OBSIDIAN_VAULT_PATH`):** No repositório de código do Tila, o arquivo `.claude/settings.json` local deve configurar `"OBSIDIAN_VAULT_PATH": "c:/Users/ryanc/Second_brain/projetos/tila"`.
4. **Preservação de Estrutura Interna:** A organização em pastas (`00-Index`, `01-Negocio`, `02-Arquitetura_ADRs`, etc.) permanece intacta sem reorganizações ou alterações destrutivas automáticas.

