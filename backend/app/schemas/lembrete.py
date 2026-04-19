from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LembreteBase(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_prazo: Optional[datetime] = None

class LembreteCreate(LembreteBase):
    pass

class LembreteUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data_prazo: Optional[datetime] = None
    concluido: Optional[bool] = None

class LembreteOut(LembreteBase):
    id: int
    concluido: bool
    criado_em: datetime
    model_config = {"from_attributes": True}
