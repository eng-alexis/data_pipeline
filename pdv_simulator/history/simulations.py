import json

# Retorna o numero da ultima simulação

def get_num_simulations (path):

    with open (path, 'r', encoding="utf-8") as file:

        dados = json.load(file)

        return dados["simulations"][0]

# Atualiza o numero da ultima simulação

def update_num_simulations (path, new_qtd):

    with open (path, 'w', encoding="utf-8") as file:

        json.dump({"simulations":[new_qtd]}, file)