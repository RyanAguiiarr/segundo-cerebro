---
title: "MOC — Segurança e LGPD"
type: moc
cluster: seguranca-lgpd
---

# MOC — Segurança e LGPD

> Mapa de navegação para notas relacionadas a segurança e conformidade LGPD.

## Decisões
- [[negocio/permanent/decisoes/ADR-001-jwt-httponly-cookie-protege-contra-xss]] — Transporte JWT via cookie
- [[negocio/permanent/decisoes/ADR-002-genericresult-envelope-universal]] — Envelope de resposta padronizado

## Padrões
- [[codebase/patterns/padrão-seguranca-jwt]] — Implementação JWT completa

## Snapshots
- [[codebase/snapshots/backend-security-2026-06-09]] — Auditoria de segurança com 4 gaps críticos

## Domínio
- [[negocio/permanent/medico/laudo-ia-exige-revisao-humana-obrigatoria]] — LGPD e decisões automatizadas

## Gaps críticos (2026-06-09)
1. 🔴 JWT secret hardcoded em application.properties
2. 🔴 Senha do banco hardcoded
3. 🔴 API key Gemini hardcoded
4. 🔴 Registro público de médicos sem verificação de CRM
5. 🟡 CPF armazenado em plaintext
6. 🟡 Dados clínicos sem criptografia em repouso
