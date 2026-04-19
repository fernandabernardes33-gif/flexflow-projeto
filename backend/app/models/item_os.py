from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ItemOS(Base):
    __tablename__ = "itens_os"
    id = Column(Integer, primary_key=True, index=True)
    os_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=True)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=True)
    quantidade = Column(Integer, default=1)
    valor_unitario = Column(Float, default=0.0)

    ordem_servico = relationship("OrdemServico", back_populates="itens")
    produto = relationship("Produto")
    servico = relationship("Servico")
