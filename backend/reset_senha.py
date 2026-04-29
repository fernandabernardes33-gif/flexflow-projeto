import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.core.security import hash_password
from app.models.usuario import Usuario

db = SessionLocal()
user = db.query(Usuario).filter(Usuario.email == "admin@aussistencia.com").first()
if user:
    user.senha_hash = hash_password("admin123")
    db.commit()
    print("Senha resetada com sucesso!")
    print("Login: admin@aussistencia.com")
    print("Senha: admin123")
else:
    print("Usuario nao encontrado.")
db.close()
