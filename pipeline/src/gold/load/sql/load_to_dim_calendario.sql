MERGE INTO gold.dim_calendario g USING(

    SELECT
            evento_time::DATE AS data,
            EXTRACT (YEAR FROM evento_time::DATE) AS ano,
            CASE WHEN EXTRACT (MONTH FROM evento_time::DATE) <= 6 THEN 1 ELSE 2 END AS semestre,
            EXTRACT(QUARTER FROM evento_time::DATE) AS trimestre,
            TO_CHAR(evento_time::DATE, 'MM') AS mes,
            TO_CHAR(evento_time::DATE,'mon') AS mes_abreviado,
            TO_CHAR(evento_time::DATE, 'Month') AS mes_nome,
            EXTRACT(DAY FROM evento_time::DATE) AS dia,
            TO_CHAR(evento_time::DATE, 'Day') AS dia_nome
            
    FROM silver.eventos
    WHERE id_silver = %s) s

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
        dia,
        dia_nome)

    VALUES(
        s.data,
        s.ano,
        s.semestre,
        s.trimestre,
        s.mes,
        s.mes_abreviado,
        s.mes_nome,
        s.dia,
        s.dia_nome
    );