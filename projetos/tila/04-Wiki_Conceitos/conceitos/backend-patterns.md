---
title: "Backend Patterns — TILA (Verificado)"
type: concept
tags: [backend, patterns, conventions]
sources: [raw/codebase/snapshots/backend-structure.md]
last_updated: 2026-05-07
---

# Backend Patterns — TILA

> Padrões reais extraídos do código em 2026-05-07.

## GenericResult Envelope
```java
GenericResult<T> { success, message, data }
GenericResult.success(data)          // message = "Operação realizada com sucesso !"
GenericResult.success(data, message) // message customizada
GenericResult.error(message)         // data = null
```
Usado em todos os controllers. `GlobalExceptionHandler` **não usa** (usa ErrorDetalhe).

## DTO como Record
```java
public record PacienteRequestDTO(
    @NotBlank String nomeCompleto,
    @NotBlank @CPF String cpf,
    @NotNull LocalDate dataNascimento,
    String telefone
) {}
```
100% dos DTOs são records. Bean Validation aplicado nos records.

## Controller Pattern
```java
@RestController
@RequestMapping("/path")
public class XController {
    // Constructor ou @Autowired (misto)
    
    @PostMapping
    public ResponseEntity<GenericResult<DTO>> criar(@RequestBody @Valid DTO dados) {
        var response = service.metodo(dados);
        return ResponseEntity.status(HttpStatus.CREATED).body(GenericResult.success(response));
    }
}
```

## Service Pattern
```java
@Service
public class XService {
    private final XRepository repository;
    
    public XService(XRepository repository) {  // Constructor injection (padrão desejado)
        this.repository = repository;
    }
    
    @Transactional
    public DTO criar(RequestDTO dto) {
        // Validação de negócio
        // Converter DTO → Entity
        // Salvar
        // Log auditoria
        // Converter Entity → ResponseDTO
        return responseDTO;
    }
}
```

## Audit Log Pattern (inconsistente)
### No Controller (inline)
```java
LogAuditoria log = new LogAuditoria();
log.setUsuario(usuario);
log.setAcao("ACAO");
log.setDataHora(LocalDateTime.now());
logAuditoriaRepository.save(log);
```

### No Service (via helper)
```java
public void registrarLog(Usuario usuario, String acao, LocalDateTime dataHora) {
    var log = new LogAuditoria(usuario, acao, dataHora);
    logAuditoriaRepository.save(log);
}
```

⚠️ **Inconsistente** — deveria ser um service dedicado (`AuditService`) injetado onde necessário.

## Entity Pattern
```java
@Entity
@Table(name = "tabela")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor
public class Entidade {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    // campos...
}
```
- Lombok para boilerplate
- `IDENTITY` para geração de ID (exceto UUID para Usuario)
- Sem `@Builder` em nenhuma entity

## DTO Naming Pattern
Todos os DTOs do sistema devem seguir a nomenclatura padronizada e explícita baseada na direção dos dados. DTOs legados em português ou genéricos (como `DadosAutenticacao` ou `DadosResponseLogin`) foram refatorados:
- **Requisições (Frontend ➡️ Backend)**: `{Contexto}RequestDTO` (ex: `LoginRequestDTO`, `MedicoRequestDTO`)
- **Respostas (Backend ➡️ Frontend)**: `{Contexto}ResponseDTO` (ex: `LoginResponseDTO`, `ExameResponseDTO`)

## Spring Repository Pattern
Todos os repositórios JPA devem obrigatoriamente estender `JpaRepository<T, ID>` e possuir a anotação explícita `@Repository`. Isso garante a injeção apropriada e a tradução de exceções específicas de banco de dados pelo Spring.

## Backlinks
- [[context/coding-conventions]]
- [[wiki/concepts/backend-services]]
- [[wiki/sources/2026-06-07-refatoracao-auth-signals]]
