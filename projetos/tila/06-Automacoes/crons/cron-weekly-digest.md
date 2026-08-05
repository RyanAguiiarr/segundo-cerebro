---
name: cron-weekly-digest
trigger: "/digest" or automatic every Monday
description: "Gera um resumo semanal do crescimento da wiki e questões em aberto."
---

# Cron: Weekly Digest

## Schedule
Executar toda segunda-feira ou sob demanda com `/digest`.

## Steps (Autônomo — sem interação)

1. **Ler `log.md`** — filtrar entradas dos últimos 7 dias.

2. **Ler `index.md`** — contar total de páginas por categoria.

3. **Produzir digest** cobrindo:

### Seção 1 — Fontes Ingeridas
- Listar todas as fontes ingeridas na semana.
- Para cada: título, tipo, e quantas páginas wiki foram criadas/atualizadas.

### Seção 2 — Páginas Wiki
- Novas páginas criadas esta semana (com links).
- Páginas atualizadas esta semana (com resumo da mudança).
- Total de páginas no wiki: [N] (variação: +X desde último digest).

### Seção 3 — ADRs Registradas
- Novas decisions registradas.
- ADRs que foram superseded.

### Seção 4 — Features Capturadas
- Features completadas e capturadas via `skill-capture-feature`.
- Impacto no roadmap (items completados).

### Seção 5 — Questões em Aberto
- Questões não respondidas levantadas durante a semana.
- Items do roadmap que estão bloqueados.
- Decisões pendentes de `context/roadmap.md`.

### Seção 6 — Health Score
Atribuir um score qualitativo:
- 🟢 **Saudável**: Wiki crescendo, sem contradições, roadmap avançando.
- 🟡 **Atenção**: Crescimento lento ou questões pendentes acumulando.
- 🔴 **Crítico**: Contradições encontradas, LGPD gaps, ou roadmap bloqueado.

4. **Arquivar** o digest em `wiki/outputs/digest-YYYY-MM-DD.md` com frontmatter:
```yaml
---
title: "Weekly Digest — YYYY-MM-DD"
type: output
tags: [digest, weekly]
sources: []
last_updated: YYYY-MM-DD
---
```

5. **Atualizar `index.md`** com a nova página de output.

6. **Append em `log.md`**:
```
## [YYYY-MM-DD HH:MM] digest | Weekly Digest
[Resumo de uma linha do health score e destaques.]
```

## Rules
- Execução autônoma — não perguntar nada, apenas gerar e arquivar.
- Se não houver atividade na semana, registrar isso no digest (é informação útil).
- Se o health score for 🔴, destacar os items críticos no topo do digest.
