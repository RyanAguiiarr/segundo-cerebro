# ADR-007: Microsserviço Python (FastAPI) Isolado para Pipeline de IA

- **Status:** Aceito
- **Data:** 2026-06-27
- **Decisores:** Ryan, Agente Antigravity, Validação Externa (IA)

## Contexto e Problema

O TILA originalmente foi concebido com uma arquitetura monolítica no backend Spring Boot utilizando LangChain4j e chamadas para APIs remotas (Gemini Flash). No entanto, o processamento de imagens médicas (radiografias DICOM) com modelos multimodais de última geração exige processamento intensivo em GPU, manipulação de tensores (PyTorch) e anonimização rigorosa pré-inferência. O ecossistema Java não possui ferramental maduro nem performance competitiva para inferência local multimodal em GPU (CUDA).

## Decisão

Criar um microsserviço independente em Python 3.11 exposto via **FastAPI** (`tila-ai-service`, operando na porta `8001`) dedicado exclusivamente à ingestão DICOM, triagem por visão computacional (TorchXRayVision), busca vetorial clínica (ClinicalBERT + pgvector) e geração multimodal do pré-laudo (MedGemma 1.5 4B).

O backend Spring Boot se comunicará com o microsserviço de IA de forma síncrona/assíncrona via HTTP REST (`TilaAIIntegrationService`), atuando como orquestrador transacional e guardião das regras de negócio e persistência principal.

## Consequências

### Positivas
- **Isolamento de Recursos:** O ciclo de vida pesado da GPU (carregamento de pesos de 4B parâmetros na VRAM da RTX 4060) não afeta a memória JVM nem a latência das requisições web transacionais no Spring Boot.
- **Especialização de Stack:** Permite o uso nativo do ecossistema líder em IA médica (Hugging Face Transformers, PyTorch, pydicom).
- **Escalabilidade Independente:** O serviço de IA pode ser escalado em nós dedicados com GPU sem necessidade de replicar a aplicação corporativa Spring Boot.

### Negativas / Riscos
- **Complexidade Operacional:** Necessidade de gerenciar dois runtimes em produção (JVM Java 21 e Python 3.11 venv).
- **Orquestração de Falhas:** O Spring Boot precisa tratar timeouts e indisponibilidades temporárias do serviço de IA (mitigado por estados como `FALHA_IA` no banco de dados).
