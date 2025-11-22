import os
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document import Document
from app.core.config import settings

def ensure_upload_dir():
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

def save_document(db: Session, user_id: int, filename: str, file_bytes: bytes, mime_type: str | None) -> Document:
    _ensure_document_column(db)
    ensure_upload_dir()
    safe_name = f"{user_id}_{filename}"
    path = os.path.join(settings.UPLOAD_DIR, safe_name)
    with open(path, "wb") as f:
        f.write(file_bytes)
    doc = Document(user_id=user_id, filename=filename, path=path, mime_type=mime_type)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

def list_documents(db: Session, user_id: int) -> List[Document]:
    return db.query(Document).filter(Document.user_id == user_id).order_by(Document.id.desc()).all()

def get_document(db: Session, doc_id: int, user_id: int) -> Document | None:
    return db.query(Document).filter(Document.id == doc_id, Document.user_id == user_id).first()

def set_ocr_text(db: Session, doc: Document, text: str, confidence: float | None = None):
    doc.ocr_text = text
    doc.ocr_confidence = confidence
    db.commit()
    db.refresh(doc)
    return doc
def _ensure_document_column(db: Session):
    try:
        cols = db.execute(text('PRAGMA table_info(documents)')).mappings().all()
        names = {c['name'] for c in cols}
        if 'ocr_confidence' not in names:
            db.execute(text('ALTER TABLE documents ADD COLUMN ocr_confidence FLOAT'))
    except Exception:
        pass
