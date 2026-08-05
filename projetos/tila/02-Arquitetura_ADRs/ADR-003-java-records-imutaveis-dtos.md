---
title: "ADR-003: Java records imutáveis para DTOs eliminam bugs de estado mutável"
type: decision
date: 2026-05-07
status: Accepted
---

# ADR-003: Java records imutáveis para DTOs eliminam bugs de estado mutável

## Context
DTOs transportam dados entre camadas. Classes mutáveis com getters/setters permitem modificação acidental. Java 16+ oferece records como alternativa imutável.

## Decision
Todos os DTOs são Java records com Bean Validation annotations.

## Alternatives considered
1. **Classes com Lombok @Data** — mutáveis, @Data gera equals/hashCode que pode quebrar em collections
2. **Java records** — imutáveis, compactos, equals/hashCode automáticos
3. **Protobuf/Avro** — overhead desnecessário para API REST simples

## Consequences
- ✅ Imutabilidade garantida pelo compilador
- ✅ Código mais conciso (sem boilerplate)
- ✅ 11 de 13 DTOs são records (verificado 2026-06-09)
- ✅ Response DTOs usam `fromEntity()` factory methods
- ⚠️ Records não suportam herança — não é problema para DTOs

## Verified in code
- `LoginRequestDTO`, `MedicoRequestDTO`, `PacienteRequestDTO`, `LaudoGeracaoRequestDTO`: records com @NotBlank/@Email/@CPF
- `PacienteResponseDTO`, `LaudoResponseDTO`: records com `static fromEntity()`
- `GeminiLaudoResponse`: record para resposta da IA

## Backlinks
- [[codebase/patterns/padrão-dto-records]]
