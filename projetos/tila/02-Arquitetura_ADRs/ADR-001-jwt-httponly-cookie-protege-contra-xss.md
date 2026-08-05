---
title: "ADR-001: JWT via HttpOnly cookie protege TILA contra XSS melhor que localStorage"
type: decision
date: 2026-05-07
status: Accepted
---

# ADR-001: JWT via HttpOnly cookie protege TILA contra XSS melhor que localStorage

## Context
O TILA precisa transportar o token JWT entre frontend (Angular) e backend (Spring Boot). As duas opções principais são localStorage e HttpOnly cookies.

## Decision
Usar HttpOnly cookie como transporte primário, com fallback em Authorization header.

## Alternatives considered
1. **localStorage** — mais simples, mas acessível via JavaScript (vulnerável a XSS)
2. **HttpOnly cookie** — não acessível via JavaScript, proteção nativa contra XSS
3. **sessionStorage** — perde token ao fechar aba

## Consequences
- ✅ Token inacessível via `document.cookie` ou JavaScript
- ✅ `SameSite=Lax` oferece proteção parcial contra CSRF
- ✅ `withCredentials: true` no interceptor Angular garante envio automático
- ⚠️ `secure=false` no momento — deve ser true em produção (HTTPS)
- ⚠️ Sem refresh token — sessão expira após 1h abruptamente

## Verified in code
- `AutenticacaoController.java`: `ResponseCookie.from("accessToken"...)`
- `SecurityFilter.java`: `recuperarToken()` prioriza cookie
- `auth.interceptor.ts`: `withCredentials: true`

## Backlinks
- [[codebase/patterns/padrão-seguranca-jwt]]
