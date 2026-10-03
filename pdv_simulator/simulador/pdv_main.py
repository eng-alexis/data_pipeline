print("""

+----------------- PDV SIMULATOR ------------------+

Digite o intervalo que deseja simular:
""")

from pdv_simulator.src.create_json import salvar_json, export_catalogo, export_lojas
from pdv_simulator.src.sales_day_simulatior import day_simulation
from pdv_simulator.config.paths import PDV_NEW_FILES_DIR, NUM_SIMULATIONS
from pdv_simulator.config.context import LOJAS, CAIXAS_POR_LOJA, DATA, QTD_DIAS
from pdv_simulator.history.simulations import get_num_simulations, update_num_simulations
from datetime import datetime

print(f"""
---------------- Simulador iniciado ----------------

— Simulando {QTD_DIAS} dia(s) de vendas...

por favor aguarde...""")

inicio_simulador = datetime.now()

contador = 0

for data in DATA:

    data_convertida = datetime.strptime(data, '%Y-%m-%d')

    ano = data_convertida.year
    mes = data_convertida.month
    dia = data_convertida.day

    for loja in LOJAS:

        for caixa in CAIXAS_POR_LOJA[loja]:

            for simulacao in day_simulation(data, loja, caixa):

                raiz = PDV_NEW_FILES_DIR
                raiz.mkdir(parents=True, exist_ok=True)

                eventos_path = raiz / "lojas" / f"loja_{loja}" / f"{ano}" / f"{mes}"/ f"{dia}" / f"{data}_eventos_l{loja}_c{caixa}.jsonl"
                eventos_path.parent.mkdir(parents=True, exist_ok=True)

                salvar_json(simulacao, eventos_path)
                
            contador += 1

qtde_simulacoes = get_num_simulations(NUM_SIMULATIONS)

if qtde_simulacoes == 0:

    produtos = raiz / "arquivos_referencia" / f"{data}_catalogo.json"
    produtos.parent.mkdir(parents=True, exist_ok=True)
    contador += 1

    lojas = raiz / "arquivos_referencia" / f"{data}_lojas.json"
    lojas.parent.mkdir(parents=True, exist_ok=True)
    contador += 1

    export_catalogo(produtos)
    export_lojas(lojas)

qtde_simulacoes += 1

update_num_simulations(NUM_SIMULATIONS, qtde_simulacoes)

fim_simulador = datetime.now()
diferenca = (fim_simulador - inicio_simulador)
duracao   = int((diferenca.total_seconds()*1000))

print(f"""
--------------- Simulador finalizado ---------------

---------------------- Resumo ----------------------

• Duração (minutos) do simulador  = {(duracao/1000) // 60:.0f}m {((duracao/1000) % 60):.0f}s

• Total de dias simulados         = {QTD_DIAS}
• Total de arquivos gerados       = {contador}

+--------------------------------------------------+

""")