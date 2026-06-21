--Tabela raw.eventos

CREATE TABLE IF NOT EXISTS raw.eventos(
    id_raw SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    entidade VARCHAR(20),
    data_ingestao_raw TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    schema_version VARCHAR(20),
    schema_status VARCHAR(20),
    observacao TEXT
);

--Tabela raw.quarantine

CREATE TABLE IF NOT EXISTS raw.quarantine(
    id_raw SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    entidade VARCHAR(20),
    data_ingestao_raw TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    schema_version VARCHAR(20),
    schema_status VARCHAR(20),
    schema_error TEXT
);