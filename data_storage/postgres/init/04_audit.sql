-- Tabelas de auditoria

CREATE TABLE IF NOT EXISTS audit.pipeline_execution(
    id_exec BIGINT PRIMARY KEY,
    inicio TIMESTAMP,
    fim TIMESTAMP,
    arquivo VARCHAR(50),
    hash VARCHAR(64),
    status VARCHAR(15),
    mensagem VARCHAR(50),

    CONSTRAINT ck_status
    CHECK ( status IN (
        'PROCESSANDO',
        'SUCESSO',
        'DUPLICADO',
        'ERRO'))
);

CREATE TABLE IF NOT EXISTS audit.file_history(
    id_arquivo BIGSERIAL PRIMARY KEY,
    hash VARCHAR(64),
    nome_arquivo VARCHAR(100),
    tamanho_bytes BIGINT,
    data_ingestao TIMESTAMP,
    id_exec BIGINT,
    status VARCHAR(15),

    CONSTRAINT fk_id_exec 
    FOREIGN KEY (id_exec)
    REFERENCES audit.pipeline_execution(id_exec),

    CONSTRAINT uq_hash 
    UNIQUE(hash),

    CONSTRAINT ck_status
    CHECK ( status IN (
        'PROCESSADO',
        'ERRO'))
);

CREATE TABLE IF NOT EXISTS audit.pipeline_step(
    id_step BIGSERIAL PRIMARY KEY,
    id_exec BIGINT,
    id_arquivo BIGINT,
    camada VARCHAR(15),
    entidade VARCHAR(30),
    linhas_lidas INTEGER,
    linhas_gravadas INTEGER,
    inicio TIMESTAMP,
    fim TIMESTAMP,
    duracao_ms BIGINT,
    status VARCHAR(15),

    CONSTRAINT fk_id_exec
    FOREIGN KEY (id_exec)
    REFERENCES audit.pipeline_execution(id_exec),

    CONSTRAINT fk_file_name 
    FOREIGN KEY (id_arquivo)
    REFERENCES audit.file_history(id_arquivo)
);

CREATE TABLE audit.pipeline_watermark(
    id_watermark SERIAL,
    watermark_name VARCHAR(40),
    ultimo_id INTEGER,
    data_execucao TIMESTAMP
);

INSERT INTO audit.pipeline_watermark(watermark_name) VALUES('context_last_id');
INSERT INTO audit.pipeline_watermark(watermark_name) VALUES('raw.eventos_last_id');
INSERT INTO audit.pipeline_watermark(watermark_name) VALUES('silver.eventos_last_id');