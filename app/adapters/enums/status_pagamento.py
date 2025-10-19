from enum import Enum

class PagamentoStatusEnum(str, Enum):
    Aprovado = 1
    Reprovado = 2
    EmAndamento = 3
    Cancelado = 4
    