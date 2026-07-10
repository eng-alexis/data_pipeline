# Encontra arquivos jsonl no caminho especificado pelo usuário

import json
from pathlib import Path

def encontrar_arquivos(caminho, formato):

    path = Path(caminho)
    arquivos_jsonl = list(path.rglob(f"*.{formato}"))
    
    for arquivo in arquivos_jsonl:

        if arquivo:
            yield arquivo

# Verifica se o arquivo esta vazio

def is_file_empty(arquivo):
        
    with open(arquivo, 'r', encoding="utf-8") as arq_json:

        conteudo = arq_json.read().strip()

        return False if conteudo else True

# Extrair registros de arquivos jsonl e json

def extrair_registros(arquivo, tipo_file):

    with open(arquivo, 'r', encoding="utf-8") as arq_json:

        if tipo_file == "jsonl":

            for linha in arq_json:
                linha = linha.strip()

                if linha:
                    yield json.loads(linha)  


        elif tipo_file == "json":

            registros = json.load(arq_json)

            for linha in registros:

                if linha:
                    yield linha

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