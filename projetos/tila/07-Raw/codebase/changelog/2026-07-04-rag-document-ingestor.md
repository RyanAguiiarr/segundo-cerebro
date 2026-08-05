# Changelog: RAG Document Ingestor e Semantic Chunking (v2)

**Data**: 2026-07-04  
**Tipo**: Feature / Melhoria Arquitetural  
**Status**: Concluído  

---

## Intenção da Feature
Substituir a ingestão estática/demonstrativa (`ingest_protocols.py`) por um pipeline de ingestão profissional e incremental (`ingest_documents.py`), capaz de ler arquivos reais de diretrizes médicas e laudos de referência, aplicando fatiamento semântico (*Semantic Chunking*) e otimização de busca vetorial via índices HNSW no PostgreSQL (`pgvector`).

---

## Arquivos Criados ou Modificados

### [NEW] `tila-ai-service/scripts/ingest_documents.py`
- Pipeline de ingestão v2 implementado com classe `DocumentIngestor`.
- Suporte a leitura de arquivos `.md`, `.txt`, `.pdf` (via `pypdf`) e `.json` (amostras MIMIC-CXR).
- **Semantic Chunking**: algoritmo que divide textos por cabeçalhos Markdown (`##`/`###`) ou parágrafos de até ~350 palavras, garantindo que o contexto médico não seja cortado abruptamente.
- **Ingestão Incremental (Zero Truncate)**: verificação de duplicidade via hash MD5 (`md5_hash VARCHAR(32) UNIQUE`), evitando reprocessamento de embeddings e permitindo adicionar novos arquivos sem apagar os laudos existentes.
- **Índices HNSW**: criação automática de índices vetoriais (`USING hnsw (embedding vector_cosine_ops)`) nas tabelas `diretrizes_clinicas` e `tila_laudos_referencia`.

### [NEW] `tila-ai-service/data/diretrizes/exemplo_diretriz_sbpt.md`
- Arquivo de diretriz clínica em Markdown contendo protocolos da SBPT/CBR (tuberculose, pneumotórax, nódulo pulmonar, ICC) para validar o Semantic Chunking.

### [NEW] `tila-ai-service/data/mimic_samples/exemplo_laudos_mimic.json`
- Amostras curadas de laudos no padrão MIMIC-CXR (opacidade, consolidação, derrame pleural, normal) para demonstrar ingestão de Few-Shot RAG.

### [MODIFY] `tila-ai-service/requirements.txt`
- Adicionado `pypdf>=4.0.0` para leitura nativa de PDFs no módulo de ingestão.

---

## Padrões e Decisões Adotadas
1. **Curadoria de Dados (Quality > Quantity)**: Alinhado com a ADR-008 e estratégias de engenharia de IA, o RAG é alimentado com amostras curadas e diretrizes estruturadas em vez de dumps brutos de 370k laudos, prevenindo poluição semântica e degradação da precisão de busca.
2. **Índices HNSW em vez de IVFFlat**: HNSW oferece busca por similaridade muito mais rápida (< 5ms) sem necessidade de re-treinar listas de centroides após inserções incrementais.
3. **Idempotência por MD5**: Garante que o script possa ser rodado em cron jobs ou no boot do microsserviço sem gerar chaves duplicadas no banco vetorial.

---

## Referências
- [[04-Wiki_Conceitos/conceitos/motor-hibrido-ia-tila-engine]]
- [[04-Wiki_Conceitos/conceitos/rag-vs-llm-wiki]]
- [[02-Arquitetura_ADRs/ADR-008-medgemma-substitui-gemini-flash]]
