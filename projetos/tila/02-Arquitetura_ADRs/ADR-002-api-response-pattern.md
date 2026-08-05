---
title: "ADR-002: Padrão de Resposta de API (GenericResult)"
type: decision
tags: [adr, api, rest, pattern, generic-result]
status: Accepted (com ressalvas)
last_updated: 2026-05-07
---

# ADR-002: Padrão de Resposta de API (GenericResult)

## Status
Aceito e Implementado (porém com falha de consistência no tratamento de exceções).

## Contexto
O projeto TILA (Tecnologia Integradora de Laudos Automatizados) exige uma comunicação assíncrona robusta entre o Frontend Angular (que funciona 100% via requisições AJAX/HttpClient) e o Backend Spring Boot.
Historicamente, APIs REST mal projetadas retornam diretamente os objetos de domínio (ex: `[{"id": 1, "nome": "João"}]`) ou status code puro sem corpo em caso de erro, obrigando o Frontend a "adivinhar" o que deu errado.
A equipe precisava de um contrato unificado, um "envelope", para que o Frontend soubesse exatamente onde ler a mensagem de sucesso/erro e os dados de carga útil (payload).

## Decisão

Adotamos o padrão **Wrapper Envelope** através da classe genérica `GenericResult<T>`.
Todas as respostas (2xx, 4xx, 5xx) deverão seguir estritamente o seguinte contrato JSON:

```json
{
  "success": boolean,
  "message": string,
  "data": T | null
}
```

A classe base foi estruturada para ser imutável e criada apenas através de factory methods estáticos, forçando o desenvolvedor a não adulterar a resposta no meio do request.

**Código Central da Decisão (`GenericResult.java`):**
```java
@Getter
public class GenericResult<T> {
    private final boolean success;
    private final String message;
    private final T data;

    protected GenericResult(boolean success, String message, T data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }

    public static <T> GenericResult<T> success(T data){
        return new GenericResult<>(true, "Operação realizada com sucesso !", data);
    }

    public static <T> GenericResult<T> error(String message){
        return new GenericResult<>(false, message, null);
    }
}
```

## Consequências

### Pontos Positivos
* **Consistência no Frontend**: O Angular precisa apenas de uma única interface global:
  ```typescript
  export interface GenericResult<T> {
    success: boolean;
    message: string;
    data: T;
  }
  ```
* **Tratamento Reativo Elegante**: Todos os `ApiServices` do Angular interceptam via `RxJS tap()` se a requisição é `res.success` e disparam um erro customizado se não for, impedindo que os componentes de UI tenham que lidar com ifs complexos.

  ```typescript
  // Exemplo de como o Frontend se beneficiou do ADR
  return this.http.post<GenericResult<User>>(`${this.baseUrl}/login`, req).pipe(
      tap({
          next: (res) => { if (!res.success) throw new Error(res.message); }
      })
  );
  ```
* **Padrão Fácil para a Equipe**: Qualquer novo programador Spring só precisa fazer `return ResponseEntity.ok(GenericResult.success(dto));`.

### Pontos Negativos & Dívida Técnica Gerada (GAPS IDENTIFICADOS)

Infelizmente, a decisão arquitetural foi **quebrada** no tratamento global de erros (ControllerAdvice).

Ao invés de retornar o GenericResult configurado com `false` para erros de aplicação (como "Paciente não encontrado" - HTTP 404), o `GlobalExceptionHandler` introduziu um record privado chamado `ErrorDetalhe`, desrespeitando este próprio ADR.

**O Desvio (Anti-pattern Atual):**
```java
// Em GlobalExceptionHandler.java
private record ErrorDetalhe(String mensagem){} // 🔴 VIOLAÇÃO DO ADR!

@ExceptionHandler(EntityNotFoundException.class)
public ResponseEntity handle404(EntityNotFoundException ex){
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(new ErrorDetalhe(ex.getMessage())); // Retorna { "mensagem": "..." }
}
```

**Consequência do Desvio:**
O frontend tenta interceptar a propriedade `message`, mas o JSON contém `mensagem`. O RxJS tentará acessar `res.success`, que será `undefined` (falsy) – lançando um erro vago na UI em vez do erro formatado do backend.

## Ação de Correção Recomendada
Refatorar imediatamente o `GlobalExceptionHandler` para respeitar este ADR.

```java
// O Código deveria ser assim:
@ExceptionHandler(EntityNotFoundException.class)
public ResponseEntity<GenericResult<Void>> handle404(EntityNotFoundException ex){
    return ResponseEntity.status(HttpStatus.NOT_FOUND)
        .body(GenericResult.error(ex.getMessage())); // Retorna { "success": false, "message": "...", "data": null }
}
```

## Backlinks
- [[wiki/concepts/backend-patterns]]
- [[context/coding-conventions]]
