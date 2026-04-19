from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from io import BytesIO
from app.database import get_db
from app.models.ordem_servico import OrdemServico
from app.models.item_os import ItemOS
from app.schemas.ordem_servico import OrdemServicoCreate, OrdemServicoUpdate, OrdemServicoOut
from app.dependencies import get_current_user
from app.services.exportacao import exportar_ordens_servico

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
    total = sum(i.quantidade * i.valor_unitario for i in itens_data)
    os.valor_total = total
    db.add(os)
    db.flush()
    for i in itens_data:
        db.add(ItemOS(os_id=os.id, **i.model_dump()))
    db.commit()
    db.refresh(os)
    return os

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

@router.get("/exportar/excel")
def exportar_excel(status: str = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Exporta ordens de servico em Excel sem dados pessoais (LGPD)."""
    q = db.query(OrdemServico)
    if status:
        q = q.filter(OrdemServico.status == status)
    return exportar_ordens_servico(q.all())

@router.get("/{id}/pdf")
def exportar_pdf(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    os = db.query(OrdemServico).filter(OrdemServico.id == id).first()
    if not os:
        raise HTTPException(404, "OS nao encontrada")
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, h - 50, f"Ordem de Servico #{os.id}")
    c.setFont("Helvetica", 12)
    c.drawString(50, h - 80, f"Status: {os.status}")
    c.drawString(50, h - 100, f"Abertura: {os.data_abertura.strftime('%d/%m/%Y')}")
    c.drawString(50, h - 120, f"Problema: {os.descricao_problema or '-'}")
    c.drawString(50, h - 140, f"Total: R$ {os.valor_total:.2f}")
    c.save()
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=OS_{id}.pdf"})
