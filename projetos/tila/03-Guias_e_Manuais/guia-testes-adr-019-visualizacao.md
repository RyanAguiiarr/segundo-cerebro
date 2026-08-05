# Guia de Testes - ADR-019: Camada de Visualização e Explicabilidade

**Data de Implementação:** 2026-08-01  
**Status:** Pronto para testes  
**Desenvolvedor:** Ryan

---

## 📋 Resumo Executivo

Foi implementada uma camada completa de visualização e explicabilidade para laudos médicos, permitindo que o usuário veja **onde** o sistema identificou cada achado na radiografia através de overlays visuais interativos.

**Principais Componentes:**
- **Backend Python**: Stage 6.5 que converte máscaras PSPNet → polígonos vetoriais (OpenCV)
- **Backend Java**: 17 novos DTOs alinhados à estrutura Python de 7 estágios
- **Frontend Angular**: Overlay SVG responsivo + painel de achados clicáveis

---

## ✅ Checklist de Testes

### 1. Backend Python (`tila-ai-cloud-service`)

#### 1.1 Testes Unitários
```bash
cd C:/Tila/tila-ai-cloud-service
pytest tests/ -v
```

**Verificar:**
- ✅ Todos os testes existentes (104/104) continuam passando
- ✅ Stage 6.5 não quebra pipeline quando falha (graceful degradation)
- ✅ Campo `visualizacoes` aparece no JSON de resposta

#### 1.2 Teste Manual do Stage 6.5
```bash
# Executar contra imagem de teste
python -m pytest tests/test_api.py -v -k "test_gerar_laudo"
```

**Verificar no JSON de resposta:**
```json
{
  "visualizacoes": [
    {
      "id": "evidencia_coracao",
      "achado_relacionado": "Cardiomegalia",
      "tipo": "mascara_poligono",
      "status": "PRESENTE",
      "fonte": "pspnet_stage2_5",
      "confianca": 0.85,
      "poligono": [[450, 400], [500, 380], ...]
    }
  ]
}
```

#### 1.3 Validar OpenCV
```bash
python -c "import cv2; print(cv2.__version__)"
```

**Esperado:** Versão do OpenCV sem erros (necessário para `cv2.findContours`)

---

### 2. Backend Java (`Tila_BackEnd`)

#### 2.1 Compilação
```bash
cd C:/Tila/Tila_BackEnd/tila
./mvnw clean compile
```

**Verificar:**
- ✅ Compilação sem erros
- ✅ Todos os 17 novos DTOs reconhecidos
- ✅ `PythonAIResponseDTO` deserializa JSON do Python

#### 2.2 Testar Deserialização
Criar teste unitário em `TilaAIIntegrationServiceTest.java`:
```java
@Test
void testDeserializacaoComVisualizacoes() throws Exception {
    String json = """
        {
          "billing_mode_utilizado": "paid",
          "modelo_ia_utilizado": "test",
          "etapa_0_ingestao": {...},
          ...
          "visualizacoes": [
            {
              "id": "test",
              "achadoRelacionado": "Cardiomegalia",
              "tipo": "mascara_poligono",
              "status": "PRESENTE",
              "fonte": "pspnet_stage2_5",
              "confianca": 0.85,
              "poligono": [[450, 400]]
            }
          ]
        }
    """;
    
    PythonAIResponseDTO dto = objectMapper.readValue(json, PythonAIResponseDTO.class);
    assertNotNull(dto.visualizacoes());
    assertEquals(1, dto.visualizacoes().size());
}
```

---

### 3. Frontend Angular (`Tila_Frontend`)

#### 3.1 Compilação
```bash
cd C:/Tila/Tila_Frontend
ng serve
```

**Verificar:**
- ✅ Compilação sem erros TypeScript
- ✅ Componente `VisualizadorAchadosComponent` carrega
- ✅ Service `EvidenciaSelecaoService` injetável

#### 3.2 Testes Visuais

##### Layout
- [ ] Grid 2 colunas (imagem esquerda, laudo direita) em desktop
- [ ] Grid 1 coluna em mobile (<1200px)
- [ ] Imagem ocupa 600px de altura
- [ ] Painel de achados scrollável (max 400px)

##### Overlay SVG
- [ ] Polígonos renderizam sobre a imagem
- [ ] Bounding boxes aparecem como retângulos
- [ ] Pontos aparecem como círculos
- [ ] Cores correspondem ao status:
  - Verde/Cyan (`--primary-container`): PRESENTE
  - Âmbar (`#ffa000`): INDETERMINADO
  - Cinza (`--outline-variant`): AUSENTE

##### Interatividade
- [ ] Hover em evidência aumenta opacidade e stroke
- [ ] Clique em evidência a seleciona (borda destacada)
- [ ] Clique em achado no painel seleciona overlay correspondente
- [ ] Botões "Confirmados/Todos/Em Avaliação" filtram corretamente

##### Responsividade
- [ ] SVG escala proporcionalmente com o container
- [ ] Coordenadas normalizadas (0-1000) mapeiam corretamente

---

## 🔧 Ajustes Esperados

### Ajuste 1: Conectar API Real

**Arquivo:** `laudo-ia.component.ts`

**Adicionar:**
```typescript
async carregarLaudoComVisualizacoes(exameId: number) {
  try {
    const response = await this.laudoService.gerarPreLaudo(exameId);
    
    this.draftData.set({
      secaoTecnica: response.etapa6LaudoFinal.secaoTecnica,
      secaoAchados: response.etapa6LaudoFinal.secaoAchados,
      secaoConclusao: response.etapa6LaudoFinal.secaoConclusao,
      secaoRecomendacoes: response.etapa6LaudoFinal.secaoRecomendacoes
    });
    
    this.evidencias.set(response.visualizacoes || []);
    this.confidenceScore.set(
      response.etapa6LaudoFinal.confiancaGeral === 'alta' ? 85 : 65
    );
    this.criticidade.set(response.etapa6LaudoFinal.criticidadeGeral);
    
    // TODO: Carregar URL real da imagem do exame
    this.imagemUrl.set(/* caminho da imagem */);
  } catch (error) {
    console.error('Erro ao carregar laudo:', error);
  }
}
```

**Chamar no `ngOnInit()`:**
```typescript
ngOnInit() {
  this.route.params.subscribe(params => {
    const exameId = params['exameId'];
    if (exameId) {
      this.carregarLaudoComVisualizacoes(Number(exameId));
    }
  });
}
```

---

### Ajuste 2: Scroll Automático (Opcional)

**Adicionar ao `laudo-ia.component.ts`:**
```typescript
selecionarAchado(evidenciaId: string) {
  this.evidenciaService.selecionar(evidenciaId);
  
  // Scroll até a seção de achados no laudo
  const elemento = document.querySelector(`[data-achado-id="${evidenciaId}"]`);
  if (elemento) {
    elemento.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}
```

**Adicionar `data-achado-id` no HTML do laudo** (onde o achado é mencionado).

---

### Ajuste 3: Cores em Dark Mode

**Verificar contraste em dark mode:**
```css
[data-theme="dark"] {
  .status-presente {
    stroke: var(--primary-container, #c3f5ff);
    fill: var(--primary-container, #c3f5ff);
  }
  
  .status-indeterminado {
    stroke: #ffb74d; /* Âmbar mais claro */
    fill: #ffb74d;
  }
}
```

---

## 🐛 Problemas Conhecidos e Soluções

### Problema 1: OpenCV não instalado
**Erro:** `ModuleNotFoundError: No module named 'cv2'`

**Solução:**
```bash
cd C:/Tila/tila-ai-cloud-service
pip install opencv-python
```

---

### Problema 2: Máscaras vazias no Stage 6.5
**Sintoma:** `visualizacoes: []` no JSON

**Causas possíveis:**
1. PSPNet não detectou máscaras (verificar `seg_result.mascara_*_array`)
2. Conversão `tolist()` falhou
3. Imagem de entrada inválida

**Debug:**
```python
# Adicionar log no stage6_5_evidence_serialization.py
logger.info(f"Máscaras disponíveis: pulmao_d={seg_result.mascara_pulmao_d}, coracao={seg_result.mascara_coracao}")
```

---

### Problema 3: SVG não renderiza
**Sintoma:** Overlay invisível sobre a imagem

**Causas possíveis:**
1. `viewBox` mal configurado
2. Coordenadas fora do range 0-1000
3. `pointer-events: none` bloqueando interação

**Solução:**
- Inspecionar elemento no DevTools
- Verificar se `<svg class="overlay">` está presente
- Validar array `poligono` no JSON

---

## 📊 Métricas de Sucesso

- ✅ Pipeline Python executa sem erros
- ✅ Stage 6.5 retorna ≥1 evidência visual por exame
- ✅ Backend Java deserializa DTO sem exceções
- ✅ Frontend renderiza overlay SVG sobre imagem
- ✅ Clique em achado destaca região na imagem
- ✅ Clique em região destaca achado no painel
- ✅ Tempo de resposta API <500ms adicional (Stage 6.5)

---

## 📁 Arquivos Modificados (Referência Rápida)

### Python
- `pipeline/stage6_5_evidence_serialization.py` (NOVO)
- `pipeline/stage2_5_segmentation.py` (modificado - linha 271)
- `schemas/contracts.py` (modificado - linhas 276-291, 159-167, 506-515)
- `app/cloud_llm_client.py` (modificado - linhas 372-378)
- `app/main.py` (modificado - linhas 161-170)

### Java
- 17 arquivos `*DTO.java` (NOVOS) em `ai/dto/`
- `PythonAIResponseDTO.java` (substituído)
- `CloudVisionConcordanciaDTO.java` (modificado)

### Angular
- `evidencia-selecao.service.ts` (NOVO)
- `visualizador-achados.component.ts` (NOVO)
- `laudo-ia.component.ts` (modificado)
- `laudo-ia.component.html` (substituído)
- `laudo-ia.component.css` (estendido)

---

## 🚀 Próximos Passos Após Testes

1. **Validar com imagens reais**: Testar com exames de tórax PA/AP reais
2. **Calibrar cores**: Ajustar contraste em dark mode se necessário
3. **Performance**: Medir impacto do Stage 6.5 no tempo de resposta
4. **Documentação médica**: Validar com radiologista se visualizações são clinicamente úteis
5. **Acessibilidade**: Garantir que overlays tenham `aria-label` adequados

---

## 📞 Suporte

Se encontrar problemas, verificar:
1. **Logs do Python**: `tila-ai-cloud-service/logs/`
2. **Console do navegador**: DevTools → Console
3. **Network tab**: Verificar se `visualizacoes` está no response JSON
4. **ADR-019**: `C:/Tila/Tila_Brain/02-Arquitetura_ADRs/ADR-019-camada-visualizacao-explicabilidade-laudos.md`

---

**Autor:** Claude (Fable Method)  
**Sessão:** 2026-08-01-17-28  
**Tempo de implementação:** ~4h 18min
