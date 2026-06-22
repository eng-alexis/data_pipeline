import shutil
from pathlib import Path

# Registra novo arquivo no banco

def reg_novo_arquivo(connection_db, hash, nome_arquivo, data_ingestao, tamanho_bytes, id_exec):

    conx = connection_db

    cursor = conx.cursor()

    query= """INSERT INTO audit.file_history(
                hash, nome_arquivo, tamanho_bytes,
                data_ingestao, id_exec, status)
                VALUES(%s, %s, %s, %s, %s, 'PROCESSADO')
                RETURNING id_arquivo"""
    
    valores = (hash, nome_arquivo, tamanho_bytes, data_ingestao, id_exec)

    try:

        cursor.execute(query, valores)
        file_id = cursor.fetchone()[0]

        conx.commit()

        return file_id

    except Exception as e:
        print(f"Erro ao registrar file: {nome_arquivo} - {e}")

# Move arquivos processados

def move_file(arquivo, destino):

    shutil.move(arquivo,destino)
    
    return True

# Deleta diretorios vazios

def delete_empty_dir(arquivo):

    try:

        file_dir = Path(arquivo).resolve().parent
        file_dir.rmdir()

    except OSError:
        pass