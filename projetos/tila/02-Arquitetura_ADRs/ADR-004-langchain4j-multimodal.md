---
title: "ADR-004: Abordagem Multimodal Direta com ChatModel vs AiServices"
type: decision
tags: [architecture, adr, langchain4j, ai]
sources: [raw/codebase/snapshots/2026-06-03-langchain4j-multimodal.md]
last_updated: 2026-06-03
---

# ADR-004: Abordagem Multimodal Direta com ChatModel vs AiServices

## Status
Accepted

## Context
Durante a integração da análise de imagens de Raio-X com Gemini via LangChain4j 1.0.1, enfrentamos conflitos no uso da interface declarativa `@AiService`. A anotação `@UserMessage` usada no template do contexto do exame (texto) entrava em conflito com o parâmetro `Image`. Se a imagem ficasse sem anotação, ocorria exceção de configuração (todos os parâmetros precisam de anotação). Se anotada com `@UserMessage`, a imagem substituía a mensagem de contexto textual. Como resultado, a IA recebia a imagem "cega", sem a instrução sobre como estruturar o laudo, devolvendo erro alegando falta de imagens.

## Decision
Abandonar o uso de `Image` dentro das interfaces `@AiService` e instanciar manualmente a chamada multimodal utilizando o `ChatModel` direto na camada de serviço (`LaudoService`). O serviço constrói as listas de `SystemMessage` e `UserMessage` com ambos `TextContent` e `ImageContent`.

## Alternatives Considered

### Alternativa 1: Wrapper Customizado para Image
Criar um wrapper para tentar passar a imagem como variável `@V` e processar internamente no LangChain4j.
*Rejeitada*: O fluxo interno de parser de templates do LangChain4j não prevê injeção fácil de ContentObjects complexos via template Handlebars.

### Alternativa 2: Downgrade do LangChain4j
Reverter para versões 0.3x do LangChain4j onde as validações de anotação poderiam ser menos restritas.
*Rejeitada*: Estamos consolidando as dependências para uso de Spring Boot 4 e compatibilidade atualizada. Retroceder criaria Technical Debt com a stack atualizada do projeto.

## Consequences

### Positivas
- Controle total sobre o conteúdo da mensagem: textos e imagens são enviados com garantia de não substituição.
- Menos "magia": a construção da requisição multimodal no `LaudoService` é explícita e fácil de debugar.

### Negativas
- Maior verbosidade no `LaudoService`.
- Acoplamento do `LaudoService` direto com `ChatModel` e suas APIs em vez de depender apenas da abstração de negócio `TilaRadiologistaAgent`.

### Riscos
- À medida que outras chamadas de agentes AI forem criadas (ex: `RevisorAgent`), corre-se o risco de haver código repetitivo manipulando `SystemMessage` e `UserMessage`. Será necessário refatorar em classes utilitárias no futuro se o padrão se repetir.

## Backlinks
- [[raw/codebase/snapshots/2026-06-03-langchain4j-multimodal.md]]
- [[wiki/concepts/langchain4j-multimodal-workaround]]
