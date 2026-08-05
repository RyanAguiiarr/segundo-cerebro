---
title: "ADR-001: JWT Cookie Transport"
type: decision
tags: [architecture, adr, security, jwt, cookies]
sources: []
last_updated: 2026-05-07
---

# ADR-001: JWT Cookie Transport

## Status
Accepted

## Context
O TILA precisa transportar o JWT entre frontend (Angular, localhost:4200) e backend (Spring Boot, localhost:8080). Existem duas abordagens padrão: armazenar no `localStorage`/`sessionStorage` e enviar via header `Authorization`, ou usar HttpOnly cookies.

O sistema trata dados médicos sensíveis e está sujeito à LGPD. A segurança do transporte do token é uma decisão arquitetural crítica, pois impacta diretamente a superfície de ataque para XSS e CSRF.

## Decision
Usar **HttpOnly cookie** como transporte primário do JWT, com **Authorization header** como fallback para clientes não-browser (mobile, API consumers).

### Configuração do Cookie
```
Name: jwt_token
HttpOnly: true      ← JavaScript não pode ler
Secure: true         ← Apenas HTTPS (em produção)
SameSite: Lax        ← Proteção parcial contra CSRF
Max-Age: 3600        ← 1 hora (alinhado com JWT expiry)
Path: /              ← Disponível em todas as rotas
```

### Detecção no JwtFilter
O filtro tenta extrair o token nesta ordem:
1. Cookie `jwt_token`
2. Header `Authorization: Bearer <token>`

## Alternatives Considered

### Alternativa 1: localStorage + Authorization Header
- **Prós**: Simples de implementar, sem complicações de CORS.
- **Contras**: Vulnerável a XSS — qualquer script injetado pode ler o `localStorage` e exfiltrar o token.
- **Rejeitado porque**: Dado que o TILA trata dados médicos sensíveis (LGPD Art. 11 — dados de saúde), o risco de XSS é inaceitável.

### Alternativa 2: sessionStorage + Authorization Header
- **Prós**: Token não persiste entre abas/sessões.
- **Contras**: Mesma vulnerabilidade XSS que localStorage. Cada aba requer login separado (UX ruim).
- **Rejeitado porque**: Vulnerabilidade XSS permanece.

### Alternativa 3: HttpOnly Cookie exclusivo (sem header fallback)
- **Prós**: Superfície de ataque mínima.
- **Contras**: Inviabiliza clientes mobile nativos e API consumers que não suportam cookies.
- **Rejeitado porque**: TILA pode ter clientes mobile no futuro.

## Consequences

### Positivas
- **Mitigação XSS**: JavaScript não pode acessar o token (HttpOnly).
- **Transporte automático**: Browser envia o cookie automaticamente.
- **LGPD compliance**: Reduz risco de vazamento de credenciais.
- **Flexibilidade**: Header fallback permite clientes não-browser.

### Negativas
- **CORS mais complexo**: `allowCredentials: true` é obrigatório, e o `allowedOrigins` não pode ser `*`.
- **CSRF residual**: Embora `SameSite: Lax` mitigue parcialmente, um CSRF token adicional pode ser necessário em produção.
- **Deploy**: `Secure: true` requer HTTPS — desenvolvimento local usa HTTP sem o flag Secure.

### Riscos
- Se o frontend e backend forem deployed em domínios diferentes (não subdomínios), o cookie pode ser bloqueado pelo browser. Solução: usar subdomínios (`api.tila.com` + `tila.com`) ou proxy reverso.
- `SameSite: Lax` não protege contra todos os ataques CSRF (apenas GET requests cross-origin são permitidas). Em produção, considerar CSRF token para operações de escrita.

## Backlinks
- [[wiki/overview]]
- [[wiki/concepts/jwt-authentication]]
- [[context/security-lgpd]]
