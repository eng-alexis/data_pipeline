-- Tabela silver.eventos

CREATE TABLE IF NOT EXISTS silver.eventos(
    evento_id   UUID,
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
    id_pipeline_exec BIGINT,
    data_ingestao TIMESTAMP
);

-- Tabela silver.produtos

CREATE TABLE IF NOT EXISTS silver.produtos(
    produto_id INTEGER,
    produto    VARCHAR(30),
    valor      NUMERIC(6,2)
);

-- Tabela silver.lojas

CREATE TABLE IF NOT EXISTS silver.loja(
    loja_id INTEGER,
    caixas  JSONB
);
