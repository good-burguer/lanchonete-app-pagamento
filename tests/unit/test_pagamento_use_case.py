import pytest
from unittest.mock import MagicMock
from app.use_cases.pagamento_use_case import PagamentoUseCase
from app.adapters.schemas.pagamento import PagamentoResponseSchema
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema

@pytest.fixture
def fake_pagamento_entity():
    return MagicMock()

@pytest.fixture
def use_case(fake_pagamento_entity):
    return PagamentoUseCase(entities=fake_pagamento_entity)

@pytest.fixture
def pagamento_model():
    return {
        "pedido": 10,
        "codigo_pagamento": "ABC123",
        "status": 3
    }



def test_criar_pagamento_sucesso(use_case, fake_pagamento_entity):
    fake_pagamento = MagicMock(pedido=1, codigo_pagamento="123", status="1")
    fake_pagamento_entity.criar_pagamento.return_value = fake_pagamento

    schema_input = PagamentoCreateSchema(pedido_id=1)
    result = use_case.criar_pagamento(schema_input)

    assert isinstance(result, PagamentoResponseSchema)
    assert result.pedido_id == 1
    assert result.codigo_pagamento == "123"
    assert result.status == 1



def test_buscar_pagamento_sucesso(use_case, fake_pagamento_entity, pagamento_model):
    fake_pagamento_entity.buscar_pagamento.return_value = pagamento_model

    result = use_case.buscar_pagamento("ABC123")

    assert isinstance(result, PagamentoResponseSchema)
    assert result.codigo_pagamento == "ABC123"
    assert result.pedido_id == 10


def test_buscar_pagamento_nao_encontrado(use_case, fake_pagamento_entity):
    fake_pagamento_entity.buscar_pagamento.return_value = None

    with pytest.raises(ValueError) as exc:
        use_case.buscar_pagamento("NOT_FOUND")
    assert "Pagamento não encontrado" in str(exc.value)



def test_listar_todos_pagamentos_sucesso(use_case, fake_pagamento_entity, pagamento_model):
    fake_pagamento_entity.listar_todos_pagamentos.return_value = [pagamento_model]

    result = use_case.listar_todos_pagamentos()

    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], PagamentoResponseSchema)
    assert result[0].codigo_pagamento == "ABC123"


def test_listar_todos_pagamentos_vazio(use_case, fake_pagamento_entity):
    fake_pagamento_entity.listar_todos_pagamentos.return_value = []

    result = use_case.listar_todos_pagamentos()

    assert result == []



def test_atualizar_pagamento_sucesso(use_case, fake_pagamento_entity):
    atualizado = {
        "pedido": 1,
        "codigo_pagamento": "XYZ789",
        "status": 2
    }
    fake_pagamento_entity.atualizar_pagamento.return_value = atualizado

    result = use_case.atualizar_pagamento("XYZ789", "2")

    assert isinstance(result, PagamentoResponseSchema)
    assert result.codigo_pagamento == "XYZ789"
    assert result.status == 2


def test_atualizar_pagamento_nao_encontrado(use_case, fake_pagamento_entity):
    fake_pagamento_entity.atualizar_pagamento.return_value = None

    with pytest.raises(ValueError) as exc:
        use_case.atualizar_pagamento("NAO_EXISTE", "2")
    assert "Pagamento não encontrado" in str(exc.value)



def test_deletar_pagamento_chama_entidade(use_case, fake_pagamento_entity):
    use_case.deletar_pagamento("XYZ789")

    fake_pagamento_entity.deletar_pagamento.assert_called_once_with(codigo_pagamento="XYZ789")



def test_response_schema_converte_dados(use_case, pagamento_model):
    result = use_case._response_schema(pagamento_model)

    assert isinstance(result, PagamentoResponseSchema)
    assert result.pedido_id == pagamento_model["pedido"]
    assert result.codigo_pagamento == pagamento_model["codigo_pagamento"]
    assert result.status == pagamento_model["status"]
