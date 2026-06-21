MERGE INTO silver.lojas s USING(
            SELECT
            (dados->>'ID')::INTEGER AS id_loja,
            (dados->>'CNPJ')::VARCHAR(20) AS cnpj,
            (dados->>'Endereço')::VARCHAR(60) AS endereco,
            (dados->>'Bairro')::VARCHAR(30) AS bairro,
            (dados->>'Cidade')::VARCHAR(30) AS cidade,
            (dados->>'Estado')::VARCHAR(30) AS estado,
            (dados->>'Gerente')::VARCHAR(30) AS gerente,
            (dados->>'Horário_de_Atendimento')::VARCHAR(60) AS horario_atendimento,
            (id_raw)::BIGINT AS id_raw,
            (data_ingestao_raw)::TIMESTAMP AS data_ingestao_raw,
            (entidade)::VARCHAR(20) AS entidade,
            (schema_status)::VARCHAR(20) AS schema_status

        FROM 
            raw.eventos
        WHERE
            id_raw > %s AND entidade = 'lojas' AND schema_status = 'VALIDO') r
        
            ON (r.id_loja = s.id_loja)

        WHEN NOT MATCHED THEN

        INSERT(
            id_loja,
            cnpj,
            endereco,
            bairro,
            cidade,
            estado,
            gerente,
            horario_atendimento,
            id_raw,
            data_ingestao_raw)

        VALUES(
            r.id_loja,
            r.cnpj,
            r.endereco,
            r.bairro,
            r.cidade,
            r.estado,
            r.gerente,
            r.horario_atendimento,
            r.id_raw,
            r.data_ingestao_raw);