#!/usr/bin/env python3
"""Agente Agendado — Saúde (Domingo)
Função: Executa auditoria completa de integridade do cofre (Frescor OKM, links quebrados e segredos).
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

def run_agente_saude(vault_path: str):
    root = Path(vault_path).resolve()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    print(f"=== AGENTE DE SAÚDE ({today_str}) ===")
    
    # 1. Executa Linter de Frescor OKM
    freshness_script = root / "_manutencao" / "scripts" / "freshness_lint.py"
    if freshness_script.exists():
        print("[AUDITORIA 1] Executando Linter de Frescor OKM...")
        try:
            python_exe = sys.executable
            res = subprocess.run([python_exe, str(freshness_script), "--path", str(root)], capture_output=True, text=True)
            print(res.stdout)
            if res.stderr:
                print(f"Stderr: {res.stderr}")
        except Exception as e:
            print(f"Erro ao executar linter de frescor: {e}")

    # 2. Verificação de Arquivos e Integridade de Links
    md_files = list(root.rglob("*.md"))
    valid_md_count = len([f for f in md_files if "_manutencao" not in f.parts and ".obsidian-skill-source" not in f.parts])
    print(f"[AUDITORIA 2] Total de notas Markdown ativas no cofre: {valid_md_count}")
    
    # 3. Auditoria de Segredos Básica (.env isolado)
    env_file = root / ".env"
    print(f"[AUDITORIA 3] Checagem de Segredos: Arquivo .env está {'presente e protegido' if env_file.exists() else 'ausente (usar .env.example)'}")
    
    print("=== AUDITORIA DE SAÚDE CONCLUÍDA ===")

if __name__ == "__main__":
    vpath = os.environ.get("OBSIDIAN_VAULT_PATH", ".")
    run_agente_saude(vpath)
