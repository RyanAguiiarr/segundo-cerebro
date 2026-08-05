---
title: "Laudo médico brasileiro tem 5 seções obrigatórias que o pré-laudo TILA deve mapear"
type: permanent
domain: medico
tags: [laudo, medico, regulamentação]
date: 2026-06-09
---

# Laudo médico brasileiro tem 5 seções obrigatórias que o pré-laudo TILA deve mapear

## Estrutura de um laudo médico radiológico brasileiro

Um laudo de exame radiológico no sistema de saúde brasileiro segue uma estrutura padronizada com 5 seções essenciais:

### 1. Indicação Clínica
- Motivo do exame, hipótese diagnóstica
- Preenchida pelo médico solicitante
- No TILA: vem de `observacoesMedico` no LaudoGeracaoRequestDTO

### 2. Técnica
- Descrição da técnica radiológica utilizada
- Tipo de exame, incidências, contraste
- No TILA: derivada de `tipoExame` no Exame entity

### 3. Achados / Descrição
- Descrição sistemática dos achados radiológicos
- Linguagem técnica, região por região
- No TILA: campo `achados` no GeminiLaudoResponse → `achadosJson` no Laudo

### 4. Impressão Diagnóstica
- Conclusão do radiologista baseada nos achados
- Diagnóstico presumível ou diferencial
- No TILA: campo `impressaoDiagnostica` no GeminiLaudoResponse → `impressaoJson` no Laudo

### 5. Recomendações
- Exames complementares sugeridos, follow-up
- Opcional, mas padrão em laudos de RX de tórax
- No TILA: campo `recomendacoes` no GeminiLaudoResponse

## Registro de linguagem

Laudos médicos brasileiros usam:
- Linguagem técnica, registro formal
- Termos anatômicos em português (não latim)
- Estruturas padronizadas: "Observa-se...", "Nota-se...", "Sem evidências de..."
- Nunca linguagem coloquial ou termos em inglês

## Mapeamento TILA: Pré-laudo → Laudo final

O pré-laudo gerado pela IA (rascunhoIA) é um **RASCUNHO** que:
1. É gerado com status `RASCUNHO`
2. Deve ser revisado pelo médico (transição para `EM_REVISAO`)
3. Pode ser editado (campo `textoFinal` diferente de `rascunhoIA`)
4. Só se torna oficial após assinatura digital (status `ASSINADO`)

## Restrições LGPD
- Laudos contêm dados clínicos sensíveis (Art. 5, II, LGPD)
- Acesso restrito ao médico responsável e equipe assistencial
- Armazenamento deve ser criptografado em repouso
- Ver [[negocio/mocs/moc-seguranca-lgpd]]

## Backlinks
- [[negocio/permanent/medico/laudo-ia-exige-revisao-humana-obrigatoria]]
- [[codebase/patterns/padrão-seguranca-jwt]]
- [[negocio/mocs/moc-laudo-medico]]
