--Tabela raw.eventos

CREATE TABLE IF NOT EXISTS raw.eventos(
    id_raw SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao_raw TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    schema_status VARCHAR(20),
    schema_version VARCHAR(20),
    schema_error TEXT
);

--Tabela raw.produtos

CREATE TABLE IF NOT EXISTS raw.produtos(
    id_raw SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabela raw.lojas

CREATE TABLE IF NOT EXISTS raw.lojas(
    id_raw SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabela raw.quarantine

CREATE TABLE IF NOT EXISTS raw.quarantine(
    id_raw SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);