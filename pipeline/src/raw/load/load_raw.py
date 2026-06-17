from psycopg2.extras import Json

from pipeline.src.raw.validate.schema_validate import schema_validation



# Carrega dados do jsonl na banco RAW

def load_to_raw(conx, nome_arquivo, lote):

    cursor = conx.cursor()

    try:

        for linha in lote:

            status, motivo = schema_validation(linha)

            query = """INSERT INTO raw.eventos(arquivo_origem, dados, schema_version, schema_status, schema_error)
                            VALUES(%s, %s, %s, %s, %s);"""

            valores = (nome_arquivo, Json(linha), 'V1', status, motivo)

            cursor.execute(query,valores)

        return True

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")