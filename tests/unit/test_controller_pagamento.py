import pytest
from fastapi import HTTPException

from app.controllers.pagamento_controller import PagamentoController
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema


def test_criar_pagamento_success(monkeypatch):
    class FakeUseCase:
        def __init__(self, db_session):
            pass

        def criar_pagamento(self, cliente_data):
            return {"pedido_id": cliente_data.pedido_id, "codigo_pagamento": "abc", "status": 1}

    monkeypatch.setattr("app.controllers.pagamento_controller.PagamentoUseCase", FakeUseCase)

    controller = PagamentoController(db_session=None)
    result = controller.criar_pagamento(PagamentoCreateSchema(pedido_id=7))

    assert result.status == "success"
    assert result.data["pedido"] == 7


def test_buscar_pagamento_not_found(monkeypatch):
    class FakeUseCase:
        def __init__(self, db_session):
            pass

        def buscar_pagamento(self, codigo):
            raise ValueError("Pagamento não encontrado")

    monkeypatch.setattr("app.controllers.pagamento_controller.PagamentoUseCase", FakeUseCase)

    controller = PagamentoController(db_session=None)
    with pytest.raises(HTTPException) as exc_info:
        controller.buscar_pagamento("x")

    assert exc_info.value.status_code == 404
