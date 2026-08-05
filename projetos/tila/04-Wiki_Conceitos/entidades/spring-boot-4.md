---
title: "Spring Boot 4"
type: entity
tags: [framework, java, spring, backend]
sources: []
last_updated: 2026-05-07
---

# Spring Boot 4

## Visão Geral

**Spring Boot 4** é a versão atual do framework utilizado pelo backend do TILA. Construído sobre o Spring Framework 6, traz avanços significativos em segurança, performance (Virtual Threads do Java 21), e simplificação de configuração.

## Relevância para o TILA

O TILA utiliza Spring Boot 4 como base do backend, aproveitando:

### SecurityFilterChain Pattern
A configuração de segurança no Spring Boot 4 usa o padrão `SecurityFilterChain` como `@Bean`, substituindo o antigo `WebSecurityConfigurerAdapter` (deprecated desde Spring Security 5.7):

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/auth/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated())
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

### Spring Data JPA com Java 21 Records
DTOs são implementados como Java records, aproveitando a concisão da feature do Java 21:

```java
public record PacienteDTO(
    Long id,
    @NotBlank String nome,
    @NotNull @Past LocalDate dataNascimento,
    @Email String email
) {}
```

> ⚠️ **Nota**: Entidades JPA (`@Entity`) ainda precisam ser classes (não records) por limitações do JPA/Hibernate que requer construtor padrão e campos mutáveis.

### Bean Validation
Integração nativa com Jakarta Bean Validation 3.0:
- `@NotBlank`, `@NotNull`, `@Past`, `@Email`, `@Size`, etc.
- Validação automática com `@Valid` nos controllers.
- Mensagens de erro customizáveis via `messages.properties`.

### Sessões STATELESS
O TILA opera em modo totalmente stateless — sem sessão HTTP no servidor:

```java
.sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
```

Isso é essencial para:
- Escalabilidade horizontal (qualquer instância pode atender qualquer request)
- Compatibilidade com JWT (token contém toda a informação necessária)
- Simplificação do gerenciamento de estado

### Constructor Injection
Spring Boot 4 favorece constructor injection (padrão do TILA):

```java
@Service
public class PacienteService {
    private final PacienteRepository repository;
    
    public PacienteService(PacienteRepository repository) {
        this.repository = repository;
    }
}
```

Quando há um único construtor, `@Autowired` é desnecessário — o Spring resolve automaticamente.

### Novas Features Relevantes
| Feature | Benefício para TILA |
|---|---|
| Virtual Threads (Java 21) | Concorrência leve para I/O-bound (DB, API calls) |
| GraalVM Native Image support | Deploy com startup instantâneo (futuro) |
| Observability (Micrometer) | Métricas e tracing integrados |
| ProblemDetail (RFC 7807) | Respostas de erro padronizadas |
| HTTP Interfaces | Client HTTP declarativo (alternativa a WebClient) |

## Configuração do TILA

### application.properties
```properties
spring.datasource.url=jdbc:postgresql://localhost:5433/TilaDB
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
server.port=8080
```

## Referências
- [[wiki/concepts/jwt-authentication]] — Implementação de auth no Spring Security
- [[wiki/concepts/api-endpoints]] — Endpoints implementados
- [[context/coding-conventions]] — Convenções de código Spring Boot

## Backlinks
- [[wiki/overview]]
- [[wiki/concepts/jwt-authentication]]
- [[context/coding-conventions]]
