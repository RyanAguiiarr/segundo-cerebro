---
title: "ADR-003: Arquitetura de Segurança (Security Architecture)"
type: decision
tags: [adr, security, architecture, roles, jwt, bcrypt]
status: Accepted (com débito técnico e falhas críticas)
last_updated: 2026-05-07
---

# ADR-003: Arquitetura de Segurança (Security Architecture)

## Status
Aceito e Implementado Parcialmente. Débitos técnicos severos identificados durante a auditoria de 2026-05-07.

## Contexto
O TILA é uma plataforma médica (HealthTech) que lida com dados protegidos pela LGPD (Lei Geral de Proteção de Dados - Artigo 11). Qualquer vulnerabilidade pode causar desde sanções judiciais a danos à integridade do paciente (ex: laudos adulterados).
O time precisava decidir a estratégia de controle de acesso (AuthZ), prova de identidade (AuthN), criptografia de dados em repouso e trilha de auditoria.

## Decisões Arquiteturais Tomadas (As 6 Decisões)

### 1. Criptografia de Senha (AuthN)
Decidiu-se pelo **BCrypt (Fator 10)** para todas as senhas de `Usuario`.
```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(); // Implementação segura default do Spring
}
```

### 2. Gestão de Sessão (Transporte)
Decidiu-se por **Stateless Tokens (JWT)**.
O servidor não armazena sessões na memória (HTTP Session). Escala melhor e previne CSRF atrelado à sessão do JSESSIONID tradicional.

### 3. Controle de Acesso Baseado em Papéis (RBAC - Role Based Access Control)
Decidimos por um modelo de autorização rígido com três papéis (Roles):
- **ROLE_PACIENTE**: Acesso apenas de leitura aos próprios exames e laudos.
- **ROLE_MEDICO**: Acesso de criação/edição aos laudos, permissão para rodar a IA do TILA.
- **ROLE_ADMIN**: Pode cadastrar médicos, ver logs de auditoria e calibrar o RAG.

### 4. Modelo de Injeção das Roles no JWT
As roles não seriam puxadas do banco em cada requisição; elas seriam "carimbadas" como uma *Claim* dentro do JWT na hora do login. Isso alivia o banco de dados.

### 5. Configuração CORS Restritiva
Como a API e o Angular rodarão em domínios diferentes (ex: `api.tila.com` e `app.tila.com`), habilitou-se o CORS global, porém fechado apenas para o front-end.
```java
configuration.setAllowedOrigins(Arrays.asList("http://localhost:4200")); // Restritivo e correto para DEV
```

### 6. Trilha de Auditoria Universal
Decidimos criar uma entidade `LogAuditoria` e salvá-la em todos os pontos críticos (Controller/Service) de operações CREATE, UPDATE, DELETE e Logins, garantindo compliance com o rastreio (Data Lineage) exigido.

---

## Consequências e Débitos Técnicos (As 8 Decisões Pendentes/Mal-executadas)

O design foi bem concebido na teoria, mas a execução prática falhou gravemente em várias frentes de segurança essenciais.

### 🔴 1. A Exposição das Chaves (Secrets Leak)
A decisão de usar JWT HMAC (Simétrico) não é um problema. O problema é que a chave de assinatura (`api.security.token.secret`) não foi isolada por injeção de dependência via variável de ambiente, sendo comitada no código fonte (`Cucamole@123`). 

### 🔴 2. JWT Transportado sem SSL Flag (`Secure=false`)
Os cookies definidos por `AutenticacaoController.java` não forçam a flag `Secure`. Isso torna a aplicação altamente vulnerável a ataques de interceptação (Packet Sniffing) caso acessada num ambiente corporativo/hospitalar sem VPN.

### 🔴 3. Falha no Tratamento da Role_Admin
A configuração do SecurityFilterChain no `SecurityConfigurations.java` liberou rotas de extrema criticidade para qualquer autenticado.
```java
// O Código atual:
req.requestMatchers(HttpMethod.OPTIONS, "/**").permitAll();
req.requestMatchers("/auth/**").permitAll(); // /auth/me vazou aqui!
req.requestMatchers("/medicos/**").hasRole("MEDICO");
req.requestMatchers("/paciente/**").hasAnyRole("MEDICO", "PACIENTE");
req.anyRequest().authenticated(); // 🔴 O GET /logs está caindo aqui!
```
O endpoint que devolve os Logs de Segurança está sendo servido para **qualquer um** logado, expondo dados de IPs, IDs e hashes de usuários.

### 🔴 4. Logs de Auditoria Incompletos (O "Fantasma" ipOrigem)
A entidade LogAuditoria declara o campo `ipOrigem`, mas nas invocações dos Services o `HttpServletRequest` nunca é passado para injetar o IP do usuário real. Uma auditoria médica inútil do ponto de vista forense.

### 🟡 5. LGPD "Data at Rest" Encryption Não Implementado
Optou-se por focar no BCrypt para senhas, mas ignorou-se que Nomes de Pacientes, CPFs e os Laudos Inteiros estão armazenados em texto-plano no banco PostgreSQL. Faltou a decisão de implementar TDE (Transparent Data Encryption) do Postgres ou `@Converter(converter = CryptoConverter.class)` do Hibernate.

### 🟡 6. Ausência de Refresh Token
JWTs não podem ser revogados a menos que você crie uma Blacklist no banco (quebrando a vantagem de ser Stateless). O padrão é vida-curta (15 min) com Refresh-Token vida-longa (7 dias). A equipe colocou vida-longa (1h) sem Refresh, o que significa:
1. Uma janela de 1 hora de vulnerabilidade total se o token for roubado.
2. Médicos perdendo laudos longos na tela porque o token morre sem renovar.

### 🟡 7. Injeção de Risco (NullPointer) no SecurityFilter
Tentamos salvar acessos ao banco injetando a Role no Token, porém o filtro foi programado para ainda assim ir no banco a *cada requisição* via `usuarioRepository.findByEmail()`, com o agravante de chamar um `.get()` sem validar. Se um médico pedir demissão e seu usuário for deletado enquanto logado, o sistema derruba o servidor.

### 🔵 8. Rate Limiting Ausente
Nenhuma decisão foi tomada sobre estrangulamento de requisições. O endpoint `/auth/login` é vulnerável a *Credential Stuffing* massivo sem nenhuma trava anti-Bruteforce, bloqueio de IP ou Captcha.

## Ação de Correção Recomendada
As 4 vulnerabilidades marcadas como "🔴" devem ser atacadas imediatamente no Sprint 1 antes do provisionamento em Nuvem. O arquivo `application.properties` deve ser reescrito com referências `${}` de variáveis de sistema do SO.

## Backlinks
- [[context/security-lgpd]]
- [[wiki/concepts/jwt-authentication]]
