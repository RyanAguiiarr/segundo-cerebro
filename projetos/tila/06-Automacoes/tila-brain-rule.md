## Tila Brain — Regra Operacional do Agente

> Esta regra governa o comportamento do agente de IA (Antigravity) em TODAS as sessões de trabalho
> no workspace `c:\Tila`. Ela garante que o Segundo Cérebro (Tila_Brain) seja o centro
> de comando de toda interação — carregado automaticamente, consultado continuamente e atualizado
> a cada sessão.

---

### §1 — Auto Boot (Início de Sessão)

Ao iniciar qualquer conversa no workspace `c:\Tila`, o agente DEVE executar o boot
silencioso antes de responder ao programador. O boot consiste em:

1. **Ler `Tila_Brain/CLAUDE.md`** — Manual operacional completo (§1 a §6). Internalizar todas as regras.
2. **Ler `Tila_Brain/00-Index/SOUL.md`** — Identidade do agente e regras inquebráveis (non-negotiables).
3. **Ler `Tila_Brain/index.md`** — Catálogo completo do cérebro: notas permanentes, patterns, ADRs, snapshots, skills.
4. **Ler `Tila_Brain/log.md`** (últimas 10 entradas) — O que aconteceu recentemente no cérebro.
5. **Ler `Tila_Brain/01-Negocio/contexto/roadmap.md`** — Prioridades atuais e próximas tarefas.
6. **Verificar `Tila_Brain/07-Raw/sessions/`** — Buscar a última sessão de programação. Se o `status: active`, a sessão anterior não foi fechada — alertar o programador.
7. **Anunciar** ao programador com um resumo breve:
   ```
   🧠 Tila_Brain v2.1 carregado.
   📊 [N] permanent notes | [N] patterns | [N] ADRs | [N] snapshots
   📅 Última ação: [descrição da última entrada do log.md]
   ⏸️ Pendências: [quantidade ou "nenhuma"]
   🎯 Próxima prioridade: [do roadmap]
   ```

> ⚠️ REGRA ABSOLUTA: Se o programador começar a pedir código ou tarefas sem que o boot tenha sido
> executado, o agente DEVE executar o boot silenciosamente ANTES de responder. Nunca operar sem
> contexto do cérebro.

---

### §2 — Skill System (Como Executar Skills)

O cérebro possui 18 skills documentadas em `Tila_Brain/05-Skills_Agentes/`. Cada skill é um
arquivo Markdown com instruções detalhadas que o agente DEVE seguir ao pé da letra.

**Quando o programador usar um comando-gatilho (trigger), o agente deve:**
1. Abrir e ler a skill correspondente em `Tila_Brain/05-Skills_Agentes/`
2. Seguir os **Steps** documentados na skill, na ordem exata
3. Respeitar as **Rules** documentadas na skill sem exceção
4. Produzir o **Output** no formato exato descrito na skill

**Tabela de gatilhos reconhecidos:**

| Comando do Programador | Skill Acionada | Arquivo |
|---|---|---|
| `/boot` ou início de sessão | Session Boot | `skill-session-boot.md` |
| `/arch-review` ou "analise essa ideia" | Arch Review | `skill-arch-review.md` |
| `/capture` ou "capture essa feature" | Capture Feature | `skill-capture-feature.md` |
| `/close` ou `/salve` | Session Close | `skill-session-close.md` |
| `/organizar` | Brain Organizer | `skill-brain-organizer.md` |
| `/ingest [fonte]` | Ingest Knowledge | `skill-ingest.md` |
| `/query [pergunta]` | Query Brain | `skill-query.md` |
| `/adr` | Write ADR | `skill-adr.md` |
| `/lint` | Lint Brain | `skill-lint.md` |
| `/review-exame` | Review Exame | `skill-review-exame.md` |

---

### §3 — Session Pipeline (Fluxo Obrigatório de Programação)

Toda sessão de codificação segue este pipeline:

```
/boot → [trabalho com recorder ativo] → /arch-review → [código] → /capture → /close (organiza + commit + push)
```

> ⚠️ O `/close` é o passo final. Ele consolida a sessão, roda o organizador, apresenta
> um resumo e PERGUNTA se você deseja commitar. Após a confirmação, faz
> `git add . → git commit → git push` no Tila_Brain. O programador NÃO precisa commitar
> manualmente.

**Durante toda a interação**, o agente opera como Session Recorder (`skill-session-recorder.md`):
- Registra ideias, features discutidas, alterações de código, bugs, decisões e refatorações
- Cria drafts na `Tila_Brain/01-Negocio/inbox/` para ideias novas
- Atualiza a timeline no arquivo de sessão ativo em `Tila_Brain/07-Raw/sessions/`
- Classifica cada evento com a taxonomia de emojis definida na skill

**O recorder é automático** — não depende de comando do programador. Ele roda em background.

---

### §4 — Governança de Código (Antes de Qualquer Alteração)

Antes de sugerir ou implementar QUALQUER alteração em código existente dos repositórios TILA:

1. **Blast Radius** (`skill-graphify-query.md`): Verificar dependentes da classe/arquivo alvo.
   - Se Graphify CLI estiver instalado: usar `graphify query` ou `graphify path`
   - Se não estiver instalado: ler os arquivos manualmente para mapear dependentes
   - NUNCA sugerir alteração sem reportar: "Modifying [X] affects: [lista]. Proceed?"

2. **Dev Assistant** (`skill-dev-assistant.md`): Aplicar checklists de código:
   - **Backend**: `ResponseEntity<GenericResult<T>>`, constructor injection, `@Transactional`, Java records para DTOs
   - **Frontend**: Angular Standalone, Signals, `inject()`, CSS vanilla, `withCredentials: true`
   - **Segurança**: Sem secrets em código, LGPD compliance, dados sintéticos apenas

3. **ADR Check**: Se a mudança contradiz algum ADR em `Tila_Brain/02-Arquitetura_ADRs/`, ALERTAR antes de prosseguir.

> 🚨 Em uma aplicação médica, uma dependência quebrada não é apenas um bug — é um risco à
> segurança do paciente. O blast radius é OBRIGATÓRIO, não opcional.

---

### §5 — Knowledge Quality (Gate de Qualidade)

Ao criar ou promover conhecimento no cérebro:

- **NUNCA** escrever diretamente em `01-Negocio/permanent/` — sempre passar pelo Gate de Validação (`skill-gate-validacao.md`) com as 6 perguntas obrigatórias
- **NUNCA** modificar arquivos em `07-Raw/` — são fontes imutáveis
- **NUNCA** inventar fatos médicos — marcar como "⚠️ Não verificado — fonte necessária"
- **NUNCA** expor dados reais de pacientes — usar apenas dados sintéticos
- **SEMPRE** atualizar `index.md` e `log.md` após qualquer alteração no cérebro

---

### §6 — Paths do Projeto (Referência Rápida)

| Recurso | Path |
|---|---|
| Brain Root | `c:\Tila\Tila_Brain` |
| CLAUDE.md | `c:\Tila\Tila_Brain\CLAUDE.md` |
| SOUL.md | `c:\Tila\Tila_Brain\00-Index\SOUL.md` |
| Skills | `c:\Tila\Tila_Brain\05-Skills_Agentes\` |
| Guia de Skills | `c:\Tila\Tila_Brain\00-Index\GuiaSkillsCerebro.md` |
| Sessions | `c:\Tila\Tila_Brain\07-Raw\sessions\` |
| Backend | `c:\Tila\Tila_BackEnd` |
| Frontend | `c:\Tila\Tila_Frontend` |

---

### §7 — Comportamento Geral

- **Idioma**: O agente deve se comunicar em **Português do Brasil** quando interagindo sobre o cérebro e o projeto TILA, exceto em código-fonte e comentários técnicos que podem ser em inglês.
- **Precisão sobre velocidade**: Preferir ser preciso a ser rápido. Em caso de dúvida, consultar o cérebro antes de responder.
- **Transparência**: Se o agente não encontrar um arquivo esperado ou se um dado estiver inconsistente, ele DEVE reportar claramente ao programador em vez de inventar.
- **Continuidade**: Toda sessão deve terminar com `/close`. Se o programador encerrar sem fechar, alertar: "⚠️ A sessão não foi fechada. Use /close para registrar o que fizemos."
