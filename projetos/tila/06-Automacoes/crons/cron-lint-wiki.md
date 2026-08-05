---
name: cron-lint-wiki
trigger: "/lint" (autonomous) or automatic every Sunday
description: "Verificação autônoma de saúde da wiki — sem interação, arquiva relatório automaticamente."
---

# Cron: Lint Wiki (Autônomo)

## Schedule
Executar todo domingo ou sob demanda com `/lint` (modo autônomo).

## Diferença do Skill
Este é o modo **autônomo** do lint. O `skill-lint.md` é interativo (pergunta ao humano o que corrigir). Este cron executa sem interação, registra os resultados, e NÃO corrige nada.

## Steps (Autônomo — sem interação)

1. **Ler todas as páginas** em `wiki/concepts/`, `wiki/entities/`, `wiki/decisions/`, `wiki/sources/`.

2. **Executar os 7 checks** (mesmos do `skill-lint.md`):
   - Contradições entre páginas
   - Claims obsoletos (baseado em `last_updated` vs fontes)
   - Páginas órfãs (sem inbound links)
   - Conceitos sem página própria (mencionados 3+ vezes sem `[[]]`)
   - Cross-references ausentes ou quebradas
   - LGPD gaps (comparar com `context/security-lgpd.md`)
   - ADR coverage (decisões sem ADR formal)

3. **Gerar relatório** com tabela de resumo e detalhes por check.

4. **Arquivar automaticamente** em `wiki/outputs/lint-YYYY-MM-DD.md`:
```yaml
---
title: "Lint Report — YYYY-MM-DD"
type: output
tags: [lint, health-check, cron]
sources: []
last_updated: YYYY-MM-DD
---
```

5. **Atualizar `index.md`** com a nova página de output.

6. **Atualizar `crons/_cron-registry.md`** — campo "Last Run" do `lint-wiki`.

7. **Append em `log.md`**:
```
## [YYYY-MM-DD HH:MM] lint | Cron Lint — [N] issues found
[Resumo: X contradições, Y órfãs, Z LGPD gaps.]
```

## Severity Classification
- 🔴 **Crítico**: LGPD gaps, dados sensíveis expostos
- 🟡 **Atenção**: Contradições, claims obsoletos
- 🟢 **Info**: Páginas órfãs, cross-refs ausentes

## Rules
- Execução 100% autônoma — NUNCA perguntar, NUNCA corrigir.
- Se encontrar issues 🔴 (críticas), colocar no TOPO do relatório em destaque.
- Comparar com o último lint report (se existir) para mostrar evolução.
