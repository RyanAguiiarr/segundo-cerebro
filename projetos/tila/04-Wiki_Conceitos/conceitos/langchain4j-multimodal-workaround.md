---
title: "Padrão de Workaround Multimodal LangChain4j 1.0.1"
type: concept
tags: [langchain4j, ai, pattern, workaround]
last_updated: 2026-06-03
---

# Padrão de Workaround Multimodal LangChain4j 1.0.1

## O Padrão
Sempre que for necessário enviar uma imagem combinada com um template de texto instrucional complexo usando o LangChain4j 1.0.1, **evite usar interfaces `@AiService`**. Em vez disso, injete o `ChatModel` diretamente na camada de serviço e construa a requisição manualmente.

## Como implementar
1. Injetar `ChatModel` no construtor do Service.
2. Carregar a imagem e converter para Base64 e MimeType.
3. Carregar o System Prompt de um arquivo de resource.
4. Substituir as variáveis do User Prompt manualmente via `String.formatted()`.
5. Construir a `SystemMessage`.
6. Construir a `UserMessage` contendo tanto `TextContent.from(...)` quanto `ImageContent.from(...)`.
7. Enviar requisição via `chatModel.chat(...)`.

## Exemplo
Ver a implementação do método `gerarPreLaudo` no `LaudoService.java`.

## Backlinks
- [[wiki/decisions/ADR-004-langchain4j-multimodal]]
- [[wiki/sources/2026-06-03-langchain4j-multimodal]]
