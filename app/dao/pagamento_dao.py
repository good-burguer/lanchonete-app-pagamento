from sqlalchemy.exc import IntegrityError
import uuid

from app.models.pagamento import Pagamento
from app.models.pagamento import Pagamento as PagamentoModel
from app.adapters.enums.status_pagamento import PagamentoStatusEnum
from app.adapters.dto.pagamento_dto import PagamentoCreateSchema
from app.adapters.utils.debug import var_dump_die

class PagamentoDAO:
    
    def __init__(self, db_session):
        self.db_name = 'pagamentos'
        self.db_session = db_session

    def criar_pagamento(self, pagamento: PagamentoCreateSchema) -> PagamentoModel | None:
        pagamento_model = PagamentoModel(
            pedido=pagamento.pedido_id, 
            codigo_pagamento = str(uuid.uuid4()),
            status = PagamentoStatusEnum.EmAndamento
        )
        pagamento_dict = {
            "pedido": pagamento_model.pedido,
            "codigo_pagamento": pagamento_model.codigo_pagamento,
            "status": pagamento_model.status.value
        }
        try:
            dbname = self.db_session
            collection_name = dbname[self.db_name]
            
            collection_name.insert_one(pagamento_dict)

        except IntegrityError as e:
            raise Exception(f"Erro de integridade ao salvar pagamento: {e}")

        return pagamento_model
    
    def listar_todos_pagamentos(self):
        dbname = self.db_session
        collection_name = dbname[self.db_name]

        return list(collection_name.find())
    
    def buscar_pagamento_por_codigo(self, codigo_pagamento: str) -> Pagamento | None: 
        dbname = self.db_session
        collection_name = dbname[self.db_name]
        
        return collection_name.find_one({"codigo_pagamento": codigo_pagamento})
    
    def atualizar_pagamento(self, codigo, status) -> Pagamento | None:
        pagamento_entity = self.buscar_pagamento_por_codigo(codigo_pagamento = codigo)
        
        if pagamento_entity :
            dbname = self.db_session
            collection_name = dbname[self.db_name]

            collection_name.update_one(
                {"codigo_pagamento": codigo},
                {"$set": {"status": status}} 
            )

        return self.buscar_pagamento_por_codigo(codigo_pagamento = codigo)
    
    def deletar_pagamento(self, codigo_pagamento: str) -> Pagamento | None: 
        try :
            pagamento_deletar = self.buscar_pagamento_por_codigo(codigo_pagamento = codigo_pagamento)

            if not pagamento_deletar:
                raise ValueError("Pagamento não encontrado")
            
            dbname = self.db_session
            collection_name = dbname[self.db_name]

            collection_name.delete_one(
                {"codigo_pagamento": codigo_pagamento}
            )
        except IntegrityError as e:
            
            raise Exception(f"Erro de integridade ao deletar pagamento: {e}")