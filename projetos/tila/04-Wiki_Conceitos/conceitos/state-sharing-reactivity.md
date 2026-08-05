---
title: "Compartilhamento de Estado e Reatividade no Angular"
type: concept
tags: [frontend, angular, state-management, signals, caching]
sources: []
last_updated: 2026-06-04
---

# Compartilhamento de Estado e Reatividade no Angular

Este documento detalha o padrão arquitetural recomendado para o compartilhamento de estado entre diferentes rotas (telas) na aplicação Tila Frontend, visando performance, resiliência (resistência a F5/atualizações de página) e boas práticas de engenharia de software.

## O Problema Arquitetural Comum

Em fluxos médicos (como selecionar um paciente na lista de prontuários e navegar para a tela de geração de laudo), a tela de destino necessita dos dados completos do paciente ativo. Existem três abordagens tradicionais, cada uma com seus prós e contras:

1. **Apenas via Parâmetro de Rota (`/laudo/:id`) + API:** A tela de destino sempre faz um `GET /pacientes/:id`.
   * *Prós:* Resiliente (se o usuário der F5, o sistema busca os dados novamente).
   * *Contras:* Perfomance reduzida devido a chamadas HTTP redundantes para dados já carregados anteriormente.
2. **Apenas em Memória (Serviço Singleton ou Store):** O componente de origem salva os dados em um serviço e a página de destino consome dele.
   * *Prós:* Instantâneo (zero chamadas de rede adicionais).
   * *Contras:* Frágil. Se o usuário recarregar a página (F5) ou acessar a URL diretamente por um link compartilhado, o estado em memória é zerado e a aplicação quebra.
3. **Passagem de Estado via Router (History State):** Passar o objeto no `Router.navigate(..., { state: { ... } })`.
   * *Prós:* Rápido de programar.
   * *Contras:* Não sobrevive a recarregamentos (F5) e dificulta testes automatizados.

---

## O Padrão Híbrido: Rota + Cache Store Reativo

O padrão ideal para a arquitetura do Tila é o **Padrão Híbrido**, que combina o identificador exclusivo do recurso na URL (resiliência ao F5) com um **Store Service reativo (usando Angular Signals)** que gerencia um cache em memória (performance máxima).

```
[Navegação: /pacientes -> /laudo/42]
   │
   ├──> Componente lê ID (42) da Rota
   │
   └──> Componente pede ao PacienteStore.getPaciente(42)
           │
           ├── [Existe cache para ID 42?] ─── Sim ──> Retorna instantâneo (0 HTTP)
           │
           └── [Cache vazio ou ID diferente?] ─ Não ─> Busca na API, salva no cache e retorna
```

---

## Implementação Prática

### 1. O Store Service (`paciente.store.ts`)
Este serviço funciona como o cérebro do estado de pacientes no Frontend. Ele expõe sinais de somente leitura (`computed` ou `.asReadonly()`) e gerencia o ciclo de cache.

```typescript
import { Injectable, signal, inject } from '@angular/core';
import { PacienteApiService, Paciente } from '../api/pacienteApi/paciente-api.service';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PacienteStore {
  private pacienteApi = inject(PacienteApiService);

  // Sinais privados de escrita
  private _currentPaciente = signal<Paciente | null>(null);
  private _loading = signal<boolean>(false);

  // Sinais públicos de somente leitura
  public readonly currentPaciente = this._currentPaciente.asReadonly();
  public readonly loading = this._loading.asReadonly();

  /**
   * Obtém os dados do paciente. Se os dados já estiverem em cache para
   * este ID, retorna-os imediatamente sem bater na rede.
   */
  async getPaciente(id: number): Promise<Paciente | null> {
    const cached = this._currentPaciente();
    
    // Hit de Cache
    if (cached && cached.id === id) {
      return cached;
    }

    // Miss de Cache (Busca na API)
    this._loading.set(true);
    try {
      const response = await firstValueFrom(this.pacienteApi.buscarPacientePorId(id));
      if (response && response.data) {
        this._currentPaciente.set(response.data);
        return response.data;
      }
      return null;
    } catch (error) {
      console.error('Erro ao carregar paciente para o cache do Store:', error);
      this._currentPaciente.set(null);
      throw error;
    } finally {
      this._loading.set(false);
    }
  }

  /**
   * Limpa o cache. Recomendado no Logout do sistema.
   */
  clearCache() {
    this._currentPaciente.set(null);
  }
}
```

### 2. Acesso na Rota de Destino (`laudo-ia.component.ts`)
No componente de destino, podemos utilizar os **Component Input Bindings** do Angular (introduzido na v16) para obter automaticamente o parâmetro `:id` da rota como um input reativo:

```typescript
import { Component, OnInit, inject, input } from '@angular/core';
import { PacienteStore } from '../../core/services/store/paciente.store';

@Component({
  selector: 'app-laudo-ia',
  templateUrl: './laudo-ia.component.html'
})
export class LaudoIaComponent implements OnInit {
  // Mapeia diretamente o parâmetro `:id` definido no app.routes.ts
  id = input.required<string>(); 
  
  private pacienteStore = inject(PacienteStore);

  // Expõe os sinais reativos para o HTML
  paciente = this.pacienteStore.currentPaciente;
  loading = this.pacienteStore.loading;

  async ngOnInit() {
    const numericId = Number(this.id());
    if (!isNaN(numericId)) {
      try {
        // Solicita o paciente. Irá carregar do cache instantaneamente 
        // ou fará o fetch caso a página tenha sido atualizada com F5.
        await this.pacienteStore.getPaciente(numericId);
      } catch (err) {
        console.error('Falha ao inicializar dados do paciente:', err);
      }
    }
  }
}
```

---

## Benefícios da Arquitetura

1. **UX Fluida e Instantânea:** Ao transitar entre prontuário e laudo, os dados aparecem em tela instantaneamente (tempo de carregamento de 0ms).
2. **Resiliência a Compartilhamento e Refresh:** URLs permanecem "bookmarkables" (favoritáveis) e funcionais em qualquer circunstância.
3. **Testabilidade:** A lógica do estado está desacoplada dos componentes e pode ser testada isoladamente por meio do `PacienteStore`.

## Backlinks
- [[wiki/concepts/angular-patterns]]
- [[wiki/concepts/frontend-architecture]]
