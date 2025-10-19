from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.gateways.pagamento_gateway import PagamentoGateway
from app.infrastructure.db.database import get_db
from app.adapters.dto.pagamento_dto import PagamentoAtualizaWebhookSchema
from app.adapters.presenters.pagamento_presenter import WebhookResponse
from app.controllers.pagamento_webhook_controller import PagamentoWebhookController

router = APIRouter(prefix="/webhook", tags=["webhook"])

def get_pagamento_gateway(db: Session = Depends(get_db)) -> PagamentoGateway:
    
    return PagamentoGateway(db_session=db)

@router.post("/update-payment", response_model=WebhookResponse, responses={
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Pagamento não encontrado"
                }
            }
        }
    },
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao atualizar o pagamento"
                }
            }
        }
    }
})
def atualizar_pagamento(pagamento_data: PagamentoAtualizaWebhookSchema, gateway: PagamentoGateway = Depends(get_pagamento_gateway)):
    try:
        
        return (PagamentoWebhookController(db_session=gateway)
                .atualizar_pagamento(pagamento_data))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))