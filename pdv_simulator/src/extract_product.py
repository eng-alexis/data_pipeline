from csv import DictReader
from pdv_simulator.config.paths import CATALOGO_FILE
import random

csv_path = CATALOGO_FILE

def carregar_catalogo():

    produtos = []

    with open (csv_path, newline="", encoding='utf-8') as cat_csv:
        reader = DictReader(cat_csv)
        for row in reader:
            produtos.append({
                "id": int(row["id"]),
                "nome": row["nome"],
                "valor": float(row["valor"])
            })

        return produtos

produtos_obtidos = carregar_catalogo()

def return_one_product():
    produto = random.choice(produtos_obtidos)

    return produto["id"], produto["valor"]