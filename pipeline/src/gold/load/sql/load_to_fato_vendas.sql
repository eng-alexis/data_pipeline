MERGE INTO gold.fato_vendas g USING(

    SELECT 
        evento_time::DATE AS data, 
        evento_time::TIME AS hora,
        id_loja,
        id_caixa,
        id_pedido,
        produto_id,
        quantidade,
        (quantidade * valor_unitario) AS valor_total,
        id_silver
    FROM 
        silver.eventos 
    WHERE
        tipo_evento = 'item adicionado' 
    AND id_silver > %s) s

    ON (s.id_silver = g.id_silver)

    WHEN NOT MATCHED THEN

    INSERT(
        id_silver,
        data,
        hora,
        id_loja,
        id_caixa,
        id_pedido,
        id_produto,
        quantidade,
        valor_total)
        
    VALUES(
        s.id_silver,
        s.data,
        s.hora,
        s.id_loja,
        s.id_caixa,
        s.id_pedido,
        s.produto_id,
        s.quantidade,
        s.valor_total);