from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.db.database import Base

class Pagamento(Base):
    __tablename__ = "pagamento"

    pedido = Column(Integer, ForeignKey("pedido.pedido_id"), primary_key=True, nullable=False)
    codigo_pagamento = Column(String(255), primary_key=True, nullable=False)
    status = Column(Integer, nullable=True)

    #pedido_relacionado = relationship("Pedido", backref="pagamentos")
    
    