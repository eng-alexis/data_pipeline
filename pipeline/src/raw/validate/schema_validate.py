from pipeline.src.raw.validate.schema_version import EventoSchema_V1

from pydantic import ValidationError

# Valida cada linha

def schema_validation(linha):

    try:

        EventoSchema_V1(**linha)

        return "VALIDO", None

        

    except ValidationError as e:

        return "INVALIDO", str(e)

# Envia linhas invalidas para quarentena

from psycopg2.extras import Json
# Gera alerta

def load_to_quarentine(conection_db, registro, nome_arquivo, status, motivo):

    conx = conection_db
    cursor = conx.cursor()

    query = """INSERT INTO raw.quarantine(
                            arquivo_origem, dados, schema_version,
                            schema_status, schema_error)
                            VALUES(%s, %s, %s, %s, %s);"""
    
    valores = (nome_arquivo, Json(registro), 'V1', status, motivo)

    cursor.execute(query,valores)

    conx.commit()

    return