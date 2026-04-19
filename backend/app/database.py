"""
Camada de persistência — SQLAlchemy.

Suporta SQLite (desenvolvimento) e PostgreSQL (produção).
A escolha é feita via variável de ambiente DATABASE_URL no .env.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

_url = settings.DATABASE_URL
_is_sqlite = _url.startswith("sqlite")

# SQLite exige check_same_thread=False para funcionar com FastAPI (threads múltiplas).
# PostgreSQL não precisa disso.
_connect_args = {"check_same_thread": False} if _is_sqlite else {}

# pool_pre_ping=True descarta conexões mortas antes de reutilizá-las (importante para PostgreSQL).
engine = create_engine(
    _url,
    connect_args=_connect_args,
    pool_pre_ping=True,
    # Para SQLite, desabilita o pool de conexões (não necessário em single-file DB).
    **({"pool_size": 5, "max_overflow": 10} if not _is_sqlite else {}),
)

# Ativa enforcement de foreign keys no SQLite (desabilitado por padrão).
if _is_sqlite:
    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(conn, _):
        conn.execute("PRAGMA foreign_keys=ON")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependência FastAPI — fornece uma sessão de banco por requisição."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
