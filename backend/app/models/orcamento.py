from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Orcamento(Base):
    __tablename__ = "orcamentos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    validade = Column(DateTime, nullable=True)
    status = Column(String, default="PENDENTE")  # PENDENTE | APROVADO | RECUSADO
    valor_total = Column(Float, default=0.0)
    observacoes = Column(String, nullable=True)

    cliente = relationship("Cliente", back_populates="orcamentos")
    itens = relationship("ItemOrcamento", back_populates="orcamento", cascade="all, delete-orphan")
