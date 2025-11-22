import os
from datetime import datetime
from pathlib import Path
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader, select_autoescape
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.lib.colors import Color, HexColor, black, white, blue, gray
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib import colors
import logging
from app.core.config import settings
from app.models.report import Report

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[3]
TEMPLATE_DIR = BASE_DIR / settings.REPORT_TEMPLATE_DIR
OUTPUT_DIR = BASE_DIR / settings.REPORT_OUTPUT_DIR

env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html"])
)

# Define color scheme
PRIMARY_COLOR = HexColor('#2563eb')  # Blue
SECONDARY_COLOR = HexColor('#64748b')  # Gray
ACCENT_COLOR = HexColor('#10b981')  # Green
WARNING_COLOR = HexColor('#f59e0b')  # Orange
DANGER_COLOR = HexColor('#ef4444')  # Red

def ensure_output_dir():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def render_report(context: dict) -> str:
    template = env.get_template("career_report_template.html")
    return template.render(**context)

def save_report(db: Session, user_id: int, html: str) -> Report:
    ensure_output_dir()
    filename = f"report_{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.html"
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    r = Report(user_id=user_id, filename=filename, path=str(path))
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

def list_reports(db: Session, user_id: int):
    return db.query(Report).filter(Report.user_id == user_id).order_by(Report.id.desc()).all()

def get_report(db: Session, user_id: int, report_id: int):
    return db.query(Report).filter(Report.id == report_id, Report.user_id == user_id).first()

def create_header_footer(canvas, doc):
    """Create header and footer for PDF pages"""
    canvas.saveState()
    
    # Header
    canvas.setFillColor(PRIMARY_COLOR)
    canvas.rect(0, A4[1] - 60, A4[0], 60, fill=1)
    
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 18)
    canvas.drawString(30, A4[1] - 35, "Career Intelligence Report")
    
    canvas.setFont('Helvetica', 10)
    canvas.drawRightString(A4[0] - 30, A4[1] - 35, f"Generated on {datetime.now().strftime('%B %d, %Y')}")
    
    # Footer
    canvas.setFillColor(SECONDARY_COLOR)
    canvas.rect(0, 0, A4[0], 40, fill=1)
    
    canvas.setFillColor(white)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(30, 15, "Career Intelligence System - Powered by AI")
    canvas.drawRightString(A4[0] - 30, 15, f"Page {doc.page}")
    
    canvas.restoreState()

def get_score_color(score):
    """Get color based on score range"""
    if score >= 70:
        return ACCENT_COLOR
    elif score >= 40:
        return WARNING_COLOR
    else:
        return DANGER_COLOR

def create_score_chart(score, breakdown):
    """Create a visual chart for the career readiness score"""
    drawing = Drawing(400, 200)
    
    # Main score circle
    from reportlab.graphics.shapes import Circle, String
    
    # Background circle
    bg_circle = Circle(100, 100, 80, fillColor=gray, strokeColor=None)
    drawing.add(bg_circle)
    
    # Score circle
    score_color = get_score_color(score)
    score_circle = Circle(100, 100, 70, fillColor=score_color, strokeColor=None)
    drawing.add(score_circle)
    
    # Score text
    score_text = String(100, 100, str(score), fontSize=24, fillColor=white, textAnchor='middle')
    drawing.add(score_text)
    
    # Breakdown bars
    if breakdown:
        y_pos = 180
        for key, value in breakdown.items():
            if key.endswith('_score'):
                label = key.replace('_score', '').replace('_', ' ').title()
                bar_width = value * 150  # Scale to 150px max
                
                # Background bar
                bg_bar = Rect(220, y_pos, 150, 15, fillColor=gray, strokeColor=None)
                drawing.add(bg_bar)
                
                # Value bar
                value_bar = Rect(220, y_pos, bar_width, 15, fillColor=PRIMARY_COLOR, strokeColor=None)
                drawing.add(value_bar)
                
                # Label
                label_text = String(210, y_pos + 5, label, fontSize=8, fillColor=black, textAnchor='end')
                drawing.add(label_text)
                
                y_pos -= 25
    
    return drawing

def create_professional_pdf_report(db: Session, user_id: int, context: dict) -> Report:
    """Create a professional PDF report with charts and modern design"""
    ensure_output_dir()
    filename = f"career_report_{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    path = OUTPUT_DIR / filename
    
    try:
        # Create document
        doc = SimpleDocTemplate(
            str(path),
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=80,
            bottomMargin=60
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=PRIMARY_COLOR,
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=PRIMARY_COLOR,
            spaceBefore=20,
            spaceAfter=10
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=10,
            alignment=TA_JUSTIFY
        )
        
        # Build story
        story = []
        
        # Title page
        story.append(Spacer(1, 50))
        story.append(Paragraph("Career Intelligence Report", title_style))
        story.append(Spacer(1, 30))
        
        # Student info table
        student_data = [
            ['Name:', context.get('name', 'Not provided')],
            ['Email:', context.get('email', 'Not provided')],
            ['Education:', context.get('education_level', 'Not provided')],
            ['Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')]
        ]
        
        student_table = Table(student_data, colWidths=[2*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), SECONDARY_COLOR),
            ('TEXTCOLOR', (0, 0), (0, -1), white),
            ('BACKGROUND', (1, 0), (1, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(student_table)
        story.append(PageBreak())
        
        # Career Readiness Score Section
        story.append(Paragraph("Career Readiness Analysis", heading_style))
        
        score = context.get('score', 0)
        breakdown = context.get('breakdown', {})
        
        # Score interpretation
        if score >= 70:
            interpretation = "Excellent! You are well-prepared for your target career path."
            color = ACCENT_COLOR
        elif score >= 40:
            interpretation = "Good progress! Focus on the improvement areas to enhance your readiness."
            color = WARNING_COLOR
        else:
            interpretation = "Getting started! Significant development needed in key areas."
            color = DANGER_COLOR
        
        story.append(Paragraph(f"<b>Overall Score: {score}/100</b>", body_style))
        story.append(Paragraph(f"<font color='{color.hexval()}'>{interpretation}</font>", body_style))
        story.append(Spacer(1, 20))
        
        # Add score chart
        if breakdown:
            score_chart = create_score_chart(score, breakdown)
            story.append(score_chart)
            story.append(Spacer(1, 30))
        
        # Detailed breakdown
        story.append(Paragraph("Score Breakdown", heading_style))
        
        if breakdown:
            breakdown_data = [['Component', 'Score', 'Description']]
            
            component_descriptions = {
                'degree_score': 'Educational qualifications and academic achievements',
                'experience_score': 'Work experience and practical exposure',
                'skill_coverage': 'Technical skills alignment with target roles',
                'certificate_quality': 'Quality and relevance of certifications',
                'practical_evidence': 'Portfolio projects and hands-on experience',
                'soft_skills': 'Communication and interpersonal abilities'
            }
            
            for key, value in breakdown.items():
                if key.endswith('_score'):
                    component = key.replace('_score', '').replace('_', ' ').title()
                    description = component_descriptions.get(key, 'Component assessment')
                    breakdown_data.append([component, f"{value:.2f}", description])
            
            breakdown_table = Table(breakdown_data, colWidths=[2*inch, 1*inch, 3*inch])
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, colors.lightgrey])
            ]))
            
            story.append(breakdown_table)
        
        story.append(PageBreak())
        
        # Strengths Section
        strengths = context.get('strengths', [])
        if strengths:
            story.append(Paragraph("Your Strengths", heading_style))
            for strength in strengths:
                story.append(Paragraph(f"• {strength}", body_style))
            story.append(Spacer(1, 20))
        
        # Improvement Areas
        improvements = context.get('improvements', [])
        if improvements:
            story.append(Paragraph("Areas for Improvement", heading_style))
            for improvement in improvements:
                story.append(Paragraph(f"• {improvement}", body_style))
            story.append(Spacer(1, 20))
        
        # Job Recommendations
        job_roles = context.get('job_roles', [])
        if job_roles:
            story.append(Paragraph("Recommended Career Paths", heading_style))
            
            for i, role in enumerate(job_roles[:5], 1):
                story.append(Paragraph(f"{i}. <b>{role}</b>", body_style))
            
            story.append(Spacer(1, 20))
        
        # Skills Development
        skills_to_learn = context.get('skills_to_learn', [])
        if skills_to_learn:
            story.append(Paragraph("Skills to Develop", heading_style))
            
            skills_data = [['Priority', 'Skill', 'Importance']]
            for i, skill in enumerate(skills_to_learn[:10], 1):
                priority = 'High' if i <= 3 else 'Medium' if i <= 6 else 'Low'
                importance = 'Critical for career advancement' if i <= 3 else 'Beneficial for growth'
                skills_data.append([priority, skill, importance])
            
            skills_table = Table(skills_data, colWidths=[1*inch, 2*inch, 3*inch])
            skills_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_COLOR),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, colors.lightgrey])
            ]))
            
            story.append(skills_table)
        
        # Next Steps
        next_steps = context.get('next_steps', [])
        if next_steps:
            story.append(PageBreak())
            story.append(Paragraph("Recommended Next Steps", heading_style))
            
            for i, step in enumerate(next_steps, 1):
                story.append(Paragraph(f"{i}. {step}", body_style))
        
        # Career Path
        career_path = context.get('career_path', '')
        if career_path:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Career Path Guidance", heading_style))
            story.append(Paragraph(career_path, body_style))
        
        # Market Insights
        market_insights = context.get('market_insights', '')
        if market_insights:
            story.append(Spacer(1, 20))
            story.append(Paragraph("Market Insights", heading_style))
            story.append(Paragraph(market_insights, body_style))
        
        # Footer note
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "<i>This report is generated by AI analysis and should be used as guidance. "
            "Consider consulting with career counselors for personalized advice.</i>",
            body_style
        ))
        
        # Build PDF
        doc.build(story, onFirstPage=create_header_footer, onLaterPages=create_header_footer)
        
        # Save to database
        r = Report(user_id=user_id, filename=filename, path=str(path))
        db.add(r)
        db.commit()
        db.refresh(r)
        
        logger.info(f"Professional PDF report generated: {filename}")
        return r
        
    except Exception as e:
        logger.error(f"Error generating PDF report: {e}")
        raise

# Keep the old function for backward compatibility
def save_pdf_report(db: Session, user_id: int, context: dict) -> Report:
    """Wrapper for backward compatibility"""
    return create_professional_pdf_report(db, user_id, context)
