MERGE INTO gold.dim_produtos g USING(
    
    SELECT 
        id_produto,
        produto,
        valor 
    FROM 
        silver.produtos
    ) s

        ON (g.id_produto = s.id_produto)

        WHEN NOT MATCHED THEN

        INSERT(id_produto, produto, valor)
        VALUES(s.id_produto, s.produto, s.valor);