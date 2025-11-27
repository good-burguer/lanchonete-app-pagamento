from http import HTTPStatus
from app.adapters.dto.pagamento_dto import PagamentoAtualizaWebhookSchema
from app.adapters.utils.debug import var_dump_die

def test_webhook_atualizar_pagamento_sucesso(client):
    novo_pagamento = client.post("/pagamento/", json={"pedido_id": 999}).json()
    codigo = novo_pagamento["data"]["codigo_pagamento"]
    pagamento_data = PagamentoAtualizaWebhookSchema(codigo_pagamento=codigo, status=3)

    response = client.post("/webhook/update-payment", json=pagamento_data.model_dump())

    assert response.status_code == HTTPStatus.OK


def test_webhook_pagamento_nao_encontrado(client):
    pagamento_data = PagamentoAtualizaWebhookSchema(codigo_pagamento="codigo", status=3)
    response = client.post("/webhook/update-payment", json=pagamento_data.model_dump())

    assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST]


def test_webhook_payload_invalido(client):
    payload = {
        "codigo_errado": "ABC",
        "statuuus": "xyz"
    }

    response = client.post("/webhook/update-payment", json=payload)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
