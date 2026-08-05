---
name: skill-review-exame
trigger: "review exame" / "revisar exame" / "/review-exame"
description: "Revisa um registro de exame no sistema TILA verificando completude, conformidade LGPD e consistência."
---

# Skill: Review Exame

## Context
Quando um novo exame é registrado no sistema TILA ou quando um exame existente precisa ser auditado. Esta skill verifica a completude dos campos, conformidade com LGPD, e consistência dos dados.

## Steps

### 1. Verificação de Campos Obrigatórios
Checar se todos os campos da entidade Exame estão preenchidos:
- [ ] `tipoExame` — não nulo, valor válido do enum `TipoExame`
- [ ] `dataExame` — não nulo, data válida (não futura)
- [ ] `statusExame` — não nulo, valor válido do enum `StatusExame`
- [ ] `urlImagem` — presente se status ≥ `REALIZADO`
- [ ] `descricao` — presente e não vazia
- [ ] `paciente` — referência válida (ID existente)
- [ ] `medico` — referência válida (ID existente, role = ROLE_MEDICO)

### 2. Verificação LGPD
- [ ] Campo `paciente` referencia por ID, não por CPF bruto
- [ ] Nenhum campo contém CPF, RG, ou nome completo em texto livre
- [ ] Se `descricao` contém notas clínicas, verificar se são anonimizadas
- [ ] `urlImagem` aponta para storage seguro (não URL pública sem auth)

### 3. Verificação de Status
- [ ] Se `statusExame` = `AGENDADO`: `urlImagem` deve ser null
- [ ] Se `statusExame` = `REALIZADO`: `urlImagem` deve estar preenchido
- [ ] Se `statusExame` = `LAUDADO`: deve existir um laudo associado
- [ ] Se `statusExame` = `CANCELADO`: verificar se motivo de cancelamento está documentado

### 4. Verificação de Consistência
- [ ] `dataExame` é posterior à data de cadastro do paciente
- [ ] `medico` tem especialidade compatível com `tipoExame`
- [ ] Se existe laudo associado, verificar se `medico` do laudo = `medico` do exame

## Output format
```markdown
## Review do Exame: [ID / Tipo]

### Status: ✅ Aprovado | ⚠️ Issues encontradas | ❌ Crítico

### Checklist de Campos
| Campo | Status | Observação |
|---|---|---|
| tipoExame | ✅/❌ | ... |
| dataExame | ✅/❌ | ... |
| ... | ... | ... |

### LGPD Compliance
| Check | Status | Detalhes |
|---|---|---|
| CPF exposto | ✅/❌ | ... |
| ... | ... | ... |

### Consistência
| Check | Status | Detalhes |
|---|---|---|
| ... | ... | ... |

### Ações Recomendadas
1. [Ação necessária]
2. [Ação necessária]
```

## Rules
- Se encontrar CPF ou dados de paciente expostos, classificar como **CRÍTICO** e exigir correção imediata.
- NUNCA exibir dados reais do paciente no output da review.
- Se o status do exame é inconsistente, sugerir a correção específica.
- Referenciar `context/security-lgpd.md` para requisitos de compliance.
- Referenciar `wiki/concepts/api-endpoints.md` para validar que o endpoint de exame aplica as validações corretas.
