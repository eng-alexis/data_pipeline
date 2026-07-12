MERGE INTO gold.dim_calendario gdc USING(

    SELECT DISTINCT(
            data) AS data,
            EXTRACT (YEAR FROM data::DATE) AS ano,
            CASE WHEN EXTRACT (MONTH FROM data::DATE) <= 6 THEN 1 ELSE 2 END AS semestre,
            EXTRACT(QUARTER FROM data::DATE) AS trimestre,
            TO_CHAR(data::DATE, 'MM') AS mes,

            CASE EXTRACT(MONTH FROM data::DATE)
            WHEN 1 THEN 'Jan' WHEN 2 THEN 'Fev' WHEN 3 THEN 'Mar' WHEN 4 THEN 'Abr'
            WHEN 5 THEN 'Mai' WHEN 6 THEN 'Jun' WHEN 7 THEN 'Jul' WHEN 8 THEN 'Ago'
            WHEN 9 THEN 'Set' WHEN 10 THEN 'Out' WHEN 11 THEN 'Nov' ELSE 'Dez' END AS mes_abreviado,

            --TO_CHAR(data::DATE,'mon') AS mes_abreviado,
            TO_CHAR(data::DATE, 'Month') AS mes_nome,
            EXTRACT(WEEK FROM data::DATE) AS semana,
            EXTRACT(DOW FROM data::DATE) AS dia_semana,

            CASE EXTRACT(DOW FROM data::DATE)
            WHEN 0 THEN 'Dom' WHEN 1 THEN 'Seg' WHEN 2 THEN 'Ter'
            WHEN 3 THEN 'Qua' WHEN 4 THEN 'Qui' WHEN 5 THEN 'Sex'
            ELSE 'Sab' END AS dia_nome
            
    FROM gold.fato_vendas
    WHERE id_fato > %s) gfv 

    ON (gfv.data = gdc.data)

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
        gfv.data,
        gfv.ano,
        gfv.semestre,
        gfv.trimestre,
        gfv.mes,
        gfv.mes_abreviado,
        gfv.mes_nome,
        gfv.semana,
        gfv.dia_semana,
        gfv.dia_nome
    );