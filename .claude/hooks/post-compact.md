---
description: Hook executado após a compactação do contexto para injeção de recall delimitado (obsidian_recall.py).
---
# Hook: Post-Compact Recall

Após a compactação de contexto, o agente executa `_manutencao/scripts/obsidian_recall.py` em modo de leitura para avaliar a relevância do cofre para a instrução atual.
Se houver alta confiança, injeta até 4 notas (~900 chars). Se a confiança for baixa, abstém-se.
Loga cada decisão em `.claude-runs/recall-YYYY-MM-DD.jsonl`.
