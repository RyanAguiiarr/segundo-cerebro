---
title: "Laudo gerado por IA exige revisão humana obrigatória antes de validade clínica"
type: permanent
domain: medico
tags: [laudo, ia, ética, lgpd]
date: 2026-06-09
---

# Laudo gerado por IA exige revisão humana obrigatória antes de validade clínica

## Por que a IA gera rascunhos, não laudos finais

### 1. Razão legal
- No Brasil, laudos médicos só têm validade com assinatura de médico habilitado (CRM ativo)
- IA não tem personalidade jurídica — não pode assinar laudos
- Resolução CFM nº 2.311/2022: IA é ferramenta auxiliar, nunca substituta do médico

### 2. Razão ética
- Diagnósticos impactam diretamente na saúde e vida do paciente
- IA pode errar (alucinações, viés de treinamento, casos atípicos)
- O médico é o responsável final — ele precisa concordar, editar ou rejeitar

### 3. Razão LGPD
- Decisões automatizadas sobre dados pessoais sensíveis (Art. 20, LGPD)
- Paciente tem direito a revisão por humano de decisão baseada em tratamento automatizado
- Laudos devem manter rastro: rascunho IA vs texto final do médico

## Como o TILA implementa isso

### Fluxo no código real
1. `LaudoService.gerarPreLaudo()` → gera rascunho com Gemini → salva com `StatusLaudo.RASCUNHO`
2. `textoFinal` começa igual a `rascunhoIA` — é o ponto de partida para edição
3. Médico revisa → status muda para `EM_REVISAO`
4. Médico assina → status muda para `ASSINADO`, `dataAssinatura` é registrada
5. ⚠️ O fluxo de revisão/assinatura (PUT endpoint) NÃO está implementado ainda

### Disclaimer obrigatório
Todo pré-laudo exibido ao médico deve incluir:

> "Este é um pré-laudo gerado por inteligência artificial (TILA). 
> Ele NÃO substitui a avaliação médica profissional. 
> O médico deve revisar, editar e assinar antes que tenha validade clínica.
> Confidence Score: [N]%"

### RLHF: o loop de melhoria
- Cada edição do médico (diff entre `rascunhoIA` e `textoFinal`) é dado de treinamento
- O que o médico corrigiu indica onde a IA errou
- Esse feedback alimenta melhorias futuras no prompt e eventualmente fine-tuning
- ⚠️ Pipeline RLHF NÃO implementado — gap documentado em [[codebase/snapshots/backend-ai-agent-2026-06-09]]

## Backlinks
- [[negocio/permanent/medico/laudo-medico-brasileiro-tem-5-secoes-obrigatorias]]
- [[negocio/permanent/produto/tila-resolve-gargalo-de-laudos-manuais]]
- [[negocio/mocs/moc-laudo-medico]]
