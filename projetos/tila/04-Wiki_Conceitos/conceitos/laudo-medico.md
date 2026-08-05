---
title: "Laudo Médico"
type: concept
tags: [medical, laudo, tila, lgpd]
sources: []
last_updated: 2026-05-07
---

# Laudo Médico

## O que é

O **laudo médico** (ou relatório médico / parecer diagnóstico) é o documento oficial emitido por um médico que contém a interpretação de um exame diagnóstico (radiografia, tomografia, ressonância, ultrassonografia, etc.). No Brasil, o laudo é regulamentado pelo CFM (Conselho Federal de Medicina) e tem valor legal.

## Estrutura Padrão

Um laudo médico brasileiro segue uma estrutura relativamente padronizada, embora com variações por especialidade e instituição. As seções principais são:

### 1. Exame
- Tipo do exame realizado
- Data da realização
- Equipamento utilizado
- Identificação do paciente (nome, data de nascimento — em sistema, por ID)

### 2. Técnica
- Protocolo de aquisição utilizado
- Planos e sequências (em caso de RM)
- Uso de contraste (sim/não, tipo, dose)
- Posicionamento do paciente

### 3. Achados (Descrição)
- Descrição sistemática e objetiva dos achados
- Linguagem neutra e técnica
- Organização por região anatômica ou sistema
- Comparação com exames anteriores quando disponíveis
- Medidas quantitativas quando relevantes

### 4. Impressão Diagnóstica (Conclusão)
- Interpretação dos achados
- Diagnóstico principal e diferenciais
- Classificação de gravidade quando aplicável (ex: BI-RADS para mama)
- Correlação com dados clínicos quando fornecidos

### 5. Observações
- Limitações técnicas do exame
- Recomendações de exames complementares
- Sugestão de seguimento

### 6. Assinatura
- Nome completo do médico
- CRM (registro profissional)
- Especialidade
- Data de emissão
- Assinatura (eletrônica ou manuscrita)

## TILA e o Pré-Laudo

O TILA não substitui o médico — ele gera um **pré-laudo** (rascunho) que o médico revisa, edita se necessário, e assina. O fluxo é:

```
Imagem DICOM + Notas Clínicas
        │
        ▼
   CNN/PaliGemma → achados estruturados
        │
        ▼
   LLM (Gemini) + RAG → pré-laudo em prosa
        │
        ▼
   Médico revisa → edita → assina
        │
        ▼
   Laudo oficial emitido
```

O pré-laudo do TILA SEMPRE inclui o disclaimer:
> ⚠️ Este é um rascunho gerado por IA. Revisão e assinatura do médico responsável são obrigatórias antes de qualquer uso clínico.

## Requisitos LGPD para Laudos

A Lei Geral de Proteção de Dados (Lei 13.709/2018) classifica dados de saúde como **dados pessoais sensíveis** (Art. 5º, II). Isso impacta diretamente os laudos:

| Requisito | Impacto no TILA |
|---|---|
| Consentimento específico para dados de saúde (Art. 11) | Paciente deve consentir o processamento de seus dados de saúde |
| Finalidade determinada (Art. 6º, I) | Laudos só podem ser usados para finalidade clínica declarada |
| Minimização (Art. 6º, III) | Laudo deve conter apenas dados necessários à interpretação |
| Acesso ao titular (Art. 18, II) | Paciente tem direito de acessar seus laudos |
| Eliminação (Art. 18, VI) | Paciente pode solicitar eliminação (mas: conflito com obrigação de guarda do CFM — mínimo 20 anos) |
| Segurança (Art. 46) | Laudos devem ser armazenados com medidas de segurança apropriadas |
| Anonimização para pesquisa (Art. 11, §4) | Laudos usados para treinar IA devem ser anonimizados |

## Padrões de Laudos no TILA

Ver [[wiki/concepts/laudo-patterns]] para a catalogação detalhada dos padrões estruturais extraídos de laudos anonimizados.

## Referências
- [[wiki/concepts/dicom]] — Padrão de imagem que gera o laudo
- [[wiki/concepts/laudo-patterns]] — Padrões estruturais catalogados
- [[context/ai-pipeline]] — Pipeline de geração de pré-laudo
- [[context/security-lgpd]] — Requisitos LGPD detalhados

## Backlinks
- [[wiki/overview]]
- [[wiki/concepts/laudo-patterns]]
- [[context/ai-pipeline]]
