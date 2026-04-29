import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.core.security import verify_password, hash_password
from app.models.usuario import Usuario

db = SessionLocal()
user = db.query(Usuario).filter(Usuario.email == "admin@aussistencia.com").first()

if not user:
    print("ERRO: usuario nao encontrado no banco!")
else:
    print(f"Usuario encontrado: {user.nome} ({user.email})")
    ok = verify_password("admin123", user.senha_hash)
    print(f"Senha admin123 valida: {ok}")
    if not ok:
        print("Resetando senha agora...")
        user.senha_hash = hash_password("admin123")
        db.commit()
        print("Senha resetada! Tente logar novamente.")

db.close()
