import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, Base, engine
from app.core.security import hash_password
import app.models.usuario, app.models.cliente, app.models.produto
import app.models.movimentacao_estoque, app.models.servico
import app.models.ordem_servico, app.models.item_os
import app.models.orcamento, app.models.item_orcamento
import app.models.movimentacao_financeira, app.models.lembrete

from app.models.usuario import Usuario
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.servico import Servico
from app.models.lembrete import Lembrete
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def seed():
    if db.query(Usuario).first():
        print("Banco ja populado. Pulando seed.")
        db.close()
        return

    admin = Usuario(
        nome="Administrador",
        email="admin@aussistencia.com",
        senha_hash=hash_password("admin123"),
    )
    db.add(admin)

    for nome, tel, email in [
        ("Joao Silva", "(51) 98888-1111", "joao@email.com"),
        ("Maria Oliveira", "(51) 97777-2222", "maria@email.com"),
        ("Carlos Tech", "(51) 96666-3333", None),
    ]:
        db.add(Cliente(nome=nome, telefone=tel, email=email))

    for nome, custo, venda, estoque, minimo in [
        ("Pasta Termica", 5.0, 15.0, 20, 5),
        ("Pente de Memoria RAM DDR4 8GB", 80.0, 150.0, 10, 2),
        ("HD 1TB SATA", 150.0, 280.0, 5, 2),
        ("Cabo HDMI 1.8m", 12.0, 30.0, 3, 5),
    ]:
        db.add(Produto(nome=nome, preco_custo=custo, preco_venda=venda,
                       quantidade_estoque=estoque, quantidade_minima=minimo))

    for nome, valor in [
        ("Formatacao Windows", 120.0),
        ("Manutencao Preventiva", 80.0),
        ("Troca de Tela Notebook", 250.0),
        ("Instalacao de Programa", 40.0),
    ]:
        db.add(Servico(nome=nome, valor=valor))

    now = datetime.now()
    for titulo, prazo in [
        ("Ligar para cliente Joao sobre notebook", now + timedelta(hours=3)),
        ("Comprar pasta termica", now + timedelta(days=1)),
        ("Renovar antivirus do servidor", now + timedelta(days=7)),
    ]:
        db.add(Lembrete(titulo=titulo, data_prazo=prazo))

    db.commit()
    print("Seed concluido com sucesso!")
    print("  Login: admin@aussistencia.com")
    print("  Senha: admin123")
    db.close()

if __name__ == "__main__":
    seed()
