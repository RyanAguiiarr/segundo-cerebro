# Guia Definitivo do Graphify — Engenharia de Contexto via Grafos de Conhecimento

> **Versão:** 1.0 — Criado em 2026-06-18
> **Propósito:** Base de conhecimento e manual operacional do Graphify para agentes de IA e desenvolvedores do ecossistema Tila.
> **Uso:** Este arquivo deve ser lido por qualquer agente de IA (Antigravity, Cursor, Claude Code, Gemini CLI) antes de interagir com o código do Tila.
> **Repositório Original:** [github.com/safishamsi/graphify](https://github.com/safishamsi/graphify)

---

## 1. O que é o Graphify

O **Graphify** (desenvolvido por *safishamsi*) é uma ferramenta CLI e extensão (*skill*) para assistentes de IA que transforma repositórios de código — incluindo código-fonte, esquemas SQL, documentação, PDFs, imagens e vídeos — em um **Grafo de Conhecimento Estruturado e Semântico**.

### O Problema que ele Resolve
Assistentes de IA tradicionais sofrem com duas limitações ao analisar grandes bases de código:
1. **Janela de Contexto Limitada:** Passar milhares de linhas de código consome tokens e dilui a atenção do modelo (*Lost in the Middle*).
2. **Busca Textual Limitada (Grep):** Ferramentas como `grep` buscam correspondências de strings, mas falham em entender fluxos de execução entre camadas (ex: Front-end Angular disparando chamada HTTP que chega em um Controller Java Spring Boot, invoca um Service e persiste via JPA).

### Como ele Resolve
O Graphify quebra a base de código em uma **Árvore de Sintaxe Abstrata (AST)** localmente usando **Tree-sitter** (sem enviar código para APIs externas). Ele mapeia:
- **Nós (Nodes):** Entidades como classes, funções, tabelas, endpoints, DTOs.
- **Arestas (Edges):** Relações como chamadas de método, importações, heranças, consultas SQL.

O resultado é um **grafo direcionado consultável** que permite à IA navegar pela arquitetura do sistema em milissegundos.

---

## 2. Estrutura de Saída (`graphify-out/`)

Ao executar `/graphify .` na raiz do projeto, a ferramenta gera uma pasta `graphify-out/` contendo:

```
graphify-out/
├── graph.html             # Interface de Exploração Visual (abrir no navegador)
├── GRAPH_REPORT.md        # Relatório Executivo Arquitetural (humano e IA)
├── graph.json             # O Grafo Estruturado Completo (exclusivo para IA/MCP)
├── manifest.json          # Controle incremental (hashes AST de cada arquivo)
├── .graphify_analysis.json # Metadados internos da análise
└── .graphify_labels.json  # Rótulos de comunidades
```

### Detalhes dos Componentes

#### A. `graph.html`
Interface visual interativa para explorar o grafo no navegador. Permite:
- Clicar em nós para ver conexões de entrada e saída (*In-degree* e *Out-degree*).
- Filtrar por tipo de arquivo, subpastas ou grau de acoplamento.
- Identificar visualmente gargalos e "God Nodes".

#### B. `GRAPH_REPORT.md`
Relatório em Markdown que consolida os padrões do grafo:
- **God Nodes:** Classes/funções mais centrais e conectadas. Se quebrarem, o sistema falha.
- **Surprising Connections:** Pontes ocultas entre módulos que deveriam ser independentes (violação de arquitetura limpa).
- **The "Why":** Extrai comentários especiais (`// HACK:`, `// NOTE:`, `// FIXME:`, `// WHY:`) e docstrings, vinculando-os como nós explicativos à função que descrevem.
- **Confidence Tags:** Cada relação mapeada recebe: `EXTRACTED` (provada via AST), `INFERRED` (deduzida por proximidade semântica) ou `AMBIGUOUS` (requer verificação humana).
- **Suggested Questions:** Perguntas arquiteturais que o grafo está pronto para responder.

#### C. `graph.json`
Arquivo estruturado central com a lista indexada de nós, atributos, metadados e arestas. Este arquivo **nunca deve ser lido manualmente** por humanos — ele é consumido pelo servidor MCP ou pela CLI para alimentar agentes de IA.

#### D. `manifest.json`
Arquivo de controle incremental que armazena o `ast_hash` e a data de modificação (`mtime`) de cada arquivo analisado. Permite que o Graphify processe **apenas os arquivos modificados** em execuções subsequentes (`--update`), tornando a atualização extremamente rápida (< 2 segundos).

---

## 3. Linguagens e Arquivos Suportados

| Categoria | Extensões Suportadas | Tipo de Extração |
| :--- | :--- | :--- |
| **Código Fonte** | `.java`, `.py`, `.ts`, `.js`, `.tsx`, `.jsx`, `.go`, `.rs`, `.cpp`, `.c`, `.cs`, `.rb`, `.php`, `.kt`, `.scala`, `.swift`, `.lua`, `.zig`, `.sh`, `.bash`, `.sql`, `.razor` | Local via Tree-Sitter (AST) |
| **Infraestrutura** | `.tf`, `.tfvars`, `.hcl` (Terraform) | Requer extra `[terraform]` |
| **Configurações MCP** | `mcp.json`, `claude_desktop_config.json` | Mapeamento de servidores ativos |
| **Documentação** | `.md`, `.mdx`, `.txt`, `.html`, `.rst`, `.yaml`, `.yml` | Extração semântica |
| **Escritório** | `.docx`, `.xlsx` | Requer extra `[office]` |
| **PDFs** | `.pdf` | Requer extra `[pdf]` |
| **Mídias e Vídeos** | `.png`, `.jpg`, `.webp`, `.mp4`, `.mov`, `.mp3`, `.wav`, URLs do YouTube | Requer extra `[video]` (Whisper/Vision) |

---

## 4. Omnipresença do Graphify no Ciclo de Vida do Software

No ecossistema Tila, o Graphify é **obrigatório e onipresente**. Ele atua como o assistente central de contexto em **todas** as fases de desenvolvimento:

### A. Criação de Novas Features e Ideias
**Cenário:** O time quer criar um novo endpoint `/api/consultas` que integra com laudos e pacientes.
**Como o Graphify ajuda:**
- Antes de criar qualquer classe, a IA consulta o grafo para descobrir quais comunidades de nós existem e qual seria o ponto de menor acoplamento para inserir a nova feature.
- A IA verifica se já existem DTOs, Repositories ou Services que podem ser reutilizados, evitando duplicação de código.
- **Prompt exemplo:** *"Consulte o graphify e identifique quais entidades e services existentes já suportam dados de consultas médicas, e sugira o ponto ideal para acoplar um novo ConsultaController mantendo a coesão das comunidades."*

### B. Decisões Arquiteturais e Reviews
**Cenário:** O time discute se deve migrar de REST para GraphQL no módulo de laudos.
**Como o Graphify ajuda:**
- A IA consulta o grafo para mapear todos os Controllers REST que seriam afetados, os DTOs consumidos por cada endpoint e a profundidade das camadas envolvidas.
- O relatório mostra se a migração criaria novos "God Nodes" indesejáveis ou quebraria a modularidade das comunidades existentes.
- **Prompt exemplo:** *"Usando o graphify, mapeie todos os endpoints REST do módulo de laudos, seus DTOs e Services associados, para que eu avalie a complexidade de migrar para GraphQL."*

### C. Refatorações e Desacoplamentos
**Cenário:** O `LaudoService` tem 12 conexões e é o principal "God Node" do backend.
**Como o Graphify ajuda:**
- A IA consulta os vizinhos diretos e indiretos do `LaudoService` para entender quais responsabilidades podem ser extraídas para novos services menores.
- Identifica quais classes dependem exclusivamente de métodos específicos, permitindo refatoração segura por extração de interface.
- **Prompt exemplo:** *"Analise o LaudoService no graphify. Ele é um God Node com 12 conexões. Sugira uma estratégia de refatoração que reduza o acoplamento para no máximo 5 conexões diretas, mantendo a compatibilidade com os Controllers existentes."*

### D. Migrações de Tecnologia
**Cenário:** Migração do frontend de componentes NgModule para Standalone Components.
**Como o Graphify ajuda:**
- A IA mapeia a árvore de dependências de cada componente legado, identificando quais imports e providers precisam ser portados para o novo modelo standalone.
- Detecta dependências circulares que travariam a migração.
- **Prompt exemplo:** *"Mapeie no graphify todos os componentes Angular que ainda dependem de NgModules compartilhados e trace o caminho de migração para standalone, ordenado por menor dependência."*

### E. Diagnóstico de Bugs e Regras de Negócio
**Cenário:** O campo "saturação" do laudo está retornando fora do padrão esperado.
**Como o Graphify ajuda:**
- A IA rastreia o fluxo ponta a ponta: desde o componente Angular que exibe o campo, passando pelo Service HTTP que o consome, até o Controller Java que o recebe, o LaudoService que o processa, e a entidade JPA que o persiste no banco.
- A IA identifica exatamente em qual nó do caminho o valor está sendo malformado, lendo as regras de negócio associadas (comentários, validações, DTOs).
- **Prompt exemplo:** *"O campo 'saturação' do laudo está vindo com formato errado. Use o graphify para rastrear o caminho completo desse campo desde o frontend até a entidade no banco, e identifique onde a regra de formatação está falhando."*

### F. Análise de Impacto (Blast Radius Gate)
**Cenário:** O dev quer alterar a assinatura do método `processarLaudo()` no `LaudoService`.
**Como o Graphify ajuda:**
- A IA consulta os vizinhos de entrada (*In-degree*) do nó `processarLaudo` para listar todas as classes que invocam esse método.
- Antes de alterar uma única linha, a IA emite o relatório de impacto e pede confirmação explícita.
- **Prompt exemplo:** *"Vou alterar o método processarLaudo no LaudoService. Use o graphify para calcular o blast radius e me diga exatamente quais classes serão afetadas antes de eu prosseguir."*

---

## 5. Instalação e Comandos Essenciais

### Instalação
O pacote oficial no PyPI é **`graphifyy`** (com dois "y"). Recomenda-se instalação isolada:

```bash
# Instalação padrão recomendada usando UV
uv tool install graphifyy

# Instalação completa com suporte a MCP, PDFs e Office
uv tool install "graphifyy[all]"

# Alternativa usando Pipx
pipx install graphifyy
```

### Registro nos Assistentes de IA
```bash
graphify install          # Claude Code / Copilot
graphify cursor install   # Cursor
graphify gemini install   # Gemini CLI
graphify codex install    # Codex
graphify vscode install   # VS Code
```

### Tabela de Comandos CLI

| Comando | Função |
| :--- | :--- |
| `graphify .` | Cria o grafo do diretório atual do zero |
| `graphify . --update` | Atualiza apenas arquivos modificados (incremental, < 2s) |
| `graphify . --cluster-only` | Reagrupa comunidades sem reanalisar código |
| `graphify query "pergunta"` | Consulta o grafo via linguagem natural |
| `graphify path "ClasseA" "ClasseB"` | Caminho mais curto entre dois nós |
| `graphify explain "NomeClasse"` | Explicação arquitetural de um nó |
| `graphify export callflow-html` | Exporta diagramas de fluxo via Mermaid.js |
| `graphify hook install` | Instala automação de atualização via Git hooks |

---

## 6. Sincronização e Ciclo de Vida em Equipes (Git Workflow)

### Atualização Automática via Git Hooks
Ao executar `graphify hook install`, a CLI instala hooks `post-commit` e `post-checkout` na pasta `.git/hooks/`. Toda vez que um dev commita ou troca de branch, o Graphify roda `--update` em background automaticamente.

### Regra de Desversionamento
A pasta `graphify-out/` é tratada como **artefato efêmero de build** (como `target/` ou `dist/`):
- Cada dev gera seu próprio grafo localmente.
- A pasta é adicionada ao `.gitignore`, evitando conflitos de merge no Git.

### Resolução de Conflitos via Merge Driver
Quando `graphify hook install` é executado, ele também configura um **merge driver customizado** no Git. Se dois devs alterarem o `graph.json` em branches paralelas, o driver faz uma **União Algébrica de Grafos** automaticamente, sem conflitos de texto.

### O Arquivo `.graphifyignore`
Similar ao `.gitignore`, controla quais pastas/arquivos são ignorados pelo scanner do Graphify:

```
# Ignorar dependências e builds
node_modules/
target/
dist/
.angular/

# Ignorar mídia pesada (a menos que se use o extra [video])
*.png
*.jpg
*.gif
```

---

## 7. Integração com Model Context Protocol (MCP)

O Graphify pode ser exposto como um **servidor MCP** que dá à IA ferramentas estruturadas de consulta:

### Ferramentas Expostas via MCP

| Ferramenta | Função |
| :--- | :--- |
| `query_graph` | Busca vetorial e estrutural no grafo |
| `get_node` | Retorna metadados brutos de um componente |
| `get_neighbors` | Retorna vizinhos diretos (blast radius) |
| `shortest_path` | Menor rota de conexões entre dois nós distantes |

### Configuração no Cursor
```json
{
  "mcpServers": {
    "graphify": {
      "command": "uvx",
      "args": [
        "--with", "graphifyy[mcp]",
        "python", "-m", "graphify.serve",
        "graphify-out/graph.json"
      ],
      "type": "stdio"
    }
  }
}
```

### Configuração no Claude Code
```bash
claude mcp add graphify -- uvx --with graphifyy[mcp] python -m graphify.serve graphify-out/graph.json
```

### No Antigravity (IDE atual do Tila)
O agente do Antigravity utiliza diretamente a CLI do Graphify via terminal integrado. Não é necessário configurar servidor MCP separado — os comandos são executados nativamente no shell.

---

## 8. Engenharia de Prompt para Máxima Eficácia

### Prompts de Diagnóstico de Bugs
```
"O campo [X] do laudo está retornando fora do padrão. Use o graphify para rastrear
 o caminho completo desse campo desde o componente Angular até a entidade JPA,
 identificando onde a regra de negócio está falhando."
```

### Prompts de Análise de Impacto (Blast Radius)
```
"Vou alterar a assinatura do método [X] no [Service]. Use graphify para calcular
 o blast radius e listar todas as classes afetadas antes de prosseguir."
```

### Prompts de Criação de Features
```
"Quero criar um novo endpoint para [recurso]. Consulte o graphify e identifique
 qual comunidade de nós é a mais coesa para acoplar esse novo controller,
 e quais DTOs e repositories existentes podem ser reutilizados."
```

### Prompts de Refatoração
```
"Analise o [GodNode] no graphify. Ele tem [N] conexões. Sugira uma estratégia
 de refatoração que reduza o acoplamento para no máximo [M] conexões,
 mantendo compatibilidade com os controllers existentes."
```

### Prompts de Migração
```
"Mapeie no graphify todos os [componentes legados] que dependem de [padrão antigo]
 e trace o caminho de migração para [padrão novo], ordenado por menor dependência."
```

---

## 9. Dados Atuais do Grafo do Tila

### Backend (Tila_BackEnd)
- **Nós:** 297 | **Arestas:** 465 | **Comunidades:** 46
- **God Nodes:** `LaudoService` (12 edges), `AutenticacaoController` (10), `Laudo` (10), `Usuario` (9), `PacienteService` (8)
- **Extração:** 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS
- **Ciclos de Import:** Nenhum detectado

### Frontend (Tila_Frontend)
- Grafo gerado com mapeamento de componentes standalone Angular, services e rotas.

---

## Referências
- [Repositório Original](https://github.com/safishamsi/graphify) — safishamsi/graphify
- [Pacote PyPI](https://pypi.org/project/graphifyy/) — graphifyy (com dois "y")
- [skill-graphify-query.md](file:///c:/Tila/Tila_Brain/05-Skills_Agentes/skill-graphify-query.md) — Skill de consulta obrigatória do Tila
- [skill-arch-review.md](file:///c:/Tila/Tila_Brain/05-Skills_Agentes/skill-arch-review.md) — Skill de revisão arquitetural
- [CLAUDE.md](file:///c:/Tila/Tila_Brain/CLAUDE.md) — Manual operacional do agente
