--Tabela raw.eventos

CREATE TABLE IF NOT EXISTS raw.eventos(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabela raw.produtos

CREATE TABLE IF NOT EXISTS raw.produtos(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabela raw.lojas

CREATE TABLE IF NOT EXISTS raw.lojas(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--Tabela raw.quarantine

CREATE TABLE IF NOT EXISTS raw.quarantine(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);