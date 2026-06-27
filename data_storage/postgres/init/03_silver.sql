-- Tabela silver.eventos

CREATE TABLE IF NOT EXISTS silver.eventos(
    id_silver   BIGSERIAL,
    id_evento   UUID,
    evento_time TIMESTAMP,
    emit_time   TIMESTAMP,
    tipo_evento VARCHAR(20),
    evento_seq  INTEGER,
    id_loja     INTEGER,
    id_caixa    INTEGER,
    id_pedido   INTEGER,
    produto_id  INTEGER,
    quantidade  INTEGER,
    valor_unitario NUMERIC(6,2),
    id_raw BIGINT,
    data_ingestao_raw TIMESTAMP
);

-- Tabela silver.produtos

CREATE TABLE IF NOT EXISTS silver.produtos(
    id_produto INTEGER,
    produto    VARCHAR(30),
    valor      NUMERIC(6,2),
    id_raw BIGINT,
    data_ingestao_raw TIMESTAMP
);

-- Tabela silver.lojas

CREATE TABLE IF NOT EXISTS silver.lojas(
    id_loja INTEGER,
    cnpj VARCHAR(20),
    endereco VARCHAR(60),
    bairro VARCHAR(30),
    cidade VARCHAR(30),
    estado VARCHAR(30),
    gerente VARCHAR(60),
    horario_atendimento VARCHAR(30),
    id_raw BIGINT,
    data_ingestao_raw TIMESTAMP
);