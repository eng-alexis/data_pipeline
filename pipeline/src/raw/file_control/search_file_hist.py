# Procurar hash e nome do arquivo no banco

from pipeline.common.database.conx_database import get_db_connection

def find_hash(hash, nome_arquivo):

    conx = get_db_connection()
    cursor = conx.cursor()

    query = """SELECT EXISTS(
                    SELECT 1 FROM audit.file_history
                    WHERE hash = %s
                    AND nome_arquivo = %s);"""

    try:

        cursor.execute(query,(hash, nome_arquivo,))

        resultado = cursor.fetchone()

        return resultado[0] if resultado else False

    except Exception as e:
        print(f"Erro ao conectar ou consultar o banco: {e}")
        return False