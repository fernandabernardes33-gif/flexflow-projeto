from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.produto import Produto
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/produtos", tags=["produtos"])

@router.get("", response_model=List[ProdutoOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Produto).all()

@router.post("", response_model=ProdutoOut)
def criar(data: ProdutoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = Produto(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/{id}", response_model=ProdutoOut)
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.query(Produto).filter(Produto.id == id).first()
    if not p:
        raise HTTPException(404, "Produto nao encontrado")
    return p

@router.put("/{id}", response_model=ProdutoOut)
def atualizar(id: int, data: ProdutoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.query(Produto).filter(Produto.id == id).first()
    if not p:
        raise HTTPException(404, "Produto nao encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = db.query(Produto).filter(Produto.id == id).first()
    if not p:
        raise HTTPException(404, "Produto nao encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}
