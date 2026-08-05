---
title: "TILA — AI Pipeline (Motor Híbrido IA v2.0)"
type: context
last_updated: 2026-07-11
---

# TILA — AI Pipeline
> Honest status based on real code implementation and unit verification (60/60 tests passing on 2026-07-11).
> See detailed architectural decision: [[02-Arquitetura_ADRs/ADR-017-seguranca-anti-circunlocucao-e-triagem-4-agudos]]
> See complete technical manual: [[03-Guias_e_Manuais/guia-tila-ai-cloud-service]]

## Current Architecture (`tila-ai-cloud-service` + Backend Java)

```
[Imagem RX + Metadata JSON] 
       │
       ▼ (HTTP POST /api/v1/laudos/gerar)
[tila-ai-cloud-service: FastAPI - Porta 8002]
       │
       ├── Estágio 0: Ingestão & Safety Gates (LGPD EXIF Strip + Gate de Billing 'paid')
       ├── Estágio 1: Pré-processamento (CNN Tensor 224x224 + PNG 1024px)
       ├── Estágio 2: TorchXRayVision CNN (densenet121-res224-all - 18 patologias + confiança bruta)
       ├── Estágio 3: Gemini Vision Cloud API (Morfologia, Incidência, Qualidade e Correlação Estruturada)
       ├── Estágio 4: Reconciliação 3-Way (6 Ramificações de Decisão CNN vs LLM)
       ├── Estágio 5: MedGemma 1.5 4B (Ollama Local via REST - Redação Sem Circunlocução)
       └── Estágio 6: Integração, Triagem 4 Agudos (Edema/Pneumotórax/Consolidação/Derrame) & Veredito Leigo
       │
       ▼ (PythonAIResponseDTO)
[Java Backend LaudoService / Repositório]
```

## What WORKS & VERIFIED IN CODE (60/60 Unit Tests Passing)

| Component | Status | File / Reference |
|---|---|---|
| Ingestão & Descaracterização LGPD/EXIF | ✅ Functional | `pipeline/stage0_ingest.py` (`ImagePackage`) |
| Gate de Faturamento (`billing_mode=paid`) | ✅ Functional | `app/cloud_llm_client.py` (`BillingModeViolationError`) |
| Pré-processamento Dual (CNN + LLM) | ✅ Functional | `pipeline/stage1_prep.py` |
| TorchXRayVision CNN Local (18 Patologias) | ✅ Functional | `models/cnn_vision.py` & `pipeline/stage2_txrv.py` |
| Gemini Vision Morfologia & Correlação | ✅ Functional | `app/cloud_llm_client.py` & `pipeline/stage3_cloud_vision.py` |
| Reconciliação 3-Way (6 Ramificações) | ✅ Functional | `pipeline/stage4_reconciliation.py` |
| Redação Técnica via MedGemma 1.5 4B | ✅ Functional | `pipeline/stage5_medgemma.py` |
| Triagem dos 4 Agudos (`URGENTE` vs `ATENCAO`) | ✅ Functional | `pipeline/stage6_integration.py` |
| Sanitização de Veredito Leigo & Guardrails | ✅ Functional | `models/guardrails.py` & `pipeline/stage6_integration.py` |
| Rastreabilidade Completa no DTO | ✅ Functional | `schemas/contracts.py` (`billing_mode_utilizado`) |

## Key Safety & Compliance Rules Enforced
1. **Anti-Circunlocução Etiológica:** `correlacao_clinica` é tipado em lista estruturada (`list[CloudVisionCorrelacaoItem]`), proibindo prosas com nomes ou conjecturas sindrômicas/etiológicas na saída da IA.
2. **Triagem dos 4 Agudos:** `criticidade_geral == URGENTE` só é disparado se a imagem demonstrar `Edema`, `Pneumothorax`, `Consolidation` ou `Effusion` presentes. Achados não agudos (`Nodule`, `Mass`) geram `ATENCAO`.
3. **Resumo Leigo Seguro:** O `veredito_leigo` utiliza dicionário neutro/estrutural sem alegações probabilísticas ("benigno", "leve") e insere aviso regulatório na abertura e encerramento.
4. **Auditoria de Faturamento:** Todas as chamadas com exames de pacientes reais (`origem_exame_real=True`) exigem `CLOUD_LLM_BILLING_MODE=paid`, sob pena de bloqueio HTTP 403.
