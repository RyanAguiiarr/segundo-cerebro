---
name: skill-gate-validacao
trigger: "gate" / "validar nota" / before any write to negocio/permanent/
description: "Applies the 6-question gate before any note enters permanent/. The agent MUST call this skill before writing any permanent note."
---

# Skill: Gate de Validação

## The 6 questions
For any candidate note, answer each:

1. **ATOMIC?** Can this be split into two separate ideas?
   → If yes: split first, gate each separately.

2. **AUTHORED?** Is the content in the author's own words?
   → AI suggestions are DRAFTS. The human rewrites before promotion.
   → Exception: codebase/patterns/ notes may summarize code directly.

3. **TITLE IS THESIS?** Is the title an assertion (true/false), not a label?
   → BAD: "JWT Authentication"
   → GOOD: "JWT com HttpOnly cookie protege TILA contra XSS melhor que localStorage"

4. **CONNECTS?** Does it link to at least one other permanent note?
   → Add [[link]] before promoting. Orphan notes are prohibited.

5. **UNIQUE?** Does a note with this thesis already exist?
   → Check index.md before writing. Merge if duplicate.

6. **HAS METADATA?** Does it have YAML frontmatter with type, domain, date?
   → Add frontmatter if missing.

## Output
Print gate result for each question: ✅ PASS or ❌ FAIL [reason]
If all 6 pass: "✅ Gate passed — promoting to permanent/"
If any fail: "❌ Gate failed — returning to inbox/ — fix: [specific instruction]"
