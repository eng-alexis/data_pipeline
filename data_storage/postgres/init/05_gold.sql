CREATE TABLE IF NOT EXISTS gold.fato_vendas(
    id_fato BIGSERIAL,
    id_silver BIGINT,
    data DATE,
    hora TIME,
    id_loja INT,
    id_caixa INT,
    id_pedido BIGINT,
    id_produto INT,
    quantidade INT,
    valor_total NUMERIC(6,2)
);

CREATE TABLE IF NOT EXISTS gold.dim_produtos(
    id_produto BIGINT,
    produto VARCHAR (30),
    valor NUMERIC (6,2)
);

CREATE TABLE IF NOT EXISTS gold.dim_lojas(
    id_loja INT,
    cnpj VARCHAR(20),
    bairro VARCHAR(30),
    cidade VARCHAR(30), 
    estado VARCHAR(30),
    gerente VARCHAR(60)
);