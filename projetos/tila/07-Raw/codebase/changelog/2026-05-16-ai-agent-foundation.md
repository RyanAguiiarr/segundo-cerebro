# Changelog: AI Agent Foundation — Raio-X de Tórax
Date: 2026-05-16
Author: Ryan Cantareli de Aguiar
Session: Fases 2 e 3 do Roadmap — Agente Radiologista

## Intenção
Implementar a fundação do agente de IA Dr. TILA com foco exclusivo em Raio-X de Tórax.
Conectar os beans LangChain4j já existentes (ChatModel, EmbeddingModel, EmbeddingStore, ContentRetriever)
a uma interface de agente real, com system prompt externalizado e orquestração via LaudoService.

## Arquivos Criados

| Arquivo | Descrição |
|---|---|
| `ai/agent/TilaRadiologistaAgent.java` | Interface LangChain4j `@AiService` com `@SystemMessage(fromResource)` e template `@UserMessage` parametrizado com 7 variáveis clínicas + `Image` multimodal |
| `ai/prompt/radiologista-system.txt` | System prompt do Dr. TILA — POSIÇÃO INCORRETA (está em src/main/java ao invés de src/main/resources/prompts/) — BUG PENDENTE |
| `resources/prompts/` | Diretório criado mas VAZIO — o .txt não foi movido ainda |

## Arquivos Modificados

| Arquivo | Mudança |
|---|---|
| `ai/config/TilaRagConfig.java` | Bean `tilaAgent()` adicionado: constrói `TilaRadiologistaAgent` via `AiServices.builder()` injetando `ChatLanguageModel` + `ContentRetriever`; porta corrigida para 5434; credenciais via `@Value` |
| `context/roadmap.md` | Item "system prompt" atualizado com escopo: "Foco inicial exclusivo: Raio-X de Tórax" |
| `context/project-identity.md` | Missão atualizada: foco inicial exclusivo em Raio-X de Tórax |
| `context/ai-pipeline.md` | System prompt template atualizado para refletir especialização em RX Tórax |
| `tila_ai_agent_architecture.md` | Título e seções atualizados para refletir escopo de Raio-X de Tórax |

## Padrões Introduzidos

1. **LangChain4j AiService Pattern**: Interface Java com `@SystemMessage(fromResource = "prompts/file.txt")` para externalizar prompts do classpath. Permite editar prompts sem recompilar.
2. **Template de UserMessage parametrizado**: Uso de `@UserMessage` com chaves `{{variavel}}` e `@V("variavel")` nos parâmetros para montar contexto clínico estruturado.
3. **Multimodal via objeto Image**: `Image imagem` sem `@V` passado como parâmetro separado — LangChain4j anexa automaticamente à mensagem.
4. **DTOs planejados**: `LaudoGeracaoRequestDTO`, `LaudoResponseDTO`, `LaudoRevisaoRequestDTO` (records Java) — ainda não implementados no código.
5. **ExameRepository com JOIN FETCH**: `findByIdWithDetails()` com `@Query` JPQL para buscar Exame + Paciente + Médico em 1 query (evitar N+1).

## Decisões Arquiteturais

- Foco exclusivo em **Raio-X de Tórax (PA e Perfil)** — decisão de escopo acadêmico para simplificar o system prompt e a base de conhecimento RAG na Fase 3.
- System prompt externalizado em `.txt` (não embutido em `@SystemMessage("")`) — manutenabilidade.
- Agente construído manualmente via `AiServices.builder()` ao invés de auto-config Spring — controle explícito de qual `ContentRetriever` é injetado.

## Desvios de Convenção

- NENHUM novo desvio introduzido nesta sessão.

## Bugs Identificados / Pendências

| # | Bug | Severidade | Status |
|---|---|---|---|
| 1 | `@Value("AIzaSyBkM8J29x9tpX...")` — API Key hardcoded em `TilaRagConfig` | 🔴 CRÍTICO | **PENDENTE** |
| 2 | `radiologista-system.txt` em `src/main/java/ai/prompt/` — não será encontrado no classpath | 🔴 CRÍTICO | **PENDENTE** |
| 3 | `@V("imagem") Image imagem` — `@V` inválido para tipo `Image` no LangChain4j | 🟡 | **PENDENTE** |
| 4 | Bug original em `Laudo.onPreUpdate()` — `dataAssinatura` sempre sobrescrita no else | 🟡 | **PENDENTE** |

## Componentes Planejados (Não Implementados)

- `ExameRepository` com `findByIdWithDetails()`
- `LaudoGeracaoRequestDTO`, `LaudoResponseDTO`, `LaudoRevisaoRequestDTO`
- `LaudoService` com métodos: `gerarPreLaudo()`, `revisarLaudo()`, `assinarLaudo()`
- `LaudoController` com endpoints REST
