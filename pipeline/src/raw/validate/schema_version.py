from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class EventoSchema_V1(BaseModel):

    event_id: UUID
    event_time: datetime
    emit_time: datetime
    tipo_evento: str
    evento_seq: int 
    id_loja: int
    id_caixa: int
    id_pedido: int
    produto_id: Optional[int] = None
    quantidade: Optional[int] = None
    valor_unitario: Optional[float] = None

class ProductSchema_V1(BaseModel):

    id: int
    nome: str
    valor: float

class StoreSchema_V1(BaseModel):
    
    ID: int
    CNPJ: str
    Endereço: str
    Bairro: str
    Cidade: str
    Estado: str
    Gerente: str
    Horário_de_Atendimento: str