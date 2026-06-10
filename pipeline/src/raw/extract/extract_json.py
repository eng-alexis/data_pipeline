# Encontra arquivos jsonl no caminho especificado pelo usuário
import json
from pathlib import Path

def encontrar_arquivos(caminho):

    arquivos_encontrados = []

    path = Path(caminho)
    arquivos_jsonl = list(path.rglob(f"*.jsonl"))

    for arquivo in arquivos_jsonl:
        arquivos_encontrados.append(arquivo)

    return arquivos_encontrados

# Extrair registro e nome do arquivo jsonl

def extrair_registros(lista_arquivos):

    for arquivo in lista_arquivos:

        with open(arquivo, 'r', encoding="utf-8") as arq_json:

            for linha in arq_json:

                linha = linha.strip()

                if linha:

                    yield Path(arquivo).name, json.loads(linha)