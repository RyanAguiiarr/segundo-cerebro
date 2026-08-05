---
title: "Conversa de Desenvolvimento: Refatoração Auth e Signals"
slug: refatoracao-auth-signals
date: 2026-06-07
type: source
tags: [angular, backend, architecture, refactoring]
---

# Conversa de Desenvolvimento: Refatoração Auth e Signals

## Resumo
Esta conversa focou na implementação prática do `PacienteStore` no Frontend utilizando Signals (ADR-007) para eliminar requisições redundantes de APIs. Além disso, foram realizadas limpezas no Backend, renomeando DTOs em português e ausência de anotações essenciais (`@Repository`) nos repositórios, consolidando o terreno para implementação do cache (Redis).

## Takeaways
1. **O poder do ADR-007 (Signals)**: Centralizar o estado com Angular Signals demonstrou eficácia imediata no compartilhamento de dados do paciente entre Prontuário e Laudo sem recarregar recursos de rede.
2. **Resiliência do Ciclo de Vida da Sessão**: Interceptors em Angular com `catchError` (401/403) provaram ser o elo de conexão global necessário para revogar estados desatualizados do AuthStore e redirecionar ao login.
3. **Consistência de Nomenclaturas de DTOs**: Para a camada de API do Spring Boot escalar com sanidade, os limites de transição de dados devem ter um padrão de nomenclatura coeso (ex: `LoginRequestDTO` vs `DadosAutenticacao`).

## Conceitos e Entidades Extraídos
- [[wiki/concepts/angular-patterns]] — Reforçados e documentados os padrões de Signals e Interceptors de Autorização Global.
- [[wiki/concepts/backend-patterns]] — Adicionado e validado padrão de padronização de nomenclatura de DTOs.

## Backlinks
- [[index]]
- [[log]]
