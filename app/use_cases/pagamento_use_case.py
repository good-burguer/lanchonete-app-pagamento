
from app.entities.pagamento import PagamentoEntities
from app.adapters.schemas.pagamento import PagamentoResponseSchema
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema
from app.models.pagamento import Pagamento


from app.adapters.utils.debug import var_dump_die

class PagamentoUseCase:

    def __init__(self, entities: PagamentoEntities):
        self.pagamento_entity = entities

    def criar_pagamento(self, pedido_pagamento: PagamentoCreateSchema) -> PagamentoResponseSchema:
        pagamento_criado: Pagamento = self.pagamento_entity.criar_pagamento(pagamento=pedido_pagamento)
        
        return PagamentoResponseSchema(
            pedido_id = pagamento_criado.pedido,
            codigo_pagamento = pagamento_criado.codigo_pagamento,
            status = pagamento_criado.status
        )
    
    def buscar_pagamento(self, codigo_pagamento: str) -> PagamentoResponseSchema:
        pagamento_consulta: Pagamento = self.pagamento_entity.buscar_pagamento(codigo_pagamento=codigo_pagamento)
        
        if not pagamento_consulta:
            raise ValueError("Pagamento não encontrado")

        return self._response_schema(pagamento_consulta)
    
    def listar_todos_pagamentos(self) -> list[PagamentoResponseSchema]: 
        consulta_pagamento: list[Pagamento] = self.pagamento_entity.listar_todos_pagamentos()
        pagamento_response: list[PagamentoResponseSchema] = []
        
        for row in consulta_pagamento:
            pagamento_response.append(
                self._response_schema(row)
            )
        
        return pagamento_response
            
    def atualizar_pagamento(self, codigo, status) -> PagamentoResponseSchema:
        clienteAtualizado: Pagamento = self.pagamento_entity.atualizar_pagamento(codigo, status)

        if not clienteAtualizado:
            raise ValueError("Pagamento não encontrado")

        return (PagamentoResponseSchema(
                pedido_id = clienteAtualizado['pedido'],
                codigo_pagamento = clienteAtualizado['codigo_pagamento'],
                status = clienteAtualizado['status']
            ))
    
    def deletar_pagamento(self, codigo_pagamento: str): 
        self.pagamento_entity.deletar_pagamento(codigo_pagamento=codigo_pagamento)

    def _response_schema(self, pagamento) : 
        
        return PagamentoResponseSchema(
            pedido_id = pagamento['pedido'],
            codigo_pagamento = pagamento['codigo_pagamento'],
            status = pagamento['status']
        )
