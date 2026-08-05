#!/usr/bin/env python3
"""Agente Agendado — Manhã
Função: Gera nota diária (wiki/daily/YYYY-MM-DD.md) e lista tarefas atrasadas/pendentes.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def run_agente_manha(vault_path: str):
    root = Path(vault_path).resolve()
    today_str = datetime.now().strftime("%Y-%m-%d")
    daily_dir = root / "wiki" / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    
    daily_file = daily_dir / f"{today_str}.md"
    created = False
    if not daily_file.exists():
        content = f"""---
id: daily-{today_str}
type: daily
subtype: ""
area: []
created: {today_str}
updated: {today_str}
freshness: datado
confidence: alta
source: agente
tags:
  - daily
data: {today_str}
eventos_calendario:
  - "ver: [Google Calendar / Outlook] (conforme_em: {today_str})"
tarefas_atrasadas: []
resumo: ""
relations: []
---

## Para o Claude futuro
Nota diária de acompanhamento gerada pelo Agente Agendado da Manhã.

## Planejamento & Foco do Dia
- [ ] 

## Registro de Eventos & Notas Rápidas
- 

## Resumo Noturno (Autogerado)
- 
"""
        daily_file.write_text(content, encoding="utf-8")
        created = True

    # Varre tarefas em wiki/tasks/
    tasks_dir = root / "wiki" / "tasks"
    pending_tasks = []
    if tasks_dir.exists():
        for t in tasks_dir.glob("*.md"):
            txt = t.read_text(encoding="utf-8", errors="ignore")
            if "status: a-fazer" in txt or "status: em-andamento" in txt:
                pending_tasks.append(t.name)

    print(f"=== AGENTE DA MANHÃ ({today_str}) ===")
    print(f"[STATUS] Nota diária: {'Criada com sucesso' if created else 'Já existente'} ({daily_file.relative_to(root)})")
    print(f"[TAREFAS PENDENTES] Encontradas {len(pending_tasks)} tarefas em wiki/tasks/:")
    for task_name in pending_tasks[:5]:
        print(f"  - {task_name}")
    print("=== MANUTENÇÃO DA MANHÃ CONCLUÍDA ===")

if __name__ == "__main__":
    vpath = os.environ.get("OBSIDIAN_VAULT_PATH", ".")
    run_agente_manha(vpath)
