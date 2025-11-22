from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

is_sqlite = settings.DATABASE_URL.startswith("sqlite")
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if is_sqlite else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db_sync():
    """Synchronous database initialization"""
    # Import all models to ensure they are registered with Base
    from app.models import user, student, document, report, career_score, course, user_course, user_progress  # noqa: F401
    Base.metadata.create_all(bind=engine)

async def init_db():
    """Async wrapper for database initialization"""
    init_db_sync()
