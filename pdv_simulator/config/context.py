import pandas as pd

inicio = '2026-01-21' 
fim    = '2026-01-22'

# Gera o range de datas diretamente
DATA = pd.date_range(start=inicio, end=fim).strftime('%Y-%m-%d').tolist()

LOJAS = [1]

CAIXAS_POR_LOJA = {
    1: [1,2]
}

PERFIL_HORA = {
    8: 10,
    9: 20,
    10: 30,
    11: 40,
    12: 60,
    13: 50,
    14: 30,
    15: 25,
    16: 30,
    17: 40,
    18: 70,
    19: 80,
    20: 60,
    21: 30
}