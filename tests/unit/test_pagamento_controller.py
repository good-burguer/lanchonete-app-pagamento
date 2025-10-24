import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from fastapi.responses import Response

from app.controllers.pagamento_controller import PagamentoController
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema, PagamentoUpdateSchema
from app.adapters.presenters.pagamento_presenter import PagamentoResponse, PagamentoResponseList
from app.adapters.schemas.pagamento import PagamentoResponseSchema
from app.adapters.utils.debug import var_dump_die

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def controller(mock_db):
    return PagamentoController(db_session=mock_db)

@pytest.fixture
def fake_pagamento_data():
    return _getResponseSchema()

def _getResponseSchema():
    return PagamentoResponseSchema(pedido_id=1, codigo_pagamento='123', status='3')

def test_criar_pagamento_sucesso(controller, mock_db, fake_pagamento_data):
    fake_schema = PagamentoCreateSchema(pedido_id=1)

    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.criar_pagamento.return_value = fake_pagamento_data

        result = controller.criar_pagamento(fake_schema)

        instance.criar_pagamento.assert_called_once_with(fake_schema)

        assert isinstance(result, PagamentoResponse)
        
        assert result.data == fake_pagamento_data


def test_criar_pagamento_erro(controller):
    fake_schema = PagamentoCreateSchema(pedido_id=1)

    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.criar_pagamento.side_effect = Exception("Erro de criação")

        with pytest.raises(HTTPException) as exc_info:
            controller.criar_pagamento(fake_schema)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "Erro de criação" in str(exc_info.value.detail)


def test_buscar_pagamento_sucesso(controller, fake_pagamento_data):
    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.buscar_pagamento.return_value = fake_pagamento_data

        result = controller.buscar_pagamento("123")
        instance.buscar_pagamento.assert_called_once_with("123")
        assert isinstance(result, PagamentoResponse)
        assert result.data == fake_pagamento_data


def test_buscar_pagamento_nao_encontrado(controller):
    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.buscar_pagamento.side_effect = ValueError("Pagamento não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_pagamento("999")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert "Pagamento não encontrado" in str(exc_info.value.detail)


def test_listar_todos_pagamentos_sucesso(controller, fake_pagamento_data):
    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.listar_todos_pagamentos.return_value = [fake_pagamento_data]

        result = controller.listar_todos_pagamentos()
        instance.listar_todos_pagamentos.assert_called_once()
        assert isinstance(result, PagamentoResponseList)
        assert len(result.data) == 1


def test_listar_todos_pagamentos_erro(controller):
    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.listar_todos_pagamentos.side_effect = Exception("Erro interno")

        with pytest.raises(HTTPException) as exc_info:
            controller.listar_todos_pagamentos()
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST


def test_atualizar_pagamento_sucesso(controller, fake_pagamento_data):
    fake_update = PagamentoUpdateSchema(status="3")

    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.atualizar_pagamento.return_value = fake_pagamento_data

        result = controller.atualizar_pagamento("123", fake_update)
        instance.atualizar_pagamento.assert_called_once_with(codigo="123", status=3)
        assert isinstance(result, PagamentoResponse)


def test_atualizar_pagamento_nao_encontrado(controller):
    fake_update = PagamentoUpdateSchema(status="3")

    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.atualizar_pagamento.side_effect = ValueError("Pagamento não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_pagamento("999", fake_update)
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND


def test_deletar_pagamento_sucesso(controller):
    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value

        result = controller.deletar_pagamento("123")
        instance.deletar_pagamento.assert_called_once_with(codigo_pagamento="123")
        assert isinstance(result, Response)
        assert result.status_code == status.HTTP_204_NO_CONTENT


def test_deletar_pagamento_nao_encontrado(controller):
    with patch("app.controllers.pagamento_controller.PagamentoUseCase") as UseCaseMock:
        instance = UseCaseMock.return_value
        instance.deletar_pagamento.side_effect = ValueError("Pagamento não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.deletar_pagamento("999")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
