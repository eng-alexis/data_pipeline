# Carregar registros nas tabelas silver

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