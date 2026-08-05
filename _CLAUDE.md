# _CLAUDE.md — Segundo Cérebro Pessoal com IA

> **Manual de Instruções e Governança Operacional do Agente**
> Este arquivo define a lógica de decisão, regras de captura, política de frescor, regras de vínculo e protocolos de manutenção do cofre.

---

## 1. Visão Geral e Arquitetura

O Segundo Cérebro Pessoal é um sistema de conhecimento persistente organizado **por tipo de nota** em `wiki/` (para evitar duplicatas de entidades) e articulado por **hubs temáticos (MOCs)** em `mocs/`.

```
segundo-cerebro/
├── _CLAUDE.md          # Este arquivo (regras globais do agente)
├── index.md            # Índice central autogerado
├── log.md              # Log de operações do cofre
├── SOUL.md             # Perfil, preferências e valores do usuário
├── CRITICAL_FACTS.md   # Fatos de alta prioridade (orçamento L0 ~120 tokens)
├── START-HERE.md       # Guia de início rápido
├── GOVERNANCA.md       # Escada de autonomia do agente
├── raw/                # Funil de entrada de dados brutos (conversas, docs, áudio, capturas, vídeos)
├── wiki/               # Notas atômicas organizadas estritamente POR TIPO
├── mocs/               # Maps of Content (hubs por área de vida)
├── recursos/           # Materiais de referência e suporte
├── projetos/           # Projetos ativos, incluindo sub-vault técnico em projetos/tila/
├── boards/             # Quadros de acompanhamento (Kanban/Status)
├── templates/          # Schemas e gabaritos formais de notas
├── arquivo/            # Depósito de notas arquivadas (deleção lógica)
├── _sessoes/           # Transcrições e memórias de sessões de trabalho
└── _manutencao/        # Logs e scripts de manutenção noturna/semanal
```

---

## 2. Regra de Captura (Lógica Central de Decisão)

Toda informação capturada ou processada pelo agente **DEVE** seguir os 4 passos obrigatórios abaixo:

### 2.1. Verificação de Existência (Existence Check Pré-Criação)
- **REGRA DURA:** Antes de criar qualquer nova nota, realize uma busca por nome ou conceito semelhante dentro da pasta específica em `wiki/` (ex: `wiki/entities/`, `wiki/concepts/`) e no arquivo `index.md`.
- **OBJETIVO:** Prevenir o surgimento de entidades duplicadas ou grafias concorrentes (ex: evitar ter `Joao-Silva.md` e `João Silva.md` simultaneamente).
- Se uma entidade idêntica ou equivalente for encontrada, **NÃO crie uma nota nova**. Atualize a nota existente.

### 2.2. Régua de Decisão: Nota Nova vs. Editar In-Loco
A decisão de criar uma nota atômica nova ou editar uma nota existente baseia-se na pergunta:
> *"Isso é uma entidade/conceito/decisão autônoma que será linkada de vários lugares, ou é apenas um atributo/mudança de estado de algo que já existe?"*

1. **Nota Nova (Criar em `wiki/`):**
   - Entidades novas (pessoas, empresas, ferramentas, lugares).
   - Conceitos, decisões formais, projetos, tarefas, leituras, metas ou aprendizados autônomos.
   - A nota nasce no formato de template correspondente em `templates/` e no diretório por tipo correto em `wiki/`.

2. **Edição In-Loco e Fatos Bitemporais (Atualizar Nota Existente):**
   - Mudanças de atributos ou estados (ex: alteração de papel profissional, mudança de status de projeto, alteração de preferência).
   - **Formato Bitemporal Obrigatório:** Toda alteração de fato em nota existente deve registrar duas datas:
     - `valido_em: AAAA-MM-DD` (quando o fato se tornou verdade no mundo real).
     - `aprendido_em: AAAA-MM-DD` (quando o cérebro/agente registrou a informação).
   - **NUNCA** sobrescrever silenciosamente o histórico anterior; adicione o novo estado mantendo a rastreabilidade temporal.

3. **Tratamento de Contradições:**
   - Se uma nova informação **contradisser** diretamente o que já está registrado em uma nota:
     - **NUNCA** apague nem sobrescreva o fato antigo.
     - Marque a contradição no frontmatter da nota ou em uma nota de reconciliação:
       ```yaml
       relations:
         - type: contradiz
           target: "[[slug-da-nota-contradita]]"
       ```
     - Adicione o item à fila de reconciliação para processamento via comando `/obsidian-reconcile`.

4. **Solicitação de Novas Pastas / Áreas de Primeiro Nível:**
   - O agente **NUNCA** cria pastas de primeiro nível ou novas áreas temáticas por conta própria.
   - Se identificar um padrão recorrente que não se enquadre nas categorias existentes, o agente **DEVE parar e perguntar ao usuário** antes de criar qualquer estrutura física nova.

---

## 3. Política de Deleção Não Destrutiva

- **Deleção NUNCA é destrutiva ou definitiva.**
- **Procedimento Padrão:** Qualquer nota marcada para "remoção" deve ser movida para a pasta `arquivo/`, adicionando no topo do arquivo ou no frontmatter o motivo e a data do arquivamento.
- **Deleção Física (Permanente):** Ocorre **EXCLUSIVAMENTE** sob confirmação explícita e manual do usuário, item por item. Operações de exclusão automática ou em lote são terminantemente proibidas.

---

## 4. Gatilhos de Captura

A captura de informações é acionada por quatro vias complementares:

1. **Captura em Tempo de Conversa (Proativa):**
   - Quando o usuário afirmar um fato novo, tomar uma decisão explícita ou fizer uma correção durante o diálogo, o agente deve sugerir salvar/atualizar o fato imediatamente na nota apropriada, sem postergar para o encerramento da conversa.

2. **Comandos Explícitos (`/salvar`, `/fim-de-sessao`):**
   - Ao final de um bloco de trabalho ou ao receber comandos formais de encerramento, o agente faz a varredura do contexto da sessão, extrai fatos/decisões e atualiza o cofre.

3. **Ingestão de Fontes Externas (`raw/`):**
   - Ao receber documentos, PDFs, e-mails, transcrições de áudio ou capturas, o material é depositado em `raw/<tipo>/`.
   - O agente processa a fonte através do funil de classificação (verificação de existência -> criação de notas atômicas em `wiki/` ou atualização in-loco). O arquivo bruto nunca fica solto ou não catalogado.

4. **Manutenção Agendada (Rotinas Noturnas / Semanal):**
   - As rotinas de fundo não capturam fatos novos do mundo, mas **higienizam, reconciliam contradições e organizam** os fatos já capturados.

---

## 5. Política de Frescor (OKM — Open Knowledge Metabolism) e Fatos Bitemporais

Todo fato armazenado no cofre **DEVE** pertencer estritamente a uma das três formas legais abaixo (nenhum fato vive solto no texto):

1. **Fato Atemporal (`atemporal`):** Fatos de evolução lenta (muda em 7+ dias ou anos). Exemplo: arquitetura de um software, princípios pessoais, funcionamento de um processo.
2. **Fato Datado / Snapshot (`datado`):** Fatos válidos em um momento específico (`valido_em: AAAA-MM-DD`). Histórico imutável.
3. **Ponteiro (`ponteiro`):** Fatos de alta volatilidade (saldos, peso, medições, contagem de tarefas/treinos) **NUNCA viram valor numérico estático em nota**. Registram-se como link para o sistema vivo com carimbo de data:
   `Ver: [Planilha/App] (conforme_em: AAAA-MM-DD)` ou `(as of AAAA-MM-DD)`.

### Regra Dura para Finanças e Saúde
- **Finanças e Saúde:** Saldo bancário, peso corporal, contagem de treinos, glicemia ou qualquer métrica volátil **NUNCA são copiados como números soltos em notas**.
- Em `mocs/financas.md` e `mocs/saude.md`:
  - A seção **"Estado Atual"** é **EXCLUSIVAMENTE PONTEIRO** para a fonte viva com carimbo de data.
  - A seção **"Decisões e Estratégia"** contém prose e planejamento real.

### Linter de Frescor
- O script `_manutencao/scripts/freshness_lint.py` executa validações automáticas durante a rotina de saúde `/obsidian-health`, identificando:
  - `FRESH-1`: Afirmação no presente sobre dado volátil sem carimbo `as of` ou ponteiro.
  - `FRESH-2`: Carimbo `as of` mais antigo que a janela de frescor (padrão 7 dias).
  - `FRESH-3`: Ponteiro tipado sem mapeamento correspondente no `.freshness.json`.

---

## 6. Regras de Vínculo e Grafo de Conhecimento

### 6.1. Meta Operacional: Zero Notas Órfãs e Zero Links Forçados
- O objetivo **não é maximizar o volume de links**, mas sim garantir a utilidade e a navegabilidade do grafo sem introduzir ruído.
- **NUNCA crie links forçados ou arbitrários** entre notas que tenham apenas menções secundárias ou irrelevantes.

### 6.2. Vínculo Síncrono no Momento da Edição/Criação
- O passo de vinculação ocorre **sempre e obrigatoriamente** durante a criação ou edição de uma nota.
- Varra o texto da nota em busca de menções a entidades, conceitos, projetos ou decisões já cadastrados no cérebro e crie os `[[wikilinks]]` correspondentes na própria nota.

### 6.3. Resolução de Entidade em Duas Etapas
Para decidir se uma palavra/expressão deve virar um `[[wikilink]]` para uma nota existente:
1. **Filtro Leve (Correspondência Léxica):** Identificar se existe nota com nome exato, alias ou sinônimo no mesmo contexto (projeto/área).
2. **Checagem Semântica de Confirmação:** Verificar se a menção refere-se **à mesma entidade real** ou se é apenas uma palavra idêntica em contexto distinto. Linkar apenas em caso de correspondência semântica confirmada.

### 6.4. Mediação via Maps of Content (MOCs)
- MOCs (`mocs/*.md`) funcionam como agregadores centrais para temas transversais.
- Nem toda nota precisa se conectar diretamente a todas as outras notas da mesma área de vida. O MOC da área (ex: `mocs/saude.md`, `mocs/carreira.md`) atua como a ponte estruturadora.

### 6.5. Relações Tipadas (Vocabulário Fechado)
Opcionalmente, quando a relação possuir significado semântico específico, registre-a no bloco `relations:` do frontmatter usando **exclusivamente** o vocabulário fechado abaixo:

```yaml
relations:
  - type: depende-de | contradiz | supersede | superseded-por | gerou | pertence-a | trabalha-com | aprendido-de | referencia | correlaciona-com
    target: "[[slug-da-nota-alvo]]"
```

- **NUNCA** crie um novo tipo de relação fora desta lista sem aprovação do usuário.

### 6.6. Higienização Noturna de Órfãs
- A rotina noturna (Fase 8) executa a varredura do grafo à procura de notas órfãs (notas sem backlinks e sem links de saída) e as sinaliza no relatório sem forçar conexões artificiais.

---

## 7. Privacidade, Segredos e Versionamento

### 7.1. Acesso Total ao Cofre
- **NENHUMA pasta é excluída do agente.** Não se utiliza `OBSIDIAN_EMBED_EXCLUDE` ou listas de bloqueio por conteúdo.
- Todo o cofre (incluindo notas em `mocs/financas.md`, `mocs/saude.md`, vida pessoal e carreira) é acessível ao agente.

### 7.2. Gestão de Segredos
- O único segredo real mantido fora do repositório é o arquivo `.env` (contendo chaves de API, senhas, tokens).
- O arquivo `.env` é **sempre** ignorado pelo `.gitignore`.

### 7.3. Política de `.gitignore`
O arquivo `.gitignore` protege segredos e ignora apenas artefatos pesados/regeneráveis:
```
.env
*.embeddings-index/
.claude-runs/
.obsidian-semantic-index.json
__pycache__/
*.pyc
.venv/
```

- **Histórico de Manutenção Versionado:** A pasta `_manutencao/logs/` permanece **versionada** no git por constituir histórico operacional leve e relevante.

---

## 8. Manutenção Viva (Agentes Agendados e Agente de Fundo)

### 8.1. Os 4 Agentes Agendados
1. **Agente da Manhã (`_manutencao/scripts/agente_manha.py`):**
   - Cria a nota diária `wiki/daily/YYYY-MM-DD.md`.
   - Vaneia e destaca tarefas atrasadas/pendentes em `wiki/tasks/`.
2. **Agente da Noite (`_manutencao/scripts/agente_noite.py`):**
   - Fecha a nota diária.
   - Executa `/reconciliar` na fila de contradições.
   - Executa `/emergir` para detectar padrões de hábitos/comportamento.
   - Higieniza notas órfãs via verificação de vínculo.
   - Reconstrói o catálogo central `index.md`.
3. **Agente Semanal (`_manutencao/scripts/agente_semanal.py` — Sexta-Feira):**
   - Gera a nota de revisão semanal em `wiki/reviews/`.
   - Compila métricas, aprendizados da semana e realiza ajustes estratégicos.
4. **Agente de Saúde (`_manutencao/scripts/agente_saude.py` — Domingo):**
   - Executa a auditoria completa de saúde do cofre (`/saude-cofre`).
   - Roda o Linter de Frescor OKM (`_manutencao/scripts/freshness_lint.py`).
   - Verifica links quebrados e garante o isolamento de segredos no `.env`.

### 8.2. Agente de Fundo (PostCompact — Desligado por Padrão)
- **Gatilho:** Dispara após a compactação de contexto da conversa.
- **Superfície de Ferramentas Travada:** Permite **APENAS** leitura/escrita/edição no cofre. Sem acesso a terminal/shell e sem acesso à rede externa.
- **Operações Permissíveis:** Adiciona ou atualiza informações. **NUNCA deleta ou funde notas** autonomamente.
- **STATUS:** **DESLIGADO POR PADRÃO** (Requer autorização explícita antes de ativar).

### 8.3. Lembretes de Salvar e Injeção de Recall
- **Lembrete de Salvar:** O agente sugere acionar `/salvar` após 10+ trocas de mensagens ou ao identificar expressões como "pronto", "obrigado", "valeu".
- **Recall Bounded com Abstenção (`_manutencao/scripts/obsidian_recall.py`):**
  - Injeta um resumo breve (máximo de 4 notas e ~900 caracteres) antes da resposta quando houver alta relevância.
  - **ABSTÉM-SE** totalmente em caso de baixa confiança (silêncio é preferível a ruído).
  - Todas as decisões de injeção ou abstenção são registradas em `.claude-runs/recall-YYYY-MM-DD.jsonl`.
