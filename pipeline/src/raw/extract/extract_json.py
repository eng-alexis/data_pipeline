# Encontra arquivos jsonl no caminho especificado pelo usuário

import json
from pathlib import Path

def encontrar_arquivos(caminho, formato):

    path = Path(caminho)
    arquivos_jsonl = list(path.rglob(f"*.{formato}"))
    
    for arquivo in arquivos_jsonl:

        if arquivo:
            yield arquivo

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

                yield linha

        else:
            print("Tipo de arquivo não é permitido")