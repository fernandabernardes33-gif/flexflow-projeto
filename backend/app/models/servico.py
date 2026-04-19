from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    valor = Column(Float, default=0.0)
