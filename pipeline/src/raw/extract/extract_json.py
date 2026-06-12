# Encontra arquivos jsonl no caminho especificado pelo usuário
import json
from pathlib import Path

def encontrar_arquivos(caminho):

    path = Path(caminho)
    arquivos_jsonl = list(path.rglob(f"*.jsonl"))
    
    for arquivo in arquivos_jsonl:

        if arquivo:
            yield arquivo

# Extrair registro, pasta de origem e nome do arquivo jsonl

def extrair_registros(arquivo):

    with open(arquivo, 'r', encoding="utf-8") as arq_json:

        for linha in arq_json:
            linha = linha.strip()

            if linha:
                yield json.loads(linha)