---
title: "Serviços TILA usam injeção por construtor — @Autowired em campo é proibido"
type: pattern
domain: backend
tags: [di, spring, service]
verified_in: [AutenticacaoService.java, PacienteService.java, LaudoService.java, LogAuditoriaService.java, SecurityConfigurations.java, SecurityFilter.java, PacienteController.java, LaudoController.java, LogAuditoriaController.java]
violations_found: [AutenticacaoController.java]
last_updated: 2026-06-09
---

# Serviços TILA usam injeção por construtor — @Autowired em campo é proibido

## O padrão

Todos os services e controllers devem usar injeção de dependência via construtor.
Nunca usar `@Autowired` em campo (field injection).

## Exemplo real (verificado)

```java
// ✅ CORRETO — PacienteService
@Service
public class PacienteService {
    private final PacienteRepository pacienteRepository;
    private final LogAuditoriaRepository logAuditoriaRepository;

    public PacienteService(PacienteRepository pacienteRepository, LogAuditoriaRepository logAuditoriaRepository) {
        this.pacienteRepository = pacienteRepository;
        this.logAuditoriaRepository = logAuditoriaRepository;
    }
}
```

## Conformidade: ~95%

Quase todos os services e controllers usam construtor injection corretamente.

## Violação encontrada

`AutenticacaoController.java` — importa `@Autowired` (linha 5) mas NÃO a usa (construtor injection está correto). O import é residual e deve ser removido.

No `PacienteController.java` — também importa `@Autowired` mas usa construtor. Import residual.

## Backlinks
- [[codebase/snapshots/backend-audit-2026-06-09]]
