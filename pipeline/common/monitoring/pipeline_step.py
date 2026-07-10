# Registra informações do step do pipeline

def reg_new_step(conection_db, id_exec, camada, inicio, entidade=None):

    conx = conection_db
    cursor = conx.cursor()

    query = """INSERT INTO audit.pipeline_step(
                    id_exec,
                    camada,
                    entidade,
                    inicio,
                    status)
                VALUES(%s, %s, %s, %s, %s);
                """
    valores = (id_exec, camada, entidade, inicio, 'PROCESSANDO')

    cursor.execute(query, valores)

    conx.commit()
    
# Atualiza step com mais informações

def upd_step(conection_db, id_exec, camada, fim, status, duracao=None, id_arquivo=None, entidade=None, linhas_lidas=None, linhas_gravadas=None):

    conx = conection_db
    cursor = conx.cursor()

    query = """UPDATE audit.pipeline_step SET
                    id_arquivo = %s,
                    entidade = %s,
                    linhas_lidas = %s,
                    linhas_gravadas = %s,
                    fim = %s,
                    duracao_ms = %s,
                    status = %s
                WHERE id_exec = %s AND camada = %s AND entidade = %s;
                """
    
    valores = (id_arquivo, entidade, linhas_lidas, linhas_gravadas, fim, duracao, status, id_exec, camada, entidade)

    cursor.execute(query, valores)

    conx.commit()