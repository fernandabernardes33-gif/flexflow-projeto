from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.servico import Servico
from app.schemas.servico import ServicoCreate, ServicoUpdate, ServicoOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/servicos", tags=["servicos"])

@router.get("", response_model=List[ServicoOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Servico).all()

@router.post("", response_model=ServicoOut)
def criar(data: ServicoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    s = Servico(**data.model_dump())
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.put("/{id}", response_model=ServicoOut)
def atualizar(id: int, data: ServicoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    s = db.query(Servico).filter(Servico.id == id).first()
    if not s:
        raise HTTPException(404, "Servico nao encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    return s

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    s = db.query(Servico).filter(Servico.id == id).first()
    if not s:
        raise HTTPException(404, "Servico nao encontrado")
    db.delete(s)
    db.commit()
    return {"ok": True}
