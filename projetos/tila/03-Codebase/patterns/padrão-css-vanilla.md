---
title: "TILA usa CSS vanilla com variáveis CSS — Tailwind e frameworks externos são proibidos"
type: pattern
domain: frontend
tags: [css, styling, design]
verified_in: [app.component.css, package.json (sem Tailwind)]
violations_found: []
last_updated: 2026-06-09
---

# TILA usa CSS vanilla com variáveis CSS — Tailwind e frameworks externos são proibidos

## O padrão

O TILA usa CSS puro (vanilla) para estilização. Nenhum framework CSS (Tailwind, Bootstrap, Material) está presente nas dependências.

## Verificado no package.json

Não há nenhuma dependência de framework CSS:
- ❌ Sem Tailwind CSS
- ❌ Sem Bootstrap
- ❌ Sem Angular Material
- ❌ Sem PrimeNG
- ✅ Apenas CSS puro

## Componentes usam arquivos CSS individuais

Cada componente tem seu próprio `.css`:
```typescript
@Component({
  styleUrl: './app.component.css'
})
```

## Conformidade: 100%
Nenhum framework CSS encontrado. Todo o styling é feito com CSS vanilla.

## Backlinks
- [[codebase/snapshots/frontend-audit-2026-06-09]]
