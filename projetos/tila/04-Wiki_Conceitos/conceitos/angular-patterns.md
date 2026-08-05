---
title: "Angular Patterns — TILA (Verificado)"
type: concept
tags: [frontend, angular, patterns, signals]
sources: []
last_updated: 2026-05-07
---

# Angular Patterns — TILA (Verificado)

> Padrões reais extraídos do código em 2026-05-07.

## Standalone Components
Todos os 14 componentes usam `standalone: true` com imports explícitos:
```typescript
@Component({
  selector: 'app-pacientes',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, SidebarComponent],
  templateUrl: './pacientes.component.html',
  styleUrls: ['./pacientes.component.css']
})
```

## Signal-Based State — AuthStore
O pattern principal de estado global usa Signal:
```typescript
@Injectable({ providedIn: 'root' })
export class AuthStore {
  private readonly state = signal<AuthState>({ user: null, isAuthenticated: false });
  
  readonly user = computed(() => this.state().user);
  readonly isAuthenticated = computed(() => this.state().isAuthenticated);
  
  constructor() {
    effect(() => {
      // Persiste em localStorage quando state muda
    });
  }
  
  async fetchProfile() {
    const res = await firstValueFrom(this.authApi.getMe());
    // Atualiza state
  }
}
```

## Component State — Signals vs Plain
### Pattern com Signals (recomendado)
```typescript
pacientes = signal<Paciente[]>([]);
loading = signal(false);
errorMessage = signal<string | null>(null);
filteredPacientes = computed(() => /* ... */);
```

### Pattern com Plain Properties (legado)
```typescript
email = '';
senha = '';
errorMessage = '';
showPassword = false;
```

⚠️ 43% dos componentes ainda usam plain properties.

## API Service Pattern
```typescript
@Injectable({ providedIn: 'root' })
export class XApiService {
  private http = inject(HttpClient);
  private baseUrl = 'http://localhost:8080/x';  // ⚠️ hardcoded

  metodo(): Observable<GenericResult<T>> {
    return this.http.get<GenericResult<T>>(this.baseUrl).pipe(
      tap({
        next: (res) => { if (!res.success) throw new Error(res.message); },
        error: (err) => console.error('Erro:', err)
      })
    );
  }
}
```

## DI Pattern — `inject()`
```typescript
private router = inject(Router);
private authApi = inject(AuthApiService);
private authStore = inject(AuthStore);
```
100% dos componentes usam `inject()` function.

## Guard Pattern — Functional
```typescript
export const authGuard: CanActivateFn = (route, state) => {
  const authStore = inject(AuthStore);
  const router = inject(Router);
  if (authStore.isAuthenticated()) return true;
  router.navigate(['/login']);
  return false;
};
```

## Interceptor Pattern — Functional
```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const modified = req.clone({
    withCredentials: true,
    headers: req.headers.set('Content-Type', 'application/json')
  });
  return next(modified);
};
```

## Paginação Client-Side
```typescript
currentPage = signal(0);
itemsPerPage = 10;

// Derivados
totalPages = computed(() => Math.ceil(this.items().length / this.itemsPerPage));
paginatedItems = computed(() => {
  const start = this.currentPage() * this.itemsPerPage;
  return this.items().slice(start, start + this.itemsPerPage);
});
```
⚠️ Paginação é 100% client-side — todo o dataset é carregado.

## CSS — Vanilla com Custom Properties
```css
:host { display: block; }
.container { padding: var(--spacing-md, 1rem); }
/* Inter font family definido globalmente em styles.css */
```
Sem frameworks CSS. Sem Tailwind. Sem SCSS.

## Signal-Based State — Domínio Específico (PacienteStore)
Refletindo o ADR-007, o controle de pacientes ativos entre Prontuário e Laudo IA é feito via store baseada em Signals, evitando recarregamentos desnecessários e duplicidade de requests:
```typescript
@Injectable({ providedIn: 'root' })
export class PacienteStore {
  private pacienteAtual = signal<Paciente | null>(null);

  getPacienteAtual() {
    return this.pacienteAtual.asReadonly();
  }

  setPacienteAtual(paciente: Paciente) {
    this.pacienteAtual.set(paciente);
  }

  limparPaciente() {
    this.pacienteAtual.set(null);
  }
}
```

## Interceptor Pattern — Resiliência de Sessão
Para revogar sessões globalmente em retornos 401/403:
```typescript
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const authStore = inject(AuthStore);

  // request cloning...

  return next(modifiedReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 || error.status === 403) {
        authStore.logout();
        router.navigate(['/login']);
      }
      return throwError(() => error);
    })
  );
};
```

## Backlinks
- [[context/coding-conventions]]
- [[wiki/concepts/frontend-architecture]]
- [[wiki/sources/2026-06-07-refatoracao-auth-signals]]
