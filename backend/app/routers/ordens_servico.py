from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.ordem_servico import OrdemServico
from app.models.item_os import ItemOS
from app.schemas.ordem_servico import OrdemServicoCreate, OrdemServicoUpdate, OrdemServicoOut
from app.dependencies import get_current_user
from app.services.exportacao import exportar_ordens_servico
from app.utils.gerar_pdf import gerar_pdf_os

router = APIRouter(prefix="/ordens-servico", tags=["ordens-servico"])

@router.get("", response_model=List[OrdemServicoOut])
def listar(status: str = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(OrdemServico)
    if status:
        q = q.filter(OrdemServico.status == status)
    return q.order_by(OrdemServico.data_abertura.desc()).all()

@router.post("", response_model=OrdemServicoOut)
def criar(data: OrdemServicoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    itens_data = data.itens
    os_data = data.model_dump(exclude={"itens"})
    os = OrdemServico(**os_data)
    os.valor_total = sum(i.quantidade * i.valor_unitario for i in itens_data)
    db.add(os)
    db.flush()
    for i in itens_data:
        db.add(ItemOS(os_id=os.id, **i.model_dump()))
    db.commit()
    db.refresh(os)
    return os

@router.get("/exportar/excel")
def exportar_excel(status: str = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    q = db.query(OrdemServico)
    if status:
        q = q.filter(OrdemServico.status == status)
    return exportar_ordens_servico(q.all())

@router.get("/{id}/pdf")
def exportar_pdf(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    os = db.query(OrdemServico).filter(OrdemServico.id == id).first()
    if not os:
        raise HTTPException(404, "OS nao encontrada")
    itens = []
    for item in os.itens:
        descricao = ""
        if item.servico:
            descricao = item.servico.nome
        elif item.produto:
            descricao = item.produto.nome
        itens.append({
            "descricao": descricao,
            "quantidade": item.quantidade,
            "valor_unitario": float(item.valor_unitario),
            "subtotal": float(item.quantidade * item.valor_unitario),
        })
    os_data = {
        "id": os.id,
        "data_abertura": os.data_abertura.strftime("%d/%m/%Y") if os.data_abertura else "",
        "data_previsao": os.data_previsao.strftime("%d/%m/%Y") if os.data_previsao else "",
        "status": os.status,
        "cliente_nome": os.cliente.nome if os.cliente else "",
        "descricao_problema": os.descricao_problema or "",
        "valor_total": float(os.valor_total or 0),
        "itens": itens,
    }
    return gerar_pdf_os(os_data)

@router.get("/{id}", response_model=OrdemServicoOut)
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    os = db.query(OrdemServico).filter(OrdemServico.id == id).first()
    if not os:
        raise HTTPException(404, "OS nao encontrada")
    return os

@router.put("/{id}", response_model=OrdemServicoOut)
def atualizar(id: int, data: OrdemServicoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    os = db.query(OrdemServico).filter(OrdemServico.id == id).first()
    if not os:
        raise HTTPException(404, "OS nao encontrada")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(os, k, v)
    db.commit()
    db.refresh(os)
    return os

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    os = db.query(OrdemServico).filter(OrdemServico.id == id).first()
    if not os:
        raise HTTPException(404, "OS nao encontrada")
    db.delete(os)
    db.commit()
    return {"ok": True}
