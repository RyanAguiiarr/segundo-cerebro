---
name: skill-generate-laudo
trigger: "gerar laudo" / "generate laudo"
description: "Generate a medical report draft (pré-laudo) from exam data, using wiki context and the médico's historical patterns."
---

# Skill: Generate Laudo (Pré-Laudo)

## Context
The TILA pipeline: DICOM image + clinical notes → pre-laudo draft → médico reviews and signs.
This skill handles the LLM portion of that pipeline.

## Steps
1. Load `wiki/concepts/` pages relevant to the exam type.
2. Load `wiki/entities/[medico-name].md` if it exists — to apply their style patterns.
3. Load previous approved laudos for this exam type from `wiki/outputs/laudos/` if available.
4. Generate the pré-laudo draft in structured sections:
   - **Exame**: [type, date, equipment]
   - **Técnica**: [acquisition protocol]
   - **Achados**: [structured findings, neutral language]
   - **Impressão diagnóstica**: [interpretation, differential]
   - **Observações**: [limitations, follow-up recommendations]
5. Append disclaimer: "⚠️ Este é um rascunho gerado por IA. Revisão e assinatura do médico responsável são obrigatórias antes de qualquer uso clínico."
6. Ask: "File this draft to `wiki/outputs/laudos/[date]-[exam-type].md`?"

## Output format
```markdown
---
title: "Pré-Laudo: [Tipo de Exame] — [Data]"
type: output
tags: [laudo, pre-laudo, exam-type]
sources: []
last_updated: YYYY-MM-DD
---

# Pré-Laudo: [Tipo de Exame]

## Exame
- **Tipo**: [tipo do exame]
- **Data**: [data]
- **Equipamento**: [equipamento utilizado]

## Técnica
[Protocolo de aquisição utilizado]

## Achados
[Achados estruturados em linguagem neutra e técnica]

## Impressão Diagnóstica
[Interpretação e diagnóstico diferencial]

## Observações
[Limitações do exame, recomendações de seguimento]

---

> ⚠️ Este é um rascunho gerado por IA. Revisão e assinatura do médico responsável são obrigatórias antes de qualquer uso clínico.

## Backlinks
```

## Rules
- Never invent findings not present in the source data.
- Never include real patient identifiers.
- Always use neutral, technical Portuguese medical language.
- Confidence must be explicitly stated if findings are ambiguous.
- Always include the AI disclaimer at the end.
- If the médico has a documented style in `wiki/entities/`, adapt the language register to match.
- If prior approved laudos exist for this exam type, reference their structural patterns.
