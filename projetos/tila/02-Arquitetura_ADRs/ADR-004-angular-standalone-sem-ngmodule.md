---
title: "ADR-004: Angular standalone components removem overhead de NgModule no TILA"
type: decision
date: 2026-05-07
status: Accepted
---

# ADR-004: Angular standalone components removem overhead de NgModule no TILA

## Context
Angular 14+ suporta standalone components sem NgModule. O TILA é um projeto novo sem legado de modules.

## Decision
Usar exclusivamente standalone components. Nenhum NgModule no projeto.

## Alternatives considered
1. **NgModule-based** — padrão legado, overhead de declarações/imports
2. **Standalone** — mais simples, tree-shakeable, padrão Angular 19

## Consequences
- ✅ Imports declarados diretamente no @Component
- ✅ loadComponent() para lazy loading (mais simples que loadChildren)
- ✅ 100% dos 15 componentes são standalone (verificado 2026-06-09)
- ✅ AppConfig usa `provideRouter()` em vez de `RouterModule.forRoot()`

## Backlinks
- [[codebase/patterns/padrão-componente-standalone]]
