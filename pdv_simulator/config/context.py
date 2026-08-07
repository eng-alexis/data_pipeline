import pandas as pd
from datetime import datetime

# Input que recebe e valida datas de inicio e fim para o simulador

data_inicio = input("digite a data inicial (ex: 2026-01-01): ")
data_final  = input("digite a data final   (ex: 2026-01-02): ")

try:
    data_inicio_valida = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_final_valida  = datetime.strptime(data_final, "%Y-%m-%d").date()

except ValueError:
    print("Erro: Data inválida! Use estritamente o formato AAAA-MM-DD")

if data_inicio > data_final:
    print("Erro: Data inválida! A data inicial deve ser menor que a data final")
    raise 

# Gera o range de datas diretamente

DATA = pd.date_range(start=data_inicio, end=data_final).strftime('%Y-%m-%d').tolist()

# Retorna a quantidade de dias que serão simulados

QTD_DIAS = ((data_final_valida - data_inicio_valida).days) + 1   

# Define a quantidade de lojas e caixas por loja

LOJAS = [1]

CAIXAS_POR_LOJA = {
    1: [1,2]
}

# Define o perfil hora

PERFIL_HORA = {
    8: 3,
    9: 4,
    10: 6,
    11: 10,
    12: 11,
    13: 9,
    14: 10, 
    15: 6,
    16: 7,
    17: 9,
    18: 12,
    19: 17,
    20: 12,
    21: 4
}