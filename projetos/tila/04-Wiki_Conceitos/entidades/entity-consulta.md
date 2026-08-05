---
title: "Entity: Consulta"
type: entity
tags: [backend, jpa, entity, placeholder]
sources: [raw/codebase/snapshots/backend-structure.md]
last_updated: 2026-05-07
---

# Entity: Consulta

## Status: 🔲 PLACEHOLDER VAZIO

A entidade Consulta existe no código como um arquivo vazio (classe sem campos ou annotations). O repository `ConsultaRepository` também é um interface vazia (sem extends JpaRepository).

## Table
Nenhuma tabela — entity não tem `@Entity` ou `@Table`

## Fields
Nenhum campo definido.

## Enums Relacionados
- `StatusConsulta`: enum vazio (sem valores)
- `TipoConsulta`: enum vazio (sem valores)
- `ConsultaDTO`: record vazio

## Observations
- ⚠️ **Completamente vazio** — apenas scaffolding
- ⚠️ O frontend tem `AgendaComponent` que espera dados de consulta
- ⚠️ `agenda-api.service.ts` define interfaces (Appointment, WaitPatient, AgendaStats) mas o backend não tem endpoints correspondentes
- ⚠️ Frontend funciona com dados mockados localmente

## Próximos Passos
1. Definir campos da entidade (data, hora, tipo, paciente, medico, status)
2. Popular enums StatusConsulta e TipoConsulta
3. Criar ConsultaService e ConsultaController
4. Conectar com AgendaComponent no frontend

## Backlinks
- [[wiki/concepts/data-model]]
