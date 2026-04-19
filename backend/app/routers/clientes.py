from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.cliente import Cliente
from app.models.ordem_servico import OrdemServico
from app.models.orcamento import Orcamento
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from app.dependencies import get_current_user
from app.services.exportacao import exportar_clientes

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("", response_model=List[ClienteOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Cliente).all()

@router.post("", response_model=ClienteOut)
def criar(data: ClienteCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = Cliente(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get("/{id}", response_model=ClienteOut)
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = db.query(Cliente).filter(Cliente.id == id).first()
    if not c:
        raise HTTPException(404, "Cliente nao encontrado")
    return c

@router.put("/{id}", response_model=ClienteOut)
def atualizar(id: int, data: ClienteUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = db.query(Cliente).filter(Cliente.id == id).first()
    if not c:
        raise HTTPException(404, "Cliente nao encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    c = db.query(Cliente).filter(Cliente.id == id).first()
    if not c:
        raise HTTPException(404, "Cliente nao encontrado")
    db.delete(c)
    db.commit()
    return {"ok": True}

@router.get("/exportar/excel")
def exportar_excel(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Exporta todos os clientes em Excel com CPF mascarado (LGPD)."""
    clientes = db.query(Cliente).all()
    return exportar_clientes(clientes)

@router.get("/{id}/historico")
def historico(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    os_list = db.query(OrdemServico).filter(OrdemServico.cliente_id == id).all()
    orc_list = db.query(Orcamento).filter(Orcamento.cliente_id == id).all()
    return {
        "ordens_servico": [{"id": o.id, "status": o.status, "valor_total": o.valor_total,
                             "data_abertura": o.data_abertura} for o in os_list],
        "orcamentos": [{"id": o.id, "status": o.status, "valor_total": o.valor_total,
                        "data": o.data} for o in orc_list],
    }
