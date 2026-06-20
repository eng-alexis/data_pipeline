import json
from csv import DictReader
from pdv_simulator.config.paths import CATALOGO_FILE, LOJAS_FILE

# Cria json com eventos de vendas

def salvar_json(evento, caminho):
    if not evento:
        return
    
    with open(caminho,'a') as f:

        f.write(json.dumps(evento) + '\n')


# Cria json com catalogo de produtos

def export_catalogo(destino):
                
    csv_file = CATALOGO_FILE
    json_file = destino

    produtos = []

    with open (csv_file, encoding='utf-8') as csv:
        csvReader = DictReader(csv)
        for row in csvReader:
            produtos.append(row)

    with open (json_file, 'w', encoding='utf-8') as jsonfile:
        jsonstring = json.dump(produtos, jsonfile, indent=4, ensure_ascii=False)
    
# Cria json com informações das lojas

def export_lojas(destino):

    csv_file = LOJAS_FILE

    json_file = destino

    lojas = []

    with open (csv_file, encoding='utf-8') as csv:
        csvReader = DictReader(csv)
        for row in csvReader:
            lojas.append(row)

    with open (json_file, 'w', encoding='utf-8') as jsonfile:
        jsonstring = json.dump(lojas, jsonfile, indent=4, ensure_ascii=False)