---
title: "MOC — Pipeline de IA"
type: moc
cluster: pipeline-ia
last_updated: 2026-07-11
---

# MOC — Pipeline de IA

> Mapa de navegação para notas relacionadas ao Motor Híbrido e pipeline de inteligência artificial da Tila.

## Decisões Arquiteturais (ADRs)
- [[02-Arquitetura_ADRs/ADR-005-langchain4j-gemini-stack-ia]] — Escolha de LangChain4j + Gemini (Java)
- [[02-Arquitetura_ADRs/ADR-006-pgvector-postgresql-embeddings]] — pgvector para embeddings
- [[02-Arquitetura_ADRs/ADR-007-microsservico-python-fastapi-para-pipeline-ia]] — Microsserviço Python FastAPI isolado (`tila-ai-cloud-service`)
- [[02-Arquitetura_ADRs/ADR-008-medgemma-substitui-gemini-flash]] — MedGemma 1.5 4B local
- [[02-Arquitetura_ADRs/ADR-009-medgemma-first-pipeline]] — Pipeline MedGemma-First
- [[02-Arquitetura_ADRs/ADR-016-titan-v4-3-blind-reading-mastery]] — TITAN v4.3 Blind Reading Mastery & Raciocínio Morfológico
- [[02-Arquitetura_ADRs/ADR-017-seguranca-anti-circunlocucao-e-triagem-4-agudos]] — Pipeline Híbrido Anti-Circunlocução, Triagem dos 4 Agudos e Guardrails

## Guias Técnicos e Manuais
- [[03-Guias_e_Manuais/guia-tila-ai-cloud-service]] — Guia Técnico e Manual Operacional Detalhado do Motor Híbrido IA (`tila-ai-cloud-service`)

## Domínio e Conceitos
- [[04-Wiki_Conceitos/conceitos/motor-hibrido-ia-tila-engine]] — Motor Híbrido IA (MedGemma INT4 + TorchXRayVision + TILA Engine)
- [[01-Negocio/medico/laudo-ia-exige-revisao-humana-obrigatoria]] — Por que IA gera rascunhos de apoio ao médico
- [[01-Negocio/produto/tila-resolve-gargalo-de-laudos-manuais]] — Proposta de valor do produto

## Estado Real do Pipeline (`tila-ai-cloud-service` - 2026-07-11)
| Componente | Status | Observação |
|---|---|---|
| Ingestão HTTP & Safety Gate (`ImagePackage`) | ✅ Funcional | EXIF LGPD strip + bloqueio de faturamento free |
| TorchXRayVision CNN (`densenet121-res224-all`) | ✅ Funcional | Inferência de 18 patologias torácicas |
| Gemini Vision Cloud API | ✅ Funcional | Morfologia e correlação estruturada anti-circunlocução |
| Reconciliação 3-Way (CNN + LLM + Confiança) | ✅ Funcional | Árvore de decisão com 6 ramificações e flags de discrepância |
| Redação Técnica via MedGemma 1.5 4B | ✅ Funcional | Fronteiras estanques e scores qualitativos ("ótima/boa/limitada") |
| Triagem dos 4 Agudos (`criticidade_geral`) | ✅ Funcional | `URGENTE` reservado para Edema/Pneumotórax/Consolidação/Derrame |
| Veredito Leigo Sanitizado (`_EXPLICACOES_LEIGO`) | ✅ Funcional | Sem probabilística benigna/maligna + avisa sobre indeterminados |
| Rastreabilidade de Faturamento (`billing_mode_utilizado`) | ✅ Funcional | Proveniência completa gravada em 100% dos DTOs |
| Cobertura de Testes Unitários (`pytest -v`) | ✅ 60/60 Passando | Cobertura integral de todos os 6 estágios e guardrails |
