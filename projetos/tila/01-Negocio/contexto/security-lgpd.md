---
title: "TILA — Security & LGPD"
type: context
last_updated: 2026-06-09
---

# TILA — Security & LGPD
> Real state of security as of 2026-06-09. See full details in [[codebase/snapshots/backend-security-2026-06-09]].

## Authentication
- JWT via HMAC256, issuer "TILA-APP", 1h expiry
- Transport: HttpOnly cookie (primary) + Authorization header (fallback)
- Password: BCryptPasswordEncoder
- Roles: MEDICO, PACIENTE, ADMIN

## Security Gaps (from audit)

### 🔴 CRITICAL (4)
1. JWT secret hardcoded: `Cucamole@123` in application.properties
2. DB password hardcoded: `Cucamole@123` in application.properties
3. Gemini API key hardcoded in application.properties
4. Public registration endpoint allows anyone to create MEDICO accounts

### 🟡 MEDIUM (6)
5. Cookie `secure=false` — HTTP transport
6. No refresh token
7. `ipOrigem` always null in audit logs
8. `/logs` returns entity instead of DTO
9. No rate limiting on auth endpoints
10. Unused import `java.awt.*` in SecurityFilter

### 🔵 LOW (3)
11. Timezone hardcoded `-03:00` in TokenService
12. `ddl-auto=update` in application.properties
13. `show-sql=true` in application.properties

## LGPD Gaps
- CPF stored in plaintext (should be encrypted at rest)
- Clinical data (laudos, exames) not encrypted at rest
- No consent flow for patients
- No right to erasure endpoint
- ipOrigem never captured in audit logs
- No DPO (Data Protection Officer) configuration

## Priority for remediation
1. **Immediate**: Move secrets to environment variables
2. **Before any staging deploy**: `secure=true` on cookie, rate limiting
3. **Before production**: CPF encryption, clinical data encryption, consent flow
