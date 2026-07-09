MERGE INTO gold.dim_calendario g USING(

    SELECT
            evento_time::DATE AS data,
            EXTRACT (YEAR FROM evento_time::DATE) AS ano,
            CASE WHEN EXTRACT (MONTH FROM evento_time::DATE) <= 6 THEN 1 ELSE 2 END AS semestre,
            EXTRACT(QUARTER FROM evento_time::DATE) AS trimestre,
            TO_CHAR(evento_time::DATE, 'MM') AS mes,

            CASE EXTRACT(MONTH FROM evento_time::DATE)
            WHEN 1 THEN 'Jan' WHEN 2 THEN 'Fev' WHEN 3 THEN 'Mar' WHEN 4 THEN 'Abr'
            WHEN 5 THEN 'Mai' WHEN 6 THEN 'Jun' WHEN 7 THEN 'Jul' WHEN 8 THEN 'Ago'
            WHEN 9 THEN 'Set' WHEN 10 THEN 'Out' WHEN 11 THEN 'Nov' ELSE 'Dez' END AS mes_abreviado,

            --TO_CHAR(evento_time::DATE,'mon') AS mes_abreviado,
            TO_CHAR(evento_time::DATE, 'Month') AS mes_nome,
            EXTRACT(WEEK FROM evento_time::DATE) AS semana,
            EXTRACT(DOW FROM evento_time::DATE) AS dia_semana,

            CASE EXTRACT(DOW FROM evento_time::DATE)
            WHEN 0 THEN 'Dom' WHEN 1 THEN 'Seg' WHEN 2 THEN 'Ter'
            WHEN 3 THEN 'Qua' WHEN 4 THEN 'Qui' WHEN 5 THEN 'Sex'
            ELSE 'Sab' END AS dia_nome
            
    FROM silver.eventos
    WHERE id_raw = %s) s

    ON (g.data = s.data)

    WHEN NOT MATCHED THEN

    INSERT(
        data,
        ano,
        semestre,
        trimestre,
        mes,
        mes_abreviado,
        mes_nome,
        semana,
        dia_semana,
        dia_nome)

    VALUES(
        s.data,
        s.ano,
        s.semestre,
        s.trimestre,
        s.mes,
        s.mes_abreviado,
        s.mes_nome,
        s.semana,
        s.dia_semana,
        s.dia_nome
    );