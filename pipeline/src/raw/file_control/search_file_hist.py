# Gerar hash do novo arquivo

import hashlib

def gerar_hash(caminho_arquivo):
    sha256 = hashlib.sha256()

    with open(caminho_arquivo, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(4096), b""):
            sha256.update(bloco)

    return sha256.hexdigest()

# Procurar hash e nome do arquivo no banco

def find_hash(connection_db, hash):

    conx = connection_db
    cursor = conx.cursor()

    query = """SELECT EXISTS(
                    SELECT 1 FROM audit.file_history
                    WHERE hash = %s);"""

    try:

        cursor.execute(query, (hash,))

        resultado = cursor.fetchone()

        return resultado[0] if resultado else False

    except Exception as e:
        print(f"Erro ao conectar ou consultar o banco: {e}")
        return False