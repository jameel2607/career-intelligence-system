"""
Custom exceptions and error handlers for the Career Intelligence System
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Union

logger = logging.getLogger(__name__)

class CareerIntelligenceException(Exception):
    """Base exception for Career Intelligence System"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class ProfileNotFoundError(CareerIntelligenceException):
    """Raised when student profile is not found"""
    def __init__(self, user_id: int):
        super().__init__(f"Student profile not found for user {user_id}", "PROFILE_NOT_FOUND")

class DocumentProcessingError(CareerIntelligenceException):
    """Raised when document processing fails"""
    def __init__(self, message: str):
        super().__init__(f"Document processing failed: {message}", "DOCUMENT_PROCESSING_ERROR")

class ScoringError(CareerIntelligenceException):
    """Raised when career scoring fails"""
    def __init__(self, message: str):
        super().__init__(f"Career scoring failed: {message}", "SCORING_ERROR")

class KnowledgeBaseError(CareerIntelligenceException):
    """Raised when knowledge base operations fail"""
    def __init__(self, message: str):
        super().__init__(f"Knowledge base error: {message}", "KB_ERROR")

class ReportGenerationError(CareerIntelligenceException):
    """Raised when report generation fails"""
    def __init__(self, message: str):
        super().__init__(f"Report generation failed: {message}", "REPORT_ERROR")

class ValidationError(CareerIntelligenceException):
    """Raised when data validation fails"""
    def __init__(self, message: str):
        super().__init__(f"Validation error: {message}", "VALIDATION_ERROR")

class ExternalServiceError(CareerIntelligenceException):
    """Raised when external service calls fail"""
    def __init__(self, service: str, message: str):
        super().__init__(f"External service '{service}' error: {message}", "EXTERNAL_SERVICE_ERROR")

# Error handlers
async def career_intelligence_exception_handler(request: Request, exc: CareerIntelligenceException):
    """Handle custom Career Intelligence exceptions"""
    logger.error(f"CareerIntelligenceException: {exc.message}", exc_info=True)
    
    status_code_map = {
        "PROFILE_NOT_FOUND": 404,
        "DOCUMENT_PROCESSING_ERROR": 422,
        "SCORING_ERROR": 500,
        "KB_ERROR": 500,
        "REPORT_ERROR": 500,
        "VALIDATION_ERROR": 400,
        "EXTERNAL_SERVICE_ERROR": 503
    }
    
    status_code = status_code_map.get(exc.error_code, 500)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": True,
            "error_code": exc.error_code,
            "message": exc.message,
            "type": "CareerIntelligenceException"
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    
    # Format validation errors in a user-friendly way
    formatted_errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        formatted_errors.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "error_code": "VALIDATION_ERROR",
            "message": "Invalid input data",
            "details": formatted_errors,
            "type": "ValidationError"
        }
    )

async def http_exception_handler(request: Request, exc: Union[HTTPException, StarletteHTTPException]):
    """Handle HTTP exceptions"""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "error_code": f"HTTP_{exc.status_code}",
            "message": exc.detail,
            "type": "HTTPException"
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred. Please try again later.",
            "type": "InternalServerError"
        }
    )

def setup_exception_handlers(app):
    """Setup all exception handlers for the FastAPI app"""
    app.add_exception_handler(CareerIntelligenceException, career_intelligence_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
