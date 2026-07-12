import os
import shutil
from pathlib import Path

# Renomeia arquivo

def rename_file(arquivo, entidade, inicio):

    if entidade != "eventos":

        data = inicio.date()
        hora = inicio.strftime("%H:%M:%S")

        arquivo = Path(arquivo)
        file_parent = arquivo.resolve().parent

        file_name = arquivo.name

        original_name = arquivo
        novo_nome = os.path.join(file_parent, f"{data}_{hora}_{file_name}")

        os.rename(original_name, novo_nome)

        return Path(novo_nome)
    
    else:
        return arquivo

# Cria variavel com novo nome do arquivo

def file_new_name(arquivo, inicio):

    data = inicio.date()
    hora = inicio.strftime("%H:%M:%S")

    short_name = Path(arquivo).name

    novo_nome = f"{data}_{hora}_{short_name}"

    return novo_nome

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