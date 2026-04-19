from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemOrcamentoCreate(BaseModel):
    produto_id: Optional[int] = None
    servico_id: Optional[int] = None
    quantidade: int = 1
    valor_unitario: float = 0.0

class ItemOrcamentoOut(BaseModel):
    id: int
    produto_id: Optional[int] = None
    servico_id: Optional[int] = None
    quantidade: int
    valor_unitario: float
    model_config = {"from_attributes": True}

class OrcamentoCreate(BaseModel):
    cliente_id: int
    validade: Optional[datetime] = None
    observacoes: Optional[str] = None
    itens: List[ItemOrcamentoCreate] = []

class OrcamentoUpdate(BaseModel):
    status: Optional[str] = None
    validade: Optional[datetime] = None
    observacoes: Optional[str] = None
    valor_total: Optional[float] = None

class OrcamentoOut(BaseModel):
    id: int
    cliente_id: int
    status: str
    data: datetime
    validade: Optional[datetime] = None
    observacoes: Optional[str] = None
    valor_total: float
    itens: List[ItemOrcamentoOut] = []
    model_config = {"from_attributes": True}
