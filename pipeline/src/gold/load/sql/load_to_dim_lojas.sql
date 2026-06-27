MERGE INTO gold.dim_lojas g USING(

   SELECT
      id_loja, 
      cnpj,
      bairro,
      cidade, 
      estado,
      gerente
   FROM 
      silver.lojas
   ) s

      ON (g.id_loja = s.id_loja)

      WHEN NOT MATCHED THEN

      INSERT(id_loja, cnpj, bairro, cidade, estado, gerente)

      VALUES(s.id_loja, s.cnpj, s.bairro, s.cidade, s.estado, s.gerente);