CREATE TABLE IF NOT EXISTS gold.fato_vendas(
    id_fato BIGSERIAL,
    id_silver BIGINT,
    data DATE,
    hora TIME,
    inicio_hora TIME,
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

CREATE TABLE IF NOT EXISTS gold.dim_calendario(
    data DATE,
    ano INT,
    semestre INT,
    trimestre INT,
    mes VARCHAR(2),
    mes_abreviado VARCHAR(3),
    mes_nome VARCHAR(15),
    dia INT,
    dia_nome VARCHAR(15)
);