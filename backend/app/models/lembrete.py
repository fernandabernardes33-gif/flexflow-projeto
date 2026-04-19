from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base

class Lembrete(Base):
    __tablename__ = "lembretes"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    data_prazo = Column(DateTime, nullable=True)
    concluido = Column(Boolean, default=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
