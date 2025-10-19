from abc import ABC, abstractmethod
from app.models.pagamento import Pagamento

class PagamentoEntities(ABC):
    @abstractmethod
    def criar_pagamento(self, pedido_pagamento: Pagamento): pass

    @abstractmethod
    def buscar_pagamento(self, codigo_pagamento: str): pass

    @abstractmethod
    def listar_todos_pagamentos(self): pass

    @abstractmethod
    def atualizar_pagamento(self, codigo: str, pagamento: Pagamento): pass

    @abstractmethod
    def deletar_pagamento(self, codigo_pagamento: str): pass
