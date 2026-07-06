from psycopg2 import sql

# Retorna ID da execução

def gerar_id_contexto(conection_db):

    conx = conection_db
    cursor = conx.cursor()

    cursor.execute("""
    SELECT COALESCE(ultimo_id, 0)
    FROM audit.pipeline_watermark
    WHERE watermark_name = 'context_last_id';
    """)

    resultado = cursor.fetchone()[0]

    if resultado is None:
        valor = 1
    else:
        retorno = resultado
        valor = retorno + 1

    return valor
    
# Atualiza o id da execução

def upd_watermark_exec(conection_db, id_exec_atual, data_execução):

    conx = conection_db
    cursor = conx.cursor()

    query = ("""UPDATE audit.pipeline_watermark
                        SET ultimo_id = %s, data_execucao = %s
                        WHERE watermark_name = 'context_last_id';""")
    
    valores = (id_exec_atual, data_execução)

    cursor.execute(query, valores)

    conx.commit()

# Retorna o ultimo id processado pela etapa

def get_ultimo_id(conection_db, watermark_name):
    
    conx = conection_db
    cursor = conx.cursor()

    query = """SELECT COALESCE(ultimo_id, 0) FROM audit.pipeline_watermark
                WHERE watermark_name = %s;"""
    
    cursor.execute(query,(watermark_name,))

    return cursor.fetchone()[0]


# Atualiza ultimo id armazenado na entidade/tabela

def upd_watermark_layer(conection_bd, column_name, table_name, watermark_name, data_execução):

    conx = conection_bd
    cursor = conx.cursor()

    # Busca o ultimo id da entidade (ex: id 100)

    query_1 = f"""SELECT MAX({column_name}) FROM {table_name};"""
    # valores = (id, entidade)

    cursor.execute(query_1)
    ultimo_id = cursor.fetchone()[0]

    # Atualiza o watermark com o valor do ultimo id da entidade

    query_2 = ("""UPDATE audit.pipeline_watermark
                        SET ultimo_id = %s, data_execucao = %s 
                         WHERE watermark_name = %s;""")
    
    valores = (ultimo_id, data_execução, watermark_name)
    
    cursor.execute(query_2, valores)

    conx.commit()