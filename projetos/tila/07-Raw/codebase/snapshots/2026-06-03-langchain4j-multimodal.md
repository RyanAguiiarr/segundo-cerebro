# Snapshot: LangChain4j 1.0.1 Multimodal e AiServices Conflito

## Data
2026-06-03

## Contexto
Durante o desenvolvimento da integração RAG com LangChain4j (versão 1.0.1) e Gemini para análise de imagens de Raio-X (Tórax), encontramos um problema estrutural no uso da interface declarativa `@AiService`.

## O Problema
A interface `TilaRadiologistaAgent` usava a anotação `@UserMessage` para um template de texto longo estruturado (com variáveis `{{tipoExame}}`, etc.) e tinha um parâmetro `dev.langchain4j.data.image.Image` não anotado ou anotado com `@UserMessage`.
- Na versão 1.0.1 do LangChain4j, todos os parâmetros em um método `AiService` precisam de uma anotação válida (como `@V` ou `@UserMessage`).
- No entanto, anotar o parâmetro `Image` com `@UserMessage` enquanto já existia um template `@UserMessage` principal resultou em um conflito: o LangChain4j usou o `@UserMessage` da imagem e **ignorou/substituiu** o texto do template de contexto do exame.
- O resultado foi que a IA (Gemini) recebeu a imagem sem as instruções de texto, retornando que "nenhuma imagem ou descrição foi fornecida" para a análise estruturada que o sistema pedia (pois faltavam as instruções do prompt).

## A Solução (Decisão Arquitetural)
Como a API declarativa do LangChain4j 1.0.1 via `AiServices` não suportava de forma limpa o envio de imagens de forma isolada junto com templates `@UserMessage` complexos, a solução foi:
1. **Remover a imagem do `AiService`**: O parâmetro `Image` foi retirado da interface `TilaRadiologistaAgent`.
2. **Uso Direto do `ChatModel`**: A camada de serviço (`LaudoService.java`) passou a usar o `ChatModel` (injetado via construtor) chamando a API procedural.
3. **Construção Manual da Mensagem Multimodal**: O serviço agora lê o system prompt manualmente, constrói a `SystemMessage` e junta o `TextContent` (contexto) e o `ImageContent` numa mesma `UserMessage` antes de enviar com `chatModel.chat(ChatRequest.builder()...)`.

## Implicações
- Mais controle sobre os conteúdos e tipos multimodais (textos misturados com imagens), permitindo flexibilidade que os `@AiServices` limitam atualmente para imagens nessa versão.
- `LaudoService.java` agora orquestra a injeção do modelo e do sistema, e o `TilaRadiologistaAgent` pode ficar reservado para outras operações estritamente de texto se necessário, ou mesmo ser depreciado para análise de imagens.
