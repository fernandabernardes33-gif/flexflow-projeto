from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.orcamento import Orcamento
from app.models.item_orcamento import ItemOrcamento
from app.schemas.orcamento import OrcamentoCreate, OrcamentoUpdate, OrcamentoOut
from app.dependencies import get_current_user
from app.services.exportacao import exportar_financeiro
from app.utils.gerar_pdf import gerar_pdf_orcamento

router = APIRouter(prefix="/orcamentos", tags=["orcamentos"])

@router.get("", response_model=List[OrcamentoOut])
def listar(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Orcamento).order_by(Orcamento.data.desc()).all()

@router.post("", response_model=OrcamentoOut)
def criar(data: OrcamentoCreate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    itens_data = data.itens
    orc_data = data.model_dump(exclude={"itens"})
    orc = Orcamento(**orc_data)
    orc.valor_total = sum(i.quantidade * i.valor_unitario for i in itens_data)
    db.add(orc)
    db.flush()
    for i in itens_data:
        db.add(ItemOrcamento(orcamento_id=orc.id, **i.model_dump()))
    db.commit()
    db.refresh(orc)
    return orc

@router.get("/{id}/pdf")
def exportar_pdf(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    orc = db.query(Orcamento).filter(Orcamento.id == id).first()
    if not orc:
        raise HTTPException(404, "Orcamento nao encontrado")
    itens = []
    for item in orc.itens:
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
    orc_data = {
        "id": orc.id,
        "data": orc.data.strftime("%d/%m/%Y") if orc.data else "",
        "validade": orc.validade.strftime("%d/%m/%Y") if orc.validade else "",
        "status": orc.status,
        "cliente_nome": orc.cliente.nome if orc.cliente else "",
        "valor_total": float(orc.valor_total or 0),
        "itens": itens,
    }
    return gerar_pdf_orcamento(orc_data)

@router.get("/{id}", response_model=OrcamentoOut)
def buscar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    orc = db.query(Orcamento).filter(Orcamento.id == id).first()
    if not orc:
        raise HTTPException(404, "Orcamento nao encontrado")
    return orc

@router.put("/{id}", response_model=OrcamentoOut)
def atualizar(id: int, data: OrcamentoUpdate, db: Session = Depends(get_db), _=Depends(get_current_user)):
    orc = db.query(Orcamento).filter(Orcamento.id == id).first()
    if not orc:
        raise HTTPException(404, "Orcamento nao encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(orc, k, v)
    db.commit()
    db.refresh(orc)
    return orc

@router.delete("/{id}")
def deletar(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    orc = db.query(Orcamento).filter(Orcamento.id == id).first()
    if not orc:
        raise HTTPException(404, "Orcamento nao encontrado")
    db.delete(orc)
    db.commit()
    return {"ok": True}
