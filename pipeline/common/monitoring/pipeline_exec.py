def reg_new_execution(connection_db, inicio, nome_arquivo, hash):

    conx = connection_db
    cursor = conx.cursor()

    query = """INSERT INTO audit.pipeline_execution (inicio,
    arquivo, hash, status)
    VALUES(%s, %s, %s, 'PROCESSANDO');"""

    valores = (inicio, nome_arquivo, hash)

    cursor.execute(query,valores)

    conx.commit()

# Atualizar execução do pipeline

def update_execution(fim, connection_db, id_exec_atual, status, mensagem):
    
    conx = connection_db
    cursor = conx.cursor()

    query = """UPDATE audit.pipeline_execution
                SET fim = %s, status = %s, mensagem = %s
                WHERE id_exec = %s;"""

    valores = (fim, status, mensagem, id_exec_atual)

    cursor.execute(query, valores)

    conx.commit()