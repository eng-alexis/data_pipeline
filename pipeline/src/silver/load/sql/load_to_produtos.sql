MERGE INTO silver.produtos s USING(
            SELECT
            (dados->>'id')::INTEGER AS id_produto,
            (dados->>'nome')::VARCHAR(30) AS produto,
            (dados->>'valor')::NUMERIC(6,2) AS valor,
            (id_raw)::BIGINT AS id_raw,
            (entidade)::VARCHAR(20) AS entidade,
            (data_ingestao_raw)::TIMESTAMP AS data_ingestao_raw,
            (schema_status)::VARCHAR(20) AS schema_status
        FROM 
            raw.eventos
        WHERE
            id_raw > %s AND entidade = 'produtos' AND schema_status = 'VALIDO') r

        ON (r.id_produto = s.id_produto)

            WHEN NOT MATCHED THEN

            INSERT(
                id_produto,
                produto,
                valor,
                id_raw,
                data_ingestao_raw) 

            VALUES(
                r.id_produto,
                r.produto,
                r.valor,
                r.id_raw,
                r.data_ingestao_raw);