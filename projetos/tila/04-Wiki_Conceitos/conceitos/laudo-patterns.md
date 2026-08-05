---
title: "Padrões de Laudos Médicos"
type: concept
tags: [radiology, laudos, medicina, nlp, ai-prompting]
sources: [raw/codebase/snapshots/backend-structure.md]
last_updated: 2026-05-07
---

# Padrões de Laudos Médicos no TILA

> Este documento estabelece o guia conceitual e técnico de como a Inteligência Artificial do TILA deve formatar, redigir e estruturar os textos médicos.
> Serve como base para o desenvolvimento do `System Prompt` do LangChain4j.

---

## O Desafio do Laudo Radiológico

Um laudo médico não é um texto narrativo livre (como uma redação de colégio). É um **documento médico-legal**. Ele precisa ser:
1. **Padronizado**: Outros médicos devem bater o olho e achar rapidamente o que buscam.
2. **Conciso, porém Completo**: Evitar prosa desnecessária, mas não omitir achados incidentais.
3. **Defensivo Legalmente**: Se uma imagem está borrada, o laudo deve atestar a "limitação técnica". A IA do TILA nunca deve tentar adivinhar o que não está nítido.

---

## Estrutura Universal do Laudo TILA

A IA deverá ser "forçada" a gerar o `rascunhoIA` (Entity `Laudo`) sempre em três ou quatro sessões fixas:

### 1. Técnica (Obrigatório)
Descreve como o exame foi feito. Importante para faturamento e para alertar limitações.
* **Exemplo de IA**: "Radiografias do tórax adquiridas nas incidências posteroanterior e perfil, com inspiração adequada."
* **Se a imagem for ruim**: "Estudo com artefatos de movimento que limitam parcialmente a análise."

### 2. Relatório / Achados (Obrigatório)
A descrição anatômica objetiva e detalhada, geralmente dividida por sistemas.
* **Exemplo de IA**:
  - Parênquima pulmonar sem consolidações ou massas.
  - Seios costofrênicos livres.
  - Área cardíaca de dimensões normais.
  - Aorta torácica ectasiada e ateromatosa.

### 3. Impressão / Conclusão (Obrigatório)
O resumo sintético das alterações (ou a ausência delas). É a única parte que a maioria dos médicos solicitantes lê.
* **Exemplo de IA**: "Sem alterações cardiopulmonares agudas evidenciáveis ao método." ou "Achados compatíveis com pneumonia basal direita."

---

## Glossário Anti-Alucinação (Guardrails)

Para evitar que o Gemini (LLM) invente diagnósticos, o System Prompt deve proibir termos absolutos. Na radiologia, a imagem sugere, mas a clínica confirma.

| Expressões Proibidas para a IA | Expressões Corretas (Permitidas) |
|---|---|
| "O paciente está com câncer" | "Nódulo espiculado altamente suspeito para neoplasia primária (BI-RADS 5)" |
| "Com certeza é pneumonia" | "Opacidade alveolar basal compatível com processo infeccioso/inflamatório" |
| "Coração inchado" | "Cardiomegalia" / "Aumento do índice cardiotorácico" |

---

## Implementação no Código (O System Prompt)

Quando o `TilaRadiologistaAgent` for implementado usando `@AiService`, a formatação de laudo deve ser explicitamente mapeada na anotação `@SystemMessage`.

```java
// Exemplo arquitetural do Guardrail de Laudo
@SystemMessage("""
    Você é um Médico Radiologista Sênior no Brasil.
    Sua missão é gerar um RASCUNHO de laudo baseado nos achados.
    
    REGRA 1 - ESTRUTURA:
    O seu texto DEVE conter os cabeçalhos exatos:
    "TÉCNICA:"
    "ANÁLISE:"
    "IMPRESSÃO:"
    
    REGRA 2 - TOM DE VOZ:
    Use jargão médico padrão do CBR (Colégio Brasileiro de Radiologia).
    Seja telegráfico e objetivo. Não use pronomes pessoais ("eu vejo", "nós achamos").
    
    REGRA 3 - ÉTICA:
    Você NÃO fará diagnósticos definitivos. Use termos como "sugestivo de", "compatível com", "pode representar".
    Sempre adicione no final da impressão: "A critério clínico, correlacionar com exames laboratoriais."
""")
```

## Few-Shot Prompting via RAG (A Solução TILA)

Ao invés de tentar ensinar radiologia no prompt (o que gastaria muitos tokens e encareceria a chamada da API do Gemini), o TILA usa a entidade `ConhecimentoMedico`.

A IA primeiro busca na base de dados: *"Como um radiologista humano escreve um laudo normal de Tórax?"*
A base RAG (PgVector) retorna um texto de exemplo da categoria `LAUDO_EXEMPLO`.
O LLM copia aquele estilo perfeitamente para o caso do paciente atual.

---

## Varredura Anatômica ABCDE e Matriz Morfológica (TITAN v4.3)

Para evitar viés de normalidade e lateralização em **Triagem Cega** (exames sem indicação clínica), o TILA impõe dois guardrails estruturais na geração de laudos (ver [[ADR-016-titan-v4-3-blind-reading-mastery]]):

1. **Checklist ABCDE (Pass 1):** O modelo visual é obrigado a estruturar sua varredura em 5 etapas estritas:
   - **A (Airway):** Vias aéreas e traqueia.
   - **B (Bones):** Caixa torácica e estruturas ósseas.
   - **C (Cardiac):** Silhueta cardíaca e mediastino.
   - **D (Diaphragm):** Cúpulas diafragmáticas e seios costofrênicos (com **Ancoragem Espacial na Bolha Gástrica** para definir o lado ESQUERDO do paciente).
   - **E (Edges/Fields):** Transparência e vascularização dos campos pulmonares.

2. **Matriz Morfológica (Pass 2):** Na redação da *Análise* e *Impressão*, o LLM é proibido de emitir diagnósticos baseados em puro palpite probabilístico. As hipóteses devem ser organizadas por eixos morfológicos clássicos:
   - **Padrão Infeccioso (Tuberculose / Fúngica):** Opacidade apical + cavitação + espessamento pleural.
   - **Padrão Neoplásico (Carcinoma / Metástase):** Massa focal espiculada ou bem delimitada.
   - **Padrão Inflamatório / Alveolar:** Consolidação lobar ou infiltrado reticulonodular difuso.

## Backlinks
- [[wiki/concepts/ai-pipeline]]
- [[wiki/entities/entity-laudo]]
- [[wiki/concepts/dicom]]
- [[04-Wiki_Conceitos/conceitos/motor-hibrido-ia-tila-engine]]
- [[02-Arquitetura_ADRs/ADR-016-titan-v4-3-blind-reading-mastery]]
