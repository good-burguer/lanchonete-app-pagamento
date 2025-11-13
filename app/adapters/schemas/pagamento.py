from pydantic import BaseModel
from app.adapters.enums.status_pagamento import PagamentoStatusStringEnum

class PagamentoResponseSchema(BaseModel):
    pedido_id: int
    codigo_pagamento:str
    status: int