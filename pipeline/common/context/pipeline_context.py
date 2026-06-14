# Retorna ID da execução

def gerar_id_contexto(conection_db):

    conx = conection_db
    cursor = conx.cursor()

    cursor.execute("""
    SELECT COALESCE(ultimo_id, 0)
    FROM audit.pipeline_watermark
    WHERE watermark_name = 'pipeline_last_id_exec';
""")

    resultado = cursor.fetchone()

    if resultado is None:
        valor = 1
    else:
        retorno = resultado[0]
        valor = retorno + 1

    return valor
    
# Atualiza o id da execução

def upd_watermark_exec(conection_db, id_exec_atual, data_execução):

    conx = conection_db
    cursor = conx.cursor()

    query = ("""UPDATE audit.pipeline_watermark
                        SET ultimo_id = %s, data_execucao = %s,
                        WHERE watermark_name = 'pipeline_last_id_exec';""")
    
    valores = (id_exec_atual, data_execução)

    cursor.execute(query, valores)

    conx.commit()

# Atualiza ultimo id armazenado na entidade/tabela

def upd_watermark_layer(conection_bd, entidade, watermark_name, data_execução):

    conx = conection_bd
    cursor = conx.cursor()

    # Busca o ultimo id da entidade (ex: id 100)

    query_1 = ("""SELECT id FROM %s
                ORDER by id DESC""")

    cursor.execute(query_1, (entidade,))
    ultimo_id = cursor.fetchone()

    # Atualiza o watermark com o valor do ultimo id da entidade

    query_2 = ("""UPDATE audit.pipeline_watermark
                        SET ultimo_id = %s, data_execucao = %s 
                         WHERE watermark_name = %s;""")
    
    valores = (ultimo_id, data_execução, watermark_name)
    
    cursor.execute(query_2, valores)
    cursor.execute(query_2, valores)

    conx.commit()
