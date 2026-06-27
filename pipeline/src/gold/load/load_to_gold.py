from pipeline.config.paths import SQL_LOAD_TO_FATO_VENDAS, SQL_LOAD_TO_DIM_PRODUTOS, SQL_LOAD_TO_DIM_LOJAS

# Encontrar ultimo id na tabela de auditoria

def get_ultimo_id(conexao_db):

    conx = conexao_db
    cursor = conx.cursor()

    query = """SELECT COALESCE(ultimo_id, 0)
                FROM audit.pipeline_watermark
                WHERE watermark_name = 'silver.eventos_last_id'"""
    
    cursor.execute(query)

    return cursor.fetchone()[0]

# Encontrar script sql de load

def find_script_sql(entidade):

    if entidade == "eventos":
        script = SQL_LOAD_TO_FATO_VENDAS

    elif entidade == "produtos":
        script = SQL_LOAD_TO_DIM_PRODUTOS

    elif entidade == "lojas":
        script = SQL_LOAD_TO_DIM_LOJAS

    else:
        print("entidade não encontrada")

    return script

# Carregar registros nas tabelas gold

def load_to_gold(conexao_db, script_load, ultimo_id):
   
    conx = conexao_db
    cursor = conx.cursor()
    sql_inject_file = script_load

    with open(sql_inject_file, 'r', encoding='utf-8') as sql:

        comando = sql.read()

        cursor.execute(comando,(ultimo_id,))
        linhas_lidas = cursor.rowcount
        
        linhas_load = f"""SELECT COUNT(*) FROM gold.fato_vendas
                        WHERE id_silver > %s;"""
        
        cursor.execute(linhas_load,(ultimo_id,))
        linhas_gravadas = cursor.fetchone()[0]

        conx.commit()

    return linhas_lidas, linhas_gravadas

# Atualizar watermark

def upd_watermark(conexao_db):

    conx = conexao_db
    cursor = conx.cursor()

    query_1 = """SELECT id_silver FROM silver.eventos ORDER BY id_silver DESC LIMIT 1;"""
    cursor.execute(query_1)
    ultimo_id = cursor.fetchone()[0]

    query_2 = """UPDATE audit.pipeline_watermark
                    SET ultimo_id = %s
                    WHERE watermark_name = 'silver.eventos_last_id'"""
    
    cursor.execute(query_2,(ultimo_id,))

    return True