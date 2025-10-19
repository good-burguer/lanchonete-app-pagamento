from pydantic import BaseModel
from app.adapters.schemas.pagamento import PagamentoAtualizaSchema, PagamentoResponseSchema

class WebhookResponse(BaseModel):
    status: str
    data: PagamentoAtualizaSchema

class PagamentoResponse(BaseModel):
    status: str
    data: PagamentoResponseSchema

class PagamentoResponseList(BaseModel):
    status: str
    data: list[PagamentoResponseSchema]