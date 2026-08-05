---
description: Executa a auditoria completa de frescor OKM, links quebrados e isolamento de segredos.
---
# /saude-cofre

Dispara o script `_manutencao/scripts/freshness_lint.py` e auditores de integridade do cofre.
Verifica violações de frescor (FRESH-1, FRESH-2, FRESH-3), integridade de wikilinks e garante que o `.env` permaneça ignorado.
