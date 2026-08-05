---
title: "JWT TILA usa HMAC256 com HttpOnly cookie como transporte primário e header como fallback"
type: pattern
domain: backend
tags: [security, jwt, cookie]
verified_in: [TokenService.java, SecurityFilter.java, SecurityConfigurations.java, AutenticacaoController.java]
violations_found: []
last_updated: 2026-06-09
---

# JWT TILA usa HMAC256 com HttpOnly cookie como transporte primário e header como fallback

## O padrão

O token JWT é gerado com HMAC256, emitido como cookie HttpOnly e aceito via Authorization header como fallback.

## Fluxo real (verificado)

### 1. Geração (TokenService)
```java
Algorithm.HMAC256(secret)  // secret vem de application.properties
JWT.create()
    .withIssuer("TILA-APP")
    .withSubject(usuario.getEmail())
    .withClaim("role", usuario.getPerfil().toString())
    .withExpiresAt(/* +1h com offset -03:00 */)
    .sign(algoritimo);
```

### 2. Emissão (AutenticacaoController /auth/login)
```java
ResponseCookie.from("accessToken", tokenJWT)
    .httpOnly(true)    // Não acessível via JavaScript (anti-XSS)
    .secure(false)     // ⚠️ HTTP — alterar para true em produção
    .path("/")
    .maxAge(3600)      // 1 hora
    .sameSite("Lax")   // Proteção parcial contra CSRF
    .build();
```

### 3. Recepção (SecurityFilter)
```java
// Prioridade 1: Cookie
for(Cookie cookie: request.getCookies()) {
    if("accessToken".equals(cookie.getName())) return cookie.getValue();
}
// Prioridade 2: Header
var authorizationHeader = request.getHeader("Authorization");
if(authorizationHeader != null) return authorizationHeader.replace("Bearer ", "");
```

### 4. Validação
```java
JWT.require(algoritimo).withIssuer("TILA-APP").build().verify(tokenJWT).getSubject();
// subject = email → UsuarioRepository.findByEmail → SecurityContextHolder
```

## Conformidade: 100%
O fluxo completo é consistente. Nenhuma violação encontrada.

## Gaps
- `secure(false)` deve ser `true` em produção
- Sem refresh token
- Secret hardcoded (ver [[codebase/snapshots/backend-security-2026-06-09]])

## Backlinks
- [[negocio/permanent/decisoes/ADR-001-jwt-httponly-cookie-protege-contra-xss]]
- [[codebase/snapshots/backend-security-2026-06-09]]
