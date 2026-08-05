---
title: "Snapshot: Resolução do Bug Multimodal LangChain4j"
slug: langchain4j-multimodal
date: 2026-06-03
type: source
tags: [codebase, bugfix, langchain4j, ai]
---

# Snapshot: Resolução do Bug Multimodal LangChain4j

## Resumo
A fonte detalha a mudança arquitetural onde removemos a dependência estrita do `TilaRadiologistaAgent` via interface `@AiService` para enviar imagens ao Gemini. Devido a conflitos de anotações `@UserMessage` na versão 1.0.1 do LangChain4j, passamos a usar o `ChatModel` diretamente no `LaudoService` para construir a requisição com `TextContent` e `ImageContent` combinados.

## Takeaways
1. A API declarativa (`@AiService`) tem limitações em mensagens multimodais complexas (template de texto + imagem lado a lado) na versão 1.0.1.
2. O uso direto de `ChatModel` permite maior flexibilidade e controle no envio do prompt + imagem (embora mais verboso).
3. Foi registrada uma decisão arquitetural (ADR-004) para formalizar a abordagem no projeto.

## Entidades e Conceitos
- [[wiki/decisions/ADR-004-langchain4j-multimodal]]
- [[wiki/concepts/langchain4j-multimodal-workaround]]

## Backlinks
- [[index]]
- [[log]]
