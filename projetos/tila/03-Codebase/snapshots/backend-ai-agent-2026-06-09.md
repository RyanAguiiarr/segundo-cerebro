---
title: "Auditoria AI Agent TILA — Snapshot 2026-06-09"
type: snapshot
scope: ai
date: 2026-06-09
immutable: true
---

# Auditoria do Pipeline de IA — TILA
> Snapshot imutável de 2026-06-09

## Status geral: PARCIALMENTE FUNCIONAL (orquestração ~85%, pipeline completo ~30%)

## O que funciona hoje

### 1. LangChain4j Integration ✅
- **Versão**: 1.0.1 (via BOM)
- **Módulos**: langchain4j, langchain4j-spring-boot-starter, langchain4j-google-ai-gemini, langchain4j-pgvector
- **ChatModel**: `GoogleAiGeminiChatModel` configurado como bean
- **Model name no bean**: `gemini-2.5-flash` (⚠️ conflita com application.properties que diz `gemini-1.5-flash`)
- **Temperatura**: 0.3
- **API key**: via `${GEMINI_API_KEY}` no bean (✅), mas hardcoded em application.properties (🔴)

### 2. TilaRadiologistaAgent interface ✅
- Interface `@SystemMessage(fromResource = "prompts/radiologista-system.txt")`
- `@UserMessage` com template para contexto do exame
- Parâmetros: tipoExame, nomePaciente, idadePaciente, generoPaciente, regiaoAnatomica, dataExame, observacoesMedico
- ⚠️ Interface definida mas NÃO USADA pelo LaudoService (que usa ChatModel direto)

### 3. LaudoService — Orquestração funcional ✅
- Fluxo completo: Busca médico → Busca exame → Carrega imagem → Carrega system prompt → Monta contexto → Chama Gemini → Parseia JSON → Formata rascunho → Persiste laudo
- Usa `ChatModel` diretamente (não AiServices) — decisão documentada em ADR-004
- Mensagem multimodal: SystemMessage + UserMessage com TextContent + ImageContent
- Parse de resposta JSON com limpeza de markdown code blocks
- GeminiLaudoResponse: record com achados, impressaoDiagnostica, notaIA, confidenceScore, recomendacoes, classificacao

### 4. EmbeddingModel ✅
- `GoogleAiEmbeddingModel` com `gemini-embedding-001`
- Dimensionalidade: 768

### 5. pgvector EmbeddingStore ✅
- Configurado via `PgVectorEmbeddingStore`
- Host: localhost:5434, database: vectorDB
- Tabela: `tila_embeddings`, dimensão: 768
- ⚠️ Usa senha do banco diretamente (não variável separada para vector DB)

### 6. ContentRetriever ✅ (configurado, não testado em produção)
- `EmbeddingStoreContentRetriever` com maxResults=8, minScore=0.8
- ⚠️ ContentRetriever é injetado no bean `tilaAgent()` via AiServices, mas LaudoService NÃO usa AiServices

## O que é MOCKED ou STUB

### TilaRadiologistaAgent via AiServices ⚠️
- Bean `tilaAgent()` é criado via `AiServices.builder()` com ChatModel + ContentRetriever
- Mas `LaudoService` NÃO injeta `TilaRadiologistaAgent` — usa `ChatModel` diretamente
- Resultado: o agente com RAG está configurado mas NUNCA é chamado
- O ContentRetriever (pgvector RAG) está efetivamente desconectado do fluxo de geração

### System prompt loading ⚠️
- `carregarSystemPrompt()` lê de `classpath:prompts/radiologista-system.txt`
- Arquivo existe? Não foi possível verificar se o recurso está no classpath
- Se não existir: RuntimeException na primeira chamada

### Image loading ⚠️
- `carregarImagemExame()` tenta carregar de `{uploadPath}/{urlImagem}`
- Fallback: caminho absoluto se urlImagem já for absoluto
- ⚠️ Sem validação de mime type real (infere de extensão)
- ⚠️ Sem limite de tamanho de imagem no carregamento
- ⚠️ uploadPath padrão é `./uploads/exames` — relativo ao CWD

## O que NÃO está implementado

### DICOM Pipeline ❌
- Nenhum código DICOM no projeto
- Sem DCM4CHE ou similar
- Sem parsing de tags DICOM
- Sem scrubbing de metadados identificadores
- Gap completo entre "imagem DICOM" e "imagem processável pela IA"

### CNN (Convolutional Neural Network) ❌
- Nenhum modelo de visão computacional treinado
- Dependência total do Gemini Vision para análise de imagem
- Sem fine-tuning ou transfer learning
- Sem pipeline de treinamento ou dataset

### RLHF (Reinforcement Learning from Human Feedback) ❌
- Nenhuma infraestrutura de feedback
- `LaudoRevisaoRequestDTO` existe mas NÃO é usado em nenhum endpoint
- Sem captura de edições do médico vs rascunho da IA
- Sem loop de feedback para melhoria do modelo

### RAG Operacional ❌
- EmbeddingStore configurado mas sem ingestão de dados
- Tabela `tila_embeddings` presumivelmente vazia
- `ConhecimentoMedico` entity existe (PROTOCOLO, ANATOMIA, ACR_BIRADS, etc.)
- Mas sem endpoint ou processo para ingerir conteúdo na base de conhecimento
- Sem endpoint para popular embeddings
- ContentRetriever configurado mas desconectado do fluxo real

### Monitoramento IA ❌
- Sem tracking de latência das chamadas ao Gemini
- Sem log de custo por chamada
- Sem métricas de qualidade (confidence score médio, taxa de rejeição)
- Sem alertas

## Conflitos de configuração

1. **Modelo duplicado**: TilaRagConfig cria `ChatModel` com `gemini-2.5-flash`, mas `application.properties` configura `gemini-1.5-flash` via LangChain4j auto-config. Qual é usado depende de qual bean tem precedência.
2. **Agente não utilizado**: `tilaAgent()` bean criado com RAG, mas LaudoService injeta `ChatModel` direto.
3. **application.properties linhas 14-17**: Configuração de chat-model via properties E via bean Java — potencial conflito.

## Gap: Estado atual → Pipeline completo

```
HOJE                    →  META
─────────────────────────────────────────
Imagem JPEG/PNG         →  DICOM ingest + scrubbing
Gemini Vision direto    →  CNN pré-processamento + Gemini
Sem RAG no fluxo        →  RAG com ConhecimentoMedico
Sem feedback            →  RLHF com edições médicas
Sem monitoramento       →  Dashboard de métricas IA
1 modalidade (RX Tórax) →  Múltiplas modalidades
```

## Backlinks
- [[codebase/snapshots/backend-audit-2026-06-09]]
- [[negocio/permanent/decisoes/ADR-005-langchain4j-gemini-stack-ia]]
- [[negocio/permanent/decisoes/ADR-006-pgvector-postgresql-embeddings]]
- [[negocio/mocs/moc-pipeline-ia]]
