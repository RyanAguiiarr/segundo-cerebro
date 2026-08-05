---
id: cnc-acompanhamento-de-metricas-de-saude
type: concept
subtype: saude-monitoramento
area:
  - saude
created: 2026-08-05
updated: 2026-08-05
freshness: atemporal
confidence: alta
source: conversa
tags:
  - conceito
  - saude
  - metricas
  - okm
definicao: "Estrutura planejada para acompanhamento contínuo de métricas vitais e físicas (peso, qualidade de sono, suplementação e hidratação) utilizando ponteiros OKM."
origem: "Necessidade prioritária de monitoramento de saúde do Ryan."
aplicacoes:
  - "Definição de aplicativo ou estrutura de dados para registro diário/semanal."
  - "Integração via ponteiros conforme_em para o cofre de conhecimento."
relations: []
---

## Para o Claude futuro
Conceito que rege o rastreamento de métricas físicas do Ryan. Qualquer dado numérico resultante desta medição (peso, sono, ingestão de água) DEVE ser registrado como ponteiro tipado com carimbo `conforme_em`, nunca como número estático no cofre.

## Diretrizes do Sistema de Métricas
- **Prioridade:** Alta prioridade para estruturação inicial.
- **Formato OKM:** `Ver: [App/Planilha de Saúde] (conforme_em: AAAA-MM-DD)`.
