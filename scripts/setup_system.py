#!/usr/bin/env python3
"""
Setup script for the Career Intelligence System
This script initializes the database, creates the knowledge base, and sets up embeddings
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
backend_path = project_root / "backend"
sys.path.insert(0, str(backend_path))

from app.database import engine, Base
from app.services.embeddings_service import build_index
sys.path.insert(0, str(project_root))
from scripts.create_knowledge_base import create_knowledge_base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Create all database tables"""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

def setup_knowledge_base():
    """Create and setup the knowledge base"""
    try:
        logger.info("Setting up knowledge base...")
        kb_path = create_knowledge_base()
        logger.info(f"Knowledge base created at: {kb_path}")
        return kb_path
    except Exception as e:
        logger.error(f"Failed to setup knowledge base: {e}")
        raise

def setup_embeddings():
    """Build embeddings index for RAG"""
    try:
        logger.info("Building embeddings index...")
        build_index()
        logger.info("Embeddings index built successfully")
    except Exception as e:
        logger.error(f"Failed to build embeddings index: {e}")
        logger.warning("Embeddings will use fallback mode")

def create_directories():
    """Create necessary directories"""
    directories = [
        project_root / "backend" / "uploads",
        project_root / "reports" / "generated",
        project_root / "knowledge_base" / "embeddings"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def setup_environment():
    """Setup environment variables and configuration"""
    env_file = project_root / "backend" / ".env"
    
    if not env_file.exists():
        logger.info("Creating .env file from template...")
        env_template = project_root / "backend" / ".env.example"
        
        if env_template.exists():
            import shutil
            shutil.copy(env_template, env_file)
            logger.info("Created .env file. Please update it with your configuration.")
        else:
            logger.warning(".env.example not found. Please create .env file manually.")
    else:
        logger.info(".env file already exists")

def main():
    """Main setup function"""
    logger.info("Starting Career Intelligence System setup...")
    
    try:
        # Create necessary directories
        create_directories()
        
        # Setup environment
        setup_environment()
        
        # Setup database
        setup_database()
        
        # Setup knowledge base
        setup_knowledge_base()
        
        # Setup embeddings (optional, may fail without dependencies)
        setup_embeddings()
        
        logger.info("✅ Career Intelligence System setup completed successfully!")
        logger.info("Next steps:")
        logger.info("1. Update backend/.env with your configuration")
        logger.info("2. Install frontend dependencies: cd frontend && npm install")
        logger.info("3. Start the backend: cd backend && python -m uvicorn app.main:app --reload")
        logger.info("4. Start the frontend: cd frontend && npm run dev")
        
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
