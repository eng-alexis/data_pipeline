from psycopg2.extras import Json

# Carrega registros na tabela raw.eventos

def load_to_raw(conx, arquivo, lote, entidade, schema_version, status, obs):

    cursor = conx.cursor()

    try:

        for linha in lote:

            query = """INSERT INTO raw.eventos(arquivo_origem, dados, entidade,
                            schema_version, schema_status, observacao)
                            VALUES(%s, %s, %s, %s, %s, %s);"""

            valores = (arquivo, Json(linha), entidade, schema_version, status, obs)

            cursor.execute(query,valores)

        #conx.commit()

        return True

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return False

# Envia linhas invalidas para raw.quarentena

def load_to_quarentine(conection_db, entidade_arquivo, registro, entidade, 
                       schema_version , status, motivo):

    conx = conection_db
    cursor = conx.cursor()

    query = """INSERT INTO raw.quarantine(
                            arquivo_origem, dados, entidade, schema_version,
                            schema_status, schema_error)
                            VALUES(%s, %s, %s, %s, %s, %s);"""
    
    valores = (entidade_arquivo, Json(registro), entidade, schema_version, status, 
               motivo)

    cursor.execute(query,valores)

    conx.commit()

    return True