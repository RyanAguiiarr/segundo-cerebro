# ADR-019: Camada de Visualização e Explicabilidade para Laudos Médicos

- **Status:** Aceito (Implementado)
- **Data:** 2026-08-03
- **Decisores:** Ryan, Agente Claude (Fable)
- **Contexto:** Fable Method — Plan-first analysis

## Contexto e Problema

O microsserviço `tila-ai-cloud-service` já está consolidado com um pipeline de 7 estágios que gera laudos médicos estruturados com alta qualidade clínica. No entanto, a experiência do usuário é puramente textual — não há visualização dos achados sobre a imagem radiográfica.

### Necessidade Identificada

Ryan solicitou uma camada de apresentação que:
1. **Destaque visualmente** os achados identificados pela IA diretamente sobre a radiografia
2. **Explique visualmente** por que o sistema chegou àquela conclusão
3. **Vincule bidireccionalmente** o texto do laudo com regiões da imagem (clique no texto → destaca região; clique na região → scroll ao texto)
4. **Mantenha total desacoplamento** da lógica de análise clínica existente

### Restrições Absolutas

1. **Nenhuma alteração na lógica de decisão clínica** (Estágios 0-6 do pipeline Python)
2. **Nenhuma mudança em cálculos de confiança, criticidade ou reconciliação**
3. **Campo `visualizacoes` sempre opcional/nullable** em todas as camadas
4. **Se a serialização de evidências falhar, o laudo principal continua sendo entregue normalmente**

## Evidências Coletadas

### 1. Dados Espaciais Já Disponíveis no Pipeline

Durante a execução do pipeline, os seguintes dados espaciais **já existem em memória** mas não são transmitidos ao frontend:

| Estágio | Artefato Espacial | Formato Atual | Localização no Código |
|---------|-------------------|---------------|----------------------|
| **2.5 (PSPNet)** | Máscaras de pulmão direito/esquerdo/coração | `np.ndarray` (512×512) binário | `stage2_5_segmentation.py:246-248` |
| **2.5 (ICT)** | Largura cardíaca/torácica em pixels | `int`, `int` | `stage2_5_segmentation.py:180-213` |
| **3 (Gemini)** | Concordância por patologia com justificativa textual | `CloudVisionConcordancia` (texto) | `stage3_cloud_vision.py`, `schemas/contracts.py:143-158` |
| **4 (Reconciliação)** | Status final por achado (PRESENTE/INDETERMINADO/AUSENTE) | `ReconciledFinding.status_achado` | `stage4_reconciliation.py`, `schemas/contracts.py:194-226` |

**Surpresa identificada (Step 2, rule 7):** O Gemini no Estágio 3 **não retorna coordenadas espaciais** atualmente — apenas concordância textual. Isso significa que precisamos **estender o prompt do Gemini** para solicitar bounding boxes quando ele identificar achados visuais.

### 2. Arquitetura Frontend Atual

**Confirmado via evidências:**
- ✅ Angular 19 com **Standalone Components** (`laudo-ia.component.ts:10` — `standalone: true`)
- ✅ **Angular Signals** para gerenciamento de estado (`auth.store.ts:1` — `signal, computed, inject`)
- ✅ **Design System estabelecido** com tokens CSS (`styles.css:1-80` — `:root` com variáveis `--primary`, `--surface`, etc.)
- ✅ **Padrão de Stores** já implementado (`auth.store.ts`, `paciente.store.ts`, `medical.store.ts`)

**Componente alvo:** `laudo-ia.component.ts` atualmente possui dados mockados (`draftData`, `confidenceScore`) — será substituído por integração real com a nova API.

### 3. Contrato Atual da API (Java DTO)

**Arquivo analisado:** `Tila_BackEnd/tila/src/main/java/tecnologi/tila/tila/ai/dto/PythonAIResponseDTO.java`

**Problema identificado:** O DTO Java **não está sincronizado** com o DTO Python atual do `stage6_integration.py`. O Java possui campos legacy (`secaoIndicacao`, `secaoAnalise`) que não existem mais no Python (que usa `etapa_0_ingestao`, `etapa_1_preparacao`, etc.).

**INTENT:** O DTO Java precisa ser reescrito para refletir a estrutura de 7 estágios do Python antes de adicionar o campo `visualizacoes`. Isso é um **pré-requisito crítico** para esta ADR.

## Decisão Arquitetural

### Contrato Universal: `EvidenciaVisual`

```typescript
interface EvidenciaVisual {
  id: string;                    // Ex: "evidencia_pneumothorax_001"
  achado_relacionado: string;    // Texto do achado no laudo (vínculo bidirecional)
  tipo: "bbox" | "mascara_poligono" | "ponto";
  status: "PRESENTE" | "INDETERMINADO" | "AUSENTE";  // Do Estágio 4
  fonte: string;                 // Ex: "pspnet_stage2_5", "gemini_stage3"
  confianca: number;             // 0.0-1.0
  
  // Dados geométricos (apenas o campo relevante preenchido):
  bbox?: [number, number, number, number];      // [y0, x0, y1, x1] normalizado 0-1000
  poligono?: [number, number][];                // Pontos [x,y] normalizados 0-1000
  ponto?: [number, number];                     // [x, y] normalizado 0-1000 (fallback)
}
```

**Normalização 0-1000:** Todos os dados espaciais são normalizados para um espaço de coordenadas 1000×1000, independente do tamanho original da imagem. Isso permite que o frontend renderize com `<svg viewBox="0 0 1000 1000">` que escala automaticamente para qualquer resolução de tela.

### Arquitetura de 3 Camadas (Python → Java → Angular)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PYTHON (tila-ai-cloud-service)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │ Stage 2  │──▶│Stage 2.5 │──▶│ Stage 3  │──▶│ Stage 4  │        │
│  │  (TXRV)  │   │ (PSPNet) │   │ (Gemini) │   │(Reconcil)│        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│                       │              │              │               │
│                       │ máscaras     │ bbox?        │ status        │
│                       │ NumPy        │              │               │
│                       ▼              ▼              ▼               │
│                  ┌────────────────────────────────────┐             │
│                  │   Stage 6.5 (NOVO)                │             │
│                  │   evidence_serialization.py       │             │
│                  │                                    │             │
│                  │  • cv2.findContours(máscaras)     │             │
│                  │  • cv2.approxPolyDP (simplifica)  │             │
│                  │  • Normaliza 0-1000               │             │
│                  │  • Monta lista[EvidenciaVisual]   │             │
│                  └────────────────────────────────────┘             │
│                                │                                    │
│                                ▼                                    │
│                  ┌────────────────────────────────────┐             │
│                  │  PythonAIResponseDTO               │             │
│                  │  + visualizacoes: Optional[list]   │             │
│                  └────────────────────────────────────┘             │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ HTTP POST
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      JAVA (Tila_BackEnd)                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────┐                             │
│  │ PythonAIResponseDTO.java (record)  │                             │
│  │ + visualizacoes: List<EvidenciaVisualDTO>  (nullable)           │
│  └────────────────────────────────────┘                             │
│                    │                                                │
│                    │ ResponseEntity<GenericResult<T>>               │
│                    ▼                                                │
│  ┌────────────────────────────────────┐                             │
│  │ Controller → Service → DTO         │                             │
│  │ (Sem mudança de lógica)            │                             │
│  └────────────────────────────────────┘                             │
└───────────────────────────────┬──────────────────────────────────────┘
                                │ HTTP GET (JSON)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   ANGULAR (Tila_Frontend)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────────────┐                             │
│  │ EvidenciaSelecaoService (Signal)   │  ← Estado compartilhado     │
│  │  achadoSelecionadoId = signal<string│null>(null)                │
│  └────────────────────────────────────┘                             │
│          ▲                           ▲                              │
│          │                           │                              │
│  ┌───────┴──────────┐       ┌────────┴─────────┐                   │
│  │ Painel Achados   │◀─────▶│ Overlay SVG      │                   │
│  │ (texto clicável) │       │ (imagem + marcas)│                   │
│  └──────────────────┘       └──────────────────┘                   │
│          │                           │                              │
│          └───────────┬───────────────┘                              │
│                      │ Vínculo Bidirecional                         │
│                      ▼                                              │
│         Clique no texto → Destaca região SVG                        │
│         Clique na região SVG → Scroll até texto                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Mapeamento de Tipos de Evidência

| Origem | Tipo de Evidência | Justificativa |
|--------|-------------------|---------------|
| **PSPNet (Máscaras)** | `mascara_poligono` | Máscaras binárias 512×512 convertidas para contornos vetoriais com ~30-60 vértices via `cv2.findContours` + `cv2.approxPolyDP`. Muito mais leve que Base64 de imagem (~2KB vs ~100KB). |
| **Gemini (Achados focais)** | `bbox` | Extensão do prompt para solicitar `[y0, x0, y1, x1]` normalizado quando identificar achado focal (pneumotórax, nódulo, massa). |
| **Achados sem geometria** | `ponto` | Fallback para achados que têm apenas localização textual ("base pulmonar esquerda") sem coordenadas precisas. |

## Plano de Implementação Incremental (8 Etapas)

Cada etapa é **testável isoladamente** e **não quebra o funcionamento existente**.

### Etapa 1: Corrigir sincronização Python ↔ Java DTO (Pré-requisito)

**Objetivo:** Antes de adicionar `visualizacoes`, alinhar o `PythonAIResponseDTO.java` com a estrutura real de 7 estágios do Python.

**Arquivos alterados:**
- `Tila_BackEnd/tila/src/main/java/tecnologi/tila/tila/ai/dto/PythonAIResponseDTO.java`
- Possivelmente criar novos DTOs: `Etapa0IngestaoDTO`, `Etapa1PreparacaoDTO`, etc.

**Verificação:** Backend consome resposta do Python sem erros de deserialização.

### Etapa 2: Estender PSPNet para retornar máscaras NumPy no DTO Python

**Objetivo:** `SegmentacaoResult` passa a incluir as máscaras reais, não apenas booleanos.

**Arquivos alterados:**
- `tila-ai-cloud-service/schemas/contracts.py` (adicionar campos `Optional[list]` serializados via `.tolist()`)
- `tila-ai-cloud-service/pipeline/stage2_5_segmentation.py` (retornar as máscaras no objeto)

**Verificação:** Pipeline continua funcionando; máscaras aparecem no log mas ainda não são usadas.

### Etapa 3: Estender prompt do Gemini para retornar bounding boxes

**Objetivo:** Modificar `CloudVisionConcordancia` para incluir campo opcional `bbox`.

**Arquivos alterados:**
- `tila-ai-cloud-service/schemas/contracts.py` (adicionar `bbox: Optional[list[int]]` em `CloudVisionConcordancia`)
- `tila-ai-cloud-service/app/cloud_llm_client.py` ou prompts (incluir instrução: "se o achado for visualmente delimitável, forneça bounding box [y0,x0,y1,x1] normalizado 0-1000")

**Verificação:** Gemini retorna bboxes; decisão clínica (tri-state `concorda`) permanece inalterada.

### Etapa 4: Criar Estágio 6.5 (Serialização de Evidências)

**Objetivo:** Novo módulo que **apenas empacota** dados espaciais após todas as decisões clínicas.

**Arquivos criados:**
- `tila-ai-cloud-service/pipeline/stage6_5_evidence_serialization.py`

**Funções principais:**
```python
def serializar_evidencias(
    resultado_reconciliacao: dict,
    mascara_pulmao_d: Optional[np.ndarray],
    mascara_pulmao_e: Optional[np.ndarray],
    mascara_coracao: Optional[np.ndarray],
    achados_gemini_com_bbox: list,
    dimensoes_imagem: tuple,
) -> list[dict]:
    """Retorna lista de EvidenciaVisual."""
    evidencias = []
    
    # Converter máscaras PSPNet para polígonos
    if mascara_coracao is not None:
        poligono = _mascara_para_poligono_normalizado(mascara_coracao, dimensoes_imagem)
        evidencias.append({
            "id": "evidencia_coracao",
            "achado_relacionado": "Silhueta cardíaca / ICT",
            "tipo": "mascara_poligono",
            "status": resultado_reconciliacao.get("Cardiomegaly", {}).get("status", "AUSENTE"),
            "fonte": "pspnet_stage2_5",
            "confianca": resultado_reconciliacao.get("Cardiomegaly", {}).get("confianca", 0.0),
            "poligono": poligono,
        })
    
    # Adicionar bboxes do Gemini
    for achado in achados_gemini_com_bbox:
        if achado.get("bbox"):
            evidencias.append({
                "id": f"evidencia_{achado['patologia'].lower()}",
                "achado_relacionado": achado["patologia"],
                "tipo": "bbox",
                "status": resultado_reconciliacao.get(achado["patologia"], {}).get("status", "INDETERMINADO"),
                "fonte": "gemini_stage3",
                "confianca": achado.get("confianca", 0.5),
                "bbox": achado["bbox"],
            })
    
    return evidencias

def _mascara_para_poligono_normalizado(mascara: np.ndarray, dimensoes: tuple) -> list[list[float]]:
    """cv2.findContours + approxPolyDP para contorno leve."""
    contornos, _ = cv2.findContours(mascara.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos:
        return []
    maior_contorno = max(contornos, key=cv2.contourArea)
    epsilon = 0.005 * cv2.arcLength(maior_contorno, True)
    aproximado = cv2.approxPolyDP(maior_contorno, epsilon, True)
    h, w = dimensoes
    return [[round(p[0][0] / w * 1000, 1), round(p[0][1] / h * 1000, 1)] for p in aproximado]
```

**Integração em `app/main.py`:**
```python
resultado_final = stage6_integration.integrate(...)  # Existente, inalterado

# NOVO: Adicionar visualizações após todas as decisões clínicas
try:
    resultado_final["visualizacoes"] = stage6_5_evidence_serialization.serializar_evidencias(
        resultado_reconciliacao, mascara_pulmao_d, mascara_pulmao_e, mascara_coracao,
        achados_gemini, dimensoes_imagem
    )
except Exception as e:
    logger.warning(f"Stage 6.5 failed (non-fatal): {e}")
    resultado_final["visualizacoes"] = []  # Não quebra o laudo
```

**Verificação:** Pipeline retorna laudo completo + `visualizacoes` opcional.

### Etapa 5: Estender Java DTO (campo opcional `visualizacoes`)

**Arquivos alterados:**
- `Tila_BackEnd/tila/src/main/java/tecnologi/tila/tila/ai/dto/PythonAIResponseDTO.java`

```java
public record EvidenciaVisualDTO(
    String id,
    String achadoRelacionado,
    String tipo,
    String status,
    String fonte,
    Double confianca,
    @JsonProperty("bbox") List<Integer> bbox,
    @JsonProperty("poligono") List<List<Double>> poligono,
    @JsonProperty("ponto") List<Double> ponto
) {}

public record PythonAIResponseDTO(
    // ... campos existentes ...
    @JsonProperty("visualizacoes") List<EvidenciaVisualDTO> visualizacoes
) {}
```

**Verificação:** Backend deserializa JSON do Python sem erros; visualizações aparecem no endpoint REST.

### Etapa 6: Angular — Service de Estado Compartilhado

**Arquivo criado:**
- `Tila_Frontend/src/app/core/services/evidencia-selecao.service.ts`

```typescript
import { Injectable, signal } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class EvidenciaSelecaoService {
  achadoSelecionadoId = signal<string | null>(null);
  modoExibicao = signal<'apenas-confirmados' | 'todos' | 'apenas-indeterminados'>('apenas-confirmados');

  selecionar(id: string | null): void {
    this.achadoSelecionadoId.set(id);
  }
}
```

**Verificação:** Service injetável; nenhuma UI ainda.

### Etapa 7: Angular — Componente de Overlay SVG

**Arquivo criado:**
- `Tila_Frontend/src/app/components/visualizador-achados/visualizador-achados.component.ts`

```typescript
@Component({
  selector: 'app-visualizador-achados',
  standalone: true,
  template: `
    <div class="visualizador-container">
      <img [src]="imagemUrl()" class="imagem-base" alt="Radiografia" />
      <svg class="overlay" viewBox="0 0 1000 1000" preserveAspectRatio="none">
        @for (ev of evidenciasVisiveis(); track ev.id) {
          @switch (ev.tipo) {
            @case ('bbox') {
              <rect
                [attr.x]="ev.bbox[1]" [attr.y]="ev.bbox[0]"
                [attr.width]="ev.bbox[3] - ev.bbox[1]"
                [attr.height]="ev.bbox[2] - ev.bbox[0]"
                [class]="'evidencia bbox status-' + ev.status.toLowerCase()"
                [class.selecionado]="ev.id === selecaoService.achadoSelecionadoId()"
                (click)="selecaoService.selecionar(ev.id)" />
            }
            @case ('mascara_poligono') {
              <polygon
                [attr.points]="formatarPontos(ev.poligono)"
                [class]="'evidencia poligono status-' + ev.status.toLowerCase()"
                [class.selecionado]="ev.id === selecaoService.achadoSelecionadoId()"
                (click)="selecaoService.selecionar(ev.id)" />
            }
            @case ('ponto') {
              <circle
                [attr.cx]="ev.ponto[0]" [attr.cy]="ev.ponto[1]" r="15"
                [class]="'evidencia ponto status-' + ev.status.toLowerCase()"
                (click)="selecaoService.selecionar(ev.id)" />
            }
          }
        }
      </svg>
    </div>
  `,
  styles: [`
    .visualizador-container {
      position: relative;
      width: 100%;
      height: 100%;
    }
    .imagem-base {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
    .overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
    }
    .evidencia {
      pointer-events: auto;
      cursor: pointer;
      fill: none;
      stroke-width: 3;
      opacity: 0.6;
      transition: opacity 0.2s, stroke-width 0.2s;
    }
    .evidencia:hover, .evidencia.selecionado {
      opacity: 1;
      stroke-width: 5;
    }
    .status-presente { stroke: var(--success-green, #0f9d58); }
    .status-indeterminado { stroke: var(--error, #ba1a1a); }
    .status-ausente { stroke: var(--outline, #849396); }
    .poligono { fill: currentColor; fill-opacity: 0.1; }
  `]
})
export class VisualizadorAchadosComponent {
  @Input() imagemUrl = signal<string>('');
  @Input() evidencias = signal<EvidenciaVisual[]>([]);
  
  selecaoService = inject(EvidenciaSelecaoService);
  
  evidenciasVisiveis = computed(() => {
    const modo = this.selecaoService.modoExibicao();
    return this.evidencias().filter(ev => {
      if (modo === 'apenas-confirmados') return ev.status === 'PRESENTE';
      if (modo === 'apenas-indeterminados') return ev.status === 'INDETERMINADO';
      return true;
    });
  });
  
  formatarPontos(poligono: [number, number][]): string {
    return poligono.map(p => `${p[0]},${p[1]}`).join(' ');
  }
}
```

**Verificação:** Componente renderiza SVG sobre imagem mocada; cliques funcionam.

### Etapa 8: Angular — Painel de Transparência e Integração Final

**Arquivo alterado:**
- `Tila_Frontend/src/app/pages/laudo-ia/laudo-ia.component.ts`
- `Tila_Frontend/src/app/pages/laudo-ia/laudo-ia.component.html`

**Adições:**
- Consumir API real (remover dados mockados)
- Incluir `<app-visualizador-achados>` na template
- Criar painel lateral com lista de achados (clicáveis, vinculados ao overlay)
- Implementar scroll automático no texto quando região é clicada

**Verificação:** Fluxo end-to-end funcional; vínculo bidirecional funcionando.

## Consequências

### Positivas

1. **Zero impacto na lógica clínica**: Decisões de diagnóstico permanecem 100% inalteradas
2. **Graceful degradation**: Se Estágio 6.5 falhar, laudo continua funcionando normalmente
3. **Extensível**: Novos tipos de evidência (heatmaps, Grad-CAM) podem ser adicionados sem refatoração
4. **Performático**: Polígonos vetoriais são ~50x mais leves que máscaras bitmap
5. **Responsivo**: SVG `viewBox` escala automaticamente para qualquer resolução
6. **Auditável**: Cada evidência rastreia sua fonte (PSPNet/Gemini/TXRV) e confiança

### Negativas / Trade-offs

1. **Complexidade adicional**: +1 estágio no pipeline, +1 componente Angular, +1 DTO
2. **Dependência do OpenCV**: `cv2.findContours` pode falhar em máscaras degeneradas (tratado com try/except)
3. **Extensão do prompt Gemini**: Pedir bbox pode aumentar latência ~5-10% (aceitável)
4. **Trabalho de sincronização DTO**: Etapa 1 é pré-requisito obrigatório antes de implementar o resto

### Riscos Mitigados

- **Risco:** Estágio 6.5 quebra pipeline → **Mitigação:** Exception handling + campo opcional
- **Risco:** Máscaras muito complexas geram polígonos imensos → **Mitigação:** `cv2.approxPolyDP` reduz vértices
- **Risco:** Gemini ignora instrução de bbox → **Mitigação:** Campo opcional; frontend renderiza sem bbox
- **Risco:** Frontend trava com muitas evidências → **Mitigação:** Modo filtro (apenas-confirmados/todos)

## Alternativas Consideradas e Descartadas

### 1. Retornar Heatmaps do TorchXRayVision (Grad-CAM)

**Descartado porque:**
- TXRV não fornece heatmaps nativamente (requer implementação Grad-CAM externa)
- Heatmaps PNG Base64 são pesados (~100-200KB cada)
- Interpretação visual é menos precisa que bounding boxes

### 2. Enviar Máscaras Bitmap Completas (Base64 PNG)

**Descartado porque:**
- 512×512 PNG Base64 = ~100KB por máscara
- 3 máscaras (pulmões + coração) = ~300KB adicionais por requisição
- Polígonos vetoriais conseguem o mesmo efeito visual com <5KB

### 3. Computar Evidências no Frontend (Client-side)

**Descartado porque:**
- Requer enviar máscaras NumPy brutas ao browser (inviável)
- Duplica lógica de normalização em TypeScript
- Viola princípio de Single Source of Truth

## Dependências e Pré-requisitos

### Tecnologias

- **Python:** OpenCV (`cv2`) já instalado como dep do PSPNet
- **Java:** Jackson para deserialização (já presente)
- **Angular:** Nenhuma lib adicional necessária (SVG nativo)

### Ordem de Implementação

**Bloqueante:** Etapa 1 (Sincronizar DTO Python ↔ Java) deve ser concluída **antes** de qualquer outra etapa.

**Dependências:**
- Etapas 2-4 (Python) podem ser feitas em paralelo
- Etapa 5 (Java DTO) depende de Etapas 2-4 estarem concluídas
- Etapas 6-8 (Angular) dependem de Etapa 5

## Critérios de Aceitação (Definition of Done)

1. ✅ Pipeline Python retorna `visualizacoes` opcional sem quebrar laudos existentes
2. ✅ Backend Java deserializa e expõe `visualizacoes` via API REST
3. ✅ Frontend Angular renderiza overlay SVG com polígonos/bboxes sobre radiografia
4. ✅ Vínculo bidirecional funciona (clique texto ↔ clique imagem)
5. ✅ Todos os testes existentes (104/104) continuam passando
6. ✅ Nenhuma mudança em cálculos de confiança/criticidade observada em teste A/B
7. ✅ Componentes Angular seguem padrão Standalone + Signals

## Revisão e Aprovação

**Aguardando aprovação de:** Ryan

**Próximos passos após aprovação:**
1. Executar Etapa 1 (Sincronizar DTOs)
2. Validar com Ryan antes de prosseguir para Etapas 2-8
3. Implementar incrementalmente conforme checklist

---

**Nota:** Este ADR segue o Fable Method (plan-first). Nenhum código foi alterado ainda — toda a análise é baseada em evidências coletadas do código existente.
