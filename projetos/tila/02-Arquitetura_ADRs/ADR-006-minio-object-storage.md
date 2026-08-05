---
title: "ADR-006: MinIO Object Storage"
type: decision
tags: [architecture, adr, minio, storage]
sources: [wiki/concepts/minio-object-storage.md]
last_updated: 2026-06-06
---

# ADR-006: MinIO Object Storage

## Status
Accepted

## Context
O sistema TILA processa exames de imagens médicas (DICOM, PNG, JPEG) e gera laudos clínicos em PDF. Armazenar arquivos binários pesados diretamente no banco de dados relacional (PostgreSQL) degrada a performance do banco, encarece os backups e não escala de forma eficiente. É necessário desacoplar o armazenamento desses arquivos estáticos de grande porte.

## Decision
Adotaremos o **MinIO** como serviço de Object Storage (compatível com a API S3 da AWS):
1. **Upload**: O backend recebe os arquivos binários dos exames e laudos e faz o upload para buckets organizados no MinIO (ex: `tila-exames`, `tila-laudos`).
2. **Referência Relacional**: O banco PostgreSQL salvará apenas a URI textual de referência do arquivo (ex: `s3://tila-exames/2026/06/exame_123.png`).
3. **Acesso Seguro via Presigned URLs**: O frontend não acessará o MinIO diretamente nem o backend trafegará bytes pesados em todas as leituras. O backend gerará URLs Temporárias Assinadas (Presigned URLs) com validade curta (ex: 1 hora) para o frontend baixar as imagens diretamente do servidor de arquivos.

## Alternatives Considered

### Alternativa 1: Armazenamento em arquivos locais (Local File System)
Rejeitada porque impede escalabilidade horizontal e resiliência (dificulta a utilização em arquiteturas cloud multi-instância e dificulta backups consistentes sem downtime).

### Alternativa 2: Gravação em BLOB no banco de dados
Rejeitada devido aos altos custos operacionais de disco transacional, aumento do tamanho de backups relacionais e sobrecarga desnecessária de CPU e memória RAM no servidor PostgreSQL.

## Consequences

### Positivas
- Banco de dados relacional leve e ágil (guardando apenas metadados e caminhos textuais).
- Segurança de acesso via URLs assinadas e de tempo limitado.
- Infraestrutura local Dockerizada idêntica ao ambiente produtivo (S3/GCS/Azure Blob).

### Negativas
- Necessidade de gerenciar credenciais, buckets e políticas no MinIO.
- Latência extra pequena de rede no upload (backend -> MinIO).

### Riscos
- Links expirados no frontend se o médico deixar a aba aberta por mais de 1 hora (mitigado solicitando uma nova URL ao focar a aba ou recarregar).

## Backlinks
- [[wiki/concepts/minio-object-storage]]
- [[wiki/concepts/redis-cache-patterns]]
