"""
CloudJobHunt Database Connection
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

# SQLAlchemy engine
engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    """Initialize database tables"""
    global engine, SessionLocal
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.create_all(bind=engine)
        print(f"✅ Base de données initialisée: {settings.DATABASE_URL}")
        return True
    except Exception as e:
        print(f"⚠️  Base de données non disponible: {e}")
        print("💡 Mode read-only activé - recherche et endpoints publics fonctionnels")
        return False


def get_db() -> Session:
    """Dependency for getting database session"""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
