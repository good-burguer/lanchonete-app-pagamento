import pytest
from unittest.mock import MagicMock, patch
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema
from app.models.pagamento import Pagamento
from app.gateways.pagamento_gateway import PagamentoGateway


@pytest.fixture
def mock_dao():
    return MagicMock()


@pytest.fixture
def gateway(mock_dao):
    with patch("app.gateways.pagamento_gateway.PagamentoDAO", return_value=mock_dao):
        return PagamentoGateway(db_session=None)


@pytest.fixture
def fake_pagamento():
    return Pagamento(
        pedido=1,
        codigo_pagamento="123",
        status="3"
    )


@pytest.fixture
def fake_pagamento_create():
    return PagamentoCreateSchema(
        pedido_id=1
    )

def test_criar_pagamento_sucesso(gateway, mock_dao, fake_pagamento, fake_pagamento_create):
    mock_dao.criar_pagamento.return_value = fake_pagamento

    result = gateway.criar_pagamento(fake_pagamento_create)

    mock_dao.criar_pagamento.assert_called_once_with(fake_pagamento_create)
    assert result == fake_pagamento


def test_criar_pagamento_erro_integrity(gateway, mock_dao, fake_pagamento_create):
    mock_dao.criar_pagamento.side_effect = Exception("Erro de integridade")

    with pytest.raises(Exception) as exc_info:
        gateway.criar_pagamento(fake_pagamento_create)
    
    assert "Erro de integridade" in str(exc_info.value)


def test_buscar_pagamento_sucesso(gateway, mock_dao, fake_pagamento):
    mock_dao.buscar_pagamento_por_codigo.return_value = fake_pagamento

    result = gateway.buscar_pagamento("123")

    mock_dao.buscar_pagamento_por_codigo.assert_called_once_with(codigo_pagamento="123")
    assert result == fake_pagamento


def test_buscar_pagamento_nao_encontrado(gateway, mock_dao):
    mock_dao.buscar_pagamento_por_codigo.return_value = None

    result = gateway.buscar_pagamento("999")
    assert result is None


def test_listar_todos_pagamentos_sucesso(gateway, mock_dao, fake_pagamento):
    mock_dao.listar_todos_pagamentos.return_value = [fake_pagamento]

    result = gateway.listar_todos_pagamentos()

    mock_dao.listar_todos_pagamentos.assert_called_once()
    assert result == [fake_pagamento]


def test_atualizar_pagamento_sucesso(gateway, mock_dao, fake_pagamento):
    mock_dao.atualizar_pagamento.return_value = fake_pagamento

    result = gateway.atualizar_pagamento("123", "confirmado")

    mock_dao.atualizar_pagamento.assert_called_once_with("123", "confirmado")
    assert result == fake_pagamento


def test_atualizar_pagamento_nao_encontrado(gateway, mock_dao):
    mock_dao.atualizar_pagamento.side_effect = Exception("Pagamento não encontrado")

    with pytest.raises(Exception) as exc_info:
        gateway.atualizar_pagamento("999", "confirmado")
    
    assert "Pagamento não encontrado" in str(exc_info.value)


def test_deletar_pagamento_sucesso(gateway, mock_dao):
    mock_dao.deletar_pagamento.return_value = True

    result = gateway.deletar_pagamento("123")

    mock_dao.deletar_pagamento.assert_called_once_with("123")
    assert result is True


def test_deletar_pagamento_nao_encontrado(gateway, mock_dao):
    mock_dao.deletar_pagamento.side_effect = Exception("Pagamento não encontrado")

    with pytest.raises(Exception) as exc_info:
        gateway.deletar_pagamento("9992")
    
    assert "Pagamento não encontrado" in str(exc_info.value)
