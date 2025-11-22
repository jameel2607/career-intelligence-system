from typing import Optional, Tuple
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import EasyOCR (preferred)
easyocr_available = False
try:
    import easyocr
    easyocr_reader = None
    easyocr_available = True
    logger.info("EasyOCR is available")
except ImportError:
    logger.info("EasyOCR not available, will use Tesseract")
    easyocr_available = False

# Try to import Tesseract (fallback)
pytesseract_available = False
try:
    import pytesseract
    from PIL import Image
    pytesseract_available = True
    logger.info("Tesseract is available")
except ImportError:
    logger.info("Tesseract not available - using EasyOCR as primary OCR engine")
    pytesseract_available = False

def get_easyocr_reader():
    """Get or create EasyOCR reader instance"""
    global easyocr_reader
    if easyocr_reader is None and easyocr_available:
        try:
            # Initialize with English and common languages
            easyocr_reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have CUDA
            logger.info("EasyOCR reader initialized")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR reader: {e}")
            return None
    return easyocr_reader

def _extract_image_easyocr(path: str) -> Tuple[Optional[str], Optional[float]]:
    """Extract text from image using EasyOCR"""
    try:
        reader = get_easyocr_reader()
        if reader is None:
            return None, None
        
        # Read text from image
        results = reader.readtext(path, detail=1)
        
        if not results:
            return "", 0.0
        
        # Extract text and confidence
        texts = []
        confidences = []
        
        for (bbox, text, confidence) in results:
            if text.strip():  # Only add non-empty text
                texts.append(text.strip())
                confidences.append(confidence)
        
        combined_text = " ".join(texts)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        logger.info(f"EasyOCR extracted {len(texts)} text segments with avg confidence {avg_confidence:.2f}")
        return combined_text, float(avg_confidence) if avg_confidence is not None else 0.0
        
    except Exception as e:
        logger.error(f"EasyOCR extraction failed: {e}")
        return None, None

def _extract_image_tesseract(path: str) -> Tuple[Optional[str], Optional[float]]:
    """Extract text from image using Tesseract (fallback)"""
    try:
        img = Image.open(path)
        
        # Use better OCR configuration
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?@#$%^&*()_+-=[]{}|;:,.<>?/~` '
        txt = pytesseract.image_to_string(img, config=custom_config)
        
        try:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            confs = [float(c) for c in data.get('conf', []) if str(c).replace('-', '').isdigit() and float(c) > 0]
            conf = sum(confs) / len(confs) if confs else 0.0
        except Exception:
            conf = 0.0
        
        logger.info(f"Tesseract extracted text with confidence {conf:.2f}")
        return txt, conf / 100.0  # Normalize to 0-1 range
        
    except Exception as e:
        logger.error(f"Tesseract extraction failed: {e}")
        return None, None

def _extract_image(path: str) -> Tuple[Optional[str], Optional[float]]:
    """Extract text from image using best available OCR"""
    # Try EasyOCR first (better accuracy)
    if easyocr_available:
        result = _extract_image_easyocr(path)
        if result[0] is not None:
            return result
        logger.warning("EasyOCR failed, trying Tesseract")
    
    # Fallback to Tesseract
    if pytesseract_available:
        return _extract_image_tesseract(path)
    
    logger.error("No OCR engine available")
    return None, None

def _extract_pdf(path: str) -> Tuple[Optional[str], Optional[float]]:
    """Extract text from PDF by converting to images"""
    try:
        from pdf2image import convert_from_path
    except ImportError:
        logger.error("pdf2image not available for PDF processing")
        return None, None
    
    try:
        # Convert PDF pages to images
        pages = convert_from_path(path, dpi=200, first_page=1, last_page=3)  # Limit to first 3 pages
        
        if not pages:
            return "", 0.0
        
        all_texts = []
        all_confidences = []
        
        for i, page_image in enumerate(pages):
            logger.info(f"Processing PDF page {i+1}")
            
            # Save page as temporary image
            temp_path = f"/tmp/pdf_page_{i}.png" if os.name != 'nt' else f"temp_pdf_page_{i}.png"
            page_image.save(temp_path, 'PNG')
            
            try:
                # Extract text from page image
                text, confidence = _extract_image(temp_path)
                
                if text and text.strip():
                    all_texts.append(text.strip())
                    if confidence is not None:
                        all_confidences.append(confidence)
                
            finally:
                # Clean up temporary file
                try:
                    os.remove(temp_path)
                except:
                    pass
        
        combined_text = "\n\n".join(all_texts)
        avg_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
        
        logger.info(f"PDF processing complete: {len(all_texts)} pages, avg confidence {avg_confidence:.2f}")
        return combined_text, avg_confidence
        
    except Exception as e:
        logger.error(f"PDF extraction failed: {e}")
        return None, None

def extract_text(path: str) -> Tuple[Optional[str], Optional[float]]:
    """
    Extract text from document using the best available OCR engine.
    
    Args:
        path: Path to the document file
        
    Returns:
        Tuple of (extracted_text, confidence_score)
        confidence_score is between 0.0 and 1.0
    """
    if not os.path.exists(path):
        logger.error(f"File not found: {path}")
        return None, None
    
    # Check if any OCR engine is available
    if not easyocr_available and not pytesseract_available:
        logger.error("No OCR engine available (neither EasyOCR nor Tesseract)")
        return None, None
    
    file_path = Path(path)
    file_extension = file_path.suffix.lower()
    
    logger.info(f"Extracting text from {file_extension} file: {path}")
    
    try:
        if file_extension == '.pdf':
            return _extract_pdf(path)
        elif file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']:
            return _extract_image(path)
        else:
            logger.warning(f"Unsupported file type: {file_extension}")
            return None, None
            
    except Exception as e:
        logger.error(f"Text extraction failed for {path}: {e}")
        return None, None

def get_ocr_info() -> dict:
    """Get information about available OCR engines"""
    return {
        'easyocr_available': easyocr_available,
        'tesseract_available': pytesseract_available,
        'primary_engine': 'EasyOCR' if easyocr_available else 'Tesseract' if pytesseract_available else 'None',
        'supported_formats': ['.pdf', '.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    }
