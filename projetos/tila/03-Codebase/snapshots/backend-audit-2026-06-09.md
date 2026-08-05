---
title: "Auditoria Backend TILA — Snapshot 2026-06-09"
type: snapshot
scope: backend
date: 2026-06-09
immutable: true
---

# Auditoria Completa do Backend TILA
> Snapshot imutável de 2026-06-09 — extraído diretamente do código-fonte real.

## Stack Verificada (pom.xml)

| Dependência | Versão |
|---|---|
| Spring Boot | 4.0.3 |
| Java | 21 |
| LangChain4j BOM | 1.0.1 |
| auth0 java-jwt | 4.4.0 |
| PostgreSQL Driver | runtime (versão do parent) |
| Lombok | 1.18.42 |
| Jackson | 3.x (via Spring Boot 4) |
| Módulos LC4j | langchain4j, langchain4j-spring-boot-starter, langchain4j-google-ai-gemini, langchain4j-pgvector |

## Estrutura de Pacotes

```
tecnologi.tila.tila/
├── TilaApplication.java
├── ai/
│   ├── agent/TilaRadiologistaAgent.java
│   ├── config/TilaRagConfig.java
│   └── dto/GeminiLaudoResponse.java
├── config/
│   ├── SecurityConfigurations.java
│   └── SecurityFilter.java
├── controller/
│   ├── AutenticacaoController.java
│   ├── LaudoController/LaudoController.java
│   ├── logAuditoria/LogAuditoriaController.java
│   └── paciente/PacienteController.java
├── dto/
│   ├── auth/ (LoginRequestDTO, LoginResponseDTO, MedicoRequestDTO, UserDTO, UserProfileDTO)
│   ├── consulta/ (ConsultaDTO — vazio)
│   ├── exame/ (ExameRequestDTO, ExameResponseDTO)
│   ├── laudo/ (LaudoGeracaoRequestDTO, LaudoResponseDTO, LaudoRevisaoRequestDTO)
│   └── paciente/ (PacienteRequestDTO, PacienteResponseDTO)
├── entity/ (8 entidades)
├── enums/ (6 enums)
├── exceptions/GlobalExceptionHandler.java
├── repository/ (8 repositórios)
└── service/
    ├── GenericResult.java
    ├── TokenService.java
    ├── authenticate/AutenticacaoService.java
    ├── laudoService/LaudoService.java
    ├── logAuditoria/LogAuditoriaService.java
    └── paciente/PacienteService.java
```

## Entidades JPA

### Usuario
| Campo | Tipo | Anotações | ⚠️ LGPD |
|---|---|---|---|
| id | UUID | @Id @GeneratedValue(UUID) | |
| email | String | @Email @Column(unique, not null) | ⚠️ Dado pessoal |
| senha | String | @Column(not null) | ⚠️ Credencial |
| perfil | PerfilUser | @Enumerated(STRING) | |
| ativo | Boolean | default true | |
| ultimoAcesso | Timestamp | | |
- Tabela: `usuarios`
- Implementa `UserDetails` (Spring Security)
- `getAuthorities()`: ADMIN → ROLE_ADMIN + ROLE_MEDICO; demais → ROLE_{perfil}
- `isEnabled()` delega para `ativo`

### Medico
| Campo | Tipo | Anotações | ⚠️ LGPD |
|---|---|---|---|
| id | Long | @Id @GeneratedValue(IDENTITY) | |
| nomeCompleto | String | @Column(not null) | ⚠️ Dado pessoal |
| crm | String | @Column(not null, unique) | ⚠️ Dado profissional |
| especialidade | String | | |
| assinaturaDigital | String | @Lob (Base64) | ⚠️ Dado sensível |
| usuario | Usuario | @OneToOne @JoinColumn(usuario_id) | |
- Tabela: `medicos`

### Paciente
| Campo | Tipo | Anotações | ⚠️ LGPD |
|---|---|---|---|
| id | Long | @Id @GeneratedValue(IDENTITY) | |
| nomeCompleto | String | @Column(not null) | ⚠️ Dado pessoal |
| cpf | String | @Column(unique, not null) | ⚠️ Dado sensível (CPF) |
| dataNascimento | LocalDate | | ⚠️ Dado pessoal |
| telefone | String | | ⚠️ Dado pessoal |
| exames | List\<Exame\> | @OneToMany(mappedBy="paciente") | |
- Tabela: `pacientes`

### Exame
| Campo | Tipo | Anotações | ⚠️ LGPD |
|---|---|---|---|
| id | Long | @Id @GeneratedValue(IDENTITY) | |
| tipoExame | String | @Column(not null) | |
| dataRealização | LocalDateTime | | ⚠️ Dado clínico |
| urlImagem | String | | ⚠️ Dado clínico |
| status | StatusExame | @Enumerated(STRING) default PENDENTE | |
| paciente | Paciente | @ManyToOne @JoinColumn(paciente_id) | |
| medico | Medico | @ManyToOne @JoinColumn(medico_id) | |
- Tabela: `exames`
- ⚠️ Campo `dataRealização` usa caractere especial (ã) — pode causar problemas

### Laudo
| Campo | Tipo | Anotações | ⚠️ LGPD |
|---|---|---|---|
| id | Long | @Id @GeneratedValue(IDENTITY) | |
| rascunhoIA | String | @Column(TEXT) | ⚠️ Dado clínico |
| textoFinal | String | @Column(TEXT) | ⚠️ Dado clínico |
| achadosJson | String | @Column(TEXT) | ⚠️ Dado clínico |
| impressaoJson | String | @Column(TEXT) | ⚠️ Dado clínico |
| notaIA | String | @Column(TEXT) | |
| confidenceScore | Integer | | |
| status | StatusLaudo | @Enumerated(STRING) default RASCUNHO | |
| hashIntegridade | String | | |
| exame | Exame | @ManyToOne(LAZY) @JoinColumn(exame_id, not null) | |
| medico | Medico | @ManyToOne(LAZY) @JoinColumn(medico_id, not null) | |
| dataCriacao | LocalDateTime | @PrePersist → now() | |
| dataRevisao | LocalDateTime | | |
| dataAssinatura | LocalDateTime | @PreUpdate → set if ASSINADO | |
- Sem anotação @Table (usa nome padrão da classe)
- Construtor all-args manual (não usa Lombok @AllArgsConstructor)

### ConhecimentoMedico
| Campo | Tipo | Anotações |
|---|---|---|
| id | Long | @Id @GeneratedValue(IDENTITY) |
| titulo | String | @Column(not null) |
| conteudo | String | @Column(TEXT, not null) |
| categoriaConhecimento | CategoriaConhecimento | @Enumerated(STRING) @Column(not null) |
| tipoExameRelacionado | String | Ex: RX_TORAX |
| regiaoAnatomica | String | Ex: TORAX, CRANIO |
| dataCriacao | LocalDateTime | @Column(not null, updatable=false) @PrePersist |
| dataAtualizacao | LocalDateTime | @PreUpdate |
- Tabela: `conhecimento_medico`
- Base de conhecimento para RAG

### LogAuditoria
| Campo | Tipo | Anotações |
|---|---|---|
| id | Long | @Id @GeneratedValue(IDENTITY) |
| usuario | Usuario | @ManyToOne @JoinColumn(usuario_id) |
| acao | String | @Column(not null) |
| dataHora | LocalDateTime | @Column(not null) |
| ipOrigem | String | ⚠️ Sempre null — nunca populado |
- Tabela: `logs_auditoria`

### Consulta
- **VAZIA** — classe sem campos, sem anotações, sem @Entity, sem @Table
- Apenas `package` e class body vazio
- Placeholder puro — não é uma entidade JPA funcional

## Enums

| Enum | Valores |
|---|---|
| PerfilUser | MEDICO, PACIENTE, ADMIN |
| StatusExame | PENDENTE, EM_ANDAMENTO, CONCLUIDO |
| StatusLaudo | RASCUNHO, EM_REVISAO, ASSINADO, CANCELADO |
| CategoriaConhecimento | PROTOCOLO, ANATOMIA, ACR_BIRADS, ATLAS, LAUDO_EXEMPLO, TERMINOLOGIA, DIRETRIZ |
| StatusConsulta | (arquivo de 67 bytes — provavelmente vazio/minimal) |
| TipoConsulta | (arquivo de 65 bytes — provavelmente vazio/minimal) |

## Repositórios

| Repositório | Entidade | Métodos custom |
|---|---|---|
| UsuarioRepository | Usuario | findByEmail(String): Optional |
| MedicoRepository | Medico | findByUsuario(Usuario): Optional |
| PacienteRepository | Paciente | findByCpf(String): Optional, existsByCpf(String): boolean |
| ExameRepository | Exame | findByIdWithDetails(Long): Optional (JOIN FETCH) |
| LaudoRepository | Laudo | findByExameId(Long): Optional |
| LogAuditoriaRepository | LogAuditoria | findAll() |
| ConhecimentoMedicoRepository | ConhecimentoMedico | (JpaRepository padrão) |
| ConsultaRepository | Consulta | (JpaRepository padrão — entidade vazia) |

## Endpoints

| Método | Path | Auth | Response Type | Controller | Notas |
|---|---|---|---|---|---|
| POST | /auth/registrar | Público | GenericResult\<Boolean\> | AutenticacaoController | Registra médico + usuário |
| POST | /auth/login | Público | GenericResult\<UserDTO\> | AutenticacaoController | Retorna JWT em cookie + body |
| GET | /auth/me | Autenticado | GenericResult\<UserProfileDTO\> | AutenticacaoController | Dados do médico logado |
| POST | /paciente | ROLE_MEDICO/PACIENTE | GenericResult\<PacienteResponseDTO\> | PacienteController | Cadastra paciente |
| GET | /paciente | ROLE_MEDICO/PACIENTE | GenericResult\<List\<PacienteResponseDTO\>\> | PacienteController | Lista todos pacientes |
| GET | /paciente/{id} | ROLE_MEDICO/PACIENTE | GenericResult\<PacienteResponseDTO\> | PacienteController | Busca por ID |
| POST | /laudo | ROLE_MEDICO | GenericResult\<LaudoResponseDTO\> | LaudoController | Gera pré-laudo via IA |
| GET | /logs | ROLE_ADMIN | GenericResult\<List\<LogAuditoria\>\> | LogAuditoriaController | ⚠️ Retorna entidade, não DTO |

### Gaps de Endpoint
- 🔴 GET /logs retorna entidade direta (LogAuditoria) em vez de DTO — expõe estrutura interna
- 🔴 Nenhum endpoint de Exame (CRUD de exames não existe)
- 🔴 Nenhum endpoint de Consulta (entidade vazia)
- 🟡 Falta endpoint PUT /laudo/{id} para revisão médica
- 🟡 Falta endpoint GET /laudo/{id} para consulta de laudo
- 🟡 Falta endpoint de logout (invalidação de cookie)
- 🟡 POST /auth/registrar é público — qualquer pessoa pode criar médico

## Services

| Service | Métodos públicos | Injeção | @Transactional |
|---|---|---|---|
| AutenticacaoService | loadUserByUsername(String) | ✅ Construtor | ❌ Falta |
| TokenService | gerarToken(Usuario), getSubject(String) | ⚠️ @Value via field | ❌ N/A (stateless) |
| PacienteService | cadastrar, buscarTodosPacientes, buscarPorCpf, buscarPorId | ✅ Construtor | ✅ Sim (cadastrar, buscas read-only) |
| LaudoService | gerarPreLaudo | ✅ Construtor | ✅ Sim |
| LogAuditoriaService | buscarTodosOsLogs | ✅ Construtor | ❌ Falta @Transactional(readOnly=true) |

### Gaps de Service
- 🟡 LogAuditoriaService lança RuntimeException em vez de retorno vazio — anti-pattern
- 🟡 PacienteService.buscarPorId não tem @Transactional(readOnly=true)
- 🟡 LaudoService usa RuntimeException para erros de IO — deveria ter exception custom

## DTOs

| DTO | Tipo | Validação |
|---|---|---|
| LoginRequestDTO | record | @NotBlank em email e senha |
| MedicoRequestDTO | record | @NotBlank + @Email com messages pt-BR |
| UserDTO | record | sem validação (response) |
| UserProfileDTO | record | sem validação (response) |
| LoginResponseDTO | record | sem validação (response) |
| PacienteRequestDTO | record | @NotBlank + @CPF + @NotNull |
| PacienteResponseDTO | record | fromEntity() estático |
| LaudoGeracaoRequestDTO | record | @NotNull + @Positive |
| LaudoResponseDTO | record | fromEntity() estático |
| LaudoRevisaoRequestDTO | record | (existe mas não é usado em nenhum endpoint) |
| ExameRequestDTO | record | (existe mas não é usado) |
| ExameResponseDTO | record | (usado pelo PacienteResponseDTO) |
| ConsultaDTO | record | (vazio — placeholder) |
| GeminiLaudoResponse | record | sem validação (IA response) |

## Backlinks
- [[codebase/snapshots/backend-security-2026-06-09]]
- [[codebase/snapshots/backend-ai-agent-2026-06-09]]
- [[codebase/patterns/padrão-genericresult]]
