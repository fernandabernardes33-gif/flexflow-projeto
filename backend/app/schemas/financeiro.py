from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovimentacaoFinanceiraCreate(BaseModel):
    tipo: str  # ENTRADA | SAIDA
    valor: float
    descricao: Optional[str] = None
    categoria: Optional[str] = None
    os_id: Optional[int] = None

class MovimentacaoFinanceiraOut(BaseModel):
    id: int
    tipo: str
    valor: float
    descricao: Optional[str] = None
    data: datetime
    categoria: Optional[str] = None
    os_id: Optional[int] = None
    model_config = {"from_attributes": True}
