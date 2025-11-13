from enum import Enum

class PagamentoStatusEnum(int, Enum):
    Aprovado = 1
    Reprovado = 2
    EmAndamento = 3
    Cancelado = 4

PaymentStatus = {
    1: "Aprovado",
    2: "Reprovado",
    3: "EmAndamento",
    4: "Cancelado"
}

class PagamentoStatusStringEnum(str, Enum):
    Aprovado = PaymentStatus[1]
    Reprovado = PaymentStatus[2]
    EmAndamento = PaymentStatus[3]
    Cancelado = PaymentStatus[4]