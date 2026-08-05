# ADR-014: Arquitetura TITAN v4.0 "Gemini-Duplo" (LLM-as-Judge & Segmentação MedSAM em 16-bit)

**Status:** Aceito / Implementado  
**Data:** 05/07/2026  
**Autores:** Equipe de Arquitetura e Engenharia de IA (TILA AI)  

---

## 1. Contexto e Motivação

As versões anteriores do motor de IA radiológica (TITAN v2.0 e v3.0 MedGemma-First) trouxeram avanços significativos ao priorizar a visão pura antes do viés clínico textual. No entanto, três desafios arquiteturais e clínicos persistiam no ambiente de produção:

1. **Gargalo de Hardware e Acurácia em Modelos Locais:** A execução de modelos LLM médicos locais em 8-bit ou INT4 sofria limitações de memória e perda de precisão em nuances sutis do parênquima pulmonar.
2. **Perda de Faixa Dinâmica (Lossy 8-bit):** O preprocessamento DICOM converteu as imagens para uint8 (0-255) antes da inferência no TorchXRayVision (TXRV), comprimindo a escala de cinza e alterando as unidades Hounsfield (HU), o que gerava falsos positivos ou falsos negativos em triagens quantitativas.
3. **Ausência de Delimitação Espacial:** Os achados radiológicos eram descritos textualmente, mas faltava delimitação geométrica precisa (bounding boxes e máscaras de segmentação) para guiar o médico assistente na interface visual.
4. **Necessidade de Validação Contra Alucinações (LLM-as-Judge):** Um único passe de LLM, mesmo avançado, está sujeito a alucinações clínicas ou omissões ao sintetizar relatórios extensos.

---

## 2. Decisão Arquitetural

Adotamos a arquitetura **TITAN v4.0 "Gemini-Duplo"**, estruturada em **7 etapas operacionais** com um padrão comprovado de *self-consistency* e *LLM-as-Judge* ("Gemini no início e no fim"), integrando segmentação por MedSAM e preservação total da precisão de 16-bit no TorchXRayVision.

```
[DICOM / Imagem 16-bit] 
       │
       ▼
1. [Anonimização LGPD & Extração 16-bit] ──► (Array [-1024, 1024] HU)
       │                                             │
       ▼                                             ▼
2. [Contexto Clínico NLP]                   4. [TorchXRayVision 16-bit]
       │                                       (Triagem + Sanity Check)
       ▼                                             │
3. [Gemini 2.5 Flash - Pass 1] ──────────────────────┼──────────────┐
   (Descrição Visual + BBox 2D)                      │              │
       │                                             ▼              ▼
       │                                    6. [Validação Cruzada]  │
       ▼                                       (Pass 1 vs TXRV)     │
5. [MedSAM - Segmentação]                            │              │
   (Guiada pelas BBoxes)                             │              │
       │                                             │              │
       ▼                                             ▼              ▼
7. [Busca RAG Enriquecida] ◄─────────────────────────┴──────────────┘
   (pgvector + Diretrizes)
       │
       ▼
8. [Gemini 2.5 Pro - Pass 2] ──► (Laudo Estruturado & Reconciliação)
       │
       ▼
9. [Resumo Humanizado TITAN M8] ──► (Tradução para Leigos/Pacientes)
```

### 2.1. Padrão "Gemini no Início e no Fim" (LLM-as-Judge)
- **Pass 1 (Gemini 2.5 Flash):** Atua no início da cadeia como extrator factual ultrarrápido. Recebe apenas a imagem e gera uma descrição visual neutra, devolvendo achados focais estruturados com bounding boxes normatizadas (`[ymin, xmin, ymax, xmax]`).
- **Pass 2 (Gemini 2.5 Pro):** Atua no final da cadeia como juiz clínico e sintetizador de alta ordem. Recebe o dossiê completo de evidências (Descrição Pass 1, Scores TXRV, Métricas MedSAM, Diretrizes RAG e Alertas de Discrepância) e gera o laudo estruturado segregado, resolvendo conflitos e justificando o diagnóstico diferencial.

### 2.2. Preservação de Precisão 16-bit e Sanity Check no TXRV
- O método `dicom_service.to_xrv_array(ds)` foi implementado para normalizar diretamente os arrays DICOM de 16-bit para a escala de referência do TorchXRayVision ($[-1024, 1024]$ HU), eliminando a perda de informação da conversão intermediária para 8-bit.
- Foi introduzido o mecanismo `_sanity_check_calibration` em `triagem_service.py`, que monitora a média e o desvio padrão dos pixels. Caso identifique uma imagem mal calibrada (ex: desvio padrão muito baixo ou média fora de faixa), o sistema injeta um alerta automático de calibração na validação cruzada.

### 2.3. Segmentação Guiada (MedSAM)
- Em vez de exigir prompts manuais de segmentação, o `segmentation_service.py` consome automaticamente as bounding boxes (`box_2d`) identificadas pelo Gemini Flash no Pass 1.
- O MedSAM gera a máscara binária da patologia e calcula métricas quantitativas precisas (área em pixels, bounding box exata e porcentagem estimada de ocupação do hemitórax).

### 2.4. Validação Cruzada Centralizada (Cross-Validation Service)
- O `cross_validation_service.py` atua como árbitro determinístico entre a visão de máquina (TXRV) e a visão semântica (Gemini Flash).
- Discrepâncias bidirecionais (ex: TXRV aponta opacidade com alta probabilidade, mas o Gemini não descreveu, ou vice-versa) geram notas de alerta no dossiê que obrigam o Gemini Pro a justificar ou reavaliar o achado no Pass 2.

---

## 3. Consequências

### 3.1. Positivas
- **Redução Drástica de Alucinações:** A checagem cruzada entre modelos de naturezas diferentes (CNN quantitativa vs Transformer Multimodal) impede que o laudo final afirme patologias sem respaldo quantitativo ou visual.
- **Precisão Geométrica e Quantitativa:** O médico recebe não apenas o texto, mas a delimitação de bounding box e área de extensão da lesão.
- **Fidelidade Radiológica:** O fim do gargalo 8-bit garante que nódulos de baixa densidade e infiltrados tênues sejam avaliados corretamente pelo TorchXRayVision.
- **Resiliência Arquitetural:** Em caso de indisponibilidade de conectividade com a API Gemini ou ausência de pesos locais do MedSAM, os serviços contam com modos de fallback graciosos e simulação estruturada, mantendo a estabilidade do microsserviço.

### 3.2. Mitigações e Cuidados
- **Latência de Dupla Passagem:** O uso de duas chamadas LLM adiciona ligeira latência ao pipeline (compensada pelo uso do modelo Flash ultrarrápido na primeira passagem e execução local paralela do TXRV).
- **Compatibilidade de Terminais:** Formatações de log foram padronizadas sem caracteres especiais incompatíveis para garantir perfeita execução em servidores Windows e Linux.

---

## 4. Referências e Implementação
- **Serviço Orquestrador:** `app/services/laudo_service.py`
- **Serviços Especializados:** `gemini_service.py`, `segmentation_service.py`, `cross_validation_service.py`, `dicom_service.py`, `triagem_service.py`
- **Schemas Estruturados:** `app/models/schemas.py`
- **Suíte de Verificação:** `scripts/test_pipeline_v4.py`
