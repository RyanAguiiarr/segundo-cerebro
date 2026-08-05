diff --git a/.idea/compiler.xml b/.idea/compiler.xml
index 79aa3fb..fb28552 100644
--- a/.idea/compiler.xml
+++ b/.idea/compiler.xml
@@ -9,7 +9,6 @@
         <outputRelativeToContentRoot value="true" />
         <processorPath useClasspath="false">
           <entry name="$MAVEN_REPOSITORY$/org/projectlombok/lombok/1.18.42/lombok-1.18.42.jar" />
-          <entry name="$MAVEN_REPOSITORY$/org/projectlombok/lombok/1.18.42/lombok-1.18.42.jar" />
         </processorPath>
         <module name="tila" />
       </profile>
diff --git a/tila/pom.xml b/tila/pom.xml
index 1934d93..f5b5b41 100644
--- a/tila/pom.xml
+++ b/tila/pom.xml
@@ -34,10 +34,11 @@
 
 	<dependencyManagement>
 		<dependencies>
+			<!-- Atualizado de 0.36.2 para 1.0.1 ÔÇö vers├úo compat├¡vel com Jackson 3.x / Spring Boot 4 -->
 			<dependency>
 				<groupId>dev.langchain4j</groupId>
 				<artifactId>langchain4j-bom</artifactId>
-				<version>0.36.2</version>
+				<version>1.0.1</version>
 				<type>pom</type>
 				<scope>import</scope>
 			</dependency>
@@ -101,6 +102,12 @@
 			<groupId>com.auth0</groupId>
 			<artifactId>java-jwt</artifactId>
 			<version>4.4.0</version>
+			<exclusions>
+				<exclusion>
+					<groupId>com.fasterxml.jackson.core</groupId>
+					<artifactId>jackson-databind</artifactId>
+				</exclusion>
+			</exclusions>
 		</dependency>
 		<dependency>
 			<groupId>org.springframework.boot</groupId>
@@ -113,6 +120,7 @@
 			<scope>test</scope>
 		</dependency>
 
+		<!-- LangChain4j 1.0.1 ÔÇö n├úo depende do Jackson 2.x, compat├¡vel com Spring Boot 4 -->
 		<dependency>
 			<groupId>dev.langchain4j</groupId>
 			<artifactId>langchain4j</artifactId>
@@ -132,6 +140,7 @@
 			<groupId>dev.langchain4j</groupId>
 			<artifactId>langchain4j-pgvector</artifactId>
 		</dependency>
+
 	</dependencies>
 
 	<build>
@@ -164,4 +173,4 @@
 		</plugins>
 	</build>
 
-</project>
+</project>
\ No newline at end of file
diff --git a/tila/src/main/java/tecnologi/tila/tila/ai/agent/TilaRadiologistaAgent.java b/tila/src/main/java/tecnologi/tila/tila/ai/agent/TilaRadiologistaAgent.java
index cdd5ce7..b6b8007 100644
--- a/tila/src/main/java/tecnologi/tila/tila/ai/agent/TilaRadiologistaAgent.java
+++ b/tila/src/main/java/tecnologi/tila/tila/ai/agent/TilaRadiologistaAgent.java
@@ -1,6 +1,5 @@
 package tecnologi.tila.tila.ai.agent;
 
-import dev.langchain4j.data.image.Image;
 import dev.langchain4j.service.SystemMessage;
 import dev.langchain4j.service.UserMessage;
 import dev.langchain4j.service.V;
@@ -10,26 +9,23 @@ public interface TilaRadiologistaAgent {
     @SystemMessage(fromResource = "prompts/radiologista-system.txt")
     String gerarPreLaudo(
             @UserMessage("""
-            ## Contexto do Exame
-            - Tipo: {{tipoExame}}
-            - Paciente: {{nomePaciente}}, {{idadePaciente}} anos, {{generoPaciente}}
-            - Regi├úo anat├┤mica: {{regiaoAnatomica}}
-            - Data do exame: {{dataExame}}
-            
-            ## Observa├º├Áes do M├®dico Solicitante
-            {{observacoesMedico}}
-            
-            ## Instru├º├úo
-            Analise a imagem do exame anexada e gere o pr├®-laudo estruturado 
-            no formato JSON especificado no sistema.
-            """)
-            @V("tipoExame") String tipoExame,
+                    ## Contexto do Exame
+                    - Tipo: {{tipoExame}}
+                    - Paciente: {{nomePaciente}}, {{idadePaciente}} anos, {{generoPaciente}}
+                    - Regi├úo anat├┤mica: {{regiaoAnatomica}}
+                    - Data do exame: {{dataExame}}
+
+                    ## Observa├º├Áes do M├®dico Solicitante
+                    {{observacoesMedico}}
+
+                    ## Instru├º├úo
+                    Analise a imagem do exame anexada e gere o pr├®-laudo estruturado
+                    no formato JSON especificado no sistema.
+                    """) @V("tipoExame") String tipoExame,
             @V("nomePaciente") String nomePaciente,
             @V("idadePaciente") int idadePaciente,
             @V("generoPaciente") String generoPaciente,
             @V("regiaoAnatomica") String regiaoAnatomica,
             @V("dataExame") String dataExame,
-            @V("observacoesMedico") String observacoesMedico,
-            Image imagem
-    );
+            @V("observacoesMedico") String observacoesMedico);
 }
diff --git a/tila/src/main/java/tecnologi/tila/tila/ai/config/TilaRagConfig.java b/tila/src/main/java/tecnologi/tila/tila/ai/config/TilaRagConfig.java
index 08f5659..a8663d8 100644
--- a/tila/src/main/java/tecnologi/tila/tila/ai/config/TilaRagConfig.java
+++ b/tila/src/main/java/tecnologi/tila/tila/ai/config/TilaRagConfig.java
@@ -1,7 +1,7 @@
 package tecnologi.tila.tila.ai.config;
 
 import dev.langchain4j.data.segment.TextSegment;
-import dev.langchain4j.model.chat.ChatLanguageModel;
+import dev.langchain4j.model.chat.ChatModel;
 import dev.langchain4j.model.embedding.EmbeddingModel;
 import dev.langchain4j.model.googleai.GoogleAiEmbeddingModel;
 import dev.langchain4j.model.googleai.GoogleAiGeminiChatModel;
@@ -19,7 +19,7 @@ import tecnologi.tila.tila.ai.agent.TilaRadiologistaAgent;
 @Configuration
 public class TilaRagConfig {
 
-    @Value("AIzaSyBkM8J29x9tpXz9ZpYWDi_j93WDQPzdNaA")
+    @Value("${GEMINI_API_KEY}")
     private String geminiApiKey;
 
     @Value("${spring.datasource.username}")
@@ -29,7 +29,7 @@ public class TilaRagConfig {
     private String dbPassword;
 
     @Bean
-    public ChatLanguageModel chatLanguageModel(){
+    public ChatModel chatLanguageModel(){
         return GoogleAiGeminiChatModel.builder()
                 .apiKey(geminiApiKey)
                 .modelName("gemini-2.5-flash")
@@ -41,7 +41,8 @@ public class TilaRagConfig {
     public EmbeddingModel embeddingModel(){
         return GoogleAiEmbeddingModel.builder()
                 .apiKey(geminiApiKey)
-                .modelName("text-embedding-004")
+                .modelName("gemini-embedding-001")
+                .outputDimensionality(768)
                 .build();
     }
 
@@ -65,14 +66,14 @@ public class TilaRagConfig {
                 .embeddingStore(embeddingStore)
                 .embeddingModel(embeddingModel)
                 .maxResults(8)
-                .minScore(0.7)
+                .minScore(0.8)
                 .build();
     }
 
     @Bean
-    public TilaRadiologistaAgent tilaAgent(ChatLanguageModel model, ContentRetriever content){
+    public TilaRadiologistaAgent tilaAgent(ChatModel model, ContentRetriever content){
         return AiServices.builder(TilaRadiologistaAgent.class)
-                .chatLanguageModel(model)
+                .chatModel(model)
                 .contentRetriever(content)
                 .build();
     }
diff --git a/tila/src/main/java/tecnologi/tila/tila/ai/dto/GeminiLaudoResponse.java b/tila/src/main/java/tecnologi/tila/tila/ai/dto/GeminiLaudoResponse.java
new file mode 100644
index 0000000..1b7bef7
--- /dev/null
+++ b/tila/src/main/java/tecnologi/tila/tila/ai/dto/GeminiLaudoResponse.java
@@ -0,0 +1,13 @@
+package tecnologi.tila.tila.ai.dto;
+
+import java.util.List;
+
+public record GeminiLaudoResponse(
+        List<String> achados,
+        List<String> impressaoDiagnostica,
+        String notaIA,
+        Integer confidenceScore,
+        List<String> recomendacoes,
+        String classificacao
+) {
+}
diff --git a/tila/src/main/java/tecnologi/tila/tila/config/SecurityConfigurations.java b/tila/src/main/java/tecnologi/tila/tila/config/SecurityConfigurations.java
index 3ec94d3..ddd872d 100644
--- a/tila/src/main/java/tecnologi/tila/tila/config/SecurityConfigurations.java
+++ b/tila/src/main/java/tecnologi/tila/tila/config/SecurityConfigurations.java
@@ -40,6 +40,7 @@ public class SecurityConfigurations {
                     req.requestMatchers("/auth/**").permitAll();
                     req.requestMatchers("/medicos/**").hasRole("MEDICO");
                     req.requestMatchers("/paciente/**").hasAnyRole("MEDICO", "PACIENTE");
+                    req.requestMatchers("/laudo/**").hasRole("MEDICO");
                     req.anyRequest().authenticated();
                 })
                 .addFilterBefore(securityFilter, UsernamePasswordAuthenticationFilter.class)
diff --git a/tila/src/main/java/tecnologi/tila/tila/controller/AutenticacaoController.java b/tila/src/main/java/tecnologi/tila/tila/controller/AutenticacaoController.java
index 52cf462..226af57 100644
--- a/tila/src/main/java/tecnologi/tila/tila/controller/AutenticacaoController.java
+++ b/tila/src/main/java/tecnologi/tila/tila/controller/AutenticacaoController.java
@@ -123,7 +123,17 @@ public class AutenticacaoController {
     @GetMapping("/me")
     public ResponseEntity<GenericResult<UserProfileDTO>> obterDadosLogado(){
 
-        var usuario = (Usuario) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
+        var principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal();
+
+        Usuario usuario;
+        if (principal instanceof Usuario u) {
+            usuario = u;
+        } else {
+            // principal ├® uma String (email) quando vindo do JWT
+            String email = principal.toString();
+            usuario = usuarioRepository.findByEmail(email)
+                    .orElseThrow(() -> new EntityNotFoundException("Usu├írio n├úo encontrado"));
+        }
 
         var medico = medicoRepository.findByUsuario(usuario)
                 .orElseThrow(() -> new EntityNotFoundException("M├®dico n├úo encontrado"));
diff --git a/tila/src/main/java/tecnologi/tila/tila/controller/LaudoController/LaudoController.java b/tila/src/main/java/tecnologi/tila/tila/controller/LaudoController/LaudoController.java
new file mode 100644
index 0000000..a1300ac
--- /dev/null
+++ b/tila/src/main/java/tecnologi/tila/tila/controller/LaudoController/LaudoController.java
@@ -0,0 +1,30 @@
+package tecnologi.tila.tila.controller.LaudoController;
+
+import jakarta.validation.Valid;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.security.core.annotation.AuthenticationPrincipal;
+import org.springframework.web.bind.annotation.*;
+import tecnologi.tila.tila.dto.laudoDTO.LaudoGeracaoRequestDTO;
+import tecnologi.tila.tila.dto.laudoDTO.LaudoResponseDTO;
+import tecnologi.tila.tila.entity.Usuario;
+import tecnologi.tila.tila.service.GenericResult;
+import tecnologi.tila.tila.service.laudoService.LaudoService;
+
+@RestController
+@RequestMapping("laudo")
+public class LaudoController {
+
+    private final LaudoService laudoService;
+
+    public LaudoController(LaudoService laudoService) {
+        this.laudoService = laudoService;
+    }
+
+    @PostMapping
+    public ResponseEntity<GenericResult<LaudoResponseDTO>> gerarPreLaudo(@RequestBody @Valid LaudoGeracaoRequestDTO request,
+                                                                         @AuthenticationPrincipal Usuario usuarioLogado){
+        var response = laudoService.gerarPreLaudo(request, usuarioLogado);
+        return ResponseEntity.status(HttpStatus.CREATED).body(GenericResult.success(response));
+    }
+}
diff --git a/tila/src/main/java/tecnologi/tila/tila/dto/laudoDTO/LaudoResponseDTO.java b/tila/src/main/java/tecnologi/tila/tila/dto/laudoDTO/LaudoResponseDTO.java
index a6cec22..0389e24 100644
--- a/tila/src/main/java/tecnologi/tila/tila/dto/laudoDTO/LaudoResponseDTO.java
+++ b/tila/src/main/java/tecnologi/tila/tila/dto/laudoDTO/LaudoResponseDTO.java
@@ -14,7 +14,7 @@ public record LaudoResponseDTO(
         String rascunhoIA,
         String achadosJson,
         String impressaoJson,
-        String notaAI,
+        String notaIA,
         Integer confidenceScore,
 
         //compo preenchido pelo m├®dico ap├│s revis├óo
diff --git a/tila/src/main/java/tecnologi/tila/tila/dto/pacienteDTO/PacienteResponseDTO.java b/tila/src/main/java/tecnologi/tila/tila/dto/pacienteDTO/PacienteResponseDTO.java
index b1ca1f8..73c51a7 100644
--- a/tila/src/main/java/tecnologi/tila/tila/dto/pacienteDTO/PacienteResponseDTO.java
+++ b/tila/src/main/java/tecnologi/tila/tila/dto/pacienteDTO/PacienteResponseDTO.java
@@ -14,7 +14,7 @@ public record PacienteResponseDTO(
         String nomeCompleto,
         String cpf,
         LocalDate dataNascimento,
-        List<Exame> exames
+        List<ExameResponseDTO> exames
 ) {
 
     public static PacienteResponseDTO fromEntity(Paciente paciente){
@@ -23,7 +23,14 @@ public record PacienteResponseDTO(
                 paciente.getNomeCompleto(),
                 paciente.getCpf(),
                 paciente.getDataNascimento(),
-                paciente.getExames()
+                paciente.getExames() != null ? paciente.getExames().stream()
+                        .map(e -> new ExameResponseDTO(
+                                e.getId(),
+                                e.getTipoExame(),
+                                e.getDataRealiza├º├úo(),
+                                e.getStatus(),
+                                e.getUrlImagem()
+                        )).toList() : List.of()
         );
     }
 }
diff --git a/tila/src/main/java/tecnologi/tila/tila/entity/Laudo.java b/tila/src/main/java/tecnologi/tila/tila/entity/Laudo.java
index a87254f..5138c8b 100644
--- a/tila/src/main/java/tecnologi/tila/tila/entity/Laudo.java
+++ b/tila/src/main/java/tecnologi/tila/tila/entity/Laudo.java
@@ -80,8 +80,6 @@ public class Laudo {
     protected void onPreUpdate(){
         if(this.status == StatusLaudo.ASSINADO && this.dataAssinatura == null){
             this.dataAssinatura = LocalDateTime.now();
-        }else{
-            this.dataAssinatura = LocalDateTime.now();
         }
     }
 }
diff --git a/tila/src/main/java/tecnologi/tila/tila/service/laudoService/LaudoService.java b/tila/src/main/java/tecnologi/tila/tila/service/laudoService/LaudoService.java
index 319e681..e1c9c05 100644
--- a/tila/src/main/java/tecnologi/tila/tila/service/laudoService/LaudoService.java
+++ b/tila/src/main/java/tecnologi/tila/tila/service/laudoService/LaudoService.java
@@ -1,17 +1,41 @@
 package tecnologi.tila.tila.service.laudoService;
 
+import dev.langchain4j.data.message.*;
+import dev.langchain4j.model.chat.ChatModel;
+import dev.langchain4j.model.chat.request.ChatRequest;
+import dev.langchain4j.model.chat.response.ChatResponse;
+import jakarta.persistence.EntityNotFoundException;
+import jakarta.transaction.Transactional;
+import lombok.Data;
+import org.springframework.beans.factory.annotation.Value;
+import org.springframework.core.io.ClassPathResource;
 import org.springframework.stereotype.Service;
-import tecnologi.tila.tila.ai.agent.TilaRadiologistaAgent;
+import tecnologi.tila.tila.ai.dto.GeminiLaudoResponse;
+import tecnologi.tila.tila.dto.laudoDTO.LaudoGeracaoRequestDTO;
+import tecnologi.tila.tila.dto.laudoDTO.LaudoResponseDTO;
+import tecnologi.tila.tila.entity.Laudo;
+import tecnologi.tila.tila.entity.Usuario;
+import tecnologi.tila.tila.enuns.StatusLaudo;
 import tecnologi.tila.tila.repository.ExameRepository;
 import tecnologi.tila.tila.repository.LaudoRepository;
 import tecnologi.tila.tila.repository.MedicoRepository;
+import tools.jackson.databind.ObjectMapper;
 
-import java.lang.runtime.ObjectMethods;
+import java.io.IOException;
+import java.nio.charset.StandardCharsets;
+import java.nio.file.Files;
+import java.nio.file.Path;
+import java.util.Base64;
+import java.util.Date;
+import java.util.List;
 
 @Service
 public class LaudoService {
 
-    private final TilaRadiologistaAgent agente;
+    @Value("${tila.upload.path:./uploads/exames}")
+    private String uploadPath;
+
+    private final ChatModel chatModel;
 
     private final LaudoRepository laudoRepository;
 
@@ -19,15 +43,167 @@ public class LaudoService {
 
     private final MedicoRepository medicoRepository;
 
-    private final ObjectMethods objectMethods; //serve para parserar o json retornado pela ia
+    private final ObjectMapper objectMapper;
+
 
-    public LaudoService(TilaRadiologistaAgent agente, LaudoRepository laudoRepository, ExameRepository exameRepository, MedicoRepository medicoRepository, ObjectMethods objectMethods) {
-        this.agente = agente;
+    public LaudoService(ChatModel chatModel, LaudoRepository laudoRepository, ExameRepository exameRepository, MedicoRepository medicoRepository, ObjectMapper objectMapper) {
+        this.chatModel = chatModel;
         this.laudoRepository = laudoRepository;
         this.exameRepository = exameRepository;
         this.medicoRepository = medicoRepository;
-        this.objectMethods = objectMethods;
+        this.objectMapper = objectMapper;
+    }
+
+    @Transactional
+    public LaudoResponseDTO gerarPreLaudo(LaudoGeracaoRequestDTO dados, Usuario usuarioLogado){
+
+        // validar e buscar M├®dico logado
+        var medico = medicoRepository.findByUsuario(usuarioLogado)
+                .orElseThrow(() -> new EntityNotFoundException("M├®dico n├úo cadastrado no sistema para este us├írio"));
+
+        // buscar e validade exame com detalhes
+        var exame = exameRepository.findByIdWithDetails(dados.exameid())
+                .orElseThrow(() -> new EntityNotFoundException("Exame n├úo encontrado."));
+
+        // carregar imagem como base64 e mimeType
+        ImagemCarregada imagemData = carregarImagemExame(exame.getUrlImagem());
+
+        // carregar system prompt do recurso
+        String systemPromptText = carregarSystemPrompt();
+
+        // montar texto do contexto do exame
+        int idade = calcularIdade(exame.getPaciente().getDataNascimento());
+        String regiaoAnatomica = exame.getTipoExame().contains("T├│rax") ? "T├│rax" : "Geral";
+        String observacoes = dados.observacoesMedico() != null ? dados.observacoesMedico() : "Nenhuma observa├º├úo cl├¡nica adicional.";
+
+        String textoContexto = """
+                ## Contexto do Exame
+                - Tipo: %s
+                - Paciente: %s, %d anos, n├úo especificado
+                - Regi├úo anat├┤mica: %s
+                - Data do exame: %s
+                
+                ## Observa├º├Áes do M├®dico Solicitante
+                %s
+                
+                ## Instru├º├úo
+                Analise a imagem do exame anexada e gere o pr├®-laudo estruturado
+                no formato JSON especificado no sistema.
+                """.formatted(
+                exame.getTipoExame(),
+                exame.getPaciente().getNomeCompleto(),
+                idade,
+                regiaoAnatomica,
+                exame.getDataRealiza├º├úo().toString(),
+                observacoes
+        );
+
+        // construir mensagem multimodal (texto + imagem)
+        SystemMessage systemMessage = SystemMessage.from(systemPromptText);
+        UserMessage userMessage = UserMessage.from(
+                TextContent.from(textoContexto),
+                ImageContent.from(imagemData.base64, imagemData.mimeType)
+        );
+
+        // executar chamada ao modelo
+        ChatResponse response = chatModel.chat(ChatRequest.builder()
+                .messages(List.of(systemMessage, userMessage))
+                .build());
+
+        String respostaIA = response.aiMessage().text();
+
+        // limpar e parsear JSON retornado
+        GeminiLaudoResponse dadosLaudo = parseRespostaIA(respostaIA);
+
+        // formatar texto leg├¡vel do rascuho
+        String rascunhoIA = formatarRascunhoTexto(dadosLaudo);
+
+        // persistir laudo
+        var laudo = new Laudo();
+        laudo.setExame(exame);
+        laudo.setMedico(medico);
+        laudo.setRascunhoIA(rascunhoIA);
+        laudo.setTextoFinal(rascunhoIA); // Come├ºa id├¬ntico ao rascunho
+        laudo.setAchadosJson(respostaIA); // Guarda o JSON retornado completo
+        laudo.setImpressaoJson(dadosLaudo.impressaoDiagnostica().toString());
+        laudo.setNotaIA(dadosLaudo.notaIA());
+        laudo.setConfidenceScore(dadosLaudo.confidenceScore());
+        laudo.setStatus(StatusLaudo.RASCUNHO);
+
+        laudoRepository.save(laudo);
+
+        return LaudoResponseDTO.fromEntity(laudo);
+    }
+
+    private record ImagemCarregada(String base64, String mimeType) {}
+
+    private ImagemCarregada carregarImagemExame(String urlImagem){
+        try{
+            Path caminho = Path.of(uploadPath, urlImagem);
+
+            if(!Files.exists(caminho)){
+                // tenta carregar o caminho absoluto caso urlImagem ja seja absoluto
+                caminho = Path.of(urlImagem);
+            }
+
+            byte[] bytes = Files.readAllBytes(caminho);
+            String base64 = Base64.getEncoder().encodeToString(bytes);
+            String mimeType = urlImagem.endsWith(".png") ? "image/png" : "image/jpeg";
+            return new ImagemCarregada(base64, mimeType);
+        }catch (IOException e){
+            throw new RuntimeException("Falha ao carregar a imagem do exame: " + e.getMessage(), e);
+        }
+    }
+
+    private String carregarSystemPrompt(){
+        try {
+            ClassPathResource resource = new ClassPathResource("prompts/radiologista-system.txt");
+            return new String(resource.getInputStream().readAllBytes(), StandardCharsets.UTF_8);
+        } catch (IOException e) {
+            throw new RuntimeException("Falha ao carregar o prompt do sistema: " + e.getMessage(), e);
+        }
+    }
+
+
+    private GeminiLaudoResponse parseRespostaIA(String resposta){
+        try{
+            String jsonLimpo = resposta;
+            if (jsonLimpo.contains("```json")) {
+                jsonLimpo = jsonLimpo.substring(jsonLimpo.indexOf("```json") + 7);
+            }
+            if (jsonLimpo.contains("```")) {
+                jsonLimpo = jsonLimpo.substring(0, jsonLimpo.indexOf("```"));
+            }
+            jsonLimpo = jsonLimpo.trim();
+            return objectMapper.readValue(jsonLimpo, GeminiLaudoResponse.class);
+        }catch (Exception e){
+            throw new RuntimeException("Erro ao processar JSON retornado da IA: " + e.getMessage(), e);
+        }
     }
 
+    private String formatarRascunhoTexto(GeminiLaudoResponse dados){
+        StringBuilder sb = new StringBuilder();
+        sb.append("# PR├ë-LAUDO RADIOL├ôGICO\n\n");
+        sb.append("## Achados\n");
+        dados.achados().forEach(a -> sb.append("- ").append(a).append("\n"));
+        sb.append("\n## Impress├úo Diagn├│stica\n");
+        dados.impressaoDiagnostica().forEach(i -> sb.append("- ").append(i).append("\n"));
+        if (dados.recomendacoes() != null && !dados.recomendacoes().isEmpty()) {
+            sb.append("\n## Recomenda├º├Áes\n");
+            dados.recomendacoes().forEach(r -> sb.append("- ").append(r).append("\n"));
+        }
+        sb.append("\n\n---\n*Nota da IA (Score de Confian├ºa: ")
+                .append(dados.confidenceScore())
+                .append("%): ")
+                .append(dados.notaIA())
+                .append("*");
+        return sb.toString();
+
+    }
+
+    private int calcularIdade(java.time.LocalDate nascimento){
+        if(nascimento == null) return 0;
+        return java.time.Period.between(nascimento, java.time.LocalDate.now()).getYears();
+    }
 
 }
diff --git a/tila/src/main/java/tecnologi/tila/tila/service/paciente/PacienteService.java b/tila/src/main/java/tecnologi/tila/tila/service/paciente/PacienteService.java
index be9dde6..e4a4700 100644
--- a/tila/src/main/java/tecnologi/tila/tila/service/paciente/PacienteService.java
+++ b/tila/src/main/java/tecnologi/tila/tila/service/paciente/PacienteService.java
@@ -42,7 +42,7 @@ public class PacienteService {
 
         registrarLog(medicologado, "CADASTRO_PACIENTE", LocalDateTime.now());
 
-        return new PacienteResponseDTO(novoPaciente.getId(), novoPaciente.getNomeCompleto(), novoPaciente.getCpf(), novoPaciente.getDataNascimento(), novoPaciente.getExames());
+        return PacienteResponseDTO.fromEntity(novoPaciente);
     }
 
     @Transactional(readOnly = true)
@@ -50,7 +50,7 @@ public class PacienteService {
         var pacientes = pacienteRepository.findAll();
 
         return pacientes.stream()
-                .map(p -> new PacienteResponseDTO(p.getId(), p.getNomeCompleto(), p.getCpf(), p.getDataNascimento(), p.getExames()))
+                .map(PacienteResponseDTO::fromEntity)
                 .toList();
 
     }
@@ -61,7 +61,7 @@ public class PacienteService {
                 .orElseThrow(() -> new EntityNotFoundException("paciente n├úo localizado"));
 
         registrarLog(medicologado, "CONSULTA_PACIENTE_CPF", LocalDateTime.now());
-        return new PacienteResponseDTO(paciente.getId(), paciente.getNomeCompleto(), paciente.getCpf(),paciente.getDataNascimento(), paciente.getExames());
+        return PacienteResponseDTO.fromEntity(paciente);
     }
 
     public PacienteResponseDTO buscarPorId(Long id, Usuario medicologado){
@@ -69,7 +69,7 @@ public class PacienteService {
                 .orElseThrow(() ->  new EntityNotFoundException("paciente n├úo localizado"));
 
         registrarLog(medicologado, "CONSULTA_PACIENTE_ID", LocalDateTime.now());
-        return new PacienteResponseDTO(paciente.getId(), paciente.getNomeCompleto(), paciente.getCpf(),paciente.getDataNascimento(), paciente.getExames());
+        return PacienteResponseDTO.fromEntity(paciente);
     }
 
     public void registrarLog(Usuario usuario, String acao, LocalDateTime dataHora){
diff --git a/tila/src/main/resources/application.properties b/tila/src/main/resources/application.properties
index 9c4580b..cc4555c 100644
--- a/tila/src/main/resources/application.properties
+++ b/tila/src/main/resources/application.properties
@@ -17,7 +17,10 @@ langchain4j.google-ai-gemini.chat-model.temperature=0.3
 langchain4j.google-ai-gemini.chat-model.max-output-tokens=4096
 
 langchain4j.google-ai-gemini.embedding-model.api-key=${GEMINI_API_KEY}
-langchain4j.google-ai-gemini.embedding-model.model-name=text-embedding-004
+langchain4j.google-ai-gemini.embedding-model.model-name=gemini-embedding-001
 
 tila.upload.path=./uploads/exames
-tila.upload.max-size-mb=50
\ No newline at end of file
+tila.upload.max-size-mb=50
+
+GEMINI_API_KEY=AIzaSyBkM8J29x9tpXz9ZpYWDi_j93WDQPzdNaA
+
diff --git a/tila/uploads/exames/exame_torax_teste.png b/tila/uploads/exames/exame_torax_teste.png
new file mode 100644
index 0000000..d6c2134
Binary files /dev/null and b/tila/uploads/exames/exame_torax_teste.png differ
