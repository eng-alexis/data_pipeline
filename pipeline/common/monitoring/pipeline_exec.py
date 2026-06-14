# Registra nova execução e define o id da execução

def reg_new_execution(connection_db, id_exec, inicio, nome_arquivo, hash):

    conx = connection_db
    cursor = conx.cursor()

    query = """INSERT INTO audit.pipeline_execution (id_exec, inicio,
    arquivo, hash, status)
    VALUES(%s, %s, %s, %s, 'PROCESSANDO')
    ;"""

    valores = (id_exec, inicio, nome_arquivo, hash)
    cursor.execute(query, valores)

    return True


# Atualizar execução do pipeline

def update_execution(connection_db, id_exec_atual, fim, status, mensagem):
    
    conx = connection_db
    cursor = conx.cursor()

    query = """UPDATE audit.pipeline_execution
                SET fim = %s, status = %s, mensagem = %s
                WHERE id_exec = %s;"""

    valores = (fim, status, mensagem, id_exec_atual)

    cursor.execute(query, valores)