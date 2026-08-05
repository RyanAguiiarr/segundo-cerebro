# Guia Técnico e Manual Operacional: `tila-ai-cloud-service` (Motor Híbrido IA v2.0)

> **Versão:** 2.0.0 — Revisão Anti-Circunlocução & Triagem 4 Agudos (2026-07-11)
> **Stack:** Python 3.11 / FastAPI / TorchXRayVision 0.1.1 / Google Gemini API / MedGemma 1.5 4B (Ollama)

---

## 1. Visão Geral e Inversão Arquitetural

O microsserviço `tila-ai-cloud-service` implementa o **Motor Híbrido de IA da Tila** para análise e geração de laudos preliminares de radiografias de tórax. O sistema substitui o modelo de geração monólita em prosa livre (que causa alucinação etiológica) por um **pipeline determinístico de 7 estágios**, separando rigorosamente a extração visual geométrica/morfológica da redação textual estruturada.

```
       [ Client / API Gateway ]
                  │
                  ▼  POST /api/v1/laudos/gerar (PNG/JPEG + JSON Metadata)
 ┌─────────────────────────────────────────────────────────────┐
 │ tila-ai-cloud-service (FastAPI / Uvicorn na porta 8002)     │
 │                                                             │
 │  1. Estágio 0: Ingestão & Safety Gates (EXIF/LGPD/Billing)  │
 │  2. Estágio 1: Pré-Processamento (CNN Tensor & LLM PNG)     │
 │  3. Estágio 2: TorchXRayVision CNN (18 Patologias + conf.)  │
 │  4. Estágio 3: Gemini Vision Cloud API (Morfologia/Qualid.) │
 │  5. Estágio 4: Reconciliação 3-Way (6 Ramificações de Dec.) │
 │  6. Estágio 5: MedGemma 1.5 4B (Ollama Local Redação)       │
 │  7. Estágio 6: Integração, 4 Agudos & Veredito Leigo        │
 └─────────────────────────────────────────────────────────────┘
                  │
                  ▼  JSON (PythonAIResponseDTO)
       [ Laudo Redigido + Auditoria + Correlação Estruturada ]
```

---

## 2. Mapa Completo de Arquivos do Repositório (`c:\Tila\tila-ai-cloud-service`)

### Camada API (`app/`)
* [app/main.py](file:///c:/Tila/tila-ai-cloud-service/app/main.py): Ponto de entrada FastAPI. Expõe os endpoints `/health` e `/api/v1/laudos/gerar`. Orquestra a execução sequencial dos Estágios 0 a 6 e intercepta exceções de segurança (`BillingModeViolationError`).
* [app/config.py](file:///c:/Tila/tila-ai-cloud-service/app/config.py): Carregamento centralizado de variáveis de ambiente via `pydantic-settings` (`Settings`). Gerencia chaves (`CLOUD_LLM_API_KEY`), timeouts, modelo (`gemini-3.5-flash`), URL do Ollama (`http://localhost:11434/api/generate`) e a trava de faturamento (`CLOUD_LLM_BILLING_MODE`).
* [app/cloud_llm_client.py](file:///c:/Tila/tila-ai-cloud-service/app/cloud_llm_client.py): Cliente de integração com o Google Gemini (`GeminiVisionProvider`). Executa o gate de verificação de faturamento antes de realizar chamadas à API, gerencia o prompt do radiologista morfológico e aplica retry com autocorreção em caso de erro no parse do schema JSON (`CloudVisionOutput`).

### Camada de Modelos Local (`models/`)
* [models/cnn_vision.py](file:///c:/Tila/tila-ai-cloud-service/models/cnn_vision.py): Encapsulamento de modelo pré-treinado do `torchxrayvision` (`densenet121-res224-all`). Responsável por normalizar tensores, inferir pontuações de 0.0 a 1.0 para as 18 patologias torácicas e calcular a confiança bruta.
* [models/guardrails.py](file:///c:/Tila/tila-ai-cloud-service/models/guardrails.py): Validador pós-geração (`validate_and_sanitize` e `sanitize_text`). Expulga escores numéricos vazados, coordenadas `[x, y]` alucinadas e verifica se o modelo inventou patologias ausentes na lista reconciliada.

### Camada de Pipeline e Lógica de Negócio (`pipeline/`)
* [pipeline/stage0_ingest.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage0_ingest.py): Estágio 0. Valida metadados, remove dados EXIF de identificação do paciente (descaracterização LGPD/HIPAA), gera log de compliance no `ImagePackage` e checa a coerência da flag `origem_exame_real`.
* [pipeline/stage1_prep.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage1_prep.py): Estágio 1. Produz duas representações da imagem limpa: (1) Tensor NumPy $224 \times 224$ com *letterbox* preservando proporção para a CNN; e (2) Bytes PNG otimizados e limitados a 1024px para envio ao LLM na nuvem.
* [pipeline/stage2_txrv.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage2_txrv.py): Estágio 2. Roda a inferência da CNN local, extrai as pontuações sigmoides, aplica a fórmula de confiança bruta $\text{conf} = |s - 0.5| \times 2$ e classifica os achados entre **Tier 1** (alta urgência/frequência) e **Tier 2**.
* [pipeline/stage3_cloud_vision.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage3_cloud_vision.py): Estágio 3. Aciona o `GeminiVisionProvider` passando os achados da CNN como contexto. Retorna as avaliações estruturadas de concordância e correlação clínico-radiológica sem jargões etiológicos.
* [pipeline/stage4_reconciliation.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage4_reconciliation.py): Estágio 4. Executa a árvore de decisão de 6 ramificações para arbitrar discrepâncias entre a CNN local e o LLM na nuvem, emitindo `ReconciledFinding` com flags de discrepância quando necessário.
* [pipeline/stage5_medgemma.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage5_medgemma.py): Estágio 5. Converte o score técnico numérico para rótulo qualitativo ("ótima/boa/limitada"), constrói o prompt determinístico com fronteiras numeradas e aciona o MedGemma local (via Ollama REST) para redigir as seções técnicas e conclusivas do laudo sem circunlocução.
* [pipeline/stage6_integration.py](file:///c:/Tila/tila-ai-cloud-service/pipeline/stage6_integration.py): Estágio 6. Aplica a triagem determinística dos **4 Agudos** para definir `criticidade_geral`, gera o `veredito_leigo` usando o dicionário sanitizado anti-estatístico (`_EXPLICACOES_LEIGO`), aplica guardrails em todas as seções e serializa o DTO final com rastreabilidade de faturamento.

### Contratos e DTOs (`schemas/`)
* [schemas/contracts.py](file:///c:/Tila/tila-ai-cloud-service/schemas/contracts.py): Definição de todos os modelos Pydantic (`extra="forbid"`): `TXRVFinding`, `CloudVisionCorrelacaoItem`, `CloudVisionOutput`, `ReconciledFinding`, `MedGemmaOutput` e `PythonAIResponseDTO`.

---

## 3. Guia Detalhado dos Estágios de Operação

### Estágio 0: Ingestão e Safety Gate LGPD/Billing
- **Entrada:** Bytes da imagem e metadados HTTP.
- **Lógica:** Remove metadados EXIF/JFIF para não enviar informações identificáveis do paciente (PII) à nuvem. Valida se a imagem é real (`origem_exame_real=True`). Se for real, só permite prosseguir se `CLOUD_LLM_BILLING_MODE == "paid"`. Caso contrário, levanta `BillingModeViolationError` (HTTP 403).

### Estágio 1: Pré-Processamento Dual
- **Para TorchXRayVision:** Converte para tons de cinza, aplica preenchimento de bordas (*letterboxing*) para manter a proporção original, redimensiona para $224 \times 224$ pixels e normaliza a intensidade dos pixels no intervalo $[-1024, 1024]$ de unidades Hounsfield equivalentes.
- **Para Gemini Vision:** Converte para PNG padrão RGB/Cinza, reduz a dimensão máxima para $1024$ pixels (economizando tokens e banda) e codifica em Base64.

### Estágio 2: Inferência CNN (`densenet121-res224-all`)
- Avalia 18 patologias pulmonares e pleurais.
- Para cada score $s \in [0, 1]$, calcula a **Confiança Bruta**:
  $$\text{conf} = |s - 0.5| \times 2 \quad (\text{onde } 0.0 \text{ é incerteza máxima e } 1.0 \text{ é certeza máxima})$$
- Agrupa achados em **Tier 1** (*Atelectasis, Consolidation, Infiltration, Pneumothorax, Edema, Emphysema, Fibrosis, Effusion, Pleural_Thickening, Nodule, Mass*) e **Tier 2** (*outros*).

### Estágio 3: Extração Morfológica na Nuvem (`Gemini Vision`)
- Envia a imagem PNG e as descobertas da CNN ao Gemini.
- Exige saída no contrato `CloudVisionOutput`, contendo:
  - `incidencia`: `"PA"`, `"AP"`, `"Perfil"` ou `"Indeterminada"`.
  - `qualidade_tecnica`: Escore e flags (rotação, inspiração fraca, artefatos).
  - `concordancia_txrv`: Resposta `concorda: bool` e justificativa visual curta para os achados de Tier 1.
  - `correlacao_clinica`: Lista de `CloudVisionCorrelacaoItem` (`sintoma_referido`, `achado_estrutural_relacionado`, `pertinencia_visual`). **Estritamente proibido** sugerir etiologias (Tuberculose, Pneumonia Bacteriana, etc.).

### Estágio 4: Reconciliação 3-Way (CNN + LLM + Confiança)
Para cada patologia, executa uma de 6 regras determinísticas:
1. **Branch 1 ($s \ge 0.70$):** Se LLM concorda ou cala, é `PRESENTE`. Se LLM discorda frontalmente ("nenhum sinal visual"), é `PRESENTE` mas com `discrepancy_flag = True` (o médico deve checar o corte).
2. **Branch 2 ($0.35 \le s < 0.70$ e LLM concorda):** O apoio visual do LLM promove a suspeita moderada da CNN para `PRESENTE`.
3. **Branch 3 ($0.35 \le s < 0.70$ e LLM discorda/calado):** Permanece como `INDETERMINADO` (necessita investigação no laudo).
4. **Branch 4 ($s < 0.35$ e LLM concorda):** Reconciliado como `INDETERMINADO` (achado sutil detectado pela nuvem que a CNN pontuou pouco).
5. **Branch 5 ($s < 0.35$ e LLM discorda/calado):** Classificado como `AUSENTE`.
6. **Branch 2b/5b (Sem dados de LLM - falha na nuvem ou modo degradação):** Se não há resposta da nuvem, escores $\ge 0.50$ viram `PRESENTE`, escores $< 0.35$ viram `AUSENTE` e o intermediário vira `INDETERMINADO`.

### Estágio 5: Redação Técnica via MedGemma 1.5 4B (Ollama Local)
- Converte o escore decimal de qualidade técnica para rótulo qualitativo (`ótima`, `boa` ou `inadequada`).
- Envia um prompt estruturado em 3 blocos numerados e estanques para o modelo local `medgemma:4b`:
  - `secao_tecnica`: Descreve estritamente incidência e qualidade qualitativa.
  - `secao_achados`: Enumera os achados `PRESENTE` e `INDETERMINADO` sem criar diagnósticos etiológicos.
  - `secao_conclusao`: Apresenta a síntese radiológica sem repetir os dados técnicos.

### Estágio 6: Triagem dos 4 Agudos, Veredito Leigo e DTO Final
- **Triagem de Criticidade (`criticidade_geral`):**
  - Aciona **🚨 URGENTE** se, e somente se, houver status `PRESENTE` para algum dos **4 Agudos**: *Edema, Pneumotórax, Consolidação* ou *Derrame Pleural (`Effusion`)*.
  - Aciona **⚠️ ATENCAO** se houver outros achados positivos (`Nodule`, `Mass`, etc.), achados indeterminados ou `discrepancy_flag == True`.
  - Aciona **✅ NORMAL** apenas se todos os achados forem ausentes e não houver discrepâncias.
- **Resumo para Leigos (`veredito_leigo`):**
  - Utiliza o dicionário `_EXPLICACOES_LEIGO` estrutural e sem alucinações probabilísticas.
  - Para achados `INDETERMINADO`, insere o prefixo explicativo `[Em Avaliação / Indeterminado]`.
  - Aplica o **Aviso Regulatório Obrigatório** no início e fim do texto para o paciente.
- **Rastreabilidade (`billing_mode_utilizado` e `modelo_ia_utilizado`):**
  - Agrega a proveniência dos modelos utilizados na string de auditoria:
    `txrv:densenet121-res224-all | gemini:gemini-3.5-flash | ollama:medgemma:4b | billing_mode:paid`

---

## 4. Como Executar e Testar

### 4.1. Configuração do Ambiente e Dependências
Abra o terminal no diretório `c:\Tila\tila-ai-cloud-service`:
```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Verificar variáveis de ambiente em .env
CLOUD_LLM_API_KEY=sua_chave_gemini_aqui
CLOUD_LLM_BILLING_MODE=paid
OLLAMA_BASE_URL=http://localhost:11434/api/generate
MEDGEMMA_MODEL=medgemma:4b
```

### 4.2. Execução dos 60 Testes Unitários (`pytest`)
O microsserviço possui uma suíte de testes de 100% de passagem. Execute no terminal:
```powershell
.\venv\Scripts\pytest.exe -v
```
**Resultado Esperado:**
```text
======================== 60 passed, 1 warning in 7.00s ========================
```

### 4.3. Inicialização do Servidor API (`Uvicorn`)
Para rodar o microsserviço na porta `8002`:
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

---

## 5. Exemplo de Request e Response para Teste (`curl` ou Postman)

### Request (POST Multimodal com Form-Data)
```powershell
curl -X POST "http://localhost:8002/api/v1/laudos/gerar" `
  -H "accept: application/json" `
  -H "Content-Type: multipart/form-data" `
  -F "file=@C:\caminho\para\raiox_torax.png" `
  -F "metadata_json='{\"patient_id\": \"ANON_12345\", \"clinical_summary\": \"Paciente com tosse seca persistente há 3 semanas\", \"origem_exame_real\": true}'"
```

### Response JSON (Contrato `PythonAIResponseDTO`)
```json
{
  "sucesso": true,
  "secao_tecnica": "Radiografia de tórax na incidência póstero-anterior (PA). Qualidade técnica do exame considerada ótima, sem rotação ou limitação inspiratória significativa.",
  "secao_achados": "Nota-se formação nodular focal projetada em terço médio do pulmão direito. Campos pulmonares esquerdo e demais estruturas com transparência normal. Seios costofrênicos livres.",
  "secao_conclusao": "Achado radiológico compatível com nódulo pulmonar à direita em avaliação.",
  "secao_recomendacoes": "Recomenda-se correlação clínica e complementação diagnóstica por tomografia computadorizada de tórax sem e com contraste para melhor caracterização anatômica da lesão nodular.",
  "veredito_leigo": "AVISO REGULATÓRIO: Este texto é um rascunho de apoio à comunicação médico-paciente e não constitui diagnóstico. Deve ser revisado e validado pelo seu médico radiologista.\n\nResumo preliminar do exame de imagem:\n\n• Nódulo pulmonar: Formação estrutural focal visualizada no exame. É indispensável o acompanhamento médico e investigação com métodos de imagem tridimensionais (tomografia computadorizada) para definição adequada.\n\nAVISO REGULATÓRIO: Este texto é um rascunho de apoio à comunicação médico-paciente e não constitui diagnóstico. Deve ser revisado e validado pelo seu médico radiologista.",
  "criticidade_geral": "ATENCAO",
  "confianca_geral": "ALTA",
  "precisa_revisao_humana": true,
  "achados_detectados": [
    {
      "patologia": "Nodule",
      "status_achado": "presente",
      "discrepancy_flag": false,
      "tier": 1
    }
  ],
  "correlacao_clinica": [
    {
      "sintoma_referido": "Paciente com tosse seca persistente há 3 semanas",
      "achado_estrutural_relacionado": "Nodule",
      "pertinencia_visual": "direta"
    }
  ],
  "qualidade_tecnica": {
    "score": 0.91,
    "flags": []
  },
  "dispositivos_medicos": [],
  "metadados_processamento": {
    "latencia_total_ms": 3840.5,
    "latencia_cnn_ms": 420.1,
    "latencia_cloud_ms": 1890.2,
    "latencia_medgemma_ms": 1530.2,
    "cnn_model": "densenet121-res224-all",
    "cloud_model": "gemini-3.5-flash",
    "medgemma_model": "medgemma:4b",
    "cloud_called": true
  },
  "modelo_ia_utilizado": "txrv:densenet121-res224-all | gemini:gemini-3.5-flash | ollama:medgemma:4b | billing_mode:paid",
  "billing_mode_utilizado": "paid",
  "erros": []
}
```
