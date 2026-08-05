---
name: skill-graphify-query
trigger: automatic — runs before ANY interaction with code (modification, creation, diagnosis, architecture, refactoring, migration)
description: "O Graphify é o mecanismo de contexto central e obrigatório do Tila. Antes de qualquer interação com código — seja criar features, diagnosticar bugs, refatorar, migrar ou simplesmente entender a arquitetura — o agente DEVE consultar o grafo de conhecimento para fundamentar suas decisões com precisão estrutural."
version: 2.0
last_updated: 2026-06-18
integrates_with:
  - skill-arch-review (novas ideias e decisões arquiteturais)
  - skill-dev-assistant (governança de código)
  - skill-session-recorder (registro de blast radius)
---

# Skill: Graphify Query — Assistente Onipresente de Contexto

## Princípio Fundamental

> 🧠 O Graphify é o **GPS do código do Tila**. Assim como um GPS precisa ser consultado
> antes de dirigir para um destino desconhecido, o Graphify precisa ser consultado
> antes de qualquer decisão que envolva o código-fonte. Sem exceção.

> 🚨 Em uma aplicação médica, uma dependência quebrada não é apenas um bug —
> é um risco à segurança do paciente. O Graphify é OBRIGATÓRIO, não opcional.

---

## Quando esta Skill é Acionada

Esta skill roda **AUTOMATICAMENTE** antes de:

### 🔵 Criação e Implementação
- Criar uma nova feature, endpoint, componente ou entidade
- Implementar uma nova ideia ou requisito de negócio
- Adicionar um novo módulo ou camada ao sistema

### 🟠 Diagnóstico e Resolução de Problemas
- Investigar a causa raiz de um bug reportado
- Rastrear o fluxo de dados de ponta a ponta (Front → Controller → Service → BD)
- Entender regras de negócio vigentes que regulam um campo ou entidade específica
- Localizar onde uma validação ou formatação está falhando

### 🔴 Alteração e Refatoração
- Modificar qualquer arquivo existente do código-fonte
- Refatorar classes, métodos ou componentes
- Desacoplar "God Nodes" com alto grau de centralidade
- Extrair interfaces ou dividir services

### 🟣 Migração e Arquitetura
- Migrar de um padrão para outro (ex: NgModule → Standalone)
- Avaliar viabilidade de mudanças arquiteturais (ex: REST → GraphQL)
- Planejar a portabilidade de módulos legados

### ⚪ Entendimento e Exploração
- Responder qualquer pergunta sobre "o que existe" ou "como funciona"
- Mapear dependências de uma classe ou componente
- Gerar documentação arquitetural baseada no estado real do código

---

## Steps — Fluxo de Execução

### Etapa 1: Identificar o Objetivo
Determinar qual dos cenários acima se aplica à solicitação do programador:
- **Criação?** → Buscar ponto ótimo de acoplamento
- **Diagnóstico?** → Rastrear fluxos e regras de negócio
- **Alteração?** → Calcular blast radius
- **Migração?** → Mapear dependências legadas
- **Exploração?** → Navegar pela estrutura

### Etapa 2: Consultar o Graphify

#### Se a CLI está no PATH (preferencial):
```bash
# Para diagnóstico de bugs e rastreamento de fluxo:
graphify query "Como o campo [X] flui desde o frontend até o banco de dados?"

# Para encontrar o caminho entre dois componentes:
graphify path "[ClasseOrigem]" "[ClasseDestino]"

# Para análise de impacto (blast radius):
graphify query "[NomeClasse]" --depth 2

# Para explicação arquitetural completa de um nó:
graphify explain "[NomeClasse]"
```

#### Se a CLI NÃO está no PATH (fallback):
1. Ler o arquivo `graphify-out/GRAPH_REPORT.md` para entender a topologia geral.
2. Ler o arquivo `graphify-out/graph.json` para localizar nós e arestas específicos.
3. Complementar com leitura direta dos arquivos de código-fonte para mapear dependentes manualmente.
4. Informar ao programador: "Graphify CLI não detectada no PATH. Usando dados estáticos do último grafo gerado. Para atualizar, execute: `uv tool install graphifyy && graphify . --update`"

### Etapa 3: Analisar e Reportar

#### Para Diagnóstico de Bugs:
```markdown
🔍 DIAGNÓSTICO VIA GRAPHIFY
- Campo/Fluxo investigado: [nome do campo ou fluxo]
- Caminho rastreado:
  1. [Componente Frontend] → (chamada HTTP)
  2. [Controller] → (injeção de dependência)
  3. [Service] → (lógica de negócio)
  4. [Repository/Entity] → (persistência no BD)
- Ponto provável da falha: [arquivo:linha — descrição]
- Regras de negócio vigentes: [lista de validações encontradas]
```

#### Para Criação de Features:
```markdown
🏗️ PONTO DE ACOPLAMENTO VIA GRAPHIFY
- Feature solicitada: [descrição]
- Comunidade mais coesa para inserção: Community [N] (coesão: [X])
- Classes/DTOs reutilizáveis encontrados: [lista]
- Novo acoplamento estimado: [N] conexões novas
- Impacto na modularidade: [baixo/médio/alto]
```

#### Para Blast Radius (Alterações e Refatorações):
```markdown
🔍 BLAST RADIUS — Impacto Detectado via Graphify
- Alvo: [classe/componente a ser alterado]
- Dependentes diretos: [N] — [lista com nomes]
- Dependentes indiretos (profundidade 2): [N] — [lista]
- Risco de regressão: [alto/médio/baixo]

⚠️ Deseja prosseguir com a alteração? (Sim/Não)
```

#### Para Migrações:
```markdown
🔄 MAPA DE MIGRAÇÃO VIA GRAPHIFY
- Componentes no padrão legado: [N] — [lista]
- Componentes já migrados: [N] — [lista]
- Ordem de migração sugerida (menor dependência primeiro):
  1. [Componente A] — [N] dependentes
  2. [Componente B] — [N] dependentes
  3. ...
- Dependências circulares detectadas: [sim/não — detalhe]
```

### Etapa 4: Obter Confirmação Humana

**REGRA ABSOLUTA:** Após apresentar o relatório de blast radius de qualquer alteração de código, o agente DEVE:
1. Aguardar a confirmação explícita do programador ("Sim", "Pode prosseguir", "OK").
2. Somente após a confirmação, prosseguir com a escrita do código.
3. Se o programador disser "Não" ou pedir ajustes, voltar à Etapa 2 com o novo escopo.

---

## Se Graphify NÃO está instalado

Informar ao programador:
```
⚠️ Graphify CLI não está instalada neste ambiente.
Para instalar:
  uv tool install "graphifyy[mcp]"

Para gerar o grafo do projeto:
  graphify .

Para ativar atualização automática a cada commit:
  graphify hook install

Até a instalação, usarei os dados estáticos de graphify-out/ (se existirem)
ou farei varredura manual dos arquivos com menor precisão.
```

---

## Rules

### Regra 1: Omnipresença
O Graphify é consultado em TODA interação com código — sem exceção. Ele não é apenas para blast radius. Ele é o mecanismo primário de inteligência contextual para criação, diagnóstico, refatoração, migração e exploração.

### Regra 2: Confirmação Humana Obrigatória
NUNCA alterar código sem antes apresentar o relatório de impacto ao programador e obter confirmação explícita.

### Regra 3: Transparência
Se o grafo estiver desatualizado ou se a CLI não estiver disponível, informar claramente ao programador qual fonte de dados está sendo utilizada e qual a precisão esperada.

### Regra 4: Segurança Médica
Em um sistema médico como o Tila, a precisão do mapeamento de dependências é um requisito de segurança do paciente. Tratar toda análise de impacto com a seriedade correspondente.

---

## Referências
- [manual-contexto-graphify.md](file:///c:/Tila/Tila_Brain/00-Index/manual-contexto-graphify.md) — Base de conhecimento completa do Graphify
- [skill-arch-review.md](file:///c:/Tila/Tila_Brain/05-Skills_Agentes/skill-arch-review.md) — Review arquitetural antes de codificar
- [skill-dev-assistant.md](file:///c:/Tila/Tila_Brain/05-Skills_Agentes/skill-dev-assistant.md) — Governança de código durante implementação
- [CLAUDE.md §3](file:///c:/Tila/Tila_Brain/CLAUDE.md) — Protocolo de consulta de código
