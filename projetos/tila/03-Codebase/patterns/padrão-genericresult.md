---
title: "Todo endpoint TILA retorna ResponseEntity<GenericResult<T>> para padronizar erros e dados"
type: pattern
domain: backend
tags: [api, response, pattern]
verified_in: [AutenticacaoController.java, PacienteController.java, LaudoController.java, LogAuditoriaController.java, GlobalExceptionHandler.java]
violations_found: []
last_updated: 2026-06-09
---

# Todo endpoint TILA retorna ResponseEntity\<GenericResult\<T\>\> para padronizar erros e dados

## O padrão

`GenericResult<T>` é o envelope universal de resposta da API TILA. Toda response segue esta estrutura:

```json
{
  "success": true,
  "message": "Operação realizada com sucesso !",
  "data": { ... }
}
```

## Implementação real (GenericResult.java)

```java
@Getter
public class GenericResult<T> {
    private final boolean success;
    private final String message;
    private final T data;

    protected GenericResult(boolean success, String message, T data) { ... }

    public static <T> GenericResult<T> success(T data) { ... }
    public static <T> GenericResult<T> success(T data, String message) { ... }
    public static <T> GenericResult<T> error(String message) { ... }
}
```

## Uso nos controllers (verificado)

```java
// Success path
return ResponseEntity.status(HttpStatus.CREATED).body(GenericResult.success(response));
return ResponseEntity.ok(GenericResult.success(response));

// Error path (via GlobalExceptionHandler)
return ResponseEntity.status(HttpStatus.NOT_FOUND).body(GenericResult.error(ex.getMessage()));
return ResponseEntity.badRequest().body(GenericResult.error(ex.getMessage()));
```

## Conformidade: 100%
Todos os 8 endpoints verificados seguem o padrão. O GlobalExceptionHandler também usa GenericResult para erros.

## Backlinks
- [[negocio/permanent/decisoes/ADR-002-genericresult-envelope-universal]]
- [[codebase/snapshots/backend-audit-2026-06-09]]
