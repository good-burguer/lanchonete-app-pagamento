from fastapi import status, HTTPException

from app.adapters.dto.pagamento_dto import PagamentoAtualizaWebhookSchema
from app.use_cases.pagamento_use_case import PagamentoUseCase
from app.adapters.presenters.pagamento_presenter import WebhookResponse

class PagamentoWebhookController:
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def atualizar_pagamento(self, pagamento_data : PagamentoAtualizaWebhookSchema):
        try:
            result = PagamentoUseCase(self.db_session).atualizar_pagamento(pagamento_data)
            data : WebhookResponse = WebhookResponse(status = 'success', data = result)

            return data
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))