# ADR-016: TITAN v4.3 — Blind Reading Mastery & Raciocínio Morfológico

**Data:** 2026-07-06  
**Status:** Aceito  
**Autores:** Ryan, Pedro  
**Contexto Técnico:** Serviço de IA (`tila-ai-service` - Python / Gemini 2.5 Flash & Pro + TorchXRayVision + MedSAM)  

---

## 1. Contexto & Problema

Durante a validação de laudos radiológicos em cenários do mundo real, identificamos um desafio crítico de precisão clínica quando o sistema é submetido a **Leituras Cegas (Blind Triage)** — isto é, exames radiográficos submetidos sem nenhuma indicação clínica, histórico do paciente ou relato de sintomas:

1. **Viés de Normalidade dos LLMs (VLM):** Quando o modelo visual (Gemini 2.5 Flash no Pass 1) analisa um raio-X sem um "texto guia" indicando a suspeita (ex: "pesquisar tuberculose" ou "tosse há 3 semanas"), ele tende estatisticamente a negligenciar opacidades sutis, derrames apicais ou cavitações iniciais, classificando o exame como "dentro dos limites da normalidade".
2. **Déficits de Raciocínio Espacial / Lateralização:** Modelos de visão (VLMs) apresentam notórias dificuldades em orientação espacial abstrata em radiografias de tórax PA/AP, frequentemente confundindo o hemitórax esquerdo com o direito ou falhando ao delimitar se uma massa está no parênquima ou fundida à cúpula diafragmática.
3. **Subutilização de Alertas Quantitativos:** Na arquitetura v4.1/v4.2, se o TorchXRayVision (TXRV) detectasse alta probabilidade de uma patologia grave (ex: *Lung Opacity* 61.8% ou *Effusion* 54.3%), mas o Gemini Pass 1 não usasse essas palavras exatas por viés de normalidade, o filtro determinístico promovia o alerta para reexame, mas o Pass 2 frequentemente descartava o alerta sem uma justificativa técnica morfológica rigorosa.
4. **Abordagem Probabilística vs. Dedutiva:** O prompt de síntese (Pass 2) induzia o modelo a gerar diagnósticos baseados em puro "chute probabilístico" do LLM, em vez de seguir a dedução médica anatômica e morfológica dos radiologistas especialistas.

---

## 2. Decisão

Evoluímos a arquitetura do microsserviço de IA para a versão **TITAN v4.3 (Blind Reading Mastery)**, baseada em quatro pilares estruturais inegociáveis:

### 2.1. Método ABCDE & Ancoragem Espacial no Pass 1
O prompt do **Gemini Pass 1 (Flash)** e o schema de dados (`DescricaoVisualPass1`) foram alterados para impor a execução obrigatória do **Checklist Anatômico ABCDE** antes de permitir a emissão de um parecer preliminar:
- **A (Airway - Vias Aéreas):** Traqueia centrada ou desviada, calibre dos brônquios principais.
- **B (Bones & Wall - Ossos e Parede):** Integridade de costelas, clavículas, escápulas e coluna vertebral.
- **C (Cardiac & Mediastinum - Coração):** Silhueta cardíaca, índice cardiotorácico e mediastino superior.
- **D (Diaphragm - Diafragma):** Cúpulas diafragmáticas, ângulos costofrênicos e cardiofrênicos.
- **E (Edges/Fields - Campos Pulmonares):** Transparência, padrão vascular, terços superiores (ápices), médios e inferiores.

**Ancoragem Espacial Inquestionável:** Para eliminar erros de lateralização (esquerda/direita), o prompt impõe como regra de ouro a identificação da **Bolha Gástrica (fundus gástrico)** sob a cúpula diafragmática como âncora lateral para o lado **ESQUERDO** do paciente.

### 2.2. Safety Net "Advogado do Diabo" (`HardFilterService`)
Refatoramos a mecânica de reexame quantitativo no `hard_filter_service.py` para operar como o **Advogado do Diabo** em triagens cegas.
- Quando o TXRV detecta `probabilidade >= 0.50` para patologias de alerta grave (*Lung Opacity, Effusion, Mass, Infiltration, Consolidation, Nodule*) sem corroboração do Pass 1 em exames sem indicação clínica, o sistema gera o mandato determinístico:
  > *"ALERTA DE SEGURANÇA QUANTITATIVA / ADVOGADO DO DIABO (TITAN v4.3): O motor neural detectou [Patologia] com probabilidade de [X%]. Mesmo em triagem cega (sem indicação clínica) e embora o Pass 1 não tenha categorizado com este termo exato, você está OBRIGADO a examinar meticulosamente a película. Se houver qualquer indício visual morfológico (opacidade, cavitação, derrame ou nódulo), inclua no diagnóstico diferencial. Se decidir descartar, justifique explicitamente por que a imagem simula esse achado (ex: sobreposição ósteo-muscular ou artefato)."*
- **Efeito:** Proíbe o silêncio do modelo de síntese. O Gemini Pass 2 é obrigado a inspecionar a região visualmente e ou incluir na hipótese diagnóstica ou justificar morfologicamente o falso positivo.

### 2.3. Matriz de Diagnóstico Morfológico no Pass 2
O prompt de síntese clínica (`gemini_service.py`) foi reformulado para banir raciocínios probabilísticos genéricos. O modelo agora é obrigado a classificar e agrupar o diagnóstico diferencial seguindo a **Matriz Morfológica de Raciocínio Radiológico**:
- **Padrão Infeccioso (Tuberculose / Fúngica):** Opacidades em ápices + cavitações + retração hilar + espessamento pleural.
- **Padrão Neoplásico (Carcinoma / Metástase):** Massa focal espiculada ou bem delimitada + possível atelectasia ou derrame pleural associado.
- **Padrão Inflamatório/Alveolar/Vasculite:** Consolidação lobar ou infiltrado reticulonodular difuso com broncogramas aéreos.

### 2.4. RAG Morfológico com Padrões Clássicos da Literatura (`RagService`)
O serviço de busca em vetor (`rag_service.py`) foi adaptado. Quando o sistema detecta que se trata de uma **leitura cega** (`indicacao_clinica == ""`), o RAG injeta no contexto do Pass 2 um bloco curado com os **Padrões Radiológicos Clássicos da Literatura**, contendo gabaritos morfológicos estritos (ex: critérios para Tuberculose Pós-Primária apicoposterior, Pneumonias Alveolares, Derrames Pleurais e Cardiomegalia) para guiar a dedução clínica.

---

## 3. Consequências & Benefícios

- **Acerto em Triagem Cega:** O microsserviço agora opera com segurança e precisão máxima mesmo quando o médico solicitante ou sistema hospitalar omite o pedido médico ou histórico do paciente.
- **Fim dos Erros de Lateralização:** A bolha gástrica atua como farol espacial infalível para o VLM.
- **Eliminação do Silêncio Perigoso:** Nenhuma probabilidade alta do TXRV é descartada sem uma explicação anatômica clara, protegendo o paciente e respaldando o médico radiologista.
- **Dedução Sênior:** Os laudos gerados transparecem o raciocínio dedutivo de um radiologista experiente, organizando hipóteses diferenciais por eixos morfológicos com recomendações claras de conduta e correlação clínica.

---

## 4. Referências & Backlinks

- [[04-Wiki_Conceitos/conceitos/motor-hibrido-ia-tila-engine]] — Motor Híbrido TITAN v4.3
- [[04-Wiki_Conceitos/conceitos/laudo-patterns]] — Padrões e Guardrails de Laudos Médicos
- `c:\Tila\tila-ai-service\app\models\schemas.py` (`ChecklistABCDE`)
- `c:\Tila\tila-ai-service\app\services\gemini_service.py` (`_gerar_prompt_pass1_visual`, `_gerar_prompt_pass2_sintese`)
- `c:\Tila\tila-ai-service\app\services\hard_filter_service.py` (`filtrar_evidencia_para_pass2`)
- `c:\Tila\tila-ai-service\app\services\rag_service.py` (`_obter_padroes_classicos`)
- `c:\Tila\tila-ai-service\scratch\test_blind_reading_v43.py` (Suite de testes automatizados 100% aprovada)
