#!/usr/bin/env python3
"""
Test script to verify Career Readiness Score calculation
Run this after creating a profile to see the scoring breakdown
"""

import sys
sys.path.insert(0, '/d/Minds CIE/backend')

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.student import Student
from app.services.scoring_service import compute_score

def test_scoring():
    """Test the scoring calculation"""
    db = SessionLocal()
    
    try:
        # Get the first student profile
        profile = db.query(Student).first()
        
        if not profile:
            print("❌ No student profile found. Please create a profile first.")
            return
        
        print(f"\n{'='*60}")
        print(f"CAREER READINESS SCORE TEST")
        print(f"{'='*60}\n")
        
        print(f"📋 Profile: User ID {profile.user_id}")
        print(f"   Education: {profile.education_level}")
        print(f"   Experience: {profile.experience_years} years")
        print(f"   Skills: {profile.skills[:50]}..." if profile.skills else "   Skills: Not provided")
        print(f"   Bio: {profile.bio[:50]}..." if profile.bio else "   Bio: Not provided")
        
        # Calculate score
        score, strengths, improvements, breakdown, confidence = compute_score(db, profile)
        
        print(f"\n{'='*60}")
        print(f"📊 CAREER READINESS SCORE: {score}/100")
        print(f"{'='*60}\n")
        
        # Score interpretation
        if score >= 70:
            interpretation = "🟢 EXCELLENT - Well-prepared for target career"
        elif score >= 50:
            interpretation = "🟡 GOOD - Ready for entry/mid-level positions"
        elif score >= 30:
            interpretation = "🟠 FAIR - Needs skill development"
        else:
            interpretation = "🔴 DEVELOPING - Significant development needed"
        
        print(f"Interpretation: {interpretation}\n")
        
        # Score breakdown
        print(f"{'='*60}")
        print(f"SCORE BREAKDOWN (Component Scores)")
        print(f"{'='*60}\n")
        
        components = {
            'degree_score': ('Education Level', 0.12),
            'experience_score': ('Work Experience', 0.08),
            'skill_coverage': ('Skill Coverage', 0.30),
            'certificate_quality': ('Certificates', 0.15),
            'practical_evidence': ('Practical Evidence', 0.10),
            'soft_skills': ('Soft Skills', 0.05),
        }
        
        for key, (label, weight) in components.items():
            value = breakdown.get(key, 0)
            percentage = value * 100
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            print(f"{label:20} {bar} {percentage:5.1f}% (weight: {weight*100:.0f}%)")
        
        # Market and Meta factors
        print(f"\n{'='*60}")
        print(f"MARKET & META FACTORS")
        print(f"{'='*60}\n")
        
        print(f"Role Demand:        {breakdown.get('role_demand', 0)*100:5.1f}%")
        print(f"Salary Fit:         {breakdown.get('salary_fit', 0)*100:5.1f}%")
        print(f"Role Difficulty:    {breakdown.get('role_difficulty', 0)*100:5.1f}%")
        print(f"Evidence Confidence:{breakdown.get('evidence_confidence', 0)*100:5.1f}%")
        print(f"Data Completeness:  {breakdown.get('data_completeness', 0)*100:5.1f}%")
        
        # Calculation details
        print(f"\n{'='*60}")
        print(f"CALCULATION DETAILS")
        print(f"{'='*60}\n")
        
        raw = breakdown.get('raw_score', 0)
        market = breakdown.get('market_factor', 0)
        meta = breakdown.get('meta_factor', 0)
        
        print(f"Raw Score:          {raw:.4f}")
        print(f"Market Factor:      {market:.4f}")
        print(f"Meta Factor:        {meta:.4f}")
        print(f"Confidence:         {confidence:.4f}")
        print(f"\nFormula: 100 × {raw:.4f} × {market:.4f} × {meta:.4f} = {score}")
        
        # Strengths
        print(f"\n{'='*60}")
        print(f"✅ STRENGTHS")
        print(f"{'='*60}\n")
        
        if strengths:
            for i, strength in enumerate(strengths, 1):
                print(f"{i}. {strength}")
        else:
            print("No strengths identified yet. Complete your profile for better analysis.")
        
        # Improvements
        print(f"\n{'='*60}")
        print(f"📈 AREAS FOR IMPROVEMENT")
        print(f"{'='*60}\n")
        
        if improvements:
            for i, improvement in enumerate(improvements, 1):
                print(f"{i}. {improvement}")
        else:
            print("Great! No major improvements needed.")
        
        print(f"\n{'='*60}\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    test_scoring()
