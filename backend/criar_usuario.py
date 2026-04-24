from app.database import SessionLocal, Base, engine
from app.models.usuario import Usuario
from app.core.security import pwd_context
import sys

Base.metadata.create_all(bind=engine)

email = "fernanda.bernardes33@gmail.com"
senha = "admin"
nome  = "Fernanda Bernardes"

db = SessionLocal()
if db.query(Usuario).filter(Usuario.email == email).first():
    print(f"Usuário {email} já existe.")
else:
    u = Usuario(nome=nome, email=email, senha_hash=pwd_context.hash(senha), ativo=True)
    db.add(u)
    db.commit()
    print(f"Usuário criado: {email} / {senha}")
db.close()
