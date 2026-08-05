---
title: "ADR-007: Angular State Management"
type: decision
tags: [architecture, adr, angular, signals, state-management]
sources: [wiki/concepts/angular-state-management.md, wiki/concepts/state-sharing-reactivity.md]
last_updated: 2026-06-06
---

# ADR-007: Angular State Management

## Status
Accepted

## Context
Ao navegar no frontend entre telas complexas de fluxo clínico (ex: sair do Prontuário de um Paciente para gerar um Laudo pelo exame correspondente), precisamos repassar os dados contextuais para a nova tela. A abordagem de apenas buscar do zero via requisições HTTP adiciona latência, enquanto a abordagem de apenas guardar em memória quebra se o usuário der F5/recarregar a aba do navegador.

## Decision
Adotaremos um **Padrão Híbrido** composto por Rota Parametrizada e Store Service reativo via Angular Signals:
1. **Identificação por URL**: Os caminhos de rotas conterão IDs de recursos (ex: `/laudo/:id`). Isso garante que, se o usuário der refresh ou salvar a URL, a aplicação saiba qual recurso carregar.
2. **Store Reativo em Memória (Signals)**: Um serviço singleton (ex: `PacienteStore`) guardará o estado na memória do navegador. Ao navegar normalmente entre componentes, o componente de destino pedirá os dados ao Store. Se os dados já estiverem em memória (Cache Hit), eles serão retornados instantaneamente (0ms de latência e zero chamadas HTTP).
3. **Fallback Resiliente**: Caso os dados não estejam no Store (Cache Miss - por ex. em F5 ou link direto), o Store fará a busca na API REST do backend silenciosamente e atualizará o sinal, garantindo consistência.

## Alternatives Considered

### Alternativa 1: State Management global robusto (NgRx/Redux)
Rejeitado devido à alta verbosidade e boilerplate que introduz para uma aplicação de escopo focado. Os Angular Signals nativos fornecem reatividade ideal com menor custo de manutenção e curva de aprendizado.

### Alternativa 2: Passar objetos pesados via Router History State
Rejeitado porque não sobrevive a recarregamentos (F5) e dificulta testes unitários e acoplamento de rotas.

## Consequences

### Positivas
- Transições de tela instantâneas para dados já visualizados.
- URLs compartilháveis e resilientes ao F5.
- Componentes isolados e facilmente testáveis via injeção dos Stores.

### Negativas
- Necessidade de codificar a lógica de cache miss e gerenciar os Stores de forma dedicada.

## Backlinks
- [[wiki/concepts/angular-state-management]]
- [[wiki/concepts/state-sharing-reactivity]]
