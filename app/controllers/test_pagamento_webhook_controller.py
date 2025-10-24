import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException, status

from app.controllers.pagamento_webhook_controller import PagamentoWebhookController
from app.adapters.dto.pagamento_dto import PagamentoAtualizaWebhookSchema
from app.adapters.presenters.pagamento_presenter import WebhookResponse
from app.adapters.schemas.pagamento import PagamentoAtualizaSchema
from app.adapters.utils.debug import var_dump_die

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def controller(mock_db):
    return PagamentoWebhookController(db_session=mock_db)

@pytest.fixture
def fake_pagamento_data():
    return PagamentoAtualizaWebhookSchema(
        codigo_pagamento="123",
        status='3'
    )

@pytest.fixture
def fake_result():
    
    return PagamentoAtualizaSchema(
        status='3'
    )

def test_atualizar_pagamento_sucesso(controller, fake_pagamento_data, fake_result):
    with patch("app.controllers.pagamento_webhook_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.atualizar_pagamento.return_value = fake_result

        response = controller.atualizar_pagamento(fake_pagamento_data)
        instance.atualizar_pagamento.assert_called_once_with(fake_pagamento_data)

        assert isinstance(response, WebhookResponse)
        assert response.status == "success"
        
        assert response.data == fake_result


def test_atualizar_pagamento_nao_encontrado(controller, fake_pagamento_data):
    with patch("app.controllers.pagamento_webhook_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.atualizar_pagamento.side_effect = ValueError("Pagamento não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_pagamento(fake_pagamento_data)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Pagamento não encontrado" in str(exc_info.value.detail)


def test_atualizar_pagamento_erro_generico(controller, fake_pagamento_data):
    with patch("app.controllers.pagamento_webhook_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.atualizar_pagamento.side_effect = Exception("Erro interno")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_pagamento(fake_pagamento_data)

        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Erro interno" in str(exc_info.value.detail)
