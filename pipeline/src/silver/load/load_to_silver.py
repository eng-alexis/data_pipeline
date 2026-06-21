# Descobrir ultimo id processado (watermark)
from pipeline.common.database.conx_database import get_db_connection
from pipeline.config.paths import SQL_LOAD_TO_EVENTOS, SQL_LOAD_TO_LOJAS, SQL_LOAD_TO_PRODUTOS

conx = get_db_connection()

def get_ultimo_id(conection_db, watermark_name):
    
    conx = conection_db
    cursor = conx.cursor()

    query = """SELECT COALESCE(ultimo_id, 0) FROM audit.pipeline_watermark
                WHERE watermark_name = %s;"""
    
    cursor.execute(query,(watermark_name,))

    return cursor.fetchone()[0]

# Realizar extração

def load_to_silver(conection_db, ultimo_id, entidade, script_sql):

    conx = conection_db
    cursor = conx.cursor()

    sql_inject_file = script_sql

    with open(sql_inject_file,'r', encoding='utf-8') as sql:
        comando = sql.read()

        cursor.execute(comando, (ultimo_id,))
        linhas_lidas = cursor.rowcount


        linhas_load = f"""SELECT COUNT(*) FROM silver.{entidade}
                                WHERE id_raw > %s;"""
        
        cursor.execute(linhas_load,(ultimo_id,))
        linhas_gravadas = cursor.fetchone()[0]

        conx.commit()

    return linhas_lidas, linhas_gravadas

# Retorna o script sql correto com base na entidade

def descobrir_script_sql(entidade):

    entidade_1 = "eventos"
    entidade_2 = "produtos"
    entidade_3 = "lojas"

    if entidade == entidade_1:
        return SQL_LOAD_TO_EVENTOS
    
    elif entidade == entidade_2:
        return SQL_LOAD_TO_PRODUTOS

    elif entidade == entidade_3:
        return SQL_LOAD_TO_LOJAS

    else:
        return print(f"Script sql não encontrado para essa entidade {entidade}")