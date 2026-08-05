---
title: "ADR-006: pgvector no PostgreSQL para embeddings evita serviço externo e simplifica operação"
type: decision
date: 2026-06-06
status: Accepted
---

# ADR-006: pgvector no PostgreSQL para embeddings evita serviço externo e simplifica operação

## Context
O RAG do TILA precisa de vector store para embeddings. Opções: serviço gerenciado (Pinecone, Weaviate) ou extensão no próprio PostgreSQL (pgvector).

## Decision
Usar pgvector como extensão do PostgreSQL existente (vectorDB na porta 5434).

## Alternatives considered
1. **Pinecone** — gerenciado, mas custo mensal + vendor lock-in
2. **Weaviate** — open source, mas serviço separado para operar
3. **pgvector** — extensão do PostgreSQL, sem serviço adicional
4. **ChromaDB** — Python-first, incompatível com stack Java

## Consequences
- ✅ Sem serviço adicional — usa o mesmo PostgreSQL
- ✅ LangChain4j tem `langchain4j-pgvector` nativo
- ✅ Backup e operação unificados com o banco principal
- ⚠️ Performance pode ser inferior a Pinecone para volumes muito grandes
- ⚠️ Banco está em localhost:5434 com nome `vectorDB` — separado do banco principal?

## Verified in code
- `TilaRagConfig.java`: PgVectorEmbeddingStore(host=localhost, port=5434, database=vectorDB, table=tila_embeddings, dimension=768)
- `pom.xml`: langchain4j-pgvector no BOM
- `GoogleAiEmbeddingModel`: gemini-embedding-001, 768 dims

## Backlinks
- [[codebase/snapshots/backend-ai-agent-2026-06-09]]
- [[negocio/mocs/moc-pipeline-ia]]
