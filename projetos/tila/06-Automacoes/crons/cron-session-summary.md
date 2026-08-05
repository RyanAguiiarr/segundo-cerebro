---
name: cron-session-summary
trigger: automática a cada 10 min
description: "Resume a última sessão de 07‑Raw/sessions e envia o resumo ao Discord."
schedule: "*/10 * * * *"
---

# Cron: Session Summary (10 min)

## Schedule
Executar a cada 10 minutos (expressão cron `*/10 * * * *`).

## Steps (autônomo)

1. Invocar a skill `skill-summarize-new-session`.
2. A skill já lê a última sessão e envia o resumo ao Discord; não há arquivos a serem modificados.

## Rules
- Não interagir com o usuário; só ler sessões e enviar o resumo.
- Se nenhuma sessão nova for encontrada, enviar a mensagem “Nenhuma sessão encontrada em 07‑Raw/sessions.”.
- Garantir que nenhum dado sensível de pacientes seja incluído (a skill já filtra isso).
