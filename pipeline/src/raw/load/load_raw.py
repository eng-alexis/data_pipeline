from psycopg2.extras import Json

# descobre a entidade com base no nome do arquivo

def descobrir_entidade(arquivo):

    entidade_1 = "catalogo"
    entidade_2 = "lojas"
    entidade_3 = "eventos"

    if entidade_1 in arquivo.name:
        return "produtos"
    
    elif entidade_2 in arquivo.name:
        return entidade_2
    
    elif "20" in arquivo.name:
        return entidade_3
    
    else:
        return print("entidade não identificada")

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

        conx.commit()

        return True

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")

# Envia linhas invalidas para raw.quarentena

def load_to_quarentine(conection_db, entidade_arquivo, registro, entidade, schema_version , status, motivo):

    conx = conection_db
    cursor = conx.cursor()

    query = """INSERT INTO raw.quarantine(
                            arquivo_origem, dados, entidade, schema_version,
                            schema_status, schema_error)
                            VALUES(%s, %s, %s, %s, %s, %s);"""
    
    valores = (entidade_arquivo, Json(registro), entidade, schema_version, status, motivo)

    cursor.execute(query,valores)

    conx.commit()

    return True