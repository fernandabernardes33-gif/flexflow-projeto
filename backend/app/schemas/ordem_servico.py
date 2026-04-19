from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemOSCreate(BaseModel):
    produto_id: Optional[int] = None
    servico_id: Optional[int] = None
    quantidade: int = 1
    valor_unitario: float = 0.0

class ItemOSOut(BaseModel):
    id: int
    produto_id: Optional[int] = None
    servico_id: Optional[int] = None
    quantidade: int
    valor_unitario: float
    model_config = {"from_attributes": True}

class OrdemServicoCreate(BaseModel):
    cliente_id: int
    data_previsao: Optional[datetime] = None
    descricao_problema: Optional[str] = None
    observacoes: Optional[str] = None
    itens: List[ItemOSCreate] = []

class OrdemServicoUpdate(BaseModel):
    status: Optional[str] = None
    data_previsao: Optional[datetime] = None
    descricao_problema: Optional[str] = None
    observacoes: Optional[str] = None
    valor_total: Optional[float] = None

class OrdemServicoOut(BaseModel):
    id: int
    cliente_id: int
    status: str
    data_abertura: datetime
    data_previsao: Optional[datetime] = None
    descricao_problema: Optional[str] = None
    observacoes: Optional[str] = None
    valor_total: float
    itens: List[ItemOSOut] = []
    model_config = {"from_attributes": True}
