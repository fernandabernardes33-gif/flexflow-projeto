from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    nome: Optional[str] = None

class ClienteOut(ClienteBase):
    id: int
    model_config = {"from_attributes": True}
