from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    APP_NAME: str = "Career Intelligence System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./career.db")
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173"]
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 20 * 1024 * 1024
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".jpg", ".jpeg", ".png"]
    
    # AI Configuration
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    GPT5_API_KEY: str = os.getenv("GPT5_API_KEY", "")
    GPT5_MODEL: str = os.getenv("GPT5_MODEL", "gpt-4")
    
    # OCR Configuration
    OCR_ENGINE: str = os.getenv("OCR_ENGINE", "easyocr")
    GOOGLE_VISION_API_KEY: Optional[str] = os.getenv("GOOGLE_VISION_API_KEY")
    
    # Other settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    KB_FILE_PATH: str = "knowledge_base/career_intelligence_kb.xlsx"
    EMBEDDINGS_DIR: str = "knowledge_base/embeddings"
    REPORT_TEMPLATE_DIR: str = "reports/templates"
    REPORT_OUTPUT_DIR: str = "reports/generated"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env

settings = Settings()
