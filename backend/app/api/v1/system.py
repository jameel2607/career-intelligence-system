from fastapi import APIRouter
from app.services.ocr_service import get_ocr_info
from app.services.gpt_service import _ollama_available, _openai_available, _ollama_models, check_ollama_connection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/status")
def get_system_status():
    """Get system status including AI and OCR services"""
    
    # Check Ollama status (refresh connection)
    ollama_available, ollama_models = check_ollama_connection()
    
    # Get OCR information
    ocr_info = get_ocr_info()
    
    return {
        "status": "healthy",
        "services": {
            "ai": {
                "ollama": {
                    "available": ollama_available,
                    "models": [model.get('name', 'unknown') for model in ollama_models] if ollama_models else [],
                    "url": "http://localhost:11434",
                    "primary": True
                },
                "openai": {
                    "available": _openai_available,
                    "primary": False
                },
                "fallback_mode": not ollama_available and not _openai_available
            },
            "ocr": {
                "primary_engine": ocr_info['primary_engine'],
                "easyocr_available": ocr_info['easyocr_available'],
                "tesseract_available": ocr_info['tesseract_available'],
                "supported_formats": ocr_info['supported_formats']
            },
            "database": {
                "type": "SQLite",
                "status": "connected"
            }
        },
        "recommendations": {
            "ai": "Install Ollama and pull a model (e.g., 'ollama pull llama2') for local AI processing" if not ollama_available else "Ollama is ready!",
            "ocr": "Install EasyOCR (pip install easyocr) for better OCR accuracy" if not ocr_info['easyocr_available'] else "EasyOCR is ready!"
        }
    }

@router.get("/ai/test")
def test_ai_service():
    """Test AI service with a simple query"""
    from app.services.gpt_service import summarize
    
    test_profile = {
        'skills': 'Python, JavaScript, React',
        'interests': 'Web development, AI',
        'education_level': 'Bachelor'
    }
    
    test_roles = [
        {
            'job_role': 'Frontend Developer',
            'technical_skills': 'JavaScript, React, HTML, CSS',
            'sources': 'https://example.com'
        }
    ]
    
    try:
        result = summarize(test_profile, test_roles)
        return {
            "status": "success",
            "ai_response": result,
            "message": "AI service is working correctly"
        }
    except Exception as e:
        logger.error(f"AI test failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "message": "AI service test failed"
        }

@router.get("/ocr/test")
def test_ocr_service():
    """Test OCR service status"""
    ocr_info = get_ocr_info()
    
    return {
        "status": "success" if ocr_info['primary_engine'] != 'None' else "warning",
        "ocr_info": ocr_info,
        "message": f"OCR service using {ocr_info['primary_engine']}" if ocr_info['primary_engine'] != 'None' else "No OCR engine available"
    }
