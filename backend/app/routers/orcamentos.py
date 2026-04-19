from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from io import BytesIO
from app.database import get_db
from app.models.orcamento import Orcamento
from app.models.item_orcamento import ItemOrcamento
from app.schemas.orcamento import OrcamentoCreate, OrcamentoUpdate, OrcamentoOut
from app.dependencies import get_current_user

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

@router.get("/{id}/pdf")
def exportar_pdf(id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    orc = db.query(Orcamento).filter(Orcamento.id == id).first()
    if not orc:
        raise HTTPException(404, "Orcamento nao encontrado")
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, h - 50, f"Orcamento #{orc.id}")
    c.setFont("Helvetica", 12)
    c.drawString(50, h - 80, f"Status: {orc.status}")
    c.drawString(50, h - 100, f"Data: {orc.data.strftime('%d/%m/%Y')}")
    c.drawString(50, h - 120, f"Total: R$ {orc.valor_total:.2f}")
    c.save()
    buf.seek(0)
    return StreamingResponse(buf, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Orcamento_{id}.pdf"})
