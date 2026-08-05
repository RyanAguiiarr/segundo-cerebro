---
title: "Auditoria de Segurança Backend TILA — Snapshot 2026-06-09"
type: snapshot
scope: security
date: 2026-06-09
immutable: true
---

# Auditoria de Segurança — TILA Backend
> Snapshot imutável de 2026-06-09

## JWT Implementation

| Aspecto | Implementação real |
|---|---|
| Algoritmo | HMAC256 (via auth0 java-jwt 4.4.0) |
| Issuer | "TILA-APP" |
| Subject | email do usuário |
| Claims custom | `role` (perfil como String) |
| Expiry | 1 hora (hardcoded -03:00 offset) |
| Secret source | `@Value("${api.security.token.secret}")` |
| Transporte primário | HttpOnly cookie "accessToken" (maxAge=3600, SameSite=Lax) |
| Transporte fallback | Authorization header "Bearer {token}" |
| Cookie secure flag | ⚠️ `false` (HTTP, não HTTPS) |
| Refresh token | ❌ NÃO IMPLEMENTADO |

## Roles e Acesso

| Path pattern | Roles permitidas | Método |
|---|---|---|
| /auth/** | Público | POST, GET |
| /medicos/** | ROLE_MEDICO | * |
| /paciente/** | ROLE_MEDICO, ROLE_PACIENTE | * |
| /laudo/** | ROLE_MEDICO | * |
| /logs/** | ROLE_ADMIN | * |
| /** | authenticated | * |
| OPTIONS /** | Público | OPTIONS |

### Hierarquia de roles
- ADMIN → recebe ROLE_ADMIN + ROLE_MEDICO (acesso a tudo)
- MEDICO → ROLE_MEDICO
- PACIENTE → ROLE_PACIENTE

## CORS Configuration

| Aspecto | Valor |
|---|---|
| Allowed Origins | `http://localhost:4200` (APENAS) |
| Allowed Methods | GET, POST, PUT, DELETE, OPTIONS |
| Allowed Headers | * (wildcard) |
| Allow Credentials | true |
| ⚠️ Produção | Sem config de produção — apenas localhost |

## Security Filter Chain
- CSRF desabilitado (stateless JWT)
- Session policy: STATELESS
- SecurityFilter (OncePerRequestFilter) adicionado antes de UsernamePasswordAuthenticationFilter
- Fluxo: Cookie → Header → recuperarToken() → TokenService.getSubject() → UsuarioRepository.findByEmail() → SecurityContextHolder

## Gaps de Segurança

### 🔴 CRITICAL

1. **JWT secret hardcoded em application.properties**
   - Arquivo: `application.properties` linha 3
   - Valor: `api.security.token.secret=Cucamole@123`
   - Risco: Qualquer pessoa com acesso ao repo pode forjar tokens
   - Fix: Usar variável de ambiente `${JWT_SECRET}`

2. **Senha do banco hardcoded em application.properties**
   - Arquivo: `application.properties` linha 7
   - Valor: `spring.datasource.password=Cucamole@123`
   - Risco: Acesso direto ao banco de dados
   - Fix: Usar variável de ambiente `${DB_PASSWORD}`

3. **API key do Gemini hardcoded em application.properties**
   - Arquivo: `application.properties` linha 25
   - Valor: `GEMINI_API_KEY=AIzaSyBkM8J29x9tpXz9ZpYWDi_j93WDQPzdNaA`
   - Risco: Uso não autorizado da API, custos
   - Fix: Remover da properties, usar apenas variável de ambiente

4. **POST /auth/registrar é público sem controle**
   - Arquivo: `AutenticacaoController.java`
   - Risco: Qualquer pessoa pode criar contas de MÉDICO sem verificação de CRM
   - Fix: Proteger endpoint ou adicionar verificação de CRM

### 🟡 MEDIUM

5. **Cookie secure=false**
   - Arquivo: `AutenticacaoController.java` linha 111
   - Risco: Token transmitido via HTTP sem criptografia
   - Fix: `secure(true)` em produção

6. **Sem refresh token**
   - Risco: Após 1h o usuário é deslogado abruptamente
   - Fix: Implementar refresh token rotation

7. **ipOrigem sempre null em LogAuditoria**
   - Arquivo: `LogAuditoria.java` e todos os pontos de criação
   - Risco: Logs de auditoria incompletos — impossível rastrear origem
   - Fix: Capturar `request.getRemoteAddr()` em cada log

8. **GET /logs retorna entidade direta**
   - Arquivo: `LogAuditoriaController.java`
   - Risco: Expõe estrutura interna incluindo relação com Usuario
   - Fix: Criar LogAuditoriaResponseDTO

9. **Sem rate limiting**
   - Risco: Brute-force em /auth/login e /auth/registrar
   - Fix: Implementar rate limiting (Redis/Spring Cloud Gateway)

10. **import java.awt.* em SecurityFilter**
    - Arquivo: `SecurityFilter.java` linha 19
    - Risco: Import desnecessário (AWT em server-side), potencial confusão
    - Fix: Remover import

### 🔵 LOW

11. **Timezone hardcoded em TokenService**
    - Arquivo: `TokenService.java` linha 43
    - Valor: `ZoneOffset.of("-03:00")`
    - Risco: Falha em deploy fora do fuso BRT
    - Fix: Usar ZoneId configável

12. **ddl-auto=update em produção**
    - Arquivo: `application.properties` linha 10
    - Risco: Alterações automáticas em schema de produção
    - Fix: Usar `validate` em produção, migrations com Flyway

13. **show-sql=true**
    - Arquivo: `application.properties` linha 12
    - Risco: Performance e exposição de queries em logs
    - Fix: `false` em produção

## Mapa de Exposição LGPD

| Entidade | Campo | Classificação LGPD | Proteção atual |
|---|---|---|---|
| Usuario | email | Dado pessoal | ❌ Sem criptografia em repouso |
| Usuario | senha | Credencial | ✅ BCrypt |
| Medico | nomeCompleto | Dado pessoal | ❌ Sem proteção adicional |
| Medico | crm | Dado profissional | ❌ Sem proteção adicional |
| Medico | assinaturaDigital | Dado sensível | ❌ Base64 sem criptografia |
| Paciente | nomeCompleto | Dado pessoal | ❌ Sem proteção adicional |
| Paciente | cpf | Dado sensível | ❌ Plaintext no banco! |
| Paciente | dataNascimento | Dado pessoal | ❌ Sem proteção adicional |
| Paciente | telefone | Dado pessoal | ❌ Sem proteção adicional |
| Exame | urlImagem | Dado clínico | ❌ Path no filesystem |
| Laudo | rascunhoIA | Dado clínico | ❌ TEXT sem criptografia |
| Laudo | textoFinal | Dado clínico | ❌ TEXT sem criptografia |
| Laudo | achadosJson | Dado clínico | ❌ TEXT sem criptografia |

### Gaps LGPD críticos
1. **CPF armazenado em plaintext** — deve ser criptografado em repouso
2. **Dados clínicos sem criptografia** — laudos e exames contêm dados médicos sensíveis
3. **Sem consentimento do paciente** — nenhum campo ou fluxo de consentimento implementado
4. **Sem direito ao esquecimento** — nenhum endpoint de anonimização ou exclusão
5. **Sem log de acesso a dados pessoais** — ipOrigem sempre null

## Backlinks
- [[codebase/snapshots/backend-audit-2026-06-09]]
- [[negocio/permanent/decisoes/ADR-001-jwt-httponly-cookie-protege-contra-xss]]
- [[negocio/mocs/moc-seguranca-lgpd]]
