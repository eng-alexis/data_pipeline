# Descobrir ultimo id processado (watermark)
from pipeline.common.database.conx_database import get_db_connection

conx = get_db_connection()

def get_ultimo_id(conection_db, watermark_name):
    
    conx = conection_db
    cursor = conx.cursor()

    query = """SELECT COALESCE(ultimo_id, 0) FROM audit.pipeline_watermark
                WHERE watermark_name = %s;"""
    
    cursor.execute(query,(watermark_name,))

    return cursor.fetchone()[0]

# Realizar extração

def load_to_silver(conection_db, ultimo_id, script_sql):

    conx = conection_db
    cursor = conx.cursor()
    id_anterior = ultimo_id

    sql_inject_file = script_sql

    with open(sql_inject_file,'r', encoding='utf-8') as sql:
        comando = sql.read()

        cursor.execute(comando,(ultimo_id,))
        linhas_lidas = cursor.rowcount

        linhas_load = """SELECT COUNT(*) FROM silver.eventos
                                WHERE id_raw > %s;"""
        
        cursor.execute(linhas_load,(ultimo_id,))
        linhas_gravadas = cursor.fetchone()[0]

        conx.commit()

    return linhas_lidas, linhas_gravadas