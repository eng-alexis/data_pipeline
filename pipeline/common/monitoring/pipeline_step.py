# Registra informações do step do pipeline

def reg_new_step(conection_db, id_exec, id_arquivo, camada, entidade, linhas_lidas, linhas_gravadas, inicio, fim, duracao):

    conx = conection_db
    cursor = conx.cursor()

    query = """INSERT INTO audit.pipeline_step(
                    id_exec,
                    id_arquivo,
                    camada,
                    entidade,
                    linhas_lidas,
                    linhas_gravadas,
                    inicio,
                    fim,
                    duracao_ms,
                    status)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
    valores = (id_exec, id_arquivo, camada, entidade, linhas_lidas, linhas_gravadas, inicio, fim, duracao,'SUCESSO')

    cursor.execute(query, valores)

    conx.commit()