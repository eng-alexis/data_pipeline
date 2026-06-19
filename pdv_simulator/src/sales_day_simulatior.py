from pdv_simulator.src.create_order import gerar_pedido_completo
from datetime import datetime
from pdv_simulator.config.context import PERFIL_HORA
import random

def day_simulation(data, loja, caixa):

    id_pedido = 1
    data_base = datetime.strptime(data,"%Y-%m-%d")

    for hora, peso in PERFIL_HORA.items():

        pedidos = peso * random.randint(1,3)

        for _ in range(pedidos):

            timestamp = data_base.replace(
                hour=hora,
                minute=random.randint(0,59),
                second=random.randint(0,59))

            for pedido_completo in gerar_pedido_completo(timestamp, id_pedido, loja, caixa):

                yield pedido_completo

            id_pedido += 1