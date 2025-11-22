from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db, get_current_user
from app.services.student_service import get_by_user_id, create_profile, update_profile
from app.schemas.student import StudentCreate, StudentUpdate, StudentRead
from app.services.scoring_service import compute_score
from app.services.document_service import get_document, set_ocr_text
from app.services.ocr_service import extract_text
from app.services.report_service import get_report

router = APIRouter()

# Auth logout (compat)
@router.post('/api/auth/logout')
def logout():
    return {'success': True}

# Student profile (compat)
@router.get('/api/student/profile', response_model=StudentRead)
def compat_profile_get(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail='Profile not found')
    return profile

@router.post('/api/student/profile', response_model=StudentRead, status_code=201)
def compat_profile_create(data: StudentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    existing = get_by_user_id(db, current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail='Profile already exists')
    return create_profile(db, current_user.id, data)

@router.put('/api/student/profile', response_model=StudentRead)
def compat_profile_update(data: StudentUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail='Profile not found')
    return update_profile(db, profile, data)

# Documents analyze (compat)
class AnalyzeRequest:
    document_ids: Optional[List[int]] = None

@router.post('/api/documents/analyze')
def compat_documents_analyze(body: dict, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    ids = body.get('document_ids') or []
    processed = []
    for doc_id in ids:
        doc = get_document(db, int(doc_id), current_user.id)
        if not doc:
            continue
        text = extract_text(doc.path) or ''
        set_ocr_text(db, doc, text)
        processed.append(doc_id)
    return {'analysis_id': 'local', 'status': 'completed', 'processed': processed}

@router.post('/api/documents/extract-skills')
def compat_extract_skills(body: dict):
    return {'skills': [], 'confidence': 0.0}

# Career calculate-score + skill-gaps (compat)
@router.post('/api/career/calculate-score')
def compat_calculate_score(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail='Profile not found')
    s, strengths, improvements, breakdown, confidence = compute_score(db, profile)
    return {'score': s, 'breakdown': breakdown, 'confidence': confidence}

@router.post('/api/career/skill-gaps')
def compat_skill_gaps(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    skills = (profile.skills or '').lower()
    gaps = []
    for k in ['sql','docker','linux']:
        if k not in skills:
            gaps.append(k)
    return {'skill_gaps': gaps}

# Reports status (compat)
@router.get('/api/reports/{id}')
def compat_report_status(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    r = get_report(db, current_user.id, id)
    if not r:
        raise HTTPException(status_code=404, detail='Report not found')
    return {'id': r.id, 'path': r.path, 'filename': r.filename}
