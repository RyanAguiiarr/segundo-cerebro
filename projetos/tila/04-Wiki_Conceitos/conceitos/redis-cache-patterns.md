---
title: "Redis e Padrões de Cache no Tila"
type: concept
tags: [redis, backend-patterns, cache, architecture, performance]
sources: [raw/codebase/conversations/2026-06-05-layout-state-management.md]
last_updated: 2026-06-05
---

# Padrões de Cache com Redis

Redis (Remote Dictionary Server) é um armazenamento de estrutura de dados em memória, open-source, usado como banco de dados em memória, cache, message broker e streaming engine. Em uma infraestrutura Dockerizada do Tila, o Redis roda em seu próprio container e ajuda significativamente a melhorar a performance e escalar o backend.

## Como o Redis difere do Estado do Angular?
Enquanto a [Gestão de Estado no Frontend (Angular)](./angular-state-management.md) cuida de manter os dados vivos *na memória do navegador do usuário*, o Redis gerencia estado *no backend*. O Redis não salva a aba do navegador de "recarregar" instantaneamente por conta própria, mas ele permite que o backend devolva esses dados de forma quase instantânea para o frontend se ele pedir novamente.

## Casos de Uso Simples e Comuns no Tila

### 1. Cache de Requisições Demoradas (Exames/Prontuários)
A funcionalidade mais clássica. Se buscar todos os exames de um paciente envolve ler o banco relacional, fazer joins pesados e ler chaves do MinIO, isso pode levar vários milissegundos.
- **Implementação**: Quando o backend busca os dados da primeira vez, ele salva o resultado JSON no Redis com a chave `prontuario:{pacienteId}`.
- **Resultado**: Nas próximas vezes que qualquer médico acessar esse prontuário ou se o frontend der "F5", o backend não bate no banco de dados; ele pega do Redis instantaneamente (tempo de resposta sub-milissegundo).

### 2. Gestão de Sessões de Usuário (Session Store)
Para não ter que ler o banco de dados toda vez que validar um token ou sessão de usuário.
- **Implementação**: Armazenar os tokens ou identificadores de login ativos no Redis com tempo de expiração (TTL).
- **Vantagem**: Permite invalidação instantânea de sessões (ex: "Deslogar de todos os dispositivos") e checagens muito rápidas em cada requisição autenticada, aumentando a segurança.

### 3. Rate Limiting (Controle de Limite de Requisições)
Evitar que um único usuário sobrecarregue os serviços, especialmente requisições caras (como chamar o modelo Gemini para gerar laudos).
- **Implementação**: Usar as estruturas do Redis para contar quantas requisições de geração de laudo o usuário fez no último minuto (`limite:laudos:userId:123`).
- **Resultado**: Se passar do limite, o backend recusa a requisição rapidamente com um HTTP 429, protegendo a conta da cloud e a infraestrutura.

## Integração no ecossistema
O container do Redis é acessado através das aplicações backend (como Spring Boot) do Tila.

## Backlinks
- [[wiki/sources/layout-state-management]]
- [[wiki/concepts/angular-state-management]]
- [[wiki/concepts/minio-object-storage]]
