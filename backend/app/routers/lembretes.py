from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.lembrete import Lembrete
from app.schemas.lembrete import LembreteCreate, LembreteUpdate, LembreteOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/lembretes", tags=["lembretes"])

@router.get("", response_model=List[LembreteOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Lembrete).order_by(Lembrete.criado_em.desc()).all()

@router.post("", response_model=LembreteOut)
def criar(data: LembreteCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    l = Lembrete(**data.model_dump())
    db.add(l)
    db.commit()
    db.refresh(l)
    return l

@router.put("/{id}", response_model=LembreteOut)
def atualizar(id: int, data: LembreteUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    l = db.query(Lembrete).filter(Lembrete.id == id).first()
    if not l:
        raise HTTPException(404, "Lembrete nao encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(l, k, v)
    db.commit()
    db.refresh(l)
    return l

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    l = db.query(Lembrete).filter(Lembrete.id == id).first()
    if l:
        db.delete(l)
        db.commit()
    return {"ok": True}
