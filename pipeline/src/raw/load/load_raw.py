from psycopg2.extras import Json

from pipeline.src.raw.validate.schema_validate import schema_validation



# Carrega registros na tabela raw.eventos

def load_to_raw(conx, nome_arquivo, lote, schema_version, status, obs):

    cursor = conx.cursor()

    try:

        for linha in lote:

            query = """INSERT INTO raw.eventos(arquivo_origem, dados, 
                            schema_version, schema_status, observacao)
                            VALUES(%s, %s, %s, %s, %s);"""

            valores = (nome_arquivo, Json(linha), schema_version, status, obs)

            cursor.execute(query,valores)

        return True

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")