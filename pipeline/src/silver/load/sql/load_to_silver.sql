MERGE INTO silver.eventos s USING(
            SELECT
            (dados->>'event_id')::UUID AS evento_id,
            (dados->>'event_time')::TIMESTAMP AS evento_time,
            (dados->>'emit_time')::TIMESTAMP AS emit_time,
            (dados->>'tipo_evento')::VARCHAR(20) AS tipo_evento,
            (dados->>'evento_seq')::INTEGER AS evento_seq,
            (dados->>'id_loja')::INTEGER AS id_loja,
            (dados->>'id_caixa')::INTEGER AS id_caixa,
            (dados->>'id_pedido')::INTEGER AS id_pedido,
            (dados->>'produto_id')::INTEGER AS produto_id,
            (dados->>'quantidade')::INTEGER AS quantidade,
            (dados->>'valor_unitario')::NUMERIC(6,2) AS valor_unitario,
            (id_raw)::BIGINT AS id_raw,
            (data_ingestao_raw)::TIMESTAMP AS data_ingestao_raw,
            (schema_status)::VARCHAR(20) AS schema_status,
            (schema_version)::VARCHAR(20) AS schema_version,
            (observacao)::TEXT AS observacao
        FROM 
            raw.eventos
        WHERE
            id_raw > %s AND schema_status = 'VALIDO') r

            ON (r.evento_id = s.evento_id)

        WHEN NOT MATCHED THEN

        INSERT(
            evento_id,
            evento_time,
            emit_time,
            tipo_evento,
            evento_seq,
            id_loja,
            id_caixa,
            id_pedido,
            produto_id,
            quantidade,
            valor_unitario,
            id_raw,
            data_ingestao_raw) 

        VALUES(
            r.evento_id,
            r.evento_time,
            r.emit_time,
            r.tipo_evento,
            r.evento_seq,
            r.id_loja,
            r.id_caixa,
            r.id_pedido,
            r.produto_id,
            r.quantidade,
            r.valor_unitario,
            r.id_raw,
            r.data_ingestao_raw);