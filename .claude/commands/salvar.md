---
description: Captura proativa e salvamento de fatos, decisões e aprendizados da sessão no cofre.
---
# /salvar

Quando acionado, o agente executa a varredura do contexto da sessão atual:
1. Realiza a verificação de existência em `wiki/` e `index.md`.
2. Cria notas atômicas para entidades/conceitos/decisões novas ou atualiza in-loco notas existentes com fatos bitemporais (`valido_em` e `aprendido_em`).
3. Registra contradições com a tag `relations: [{type: contradiz, target: "..."}]` se houver divergência de dados.
4. Aplica as regras de vínculo (`[[wikilinks]]`) e OKM (frescor).
