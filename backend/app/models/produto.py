from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco_custo = Column(Float, default=0.0)
    preco_venda = Column(Float, default=0.0)
    quantidade_estoque = Column(Integer, default=0)
    quantidade_minima = Column(Integer, default=1)

    movimentacoes = relationship("MovimentacaoEstoque", back_populates="produto")
