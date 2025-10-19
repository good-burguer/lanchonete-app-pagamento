from fastapi import APIRouter, HTTPException, Depends, Response, status
from sqlalchemy.orm import Session

from app.infrastructure.db.database import get_db
from app.gateways.pagamento_gateway import PagamentoGateway
from app.adapters.presenters.pagamento_presenter import PagamentoResponse
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema, PagamentoUpdateSchema
from app.controllers.pagamento_controller import PagamentoController
from app.adapters.utils.debug import var_dump_die

router = APIRouter(prefix="/pagamento", tags=["pagamento"])

def get_pagamento_gateway(db: Session = Depends(get_db)) -> PagamentoGateway:
    
    return PagamentoGateway(db_session=db)

@router.post("/", response_model=PagamentoResponse, status_code=status.HTTP_201_CREATED, summary="Criar pagamento do pedido", responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao salvar o pagamento"
                }
            }
        }
    }
})
def efetuar_pagamento_pedido(pedido_id: PagamentoCreateSchema, gateway: PagamentoGateway = Depends(get_pagamento_gateway)):
    try:

        return (PagamentoController(db_session=gateway)
                    .criar_pagamento(cliente_data=pedido_id))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{codigo_pagamento}", response_model=PagamentoResponse, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar o pagamento"
                }
            }
        }
    },
    404: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Pagamento não encontrado"
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def buscar_pagamento(codigo_pagamento: str, gateway: PagamentoGateway = Depends(get_pagamento_gateway)):
    try:
        
        return (PagamentoController(db_session=gateway)
                    .buscar_pagamento(codigo_pagamento=codigo_pagamento))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/", summary="Listar todos os pagamentos realizado", responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao buscar os pagamentos"
                }
            }
        }
    }
}, openapi_extra={
    "responses": {
        "422": None  
    }
})
def listar_pagamentos(gateway: PagamentoGateway = Depends(get_pagamento_gateway)):
    try:
        
        return (PagamentoController(db_session=gateway)
                .listar_todos_pagamentos())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{codigo_pagamento}", response_model=PagamentoResponse, responses={
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
def atualizar_pagamento(codigo_pagamento: str, pagamento_data: PagamentoUpdateSchema, gateway: PagamentoGateway = Depends(get_pagamento_gateway)):
    try:

        return PagamentoController(db_session=gateway).atualizar_pagamento(codigo=codigo_pagamento, pagamento_data=pagamento_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{codigo_pagamento}", status_code=status.HTTP_204_NO_CONTENT, responses={
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
                    "message": "Erro de integridade ao remover o pagamento"
                }
            }
        }
    },
    204: {
        "description": "Pagamento deletado com sucesso",
        "content": {
            "application/json": {
                "example": {}
            }
        }
    }
})
def deletar_pagamento(codigo_pagamento: str, gateway: PagamentoGateway = Depends(get_pagamento_gateway)):
    try:
        return (PagamentoController(db_session=gateway)
                    .deletar_pagamento(codigo_pagamento=codigo_pagamento))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
