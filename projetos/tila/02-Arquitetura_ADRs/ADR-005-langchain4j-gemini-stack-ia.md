---
title: "ADR-005: LangChain4j + Gemini como stack de IA por compatibilidade com Spring Boot 4 e Java 21"
type: decision
date: 2026-05-16
status: Accepted
---

# ADR-005: LangChain4j + Gemini como stack de IA por compatibilidade com Spring Boot 4 e Java 21

## Context
O TILA precisa de um framework de IA para integrar LLM multimodal (texto + imagem) com RAG. A stack deve ser compatível com Spring Boot 4 (Jackson 3) e Java 21.

## Decision
LangChain4j 1.0.1 com Google Gemini (gemini-2.5-flash) e pgvector para embeddings.

## Alternatives considered
1. **LangChain (Python)** — maturidade superior, mas TILA é Java
2. **Spring AI** — incipiente em 2026, menos suporte a Gemini
3. **LangChain4j** — Java nativo, Spring Boot starter, compatível com Jackson 3
4. **OpenAI API direto** — sem framework de RAG integrado

## Consequences
- ✅ Integração nativa com Spring Boot via starter
- ✅ AiServices para interface declarativa (TilaRadiologistaAgent)
- ✅ ChatModel para chamadas diretas quando AiServices é limitado (multimodal)
- ✅ EmbeddingStore com pgvector — sem serviço externo
- ⚠️ LangChain4j 1.0.1 teve breaking change de 0.36.2 → 1.0.1
- ⚠️ AiServices não suporta imagem + @UserMessage simultaneamente → workaround com ChatModel direto (ver ADR no código)

## Verified in code
- `pom.xml`: langchain4j-bom 1.0.1
- `TilaRagConfig.java`: beans ChatModel, EmbeddingModel, EmbeddingStore, ContentRetriever, TilaRadiologistaAgent
- `LaudoService.java`: usa ChatModel direto (não AiServices)

## Backlinks
- [[codebase/snapshots/backend-ai-agent-2026-06-09]]
- [[negocio/mocs/moc-pipeline-ia]]
