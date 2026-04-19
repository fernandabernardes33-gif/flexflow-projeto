from pydantic import BaseModel
from typing import Optional

class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    valor: float = 0.0

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(ServicoBase):
    nome: Optional[str] = None

class ServicoOut(ServicoBase):
    id: int
    model_config = {"from_attributes": True}
