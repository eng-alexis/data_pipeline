# DATABASE

O database `PDV_SALES` é responsável por armazenar e organizar os dados
provenientes dos arquivos gerados pelo sistema PDV, desde sua ingestão
em formato bruto até sua transformação em dados destinados à análise.

## Tecnologia

- PostgreSQL
- Docker

O PostgreSQL é executado em um container Docker para facilitar a
padronização do ambiente de desenvolvimento.

## Schemas

![Database](../../images/database/database_v3.png)

O database é composto por quatro schemas, cada um com uma responsabilidade
específica dentro do pipeline:

- `RAW` — dados brutos provenientes da origem;
- `SILVER` — dados tratados, validados e padronizados;
- `GOLD` — dados modelados para análise;
- `AUDIT` — informações de controle e histórico do pipeline.

## Fluxo dos dados

Arquivos gerados pelo PDV
↓
`RAW`
↓
`SILVER`
↓
`GOLD`
↓
Power BI

Paralelamente, as execuções e o processamento dos arquivos são registrados
no schema `AUDIT`.

## Schema RAW

### Objetivo

Armazenar os registros em sua forma mais próxima possível da origem,
preservando os dados para auditoria e reprocessamento.

| Tabela | Descrição |
|---|---|
| `raw.eventos` | Armazena os eventos brutos recebidos. |
| `raw.quarantine` | Armazena registros considerados inválidos durante a validação. |

## Schema SILVER

### Objetivo

Armazenar dados válidos, tratados e padronizados, fornecendo uma base
confiável para as transformações analíticas.

| Tabela | Descrição |
|---|---|
| `silver.eventos` | Armazena eventos válidos e tratados. |
| `silver.lojas` | Armazena informações das lojas. |
| `silver.produtos` | Armazena o catálogo de produtos. |

## Schema GOLD

### Objetivo

Disponibilizar dados modelados para análises de negócio.

| Tabela | Descrição |
|---|---|
| `gold.fato_vendas` | Armazena os eventos de venda do tipo `item_adicionado` em estrutura de fato. |
| `gold.dim_lojas` | Dimensão contendo informações das lojas. |
| `gold.dim_produtos` | Dimensão contendo informações dos produtos. |
| `gold.dim_calendario` | Dimensão contendo informações de datas. |

## Schema AUDIT

### Objetivo

Registrar informações de controle e histórico das execuções do pipeline.

| Tabela | Descrição |
|---|---|
| `audit.pipeline_cycle` | Registra os ciclos de execução do pipeline. |
| `audit.pipeline_execution` | Registra cada execução individual do pipeline. |
| `audit.pipeline_step` | Registra o processamento de cada etapa. |
| `audit.pipeline_watermark` | Controla o último ID processado por cada camada. |
| `audit.file_history` | Registra informações dos arquivos processados. |