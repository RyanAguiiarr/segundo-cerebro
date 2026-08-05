---
title: "DTOs TILA são Java records com Bean Validation — nunca classes mutáveis"
type: pattern
domain: backend
tags: [dto, records, validation]
verified_in: [LoginRequestDTO.java, MedicoRequestDTO.java, PacienteRequestDTO.java, LaudoGeracaoRequestDTO.java, LaudoResponseDTO.java, PacienteResponseDTO.java, GeminiLaudoResponse.java]
violations_found: [ConsultaDTO.java, ExameRequestDTO.java]
last_updated: 2026-06-09
---

# DTOs TILA são Java records com Bean Validation — nunca classes mutáveis

## O padrão

Todos os DTOs são Java `record` — imutáveis por definição. Request DTOs usam Jakarta Bean Validation.

## Exemplos reais (verificados)

### Request DTO com validação
```java
public record MedicoRequestDTO(
    @NotBlank(message = "campo email não pode ser nulo.") @Email String email,
    @NotBlank(message = "campo senha não pode ser nulo.") String senha,
    @NotBlank(message = "campo crm não pode ser nulo.") String crm,
    @NotBlank(message = "campo nome não pode ser nulo.") String nome,
    @NotBlank(message = "campo especialidade não pode ser nulo.") String especialidade
) {}
```

### Response DTO com factory method
```java
public record PacienteResponseDTO(
    Long id, String nomeCompleto, String cpf, LocalDate dataNascimento, List<ExameResponseDTO> exames
) {
    public static PacienteResponseDTO fromEntity(Paciente paciente) { ... }
}
```

### IA Response DTO
```java
public record GeminiLaudoResponse(
    List<String> achados, List<String> impressaoDiagnostica,
    String notaIA, Integer confidenceScore,
    List<String> recomendacoes, String classificacao
) {}
```

## Conformidade: ~90%
- 11 de 13 DTOs são records ✅
- ConsultaDTO é record vazio (placeholder) ⚠️
- Todos os request DTOs com validação usam @Valid no controller ✅

## Backlinks
- [[negocio/permanent/decisoes/ADR-003-java-records-imutaveis-dtos]]
- [[codebase/snapshots/backend-audit-2026-06-09]]
