from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco_custo: float = 0.0
    preco_venda: float = 0.0
    quantidade_estoque: int = 0
    quantidade_minima: int = 1

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    nome: Optional[str] = None

class ProdutoOut(ProdutoBase):
    id: int
    model_config = {"from_attributes": True}

class MovimentacaoEstoqueCreate(BaseModel):
    produto_id: int
    tipo: str  # ENTRADA | SAIDA
    quantidade: int
    observacao: Optional[str] = None

class MovimentacaoEstoqueOut(BaseModel):
    id: int
    produto_id: int
    tipo: str
    quantidade: int
    observacao: Optional[str] = None
    data: str
    model_config = {"from_attributes": True}
