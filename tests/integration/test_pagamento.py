from http import HTTPStatus
from app.adapters.utils.debug import var_dump_die

def test_criar_pagamento(client):
    payload = {
        "pedido_id": 112,
    }

    response = client.post("/pagamento/", json=payload)

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()

    assert body["data"]["pedido_id"] == payload["pedido_id"]
    assert "codigo_pagamento" in body["data"]


def test_listar_pagamentos(client):
    response = client.get("/pagamento/")
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert isinstance(body, dict)
    assert "data" in body
    assert "status" in body
    assert isinstance(body["data"], list)
    assert body["status"] == "success"


def test_buscar_pagamento_existente(client):
    novo = client.post("/pagamento/", json={
        "pedido_id": 1
    }).json()

    codigo = novo["data"]["codigo_pagamento"]

    response = client.get(f"/pagamento/{codigo}")
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["data"]["codigo_pagamento"] == codigo


def test_buscar_pagamento_inexistente(client):
    response = client.get("/pagamento/NAO_EXISTE")
    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST]


def test_atualizar_pagamento(client):
    novo = client.post("/pagamento/", json={
        "pedido_id": 1
    }).json()

    codigo = novo["data"]["codigo_pagamento"]

    response = client.put(f"/pagamento/{codigo}", json={
        "status": 3
    })

    assert response.status_code == HTTPStatus.OK
    assert response.json()["data"]["status"] == '3'


def test_deletar_pagamento(client):
    novo = client.post("/pagamento/", json={
        "pedido_id": 1
    }).json()

    codigo = novo["data"]["codigo_pagamento"]
    response = client.delete(f"/pagamento/{codigo}")

    assert response.status_code == HTTPStatus.NO_CONTENT

    # response2 = client.get(f"/pagamento/{codigo}")

    # assert response2.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST, HTTPStatus.NO_CONTENT]
