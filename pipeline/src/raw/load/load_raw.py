from psycopg2.extras import Json

# Carrega dados do jsonl na banco RAW

def load_to_raw(conx, nome_arquivo, lote):

    cursor = conx.cursor()
    
    try:

        for linha in lote:

            query = """INSERT INTO raw.eventos(arquivo_origem, dados)
                            VALUES(%s, %s);"""

            valores = (nome_arquivo, Json(linha))

            cursor.execute(query,valores)

        return True

    except Exception as e:
        print(f"Erro ao carregar dados: {e}")