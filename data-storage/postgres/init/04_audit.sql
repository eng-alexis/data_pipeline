CREATE TABLE IF NOT EXISTS audit.pipeline_execution(
    id_exec BIGSERIAL PRIMARY KEY,
    inicio TIMESTAMP,
    fim TIMESTAMP,
    status VARCHAR(15),

    CONSTRAINT ck_status
    CHECK ( status IN (
        'PENDENTE',
        'PROCESSANDO',
        'SUCESSO',
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