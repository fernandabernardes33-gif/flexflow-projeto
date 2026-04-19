from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.produto import Produto
from app.models.movimentacao_estoque import MovimentacaoEstoque
from app.schemas.produto import MovimentacaoEstoqueCreate, MovimentacaoEstoqueOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/estoque", tags=["estoque"])

@router.get("", response_model=List[MovimentacaoEstoqueOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    movs = db.query(MovimentacaoEstoque).order_by(MovimentacaoEstoque.data.desc()).all()
    return [MovimentacaoEstoqueOut(
        id=m.id, produto_id=m.produto_id, tipo=m.tipo,
        quantidade=m.quantidade, observacao=m.observacao,
        data=str(m.data)
    ) for m in movs]

@router.post("", response_model=MovimentacaoEstoqueOut)
def registrar(data: MovimentacaoEstoqueCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    produto = db.query(Produto).filter(Produto.id == data.produto_id).first()
    if not produto:
        raise HTTPException(404, "Produto nao encontrado")
    if data.tipo == "ENTRADA":
        produto.quantidade_estoque += data.quantidade
    elif data.tipo == "SAIDA":
        if produto.quantidade_estoque < data.quantidade:
            raise HTTPException(400, "Estoque insuficiente")
        produto.quantidade_estoque -= data.quantidade
    else:
        raise HTTPException(400, "Tipo deve ser ENTRADA ou SAIDA")
    mov = MovimentacaoEstoque(**data.model_dump())
    db.add(mov)
    db.commit()
    db.refresh(mov)
    return MovimentacaoEstoqueOut(
        id=mov.id, produto_id=mov.produto_id, tipo=mov.tipo,
        quantidade=mov.quantidade, observacao=mov.observacao,
        data=str(mov.data)
    )
