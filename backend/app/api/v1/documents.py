from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas import DocumentRead
from app.services.document_service import save_document, list_documents, get_document, set_ocr_text
from app.services.kb_service import load_kb
from app.services.ocr_service import extract_text

router = APIRouter()

@router.get("/", response_model=list[DocumentRead])
def list_my_documents(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_documents(db, current_user.id)

@router.post("/upload", response_model=DocumentRead)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    content = await file.read()
    doc = save_document(db, current_user.id, file.filename, content, file.content_type)
    return doc

@router.post("/{doc_id}/ocr", response_model=DocumentRead)
def ocr(doc_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    doc = get_document(db, doc_id, current_user.id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    text, conf = extract_text(doc.path)
    doc = set_ocr_text(db, doc, (text or ""), conf)
    return doc

@router.post("/extract-skills")
def extract_skills(body: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ids = body.get('document_ids') or []
    skills = []
    kb = load_kb()
    skill_col = None
    for c in kb.columns:
        if 'technical' in c.lower() and 'skills' in c.lower():
            skill_col = c
            break
    skill_vocab = set()
    if skill_col:
        for s in kb[skill_col].dropna().astype(str).tolist():
            for token in s.replace(';', ',').split(','):
                t = token.strip().lower()
                if t:
                    skill_vocab.add(t)
    for doc_id in ids:
        doc = get_document(db, int(doc_id), current_user.id)
        if not doc or not doc.ocr_text:
            continue
        text = doc.ocr_text.lower()
        found = [sv for sv in skill_vocab if sv and sv in text][:20]
        for f in found:
            skills.append(f)
    return {'skills': sorted(set(skills)), 'confidence': 0.6}
