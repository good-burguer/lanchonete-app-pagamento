import pytest

from app.dao.pagamento_dao import PagamentoDAO
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema


class FakeCollection:
    def __init__(self):
        self.inserted = None
        self._store = {}

    def insert_one(self, payload):
        self.inserted = payload

    def find(self):
        return []

    def find_one(self, query):
        # simulate find_one lookup by codigo_pagamento
        codigo = query.get("codigo_pagamento")
        return self._store.get(codigo)

    def update_one(self, query, update):
        codigo = query.get("codigo_pagamento")
        if codigo in self._store:
            self._store[codigo]["status"] = update.get("$set", {}).get("status")

    def delete_one(self, query):
        codigo = query.get("codigo_pagamento")
        if codigo in self._store:
            del self._store[codigo]


def test_criar_pagamento_inserts_and_returns_model():
    db = {"pagamentos": FakeCollection()}
    dao = PagamentoDAO(db)

    input_schema = PagamentoCreateSchema(pedido_id=42)
    model = dao.criar_pagamento(input_schema)

    assert model.pedido == 42
    assert db["pagamentos"].inserted["pedido"] == 42
    assert isinstance(db["pagamentos"].inserted["codigo_pagamento"], str)


def test_deletar_pagamento_raises_when_not_found():
    class EmptyCollection(FakeCollection):
        def find_one(self, query):
            return None

    db = {"pagamentos": EmptyCollection()}
    dao = PagamentoDAO(db)

    with pytest.raises(ValueError):
        dao.deletar_pagamento("non-existent")
