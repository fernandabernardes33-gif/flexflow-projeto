from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class OrdemServico(Base):
    __tablename__ = "ordens_servico"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_abertura = Column(DateTime, default=datetime.utcnow)
    data_previsao = Column(DateTime, nullable=True)
    status = Column(String, default="ABERTA")  # ABERTA | EM_ANDAMENTO | CONCLUIDA | CANCELADA
    descricao_problema = Column(String, nullable=True)
    valor_total = Column(Float, default=0.0)
    observacoes = Column(String, nullable=True)

    cliente = relationship("Cliente", back_populates="ordens_servico")
    itens = relationship("ItemOS", back_populates="ordem_servico", cascade="all, delete-orphan")
