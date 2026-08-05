---
title: "RAG vs LLM Wiki — Comparação"
type: concept
tags: [architecture, rag, llm-wiki, karpathy, knowledge-management]
sources: []
last_updated: 2026-05-07
---

# RAG vs LLM Wiki — Comparação

## Dois Paradigmas de Gestão de Conhecimento com LLM

Existem duas abordagens fundamentalmente diferentes para manter e acessar conhecimento com assistentes de IA. Entender quando usar cada uma é crucial para o design do TILA.

---

## RAG — Retrieval-Augmented Generation

### Como Funciona
1. **Indexação**: Documentos são divididos em chunks e convertidos em embeddings (vetores numéricos).
2. **Armazenamento**: Embeddings são armazenados em um vector database (ex: pgvector, Pinecone, Chroma).
3. **Query**: A pergunta do usuário é convertida em embedding.
4. **Retrieval**: Os chunks mais similares são recuperados via similarity search.
5. **Generation**: O LLM recebe os chunks como contexto e gera a resposta.

### Vantagens
| Vantagem | Detalhes |
|---|---|
| Escala | Funciona com milhões de documentos |
| Atualização fácil | Basta re-indexar novos documentos |
| Citabilidade | Pode apontar para o documento fonte exato |
| Sem curadoria | Automatizado — não requer organização manual |
| Bom para dados brutos | Funciona com PDFs, artigos, manuais tal como estão |

### Desvantagens
| Desvantagem | Detalhes |
|---|---|
| Retrieval noise | Chunks irrelevantes podem poluir o contexto |
| Sem síntese | Não cria conhecimento novo — apenas busca o existente |
| Fragmentação | Conhecimento dividido em chunks sem visão holística |
| Dependência de embeddings | Qualidade depende do modelo de embedding |
| Sem interligação | Chunks não se referenciam — sem grafo de conhecimento |

---

## LLM Wiki — Padrão Karpathy

### Como Funciona
1. **Raw sources** (`raw/`): Documentos brutos são depositados pelo humano.
2. **Compilação**: O LLM lê a fonte, extrai insights, e escreve páginas `.md` interligadas em `wiki/`.
3. **Síntese**: A cada nova fonte, o LLM atualiza páginas existentes, resolve contradições, e mantém um overview coerente.
4. **Query**: Para responder perguntas, o LLM lê o index e as páginas relevantes — como um humano consultando uma enciclopédia.
5. **Evolução**: O conhecimento é **compilado** e **acumulado** — nunca evapora.

### Vantagens
| Vantagem | Detalhes |
|---|---|
| Síntese ativa | O LLM cria conhecimento novo, conecta ideias, resolve contradições |
| Persistência | Conhecimento sobrevive entre sessões — é materializado em `.md` |
| Interligação | Wiki com cross-references cria um grafo de conhecimento navegável |
| Legibilidade | Páginas são legíveis por humanos (Obsidian, VS Code, etc.) |
| Qualidade crescente | Cada ingest melhora a wiki — efeito compounding |
| Auditabilidade | Todas as mudanças são versionáveis (Git) |

### Desvantagens
| Desvantagem | Detalhes |
|---|---|
| Escala limitada | Não funciona para milhões de documentos — curadoria é necessária |
| Custo por ingest | Cada ingest consome tokens LLM significativos |
| Manutenção | Wiki pode acumular contradições se não for lintada periodicamente |
| Overhead | Requer schema, skills, convenções — setup inicial significativo |

---

## Quando Usar Cada Abordagem

| Cenário | RAG | LLM Wiki | Razão |
|---|---|---|---|
| Base de conhecimento médico (100k+ docs) | ✅ | ❌ | Escala massiva — RAG + pgvector |
| Decisões arquiteturais do projeto | ❌ | ✅ | Poucos itens, alta interconexão, evolução constante |
| Laudos anonimizados para padrões | ❌ | ✅ | Extrair padrões, não buscar documentos |
| Artigos científicos para consulta | ✅ | ❌ | Volume alto, consulta pontual |
| Convenções de código do time | ❌ | ✅ | Poucos itens, alta importância, evoluem com o projeto |
| FAQs de suporte ao paciente | ✅ | ❌ | Volume moderado, respostas padronizadas |

---

## Decisão do TILA

O Tila_Brain (este vault) usa o **padrão LLM Wiki** porque:

1. **O escopo é gerenciável** — centenas de páginas, não milhões de documentos.
2. **Interconexão é essencial** — decisões arquiteturais, convenções, e requisitos LGPD se referenciam mutuamente.
3. **Síntese importa mais que busca** — queremos que o LLM entenda o projeto holisticamente, não que busque snippets.
4. **Persistência entre sessões** — cada sessão de trabalho constrói sobre o conhecimento anterior.
5. **Auditabilidade** — todas as mudanças são versionadas no Git.

O RAG será usado **dentro do pipeline do TILA** (Stage 3 do [[context/ai-pipeline]]) para a **base de conhecimento médico** — guidelines, protocolos, achados de referência. São dois sistemas complementares, não competitivos:

```
Tila_Brain (LLM Wiki)          TILA Pipeline (RAG)
├── Conhecimento do projeto    ├── Conhecimento médico
├── Decisões arquiteturais     ├── Guidelines clínicos
├── Convenções de código       ├── Protocolos de exame
└── Evolução curada            └── Busca semântica massiva
```

## Referências
- [[context/ai-pipeline]] — Pipeline que usa RAG no Stage 3
- [[wiki/overview]] — Visão geral do brain

## Backlinks
- [[wiki/overview]]
- [[context/ai-pipeline]]
