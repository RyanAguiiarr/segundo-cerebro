---
title: "Gestão de Estado e Navegação no Frontend (Angular)"
type: concept
tags: [angular, frontend-patterns, state-management, architecture]
sources: [raw/codebase/conversations/2026-06-05-layout-state-management.md]
last_updated: 2026-06-05
---

# Gestão de Estado no Angular (State Management)

Ao navegar entre páginas complexas no frontend (ex: saindo de um Prontuário para abrir a tela de geração de Laudo), surge a necessidade de repassar os dados do contexto atual (como `pacienteId`, `dadosClinicos`, `examesSelecionados`) para a nova tela. Qual a melhor maneira de fazer isso com boa arquitetura e performance?

## Abordagens Possíveis

### 1. Persistência via Rota (URL Parameters) - *Recomendado para Compartilhamento*
A forma mais escalável de navegar entre contextos que devem sobreviver a "F5" (refresh) da página.
- **Como funciona:** Você passa os identificadores essenciais na URL. Ex: `/laudo/novo?pacienteId=123&exameId=456`.
- **Vantagem:** A página do laudo é independente. Se o médico copiar e colar o link em outra aba, a tela de Laudo saberá carregar os dados pelo ID que está na URL, batendo no backend ou no cache (Redis).
- **Desvantagem:** Requer requisições HTTP adicionais quando a página é carregada pela primeira vez, embora isso possa ser mitigado por cache.

### 2. Angular Services (Singleton Store / Signals) - *Recomendado para Performance em SPA*
Utilizar a Injeção de Dependências do Angular para compartilhar uma instância única de uma classe (Service) entre componentes.
- **Como funciona:** Você cria um `PacienteContextService`. Quando o usuário entra no Prontuário, o Prontuário alimenta esse service com os dados (`service.setPacienteAtual(dados)`). Quando ele clica em "Gerar Laudo" e navega pra outra tela, a tela de Laudo injeta o mesmo service e pega os dados imediatamente (`service.getPacienteAtual()`).
- **Angular 16+ Signals:** A forma mais moderna e performática de fazer isso hoje é utilizando Signals (`paciente = signal<Paciente | null>(null)`). Quando o valor atualiza, apenas a UI que depende dele sofre reflow.
- **Vantagem:** Zero delay de rede, ultra performático, os dados já estão na memória do navegador.
- **Desvantagem:** Se o médico der um "F5" (reload da página) na tela de Laudo, a memória do JavaScript é limpa e ele perde os dados. É necessário ter um mecanismo de *fallback* para ir buscar no backend ou usar `localStorage` para hidratar o estado.

### 3. State Management Avançado (NgRx / Redux)
- **Como funciona:** Utiliza uma loja global de estados (Store) onde as ações disparam reducers que alteram a imutabilidade do estado.
- **Vantagem:** Extremamente previsível, fácil de debugar (Redux DevTools), maravilhoso para fluxos assíncronos muito complexos.
- **Desvantagem:** Curva de aprendizado íngreme e verbosidade alta (muito boilerplate). Para a maioria das aplicações CRUD/Dashboards modernas, Angular Signals tem substituído o NgRx de forma mais simples.

## Como o Tila deve adotar?

Para o fluxo **Prontuário ➔ Laudo**:
1. O usuário clica em "Gerar Laudo".
2. O Angular utiliza o router para navegar e injeta o `ID do Exame` e `ID do Paciente` na URL (`/laudos/novo/:exameId`).
3. Ao mesmo tempo, um `ContextService` (usando Angular Signals ou RxJS) já carrega em memória os dados pesados que o usuário acabou de ver na tela do Prontuário.
4. A tela de Laudo carrega: ela primeiro checa o `ContextService`. Se os dados já estiverem lá na memória (navegação SPA normal), ela renderiza imediatamente.
5. Se a tela de Laudo foi aberta numa nova aba ou sofreu Refresh (não tem memória), ela lê a URL, extrai o ID, e faz um *fetch* silencioso no backend para resgatar os dados do paciente, garantindo que nunca quebre.

## Backlinks
- [[wiki/sources/layout-state-management]]
- [[wiki/concepts/redis-cache-patterns]] — Pode atuar junto no backend para otimizar os fetches após "F5".
