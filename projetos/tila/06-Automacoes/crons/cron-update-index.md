---
name: cron-update-index
trigger: "/reindex"
description: "Reconstrói o index.md a partir de todas as páginas existentes na wiki."
---

# Cron: Update Index

## Schedule
Executar sob demanda com `/reindex`.

## Steps (Autônomo)

1. **Varrer** todos os diretórios da wiki:
   - `wiki/concepts/` — listar todos os `.md`
   - `wiki/entities/` — listar todos os `.md`
   - `wiki/sources/` — listar todos os `.md`
   - `wiki/decisions/` — listar todos os `.md`
   - `wiki/outputs/` — listar todos os `.md`

2. **Para cada página**, ler o frontmatter e extrair:
   - `title`
   - `type`
   - `tags`
   - `last_updated`
   - Primeira frase do conteúdo como summary.

3. **Reescrever `index.md`** seguindo a convenção definida em `CLAUDE.md`:
   - Tabela por categoria (Concepts, Entities, Sources, Decisions, Outputs)
   - Contagem total de páginas
   - Data de última atualização

4. **Append em `log.md`**:
```
## [YYYY-MM-DD HH:MM] reindex | Index rebuilt
[N] páginas indexadas: [X] concepts, [Y] entities, [Z] sources, [W] decisions, [V] outputs.
```

## Rules
- Sobrescrever `index.md` completamente — é um arquivo regenerável.
- Se uma página não tem frontmatter, reportar como warning mas incluir no index.
- Manter a ordenação alfabética dentro de cada categoria.
