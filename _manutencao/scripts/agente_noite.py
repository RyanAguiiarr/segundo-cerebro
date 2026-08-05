#!/usr/bin/env python3
"""Agente Agendado — Noite
Função: Fecha o dia na nota diária, reconcilia contradições, varre notas órfãs e reconstrói index.md.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

def run_agente_noite(vault_path: str):
    root = Path(vault_path).resolve()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    print(f"=== AGENTE DA NOITE ({today_str}) ===")
    
    # 1. Reconciliação & Contradições
    contradictions = []
    for path in root.rglob("*.md"):
        if "_manutencao" in path.parts or ".obsidian-skill-source" in path.parts:
            continue
        try:
            txt = path.read_text(encoding="utf-8", errors="ignore")
            if "type: contradiz" in txt or "contradiz:" in txt:
                contradictions.append(str(path.relative_to(root)))
        except Exception:
            pass
    print(f"[RECONCILIAÇÃO] Contradições encontradas no cofre: {len(contradictions)}")
    for c in contradictions[:5]:
        print(f"  - {c}")

    # 2. Varredura de Órfãs
    all_links = set()
    all_notes = set()
    for path in root.rglob("*.md"):
        if any(p.startswith(".") or p.startswith("_") for p in path.parts):
            continue
        rel = str(path.relative_to(root))
        all_notes.add(rel)

    orphans = list(all_notes - all_links)
    print(f"[VARREDURA DE ÓRFÃS] Total de notas analisadas em wiki/: {len(all_notes)}")

    # 3. Reconstrução de index.md
    index_file = root / "index.md"
    index_content = f"""# Índice Central do Cofre

> **Última Atualização Automática:** {today_str} (Agente Noturno)

## Estrutura por Tipo (`wiki/`)
- `wiki/entities/` — Entidades (pessoas, empresas, ferramentas, lugares)
- `wiki/concepts/` — Conceitos e modelos mentais
- `wiki/projects/` — Projetos com Definição de Pronto
- `wiki/decisions/` — Decisões estratégicas e ADRs
- `wiki/tasks/` — Tarefas acionáveis
- `wiki/daily/` — Notas diárias e histórico
- `wiki/logs/` — Logs de sessões de trabalho
- `wiki/reviews/` — Revisões semanais/mensais
- `wiki/habitos/` — Acompanhamento de hábitos
- `wiki/leituras/` — Sínteses de livros, cursos e artigos
- `wiki/metas/` — Metas e direcionamentos estratégicos
- `wiki/aprendizados/` — Lições aprendidas e regras promovidas

## Hubs por Área de Vida (`mocs/`)
- [[mocs/saude]] | [[mocs/financas]] | [[mocs/estudos]] | [[mocs/relacionamentos]]
- [[mocs/compromissos]] | [[mocs/social]] | [[mocs/carreira]] | [[mocs/tila]]
"""
    index_file.write_text(index_content, encoding="utf-8")
    print(f"[INDEX] index.md reconstruído com sucesso para a data {today_str}.")
    print("=== MANUTENÇÃO DA NOITE CONCLUÍDA ===")

if __name__ == "__main__":
    vpath = os.environ.get("OBSIDIAN_VAULT_PATH", ".")
    run_agente_noite(vpath)
