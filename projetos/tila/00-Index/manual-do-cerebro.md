# Manual Completo do Tila_Brain v2

Este é o guia definitivo de como funciona, como usar e como manter o cérebro do projeto TILA (Tecnologia Integradora de Laudos Automatizados).

## 🧠 O que é o Tila_Brain?
O Tila_Brain não é apenas uma pasta de documentação. É um **sistema vivo de conhecimento** feito para ser lido e atualizado tanto por humanos (Ryan e Pedro) quanto por agentes de Inteligência Artificial. 
Ele utiliza uma arquitetura organizada para garantir que o conhecimento da equipe, as decisões de código e as regras de negócio nunca fiquem obsoletas, incorretas ou se percam.

---

## 📂 Estrutura de Pastas: Onde guardar cada coisa?

A estrutura do cérebro é dividida em "camadas" com responsabilidades muito bem definidas:

### 1. Camada de Conhecimento de Negócio (`negocio/`)
Guarda as regras, decisões e o domínio do projeto. É a principal área de consulta.
*   **`negocio/inbox/`**: A "caixa de entrada". Notas em rascunho, ideias cruas e sugestões da IA. Nada aqui é considerado "verdade absoluta" até ser revisado e validado.
*   **`negocio/permanent/`**: O conhecimento oficial e validado.
    *   **`decisoes/`**: ADRs (Architecture Decision Records). Registros do *por que* tomamos certas decisões técnicas (ex: Por que usamos LangChain4j? Por que usamos JWT em cookie?).
    *   **`medico/`**: Regras do domínio médico (ex: estrutura de um laudo, regulamentações do CFM, obrigatoriedade de revisão humana).
    *   **`produto/`**: Visão e documentação do produto (ex: o problema que o TILA resolve, fluxos do usuário).
*   **`negocio/mocs/`**: Mapas de Conteúdo (Maps of Content). São índices temáticos que agrupam notas relacionadas para facilitar a leitura humana (ex: MOC de Segurança e LGPD, MOC de IA).

### 2. Camada de Conhecimento do Código (`codebase/`)
Guarda o entendimento do código-fonte (Backend e Frontend). Aqui não fica o código executável, apenas a *análise* sobre ele.
*   **`codebase/snapshots/`**: Auditorias completas de um momento específico no tempo. São imutáveis. Úteis para a IA saber "como estava o projeto" em uma determinada data.
*   **`codebase/patterns/`**: Padrões de código confirmados. Se o time decidiu usar `GenericResult<T>` no backend ou Angular Signals no frontend, documentamos aqui. A IA *sempre* deve ler isso antes de gerar código novo.
*   **`codebase/changelog/`**: Registros do que foi implementado em cada feature.

### 3. Camada de Fontes Imutáveis (`raw/`)
Guarda o material de estudo e referências originais. A IA e os humanos leem essas pastas, mas **nunca as modificam**.
*   **`raw/articles/`**: Artigos da web salvos.
*   **`raw/videos/`**: Transcrições de vídeos do YouTube ou aulas.
*   **`raw/laudos/`**: Exemplos de laudos médicos reais (⚠️ SEMPRE anonimizados/sintéticos).
*   **`raw/assets/`**: Imagens, PDFs e referências visuais.

### 4. Camada de Operação (`skills/` e `crons/`)
Define estritamente o comportamento da Inteligência Artificial no projeto.
*   **`skills/`**: Habilidades em formato Markdown que ensinam a IA a fazer tarefas específicas de forma repetível (ex: como validar uma nota, como atualizar o mapa de conteúdo).
*   **`crons/`**: Rotinas e manutenções que devem ocorrer periodicamente (revisões de backlog, limpezas, resumos semanais).

### 5. Camada de Contexto e Arquivos Raiz
*   **`context/`**: Arquivos vivos que ditam a realidade atual do projeto (identidade do projeto, roadmap atual, status de segurança, status do pipeline de IA). O **`SOUL.md`** (que define as regras inquebráveis e a "personalidade" da IA) mora aqui.
*   **`CLAUDE.md`**: O "manual de instruções raiz" do agente. Ele é carregado no cérebro da IA toda vez que uma sessão é iniciada.
*   **`index.md`**: O grande catálogo/índice com os links para todos os arquivos importantes do cérebro.
*   **`log.md`**: Um registro contínuo e histórico (append-only) de todas as grandes modificações, auditorias e criações ocorridas no cérebro.

---

## 🔄 Como Consumir e Adicionar Conhecimento

### Regra de Ouro: O "Gate" de Validação (Filtro Rigoroso)
Absolutamente nenhuma nota de conhecimento entra na pasta `negocio/permanent/` sem passar pelo **Skill Gate de Validação**.
Se a IA sugerir ou você mesmo quiser documentar algo novo:
1.  **Rascunho**: Cria-se um rascunho na pasta `negocio/inbox/`.
2.  **Validação**: O conteúdo deve responder positivamente a critérios como: É atômico (uma única ideia)? O título é uma tese/afirmação e não apenas um rótulo? Tem metadados? Conecta-se com outras notas do cérebro?
3.  **Promoção**: Só após ser revisada e passar no teste, a nota ganha o direito de ir para a pasta `negocio/permanent/`.

### Como interagir com o agente neste cérebro
*   **Para codificar ou refatorar:** A IA sabe que *precisa* entender o raio de impacto ("blast radius") antes de alterar classes importantes do backend ou frontend, e ela deve seguir estritamente o que está em `codebase/patterns/`.
*   **Ao resolver um problema arquitetural:** Peça para a IA "escrever um ADR" (Architecture Decision Record) detalhando o motivo da escolha. Ela salvará em `decisoes/`.
*   **Sempre mantenha os índices atualizados:** Após gerar muito conhecimento novo, você pode pedir à IA: "Atualize os MOCs, o log.md e o index.md com as mudanças de hoje".

---

## ⚠️ Linhas Vermelhas (Regras Inquebráveis)

1.  **LGPD em Primeiro Lugar**: NUNCA coloque dados reais de pacientes (nome, CPF, histórico) no cérebro. Todo exemplo deve ser 100% sintético.
2.  **Sem Segredos (Secrets)**: Não guarde senhas, chaves de API (como a chave do Gemini) ou credenciais de banco de dados no texto dos arquivos.
3.  **Fatos Médicos não se inventam**: A IA está proibida de ter "alucinações" ou inventar regras médicas para preencher lacunas. Na dúvida, ela tem ordem para pausar e solicitar validação humana.
4.  **Nunca apague o Core**: Arquivos como `CLAUDE.md` e `SOUL.md` são o coração operacional do cérebro. Deletá-los fará a IA perder suas diretrizes de segurança.

---

## 🚀 Resumo do Fluxo de Trabalho (Ritmo Diário)

1.  **Início do Dia:** A IA lê o `CLAUDE.md`, o `SOUL.md` e verifica o `context/roadmap.md` para saber o que falta fazer.
2.  **Durante a Codificação:** O time e a IA programam, sempre mantendo a padronização lida dos `patterns`.
3.  **Captura (Fim da Feature):** Quando uma feature termina, o time ou a IA geram a documentação das decisões novas, enviam para a `inbox/`, validam e publicam no `permanent/`.
4.  **Fechamento:** O `index.md` e o `log.md` recebem um carimbo do que aconteceu. O ciclo está pronto para o próximo dia.
