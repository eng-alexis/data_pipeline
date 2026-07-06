MERGE INTO silver.eventos s USING(
            SELECT
            (dados->>'event_id')::UUID AS id_evento,
            (dados->>'event_time')::TIMESTAMP AS evento_time,
            (dados->>'emit_time')::TIMESTAMP AS emit_time,
            (dados->>'tipo_evento')::VARCHAR(20) AS tipo_evento,
            (dados->>'evento_seq')::INTEGER AS evento_seq,
            (dados->>'id_loja')::INTEGER AS id_loja,
            (dados->>'id_caixa')::INTEGER AS id_caixa,
            (dados->>'id_pedido')::INTEGER AS id_pedido,
            (dados->>'produto_id')::INTEGER AS id_produto,
            (dados->>'quantidade')::INTEGER AS quantidade,
            (dados->>'valor_unitario')::NUMERIC(6,2) AS valor_unitario,
            (id_raw)::BIGINT AS id_raw,
            (entidade)::VARCHAR(20) AS entidade,
            (data_ingestao_raw)::TIMESTAMP AS data_ingestao_raw,
            (schema_status)::VARCHAR(20) AS schema_status,
            (schema_version)::VARCHAR(20) AS schema_version,
            (observacao)::TEXT AS observacao
        FROM 
            raw.eventos
        WHERE
            id_raw > %s AND entidade = 'eventos' AND schema_status = 'VALIDO') r

            ON (r.id_evento = s.id_evento)

        WHEN NOT MATCHED THEN

        INSERT(
            id_evento,
            evento_time,
            emit_time,
            tipo_evento,
            evento_seq,
            id_loja,
            id_caixa,
            id_pedido,
            id_produto,
            quantidade,
            valor_unitario,
            pedido_uid,
            id_raw,
            data_ingestao_raw) 

        VALUES(
            r.id_evento,
            r.evento_time,
            r.emit_time,
            r.tipo_evento,
            r.evento_seq,
            r.id_loja,
            r.id_caixa,
            r.id_pedido,
            r.id_produto,
            r.quantidade,
            r.valor_unitario,
            TO_CHAR(evento_time::DATE, 'YYYYMMDD') || LPAD(id_loja::TEXT, 3, '0') || 
            LPAD(id_caixa::TEXT, 3, '0') || LPAD(id_pedido::TEXT, 6,'0'),
            r.id_raw,
            r.data_ingestao_raw);