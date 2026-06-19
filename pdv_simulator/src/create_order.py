from pdv_simulator.src.create_event import criar_evento
from pdv_simulator.src.extract_product import return_one_product

import random

def gerar_pedido_completo(timestamp, id_pedido, id_loja, id_caixa):

    v_event_seq = 1
    v_pedido = id_pedido

    yield criar_evento(timestamp, 'pedido criado', v_event_seq, id_loja, id_caixa, v_pedido)
    
    v_event_seq += 1

    num_itens = range(random.randint(1,7))
    
    for n in num_itens:

        id_produto, valor_unitario = return_one_product()

        quantidade = random.randint(1,4)

        yield  criar_evento(timestamp, 'item adicionado', v_event_seq, id_loja, id_caixa, 
                                       v_pedido, id_produto, quantidade, valor_unitario)
        
        v_event_seq += 1


    yield criar_evento(timestamp, 'pagamento realizado', v_event_seq, id_loja, id_caixa, v_pedido)

    v_event_seq += 1