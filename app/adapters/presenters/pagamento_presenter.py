from pydantic import BaseModel
from app.adapters.schemas.pagamento import PagamentoResponseSchema
from app.adapters.enums.status_pagamento import PagamentoStatusStringEnum

class WebhookResponse(BaseModel):
    status: PagamentoStatusStringEnum

class PagamentoResponse(BaseModel):
    status: str
    data: PagamentoResponseSchema

class PagamentoResponseList(BaseModel):
    status: str
    data: list[PagamentoResponseSchema]