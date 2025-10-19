from pydantic import BaseModel

class PagamentoResponseSchema(BaseModel):
    pedido_id: int
    codigo_pagamento:str
    status: str

class PagamentoAtualizaSchema(BaseModel):
    status: str