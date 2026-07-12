# Registra nova execução e define o id da execução

def reg_new_execution(connection_db, id_exec, inicio):

    conx = connection_db
    cursor = conx.cursor()

    query = """INSERT INTO audit.pipeline_execution (id_exec, inicio, status)
    VALUES(%s, %s, 'PROCESSANDO');"""

    valores = (id_exec, inicio)
    cursor.execute(query, valores)

    return True

# Atualizar execução do pipeline

def update_execution(connection_db, id_exec, fim, status, arquivo=None, motivo=None, mensagem=None):
    
    conx = connection_db
    cursor = conx.cursor()

    query = """UPDATE audit.pipeline_execution
                SET fim = %s, arquivo = %s, status = %s, motivo = %s, mensagem = %s
                WHERE id_exec = %s;"""

    valores = (fim, arquivo, status, motivo, mensagem, id_exec)

    cursor.execute(query, valores)
    conx.commit()