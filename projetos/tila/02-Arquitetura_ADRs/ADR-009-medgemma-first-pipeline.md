# ADR-009: Pipeline MedGemma-First — Inversão Arquitetural para Laudos Grounded na Imagem

- **Status:** Aceito
- **Data:** 2026-07-05
- **Decisores:** Ryan, Agente Antigravity
- **Substitui:** Fluxo parcial do ADR-008 (TorchXRayVision como analisador primário)

## Contexto e Problema

O pipeline TITAN v2.0 (ADR-008) utilizava TorchXRayVision como **analisador primário** da imagem, passando seus rótulos textuais (labels) como input para o MedGemma, que atuava apenas como **escritor de texto**. Isso causava três problemas graves:

1. **Laudos genéricos (Anchoring Bias):** MedGemma recebia labels pré-classificados do TorchXRayVision e apenas os reescrevia em prosa médica. Não analisava a imagem real, produzindo laudos superficiais e repetitivos.
2. **Output excessivo:** Sem controle de tokens por seção, o MedGemma produzia textos desproporcionalmente longos e sem estrutura formal de laudo radiológico.
3. **Dependência de indicação clínica:** Quando `indicacao_clinica` era vazia, o pipeline perdia contexto clínico e os laudos ficavam ainda mais genéricos.

### Evidência do Problema

Em testes com imagens radiológicas normais (sem patologias), o pipeline v2.0 continuava gerando laudos com "achados moderados" de Infiltração Pulmonar e Fibrose (falsos positivos) porque o TorchXRayVision sempre produz probabilidades não-zero para todas as 18 patologias, e os limiares estáticos não filtravam adequadamente.

## Decisão Arquitetural

### Inversão de Papéis: MedGemma-First (TITAN v3.0)

```
ANTES (v2.0):  Image → TorchXRayVision → TEXT labels → RAG → MedGemma (escritor)
DEPOIS (v3.0): Image → MedGemma Step 1 (visual) → TorchXRayVision (validador) → Cross-validation → RAG → MedGemma Step 2 (laudo)
```

#### Step 1: Descrição Visual Pura (MedGemma)
- MedGemma recebe **APENAS a imagem** — sem indicação clínica, sem labels, sem contexto
- Descreve sistematicamente cada estrutura anatômica (campos pulmonares, pleura, coração, mediastino, ossos)
- Token limit: 1024 tokens

#### Step 2: Laudo Estruturado (MedGemma)
- MedGemma recebe: seus próprios achados visuais (Step 1) + scores do TorchXRayVision + contexto RAG + indicação clínica (se disponível)
- Gera laudo formal com seções obrigatórias: TÉCNICA, ACHADOS, IMPRESSÃO DIAGNÓSTICA, DIAGNÓSTICO DIFERENCIAL, RECOMENDAÇÕES
- Token limit: 1500 tokens com limites por seção

#### Cross-Validation Anti-Alucinação
- Compara achados do MedGemma (Step 1) vs scores do TorchXRayVision
- Sinaliza discrepâncias: MedGemma mencionou patologia que TorchXRayVision não confirmou (possível alucinação), ou TorchXRayVision detectou algo que MedGemma omitiu

## Consequências

### Positivas
- **Laudos grounded na imagem real** em vez de genéricos baseados em labels
- **indicacao_clinica verdadeiramente opcional** — pipeline funciona com imagem apenas
- **Redução drástica de falsos positivos** em exames normais (MedGemma descreve o que vê)
- **Output controlado** com limites por seção
- **Auditabilidade** via cross-validation (discrepâncias documentadas na resposta)

### Negativas / Trade-offs
- **+30% tempo de processamento** — 2 chamadas ao MedGemma em vez de 1
- **Dependência da capacidade multimodal** — requer que o modelo aceite input de imagem (atualmente opera como text-only com fallback)
- **TILA Neural Engine ampliado** — fallback determinístico agora precisa cobrir mais cenários
