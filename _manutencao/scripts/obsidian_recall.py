#!/usr/bin/env python3
"""Hook / Mecanismo de Recall Limitado com Abstenção.
Limita injeção a no máximo 4 notas (~900 caracteres).
Abstém-se quando a confiança é baixa e registra log em .claude-runs/recall-YYYY-MM-DD.jsonl
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

MAX_NOTES = 4
MAX_CHARS = 900
MIN_PROMPT_CHARS = 12

def log_recall(vault: Path, entry: dict):
    try:
        d = vault / ".claude-runs"
        d.mkdir(exist_ok=True)
        entry["ts"] = datetime.now().isoformat(timespec="seconds")
        today_str = datetime.now().strftime("%Y-%m-%d")
        with (d / f"recall-{today_str}.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

def run_recall(prompt: str, vault_path: str) -> dict:
    vault = Path(vault_path).resolve()
    if len(prompt) < MIN_PROMPT_CHARS or prompt.startswith("/"):
        log_recall(vault, {"prompt_chars": len(prompt), "abstained": True, "reason": "prompt_curto_ou_comando"})
        return {"abstained": True, "reason": "prompt_curto_ou_comando", "brief": ""}

    # Varre notas em wiki/
    wiki_dir = vault / "wiki"
    matched_notes = []
    terms = set(re.findall(r"\w+", prompt.lower()))
    
    if wiki_dir.exists():
        for note in wiki_dir.rglob("*.md"):
            try:
                txt = note.read_text(encoding="utf-8", errors="ignore")
                note_terms = set(re.findall(r"\w+", txt.lower()))
                overlap = terms & note_terms
                if len(overlap) >= 2:
                    matched_notes.append((note, len(overlap)))
            except Exception:
                pass

    if not matched_notes:
        log_recall(vault, {"prompt_chars": len(prompt), "abstained": True, "reason": "baixa_confianca_sem_match"})
        return {"abstained": True, "reason": "baixa_confianca_sem_match", "brief": ""}

    matched_notes.sort(key=lambda x: x[1], reverse=True)
    selected = matched_notes[:MAX_NOTES]

    brief_lines = ["--- RECALL DE NOTAS DO COFRE ---"]
    current_chars = 0
    injected_paths = []
    
    for note, score in selected:
        line = f"- [[{note.stem}]] ({note.relative_to(vault)})"
        if current_chars + len(line) > MAX_CHARS:
            break
        brief_lines.append(line)
        injected_paths.append(str(note.relative_to(vault)))
        current_chars += len(line)

    brief_str = "\n".join(brief_lines)
    log_recall(vault, {"prompt_chars": len(prompt), "abstained": False, "notes": injected_paths})
    return {"abstained": False, "notes": injected_paths, "brief": brief_str}

if __name__ == "__main__":
    test_prompt = sys.argv[1] if len(sys.argv) > 1 else "Como funciona a governança do cérebro?"
    vpath = os.environ.get("OBSIDIAN_VAULT_PATH", ".")
    res = run_recall(test_prompt, vpath)
    print(f"Recall Result: {res}")
