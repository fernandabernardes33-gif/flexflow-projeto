from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.movimentacao_financeira import MovimentacaoFinanceira
from app.schemas.financeiro import MovimentacaoFinanceiraCreate, MovimentacaoFinanceiraOut
from app.dependencies import get_current_user

router = APIRouter(prefix="/financeiro", tags=["financeiro"])

@router.get("", response_model=List[MovimentacaoFinanceiraOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(MovimentacaoFinanceira).order_by(MovimentacaoFinanceira.data.desc()).all()

@router.post("", response_model=MovimentacaoFinanceiraOut)
def criar(data: MovimentacaoFinanceiraCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    m = MovimentacaoFinanceira(**data.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    m = db.query(MovimentacaoFinanceira).filter(MovimentacaoFinanceira.id == id).first()
    if m:
        db.delete(m)
        db.commit()
    return {"ok": True}
