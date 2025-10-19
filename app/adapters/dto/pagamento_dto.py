from pydantic import BaseModel

class PagamentoAtualizaWebhookSchema(BaseModel):
    codigo_pagamento: str
    status: int

class PagamentoCreateSchema(BaseModel):
    pedido_id: int

class PagamentoUpdateSchema(BaseModel):
    status: int