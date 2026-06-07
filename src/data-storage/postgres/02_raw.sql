--Tabela raw.eventos

CREATE TABLE raw.eventos(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAUT CURRENT_TIMESTAMP
);

--Tabela raw.produtos

CREATE TABLE raw.produtos(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAUT CURRENT_TIMESTAMP
);

--Tabela raw.lojas

CREATE TABLE raw.lojas(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAUT CURRENT_TIMESTAMP
);

--Tabela raw.quarantine

CREATE TABLE raw.quarantine(
    id SERIAL PRIMARY KEY,
    arquivo_origem TEXT,
    dados JSONB,
    data_ingestao TIMESTAMP DEFAUT CURRENT_TIMESTAMP
);