---
name: skill-query
trigger: "any question against the wiki"
description: "Consulta a wiki para responder perguntas, com citações e score de confiança."
---

# Skill: Query

## Context
Quando o humano faz uma pergunta que pode ser respondida pelo conhecimento acumulado na wiki. O agente deve responder com precisão, citando páginas específicas e reportando seu nível de confiança.

## Steps
1. Ler `index.md` para identificar o estado atual da wiki.
2. A partir da pergunta, identificar os **top 5 páginas candidatas** mais relevantes.
3. Ler as páginas candidatas (NÃO reler a wiki inteira).
4. Se a informação não for encontrada, verificar `wiki/sources/` para resumos de fontes.
5. Sintetizar uma resposta com citações usando `[[wiki/path/page]]`.
6. Auto-reportar um **Confidence Score**:
   - **Alta**: 3+ páginas da wiki suportam a resposta diretamente.
   - **Média**: 1–2 páginas suportam, mas com lacunas.
   - **Baixa**: Nenhuma página wiki suporta — resposta baseada em conhecimento geral.
7. Se confiança for Baixa, alertar: "⚠️ Esta resposta não é suportada pela wiki atual. Considere executar `/ingest` com uma fonte relevante."
8. Perguntar: "Desejo arquivar esta resposta em `wiki/outputs/` como uma página permanente?"

## Output format
```markdown
## Resposta

[Resposta sintetizada com [[wiki/path/page]] citations]

### Confiança: [Alta | Média | Baixa]
Baseado em [N] páginas da wiki: [[page1]], [[page2]], ...

### Fontes consultadas
- [[wiki/concepts/page1]] — relevância: [breve justificativa]
- [[wiki/sources/page2]] — relevância: [breve justificativa]
```

## Rules
- SEMPRE ler `index.md` primeiro — nunca adivinhar quais páginas existem.
- NUNCA inventar informação — se a wiki não tem a resposta, dizer claramente.
- Citar todas as páginas consultadas, mesmo as que não contribuíram para a resposta.
- Se a pergunta toca em temas médicos, adicionar disclaimer: "Esta informação é para referência técnica e não substitui avaliação médica."
- Se a pergunta envolve uma decisão arquitetural, verificar `wiki/decisions/` para ADRs relevantes.
- Se a resposta for arquivada, seguir as convenções de `wiki/outputs/` (frontmatter, backlinks).
