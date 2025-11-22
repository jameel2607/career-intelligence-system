from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
from app.api.v1 import auth, students, documents, career, reports, knowledge_base, system, journey
from app.api import compat
from app.core.config import settings
from app.core.exceptions import setup_exception_handlers
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Career Intelligence System")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    yield
    logger.info("Shutting down Career Intelligence System")

app = FastAPI(
    title="Career Intelligence System API",
    description="AI-Powered Student Career Intelligence & Guidance System",
    version="1.0.0",
    lifespan=lifespan
)

# Setup exception handlers
setup_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(career.router, prefix="/api/v1/career", tags=["Career"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(knowledge_base.router, prefix="/api/v1/kb", tags=["Knowledge Base"])
app.include_router(system.router, prefix="/api/v1/system", tags=["System"])
app.include_router(journey.router, prefix="/api/v1/journey", tags=["Journey"])
app.include_router(compat.router, tags=["PRD Compat"])

@app.get("/")
async def root():
    return {"message": "Welcome to Career Intelligence System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "career-intelligence-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
