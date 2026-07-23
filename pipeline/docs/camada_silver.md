# Camada SILVER

A camada silver é responsavel pela ingestão dos dados disponibilizados pela camada Raw, realizando a padronização e separação dos dados em tabelas.

## Objetivo

* Extrair registros da tabela raw
* Realiza padronização e disponibilização dos dados.
* Registra informações de auditoria sobre o processamento.

## Fluxo da camada

    Camada RAW
        ↓
    Extração
        ↓
    Padronização
        ↓
    Persistência
        ↓
    Auditoria
        ↓
    Proxima Camada (GOLD)

## Entradas

Parâmetro | Descrição
-----|-----
execucao_id | Identificador da execução do pipeline.
id_arquivo | id do arquivo que esta sendo processado.
entidade | entidade do arquivo.

## Saidas

Essa camada não retorna dados.

## Regras

A camada utiliza um watermark como ponto de partida para extração de registros disponibilizados pela camada raw.

## Fluxo de processamento

A camada SILVER:

1. Recebe identificador da execução e do arquivo.
2. Identifica qual o ultimo registro processado pela camada.
3. Identifica qual a tabela onde serão persistidos os dados.
4. Define o script sql responsavel pela extração e persistência dos dados.
5. Filtra apenas os registros com status "valido".
6. Extrai e persiste nas tabelas do schema silver.
7. Registra informações de auditoria da camada.