from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import FileResponse
from app.dependencies import get_db, get_current_user
from app.schemas import ReportRead
from app.services.report_service import render_report, save_report, list_reports, get_report, create_professional_pdf_report
from app.services.student_service import get_by_user_id
from app.services.scoring_service import compute_score, recommend
from app.services.gpt_service import summarize
from app.services.rag_service import retrieve_roles

router = APIRouter()

@router.get("/", response_model=list[ReportRead])
def list_my_reports(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return list_reports(db, current_user.id)

@router.post("/generate", response_model=ReportRead, status_code=201)
def generate(format: str = 'html', db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = get_by_user_id(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Generate comprehensive analysis
    s, strengths, improvements, breakdown, confidence = compute_score(db, profile)
    jobs, skills_to_learn = recommend(db, profile)
    
    # Get AI recommendations
    profile_dict = {
        'skills': profile.skills or '',
        'interests': profile.interests or '',
        'education_level': profile.education_level or '',
        'bio': profile.bio or ''
    }
    
    # Retrieve relevant roles for AI analysis
    query = f"{profile.skills or ''} {profile.interests or ''}".strip() or 'software developer'
    roles = retrieve_roles(query, k=5)
    ai_summary = summarize(profile_dict, roles)
    
    # Build comprehensive context
    context = {
        "name": getattr(current_user, 'name', 'Student'),
        "email": getattr(current_user, 'email', 'Not provided'),
        "education_level": profile.education_level or "Not specified",
        "skills": profile.skills or "",
        "interests": profile.interests or "",
        "bio": profile.bio or "",
        "score": s,
        "breakdown": breakdown,
        "confidence": confidence,
        "strengths": strengths,
        "improvements": improvements,
        "job_roles": jobs,
        "skills_to_learn": skills_to_learn,
        "career_path": ai_summary.get('career_path', ''),
        "next_steps": ai_summary.get('next_steps', []),
        "market_insights": ai_summary.get('market_insights', ''),
        "detailed_recommendations": ai_summary.get('detailed_recommendations', []),
        "detailed_skills": ai_summary.get('detailed_skills', [])
    }
    
    if format == 'pdf':
        return create_professional_pdf_report(db, current_user.id, context)
    
    html = render_report(context)
    return save_report(db, current_user.id, html)

@router.get("/{report_id}/download")
def download(report_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    r = get_report(db, current_user.id, report_id)
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")
    media = "application/pdf" if r.filename.lower().endswith('.pdf') else "text/html"
    return FileResponse(r.path, media_type=media, filename=r.filename)
