import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
import app.models.usuario, app.models.cliente, app.models.produto
import app.models.movimentacao_estoque, app.models.servico
import app.models.ordem_servico, app.models.item_os
import app.models.orcamento, app.models.item_orcamento
import app.models.movimentacao_financeira, app.models.lembrete

from app.routers import auth, clientes, produtos, estoque, servicos
from app.routers import ordens_servico, orcamentos, financeiro, lembretes, painel
from app.models.usuario import Usuario
from app.core.security import hash_password

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

Base.metadata.create_all(bind=engine)


def _auto_seed():
    db = SessionLocal()
    try:
        if not db.query(Usuario).first():
            db.add(Usuario(
                nome="Administrador",
                email="admin@aussistencia.com",
                senha_hash=hash_password("admin123"),
            ))
            db.commit()
            print("Admin criado: admin@aussistencia.com / admin123")
    finally:
        db.close()


_auto_seed()

app = FastAPI(title="SIGIT API", version="1.0.0")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://aussistencia.vercel.app",
    "https://flexflow-projeto.vercel.app",
]
extra = os.getenv("FRONTEND_URL", "")
if extra:
    origins.append(extra)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(produtos.router)
app.include_router(estoque.router)
app.include_router(servicos.router)
app.include_router(ordens_servico.router)
app.include_router(orcamentos.router)
app.include_router(financeiro.router)
app.include_router(lembretes.router)
app.include_router(painel.router)

@app.get("/")
def root():
    return {"status": "SIGIT API online"}
