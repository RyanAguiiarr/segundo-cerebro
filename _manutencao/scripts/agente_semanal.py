#!/usr/bin/env python3
"""Agente Agendado — Semanal (Sexta-feira)
Função: Executa a consolidação de revisão semanal em wiki/reviews/.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def run_agente_semanal(vault_path: str):
    root = Path(vault_path).resolve()
    today_str = datetime.now().strftime("%Y-%m-%d")
    week_str = datetime.now().strftime("%Y-W%U")
    
    rev_dir = root / "wiki" / "reviews"
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / f"rev-{week_str}-semanal.md"
    
    print(f"=== AGENTE SEMANAL ({week_str}) ===")
    
    content = f"""---
id: rev-{week_str}-semanal
type: review
subtype: ""
area: []
created: {today_str}
updated: {today_str}
freshness: datado
confidence: alta
source: agente
tags:
  - review
periodo: semanal
intervalo: {today_str}
metricas:
  projetos_ativos: 0
  tarefas_concluidas: 0
aprendizados_do_periodo: []
ajustes: []
relations: []
---

## Para o Claude futuro
Revisão semanal consolidada pelo Agente Semanal de Sexta-Feira.

## Métricas & Acompanhamento
- Projetos Ativos: 
- Tarefas Concluídas no Período: 

## Aprendizados do Período
- 

## Ajustes Estratégicos & Próxima Semana
- 
"""
    rev_file.write_text(content, encoding="utf-8")
    print(f"[REVISÃO SEMANAL] Gerada nota de revisão: {rev_file.relative_to(root)}")
    print("=== MANUTENÇÃO SEMANAL CONCLUÍDA ===")

if __name__ == "__main__":
    vpath = os.environ.get("OBSIDIAN_VAULT_PATH", ".")
    run_agente_semanal(vpath)
