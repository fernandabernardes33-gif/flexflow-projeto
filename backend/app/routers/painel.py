from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models.ordem_servico import OrdemServico
from app.models.movimentacao_financeira import MovimentacaoFinanceira
from app.models.produto import Produto
from app.models.lembrete import Lembrete
from app.dependencies import get_current_user

router = APIRouter(prefix="/painel", tags=["painel"])

@router.get("")
def painel(db: Session = Depends(get_db), _=Depends(get_current_user)):
    agora = datetime.utcnow()
    inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    os_abertas = db.query(OrdemServico).filter(OrdemServico.status == "ABERTA").count()
    os_andamento = db.query(OrdemServico).filter(OrdemServico.status == "EM_ANDAMENTO").count()
    os_concluidas = db.query(OrdemServico).filter(
        OrdemServico.status == "CONCLUIDA",
        OrdemServico.data_abertura >= inicio_mes
    ).count()

    movs_mes = db.query(MovimentacaoFinanceira).filter(
        MovimentacaoFinanceira.data >= inicio_mes
    ).all()
    receita = sum(m.valor for m in movs_mes if m.tipo == "ENTRADA")
    despesas = sum(m.valor for m in movs_mes if m.tipo == "SAIDA")

    estoque_baixo = db.query(Produto).filter(
        Produto.quantidade_estoque <= Produto.quantidade_minima
    ).all()

    lembretes = db.query(Lembrete).filter(
        Lembrete.concluido == False
    ).order_by(Lembrete.data_prazo).limit(5).all()

    return {
        "os_abertas": os_abertas,
        "os_andamento": os_andamento,
        "os_concluidas_mes": os_concluidas,
        "receita_mes": receita,
        "despesas_mes": despesas,
        "saldo_mes": receita - despesas,
        "estoque_baixo": [{"id": p.id, "nome": p.nome, "estoque": p.quantidade_estoque,
                           "minimo": p.quantidade_minima} for p in estoque_baixo],
        "lembretes_pendentes": [{"id": l.id, "titulo": l.titulo,
                                 "data_prazo": l.data_prazo} for l in lembretes],
    }
