---
title: "Armazenamento de Objetos com MinIO"
type: concept
tags: [minio, backend-patterns, storage, architecture, dicom]
sources: [raw/codebase/conversations/2026-06-05-layout-state-management.md]
last_updated: 2026-06-05
---

# MinIO como Object Storage

No ecossistema Tila, o armazenamento de dados precisa lidar não apenas com textos e relacionamentos, mas também com arquivos pesados e não-estruturados, como imagens médicas (Raio-X, Tomografias), PDFs de laudos e imagens de perfil.

Para isso, utiliza-se o MinIO.

## O que é o MinIO?
MinIO é um servidor de armazenamento de objetos de alto desempenho, compatível com a API do Amazon S3. Ele roda muito bem via Docker, tornando o ambiente de desenvolvimento local idêntico à infraestrutura de cloud corporativa, onde tipicamente se utilizaria o AWS S3, Google Cloud Storage ou Azure Blob Storage.

## Por que não armazenar os arquivos no Banco de Dados Relacional?
Embora bancos relacionais suportem campos `BLOB` para armazenar binários, essa é uma prática obsoleta em arquiteturas modernas:
1. **Custos:** Bancos relacionais utilizam discos de alta performance projetados para transações. Armazenar GBs de imagens médicas tornaria o banco gigante, deixando os backups extremamente lentos e onerosos.
2. **Transferência e Streaming:** Servir um arquivo do banco de dados consome RAM e CPU valiosas da aplicação e do banco, prejudicando a performance das queries.
3. **Desacoplamento:** Object Stores lidam nativamente com uploads/downloads paralelos e podem fazer distribuição geográfica (CDN) muito mais fácil.

## Padrões de Uso no Tila

### 1. Upload de Arquivos (Ex: Laudos / Imagens de Exames)
Quando o sistema Tila faz o upload da imagem de um exame de paciente (DICOM, PNG, JPEG):
- O backend recebe o arquivo e o envia diretamente para o container do MinIO num bucket específico (ex: `tila-exames`).
- O MinIO salva o objeto e devolve uma chave do caminho, ex: `s3://tila-exames/2026/06/exame_12345.png`.
- O backend **salva apenas este caminho textual no banco de dados** (PostgreSQL).

### 2. Download e Acesso Seguro (Presigned URLs)
Quando a tela do Prontuário precisa exibir a imagem do exame:
- O frontend pede ao backend os dados do exame.
- O backend consulta o caminho no banco.
- O backend, via SDK do S3/MinIO, assina digitalmente uma **URL Temporária (Presigned URL)** válida por pouco tempo (ex: 1 hora).
- O backend devolve essa URL ao Angular.
- O navegador faz o download da imagem direto do servidor MinIO, desonerando o backend de processar o tráfego pesado da foto, ao mesmo tempo garantindo a segurança de que apenas quem possui a URL assinada pode ver a imagem do paciente.

## Backlinks
- [[wiki/sources/layout-state-management]]
- [[wiki/concepts/redis-cache-patterns]]
- [[wiki/concepts/angular-state-management]]
