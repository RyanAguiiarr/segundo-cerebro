---
title: "ADR-002: ResponseEntity<GenericResult<T>> como envelope universal de resposta"
type: decision
date: 2026-05-07
status: Accepted
---

# ADR-002: ResponseEntity\<GenericResult\<T\>\> como envelope universal de resposta

## Context
APIs REST precisam de formato consistente para responses de sucesso e erro. Sem padronização, o frontend precisa tratar cada endpoint individualmente.

## Decision
Todos os endpoints retornam `ResponseEntity<GenericResult<T>>`. O `GenericResult` tem 3 campos: `success` (boolean), `message` (String), `data` (T).

## Alternatives considered
1. **ResponseEntity direto** — inconsistente entre sucesso e erro
2. **Spring ProblemDetail (RFC 7807)** — mais complexo, focado só em erros
3. **GenericResult<T>** — simples, unifica sucesso e erro

## Consequences
- ✅ Frontend pode usar tipo genérico `GenericResult<T>` em TypeScript
- ✅ GlobalExceptionHandler também usa GenericResult para erros
- ✅ 100% dos endpoints conformes (verificado 2026-06-09)
- ⚠️ `message` em sucesso é sempre a mesma string — poderia ser mais descritiva

## Verified in code
- `GenericResult.java`: factory methods `success()` e `error()`
- Todos os controllers usam `GenericResult.success(data)`
- `GlobalExceptionHandler.java` usa `GenericResult.error(message)`

## Backlinks
- [[codebase/patterns/padrão-genericresult]]
