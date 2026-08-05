---
title: "MOC — Laudo Médico"
type: moc
cluster: laudo-medico
---

# MOC — Laudo Médico

> Mapa de navegação para notas sobre o domínio de laudos médicos radiológicos.

## Domínio médico
- [[negocio/permanent/medico/laudo-medico-brasileiro-tem-5-secoes-obrigatorias]] — Estrutura obrigatória de um laudo
- [[negocio/permanent/medico/laudo-ia-exige-revisao-humana-obrigatoria]] — Revisão humana é inegociável

## Produto
- [[negocio/permanent/produto/tila-resolve-gargalo-de-laudos-manuais]] — Proposta de valor

## Padrões de código
- [[codebase/patterns/padrão-seguranca-jwt]] — Proteção de acesso a laudos

## Snapshots
- [[codebase/snapshots/backend-ai-agent-2026-06-09]] — Status do gerador de pré-laudos

## Entidades relacionadas (do snapshot backend)
- **Laudo** — 12 campos, status workflow (RASCUNHO → EM_REVISAO → ASSINADO → CANCELADO)
- **Exame** — Imagem de entrada para geração de laudo
- **GeminiLaudoResponse** — Record com achados, impressão, recomendações, confidence score
