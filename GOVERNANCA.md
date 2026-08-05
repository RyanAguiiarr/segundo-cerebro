# GOVERNANCA.md — Escada de Autonomia e Protocolos de Operação do Agente

> **Documento Oficial de Governança e Autonomia**
> Define as fronteiras de atuação do agente IA, níveis de permissão e regras de convivência para manter a integridade do Segundo Cérebro.

---

## 1. Escada de Autonomia (Ler → Recomendar → Agir)

O agente opera sob uma escada estrita de autonomia dividida em 3 níveis:

```
[ NÍVEL 1: LER ] ──────────► [ NÍVEL 2: RECOMENDAR ] ──────────► [ NÍVEL 3: AGIR ]
Totalmente Autônomo           Propositivo / Orientador          Exige Confirmação Explícita
```

### Nível 1: Ler (100% Autônomo — Sem consulta necessária)
- Leitura e indexação de notas do cofre.
- Busca semântica e léxica.
- Auditoria de integridade (links quebrados, frescor OKM, detecção de segredos).
- Cálculo de métricas e sínteses de leitura em memória.

### Nível 2: Recomendar (Propositivo — Apresenta opções ao usuário)
- Sugestão de criação de novas notas atômicas em `wiki/`.
- Proposta de links relacionais e inserção de relações tipadas (`relations:`).
- Indicação de reconciliação de contradições detectadas.
- Sugestão de promoção de aprendizados recorrentes a regras formais.

### Nível 3: Agir (Requer Aprovação Explícita — NUNCA executa sozinho)
- **Deleção ou Arquivamento:** Qualquer movimentação para `arquivo/` ou exclusão física.
- **Movimentação em Massa:** Alteração de local de múltiplos arquivos simultaneamente.
- **Mudança Estrutural:** Criação de novas pastas de 1º nível ou inclusão de novos tipos de nota em `wiki/`.
- **Fusão de Entidades:** Unificação de duas notas existentes em uma única.

---

## 2. Marcadores Sentinela (`@generated` / `@user`)

Para notas que misturam conteúdo gerado automaticamente pelo agente e edições manuais do usuário (ex: MOCs, notas diárias, dashboards de projetos):

1. **`@generated` (Bloco de Propriedade do Agente):**
   - O agente pode atualizar, reordenar ou sobrescrever estas seções durante rotinas automáticas (ex: lista `notas_principais` em MOCs ou resumos noturnos).
2. **`@user` (Bloco de Propriedade Exclusiva do Usuário):**
   - **INTOCÁVEL.** O agente **NUNCA** altera, move ou sobrescreve texto dentro ou após um marcador `@user`.

### Exemplo de Aplicação:
```markdown
<!-- @generated:inicio -->
## Notas Principais da Área (Atualizado pelo Agente)
- [[wiki/concepts/conceito-a]]
<!-- @generated:fim -->

<!-- @user:inicio -->
## Anotações Pessoais e Reflexões (Intocável pelo Agente)
- Minhas ideias manuais e observações sem interferência da IA.
<!-- @user:fim -->
```

---

## 3. Matriz de Operações: Automáticas vs. Validação Humana

| Operação | Nível de Autonomia | Mecanismo de Controle |
|---|---|---|
| Lint de frescor OKM (`freshness_lint.py`) | 100% Automático | Executado no `/obsidian-health` e rotinas noturnas. |
| Reconstrução de `index.md` e `log.md` | 100% Automático | Executado pelo Agente da Noite. |
| Reconciliação de contradições óbvias (links) | 100% Automático | Executado via `/obsidian-reconcile`. |
| Injeção de Contexto (Recall Bounded) | 100% Automático | Injeta brief curto (máx 4 notas) se houver alta confiança. |
| Criação de notas atômicas convencionais | Requer Confirmação | Agente propõe e confirma com usuário durante a conversa. |
| Arquivamento de notas (mover para `arquivo/`) | Requer Confirmação | Agente solicita confirmação explicitando o motivo. |
| Criação de novas pastas de 1º nível | Requer Confirmação | **BLOQUEIO ABSOLUTO.** Agente deve perguntar antes. |
| Exclusão física definitiva de notas | Requer Confirmação | Confirmação explícita nota por nota (nunca em lote). |
