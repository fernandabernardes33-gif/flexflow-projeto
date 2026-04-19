from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database import Base

class MovimentacaoFinanceira(Base):
    __tablename__ = "movimentacoes_financeiras"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)  # ENTRADA | SAIDA
    valor = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.utcnow)
    categoria = Column(String, nullable=True)
    os_id = Column(Integer, ForeignKey("ordens_servico.id"), nullable=True)
