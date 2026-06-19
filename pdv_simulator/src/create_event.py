import uuid
from datetime import timedelta
import random

def criar_evento(timestamp, tipo, seq, loja, caixa, pedido,
                produto=None, qtd=None, valor=None):

    atraso = random.randint(0,5)
    emit_time = timestamp + timedelta(seconds=atraso)

    return {
        "event_id": str(uuid.uuid4()),
        "event_time": timestamp.isoformat(),
        "emit_time": emit_time.isoformat(),
        "tipo_evento": tipo,
        "evento_seq": seq,
        "id_loja": loja,
        "id_caixa": caixa,
        "id_pedido": pedido,
        "produto_id": produto,
        "quantidade": qtd,
        "valor_unitario": valor}