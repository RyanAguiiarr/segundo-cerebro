# ADR-018: Estágio 3 Fortalecido (Primed Read), Estágio 3.5 (Zoom Condicional por Recortes Anatômicos) e Resiliência Multimodal

- **Status:** Aceito e Implementado (Verificado por 109 testes unitários em 2026-07-16)
- **Decisores:** Time de Arquitetura IA Tila e Radiologia Clínica
- **Serviço Alvo:** `tila-ai-cloud-service` (Python 3.11 / FastAPI)

---

## 1. Contexto e Declaração do Problema

A evolução do Motor Híbrido de IA do Tila (`tila-ai-cloud-service`) identificou necessidades críticas de aprimoramento na acurácia diagnóstica, na resolução de ambiguidades quantitativas e na resiliência operacional da infraestrutura híbrida (Local GPU + Cloud API):

1. **Ambiguidade e Lateralidade no Estágio 3 (Cloud LLM):** Os prompts iniciais de `Blind Read` e `Primed Read` enviados ao modelo de nuvem (Gemini) não impunham âncoras espaciais estritas. Isso abria margem para erros de lateralidade (inversão direita/esquerda em exames sem marcador de chumbo explícito) e para descrições genéricas sem amarração no checklist radiológico sistemático.
2. **Indeterminações Clínicas no Tier 1 e Custo de Resolução:** Durante a reconciliação (Estágio 4), achados críticos (`Tier 1`) que resultavam em `StatusAchado.INDETERMINADO` (por escore intermediário da CNN sem corroboração do LLM na `Branch 3` ou conflito na `Branch 4`) permaneciam no laudo como indeterminados. Enviar a imagem inteira repetidamente em resolução máxima para o LLM tentar desempatar consumia quota de tokens e frequentemente mantinha a indecisão por falta de foco na região anatômica suspeita.
3. **Risco de Regressão Silenciosa de Calibração (CNN TXRV):** Historicamente, o modelo TorchXRayVision (DenseNet-121) apresentou episódios de colapso onde, por problemas de normalização no pré-processamento, todos os escores de saída ficavam agrupados próximos ao limiar de decisão (`0.50` a `0.62`), gerando confianças nulas ($|score - 0.5| \times 2 \approx 0$). Sem monitoramento contínuo, esse colapso passaria despercebido até a inspeção manual dos laudos.
4. **Fragilidade na Integração Multimodal Local (Estágio 5 - MedGemma):** A geração da redação clínica local (MedGemma 1.5 4B via Ollama) precisava incorporar a imagem em base64 (`images`) para que o modelo pudesse correlacionar visualmente os achados reconciliados. Entretanto, falhas eventuais de VRAM ou timeouts no processamento visual da GPU local poderiam derrubar a requisição e impedir a entrega do laudo completo.

---

## 2. Decisão Arquitetural

Implementamos as Fases 1 a 6 do Plano de Fortalecimento do Pipeline no microsserviço `tila-ai-cloud-service`:

### 2.1. Estágio 3 Fortalecido: Persona, Âncora de Lateralidade e Checklist ABCDE (`cloud_llm_client.py`)
Reestruturamos os prompts do `CloudVisionReasoningProvider`:
- **Persona Subespecializada:** O prompt impõe a persona de radiologista torácico com 20 anos de experiência em UTI/Pronto-Socorro, focado estritamente em morfologia visual e blindado contra especulação etiológica.
- **Ancoragem de Lateralidade Obrigatória:** Antes de descrever qualquer achado, o modelo é forçado a identificar a bolha gástrica (habitualmente à esquerda) e a altura dos hemidiafragmas para calibrar o sistema de coordenadas e prevenir inversão de lateralidade.
- **Checklist Anatômico Systematic (ABCDE):** O `Blind Read` é estruturado na sequência de leitura: **A**irways (traqueia/brônquios), **B**ones & Chest Wall (costelas/clavículas), **C**ardiac & Mediastinum (silhueta cardíaca), **D**iaphragm & Pleura (seios costofrênicos), e **E**ffusion & Fields (parênquima pulmonar).
- **Primed Read Dirigido:** Exige confirmação explícita (`concorda: sim/nao/inconclusivo`) de cada patologia detectada pela CNN, exigindo bounding boxes (`[ymin, xmin, ymax, xmax]`) no espaço normalizado 0-1000.

### 2.2. Estágio 3.5: Zoom Condicional via Recortes Anatômicos (`stage3_5_zoom_condicional.py`)
Criamos um estágio intermediário de desempate acionado dentro de `stage4_reconciliation.py`:
- **Seletividade Tier 1:** Atua exclusivamente sobre achados `Tier 1` que tenham saído da reconciliação base com `StatusAchado.INDETERMINADO`.
- **Recortes por ROI Anatômico (`_crop_roi`):** Em vez de re-analisar a imagem inteira, o sistema recorta a imagem limpa (`raw_png_bytes`) em regiões anatômicas específicas associadas à patologia:
  - `apical` ($y \in [0\%, 55\%]$): *Pneumothorax*, *Mass*, *Nodule*.
  - `basal` ($y \in [40\%, 100\%]$): *Effusion*, *Edema*, *Consolidation*, *Pneumonia*.
  - `central` ($x, y \in [18\%, 82\%]$): *Cardiomegaly*, *Lung Opacity*.
- **Desempate com Fail-Closed:** O recorte é enviado ao Gemini via `verify_zoomed_finding`.
  - Se o zoom confirmar (`concorda == "sim"`) com confiança `alta` (ou `moderada` em `branch_3` com escore > 0.35), o achado é promovido para `StatusAchado.PRESENTE` com justificativa enriquecida.
  - Se o zoom descartar (`concorda == "nao"`) com confiança `alta` (e escore CNN < 0.65), o achado é rebaixado para `StatusAchado.AUSENTE`.
  - Caso contrário (confiança moderada/baixa ou resposta inconclusiva), o sistema adota postura **fail-closed** e mantém o achado como `INDETERMINADO` para salvaguarda clínica.

### 2.3. Resiliência Multimodal e Fallback no MedGemma (`stage5_medgemma.py`)
O envio ao Ollama (`_call_ollama`) foi aprimorado:
- O payload de geração de laudo (`gerar_redacao_clinica`) agora converte a imagem (`image_for_llm`) em base64 e a anexa em `images: [image_b64]`, permitindo que o MedGemma faça raciocínio multimodal conjugado ao prompt estruturado.
- **Circuit Breaker / Fallback Textual:** Caso a requisição multimodal falhe por timeout, erro de HTTP ou exceção de conexão do Ollama, a função remove o campo `images`, registra um aviso (`logger.warning("Ollama vision call failed/timed out, falling back to text-only mode")`) e executa a chamada em modo puramente textual utilizando apenas os dados estruturados do pipeline.

### 2.4. Monitoramento Anti-Regressão de Calibração (`stage2_txrv.py`)
Para prevenir a reincidência de colapso de calibração no TorchXRayVision:
- Adicionada a verificação `verificar_calibracao(findings)` ao final de `run_txrv()`.
- A função inspeciona a variância dos escores (`std_score`) e a média de confiança bruta ($\text{mean\_conf} = \frac{1}{N}\sum |score_i - 0.5| \times 2$).
- Se `mean_conf < 0.10` ou `std_score < 0.02`, o sistema dispara um alerta de severidade alta (`logger.warning("ALERTA ANTI-REGRESSÃO: Colapso de calibração detectado na saída do TXRV!...")`), orientando a verificação imediata da normalização dos pixels de entrada.

---

## 3. Consequências e Benefícios

- **Redução de Falsos Indeterminados:** Achados limiares em ápices e bases pulmonares ganham desempate de alta acurácia espacial sem custo computacional/de tokens excessivo.
- **Estabilidade do Pipeline:** O laudo é entregue mesmo em cenários de degradação da GPU local ou falhas temporárias na API de visão do Ollama, graças ao fallback automático para modo texto.
- **Auditoria Proativa:** Degradações no modelo local ou na normalização de imagens são capturadas instantaneamente pelo monitor de calibração antes de gerarem laudos imprecisos.
- **Cobertura de Testes:** Suíte de testes (`pytest -v`) expandida com 9 novos testes especializados (`TestCropROI`, `TestRunZoomCondicional`, `TestVerificarCalibracao`), somando **109 testes unitários passando com 100% de aprovação**.
