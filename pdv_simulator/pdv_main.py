from pdv_simulator.src.create_json import salvar_json, export_catalogo, export_lojas
from pdv_simulator.src.sales_day_simulatior import day_simulation
from pdv_simulator.config.paths import PDV_ROOT
from pdv_simulator.config.context import LOJAS, CAIXAS_POR_LOJA, DATA

for data in DATA:

    for loja in LOJAS:

        for caixa in CAIXAS_POR_LOJA[loja]:

            for simulacao in day_simulation(data, loja, caixa):

                raiz = PDV_ROOT / "pdv_sales"
                raiz.mkdir(parents=True, exist_ok=True)

                eventos_path = raiz / "sales" / f"loja_{loja}" / f"{data}" / f"{data}_l{loja}_c{caixa}.jsonl"
                eventos_path.parent.mkdir(parents=True, exist_ok=True)

                salvar_json(simulacao, eventos_path)

        produtos = raiz / "database" / "catalogo.json"
        produtos.parent.mkdir(parents=True, exist_ok=True)

        lojas = raiz / "database" / "lojas.json"
        lojas.parent.mkdir(parents=True, exist_ok=True)

        export_catalogo(produtos)
        export_lojas(lojas)