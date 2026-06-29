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