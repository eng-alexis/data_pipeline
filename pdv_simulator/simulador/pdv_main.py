print("""

+----------------- PDV SIMULATOR ------------------+

Digite o intervalo que deseja simular:
""")

from pdv_simulator.src.create_json import salvar_json, export_catalogo, export_lojas
from pdv_simulator.src.sales_day_simulatior import day_simulation
from pdv_simulator.config.paths import PDV_NEW_FILES_DIR
from pdv_simulator.config.context import LOJAS, CAIXAS_POR_LOJA, DATA, QTD_DIAS, TMP_ESTIMADO
from datetime import datetime

print(f"""
▷ Simulador iniciado

Simulando {QTD_DIAS} dia(s) de vendas...
Tempo estimado = {TMP_ESTIMADO:.1F} segs""")

inicio_simulador = datetime.now()

contador = 0

for data in DATA:

    for loja in LOJAS:

        for caixa in CAIXAS_POR_LOJA[loja]:

            for simulacao in day_simulation(data, loja, caixa):

                raiz = PDV_NEW_FILES_DIR
                raiz.mkdir(parents=True, exist_ok=True)

                eventos_path = raiz / "eventos" / f"loja_{loja}" / f"{data}" / f"{data}_l{loja}_c{caixa}.jsonl"
                eventos_path.parent.mkdir(parents=True, exist_ok=True)

                salvar_json(simulacao, eventos_path)
                
            contador += 1

        produtos = raiz / "produtos" / "catalogo.json"
        produtos.parent.mkdir(parents=True, exist_ok=True)

        lojas = raiz / "lojas" / "lojas.json"
        lojas.parent.mkdir(parents=True, exist_ok=True)

        export_catalogo(produtos)
        export_lojas(lojas)

fim_simulador = datetime.now()
diferenca = (fim_simulador - inicio_simulador)
duracao   = int((diferenca.total_seconds()*1000))

print(f"""
▶ Simulador finalizado

+-------------------- Resumo ----------------------+

• Total de dias simulados         = {QTD_DIAS}
• Total de arquivos gerados       = {contador}
• Duração (segundos) do simulador = {duracao/1000:.1f} segs

+--------------------------------------------------+

""")