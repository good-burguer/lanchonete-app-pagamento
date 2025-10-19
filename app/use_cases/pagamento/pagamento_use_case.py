import uuid
from app.entities.pagamento.entities import PagamentoEntities
from app.adapters.schemas.pagamento import PagamentoResponseSchema, PagamentoAtualizaSchema
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema
from app.models.pagamento import Pagamento
from app.adapters.enums.status_pagamento import PagamentoStatusEnum

class PagamentoUseCase:

    def __init__(self, entities: PagamentoEntities):
        self.pagamento_entities = entities

    def criar_pagamento(self, pedido_pagamento: PagamentoCreateSchema) -> PagamentoResponseSchema:
        codigo_pagamento = str(uuid.uuid4())
        status_pagamento = PagamentoStatusEnum.EmAndamento
       
        pagamento_entity: Pagamento = Pagamento(pedido=pedido_pagamento.pedido_id, codigo_pagamento=codigo_pagamento, status=status_pagamento)
        pagamento_entity: Pagamento = self.pagamento_entities.criar_pagamento(pagamento=pagamento_entity)
        pagamento_response: PagamentoResponseSchema = PagamentoResponseSchema(pedido_id=pagamento_entity.pedido, codigo_pagamento=pagamento_entity.codigo_pagamento, status=pagamento_entity.status)
        
        return pagamento_response
    
    def listar_todos_pagamentos(self) -> list[PagamentoResponseSchema]: 
        consulta_pagamento: list[Pagamento] = self.pagamento_entities.listar_todos_pagamentos()
        pagamento_response: list[PagamentoResponseSchema] = []
        
        for row in consulta_pagamento:
            pagamento_response.append(
                PagamentoResponseSchema(pedido_id=row.pedido, codigo_pagamento=row.codigo_pagamento, status=row.status)
            )
        
        return pagamento_response
    
    def buscar_pagamento_por_codigo(self, codigo_pagamento: str) -> PagamentoResponseSchema:
        pagamento_consulta: Pagamento = self.pagamento_entities.buscar_pagamento_por_codigo(codigo_pagamento=codigo_pagamento)
        pagamento_response: PagamentoResponseSchema = PagamentoResponseSchema(pedido_id=pagamento_consulta.pedido, codigo_pagamento=pagamento_consulta.codigo_pagamento, status=pagamento_consulta.status)

        return pagamento_response
    
    def atualizar_pagamento(self, codigo: str, pagamento_request: PagamentoAtualizaSchema) -> PagamentoResponseSchema: 
        pagamento_entity: Pagamento = self.buscar_pagamento_por_codigo(codigo_pagamento=codigo)
        
        if not pagamento_entity:
            raise ValueError("Pagamento não encontrado")
              
        pagamento_entity.status = pagamento_request.status

        clienteAtualizado: Pagamento = self.pagamento_entities.atualizar_pagamento(codigo=codigo, pagamento=pagamento_entity)
        pagamento_response: PagamentoResponseSchema = PagamentoResponseSchema(pedido_id=clienteAtualizado.pedido_id, codigo_pagamento=clienteAtualizado.codigo_pagamento, status=clienteAtualizado.status)

        return pagamento_response
    
    def deletar_pagamento(self, codigo_pagamento: str): 
        self.pagamento_entities.deletar_pagamento(codigo_pagamento=codigo_pagamento)