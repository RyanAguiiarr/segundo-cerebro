---
name: skill-lint
trigger: "lint the wiki" / "/lint"
description: "Executa uma verificação de saúde completa na wiki e gera um relatório de problemas."
---

# Skill: Lint Wiki

## Context
Verificação periódica da integridade, consistência e completude da wiki. Deve ser executada semanalmente ou sob demanda. Identifica problemas que degradam a qualidade do conhecimento acumulado.

## Steps

### 1. Verificação de Contradições
- Ler todas as páginas em `wiki/concepts/` e `wiki/entities/`.
- Identificar afirmações que se contradizem entre páginas.
- Classificar como: **Conflito direto** (afirmações opostas) ou **Inconsistência** (dados diferentes).

### 2. Claims Obsoletos
- Comparar datas de `last_updated` com fontes em `sources:` do frontmatter.
- Se uma fonte mais recente foi ingerida que atualiza um claim antigo, marcar como obsoleto.
- Verificar se decisions em `wiki/decisions/` foram superseded por novas ADRs.

### 3. Páginas Órfãs
- Verificar todas as páginas da wiki.
- Uma página é órfã se **nenhuma outra página** a referencia via `[[wiki/path/page]]`.
- Exceção: `wiki/overview.md` e páginas em `wiki/outputs/` não precisam de inbound links.

### 4. Conceitos Sem Página
- Buscar menções a conceitos no texto de todas as páginas que NÃO possuem `[[]]` links.
- Se um conceito é mencionado 3+ vezes sem ter sua própria página, reportar.

### 5. Cross-references Ausentes
- Para cada página, verificar se todos os conceitos e entidades mencionados têm links `[[]]`.
- Reportar links quebrados (apontando para páginas que não existem).

### 6. Gaps de LGPD
- Ler `context/security-lgpd.md`.
- Verificar se todas as vulnerabilidades conhecidas estão documentadas.
- Verificar se alguma página da wiki contém inadvertidamente dados sensíveis.
- Checar se todos os endpoints em `wiki/concepts/api-endpoints.md` têm requisitos de auth documentados.

### 7. Cobertura de ADRs
- Ler `wiki/decisions/` e `wiki/concepts/`.
- Para cada decisão arquitetural significativa mencionada em conceitos, verificar se existe ADR correspondente.
- Reportar decisões sem ADR formal.

## Output format
Gerar relatório como tabela markdown:

```markdown
---
title: "Lint Report - YYYY-MM-DD"
type: output
tags: [lint, health-check]
sources: []
last_updated: YYYY-MM-DD
---

# Wiki Lint Report — YYYY-MM-DD

## Resumo
| Check | Status | Issues |
|---|---|---|
| Contradições | ✅/⚠️ | N encontrada(s) |
| Claims obsoletos | ✅/⚠️ | N encontrado(s) |
| Páginas órfãs | ✅/⚠️ | N encontrada(s) |
| Conceitos sem página | ✅/⚠️ | N encontrado(s) |
| Cross-refs ausentes | ✅/⚠️ | N encontrada(s) |
| LGPD gaps | ✅/⚠️ | N encontrado(s) |
| ADR coverage | ✅/⚠️ | N faltando |

## Detalhes

### Contradições
| Página A | Página B | Claim conflitante |
|---|---|---|
| ... | ... | ... |

### Claims Obsoletos
| Página | Claim | Fonte mais recente |
|---|---|---|
| ... | ... | ... |

[... demais seções ...]

## Backlinks
```

## Filing
Salvar automaticamente em `wiki/outputs/lint-YYYY-MM-DD.md`.

## Post-lint Actions
1. Apresentar o relatório ao humano.
2. Perguntar: "Quais issues deseja corrigir agora?"
3. Aplicar as correções autorizadas.
4. Atualizar `index.md` e `log.md`:
   ```
   ## [YYYY-MM-DD HH:MM] lint | Health check
   [Resumo das issues encontradas e corrigidas.]
   ```

## Rules
- NUNCA corrigir issues automaticamente sem aprovação humana.
- Priorizar: LGPD gaps > Contradições > Claims obsoletos > os demais.
- Se encontrar dados sensíveis de pacientes, marcar como **CRÍTICO** e pedir remoção imediata.
