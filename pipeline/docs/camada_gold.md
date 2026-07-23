# Camada GOLD

A camada Gold é responsavel por disponibilizar dados prontos para analises de negócio, realizando transformações dos dados disponibilizados pela camada silver.

## Objetivo

* Extrair registros das tabelas silver.
* Gerar e disponibilizar tabela de dimensão calêndario.
* Realiza transformações para enriquecimento dos dados.
* Persistir dados em tabelas fato e dimensão.
* Registra informações de auditoria sobre o processamento.

## Fluxo da camada

    Camada SILVER
        ↓
    Extração
        ↓
    Transformação
        ↓
    Persistência
        ↓
    Auditoria
        ↓
    Relatorio BI

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

A camada Gold:

1. Recebe identificador da execução e do arquivo.
2. Identifica qual o ultimo registro processado pela camada.
3. Identifica qual a tabela onde serão persistidos os dados.
4. Define o script sql responsavel pela extração, transformação e persistência dos dados.
5. Extrai e realiza as transformações nos dados.
6. Persiste dados transformados nas tabelas do schema Gold.
7. Gera tabela dimensão calêndario.
8. Registra informações de auditoria da camada.