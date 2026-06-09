# Encontra arquivos jsonl no caminho especificado pelo usuário

from pathlib import Path

def encontrar_arquivos(caminho):

    arquivos_encontrados = []

    path = Path(caminho)
    arquivos_jsonl = list(path.rglob(f"*.jsonl"))

    for arquivo in arquivos_jsonl:
        arquivos_encontrados.append(arquivo)

    return arquivos_encontrados