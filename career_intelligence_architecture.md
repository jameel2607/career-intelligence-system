# 🏗️ Architecture Blueprint Document (ABD)
## Project: AI-Powered Student Career Intelligence & Guidance System

---

### 1. Objective
This Architecture Blueprint defines the **technical implementation plan** for the AI-Powered Student Career Intelligence & Guidance System, aligning with the PRD specifications. It serves as a blueprint for **Trae Coder Mode** to begin modular development.

---

### 2. System Overview
The platform processes student data and certificates, analyzes skills using OCR + NLP, compares them with the Knowledge Base (KB), and generates a **Career Readiness Score** with job recommendations and a personalized report.

---

### 3. High-Level Architecture
```
┌──────────────────────────┐
│   Frontend Interface     │ ← React.js / Streamlit UI
│ - Student registration   │
│ - File upload (PDF, Img) │
│ - Report view/download   │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│  API Gateway / Backend   │ ← FastAPI / Express.js
│ - Authentication          │
│ - Data processing routes  │
│ - Report generator        │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Document Intelligence    │ ← OCR + NLP Layer
│ - File type detection     │
│ - OCR (Tesseract/Vision) │
│ - Skill extraction (GPT)  │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Career Intelligence Core │ ← GPT-5 + RAG Engine
│ - Data fusion             │
│ - Scoring algorithm       │
│ - Skill gap analysis      │
│ - Job recommendations     │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Databases & KB Layer     │
│ - Student DB (MongoDB)   │
│ - Job Role KB (Excel)    │
│ - Vector DB (FAISS)      │
└──────────┬───────────────┘
           ↓
┌──────────────────────────┐
│ Report Generator (PDF)   │
│ - jsPDF / ReportLab      │
│ - Score + roles + skills │
└──────────────────────────┘
```

---

### 4. Backend Services (APIs)

#### 4.1 API Endpoints
| Endpoint | Method | Description | Input | Output |
|-----------|---------|--------------|--------|---------|
| `/upload` | POST | Upload student profile + certificates | FormData (JSON + Files) | Upload confirmation |
| `/analyze` | POST | Triggers document parsing & skill extraction | Student ID | Extracted skill JSON |
| `/score` | POST | Computes Career Readiness Score | Profile + Skills JSON | Score + confidence |
| `/recommend` | POST | Generates top job recommendations (RAG + GPT-5) | Profile + Score JSON | Role list + skill gaps |
| `/report` | GET | Generates PDF report | Student ID | PDF download |
| `/kb/upload` | POST | Upload/refresh Excel KB | Excel File | Confirmation |
| `/kb/query` | POST | Search job roles using FAISS | Search vector/query text | Role matches |

---

### 5. Data Models

#### 5.1 Student Profile Schema
```json
{
  "student_id": "UUID",
  "name": "string",
  "degree": "string",
  "specialization": "string",
  "marks": {
    "school": "float",
    "ug": "float",
    "pg": "float"
  },
  "experience_years": "float",
  "interests": ["string"],
  "soft_skills": ["string"],
  "target_salary": "float",
  "uploaded_files": ["string"],
  "created_at": "datetime"
}
```

#### 5.2 Extracted Certificate Schema
```json
{
  "certificate_id": "UUID",
  "student_id": "UUID",
  "name": "string",
  "provider": "string",
  "issue_date": "string",
  "verified": "boolean",
  "skills": ["string"],
  "ocr_confidence": "float"
}
```

#### 5.3 Job Knowledge Base Schema
(Mirrors Excel Structure)
```json
{
  "cluster": "string",
  "job_family": "string",
  "job_role": "string",
  "level": "string",
  "qualifications": ["string"],
  "technical_skills": ["string"],
  "soft_skills": ["string"],
  "domain_skills": ["string"],
  "experience_range": "string",
  "job_index": "string",
  "description": "string",
  "average_salary": "string",
  "sources": ["string"]
}
```

#### 5.4 Career Readiness Result Schema
```json
{
  "student_id": "UUID",
  "readiness_score": "int",
  "confidence": "float",
  "top_factors": ["string"],
  "skill_gaps": ["string"],
  "recommended_roles": ["string"],
  "report_path": "string"
}
```

---

### 6. Career Readiness Algorithm Implementation

**Steps:**
1. Retrieve student profile and extracted skills.
2. Match target job roles from KB.
3. Compute following metrics:
   - Degree Score (D)
   - Experience Score (E)
   - Skill Coverage (CSC)
   - Certificate Quality (CQ)
   - Practical Evidence (P)
   - Soft Skill (SS)
   - Role Demand (RD)
   - Salary Fit (SF)
   - Role Difficulty (RDf)
   - Evidence Confidence (EC)
   - Data Completeness (DC)
4. Apply formula:
   ```
   Raw = 0.12*D + 0.08*E + 0.30*CSC + 0.15*CQ + 0.10*P + 0.05*SS
   MarketFactor = 0.6*RD + 0.2*SF + 0.2*(1-RDf)
   MetaFactor = 0.8*EC + 0.2*DC
   FinalScore = round(100 * Raw * MarketFactor * MetaFactor)
   ```
5. Return: FinalScore, Confidence, Contributing Factors.

---

### 7. RAG (Retrieval-Augmented Generation) Flow
1. Convert KB Excel into vector embeddings (Sentence-BERT).
2. Store embeddings in FAISS.
3. When student profile is analyzed:
   - Generate profile embedding.
   - Retrieve Top-K (e.g., 5) job roles from FAISS.
   - Inject them into GPT-5 context.
4. GPT-5 generates:
   - Job Recommendations
   - Skill Gap Summary
   - Market Outlook
   - References (from KB)

---

### 8. Report Generator
- Framework: **jsPDF (Node)** or **ReportLab (Python)**
- Report Sections:
  1. Student Profile Overview
  2. Extracted Certificates + Skills
  3. Career Readiness Score Summary
  4. Recommended Roles (with skills, salaries)
  5. Personalized Learning Path
  6. References & Confidence Band

---

### 9. Folder Structure (Suggested)
```
career_intelligence_system/
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── upload.py
│   │   │   ├── analyze.py
│   │   │   ├── score.py
│   │   │   ├── recommend.py
│   │   │   ├── report.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── student_model.py
│   │   ├── certificate_model.py
│   │   ├── kb_model.py
│   │   └── score_model.py
│   ├── services/
│   │   ├── ocr_service.py
│   │   ├── nlp_service.py
│   │   ├── scoring_service.py
│   │   ├── rag_service.py
│   │   └── report_service.py
│   ├── utils/
│   │   ├── validation.py
│   │   ├── file_handler.py
│   │   └── embeddings.py
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── package.json
│   └── public/
├── knowledge_base/
│   ├── career_intelligence_kb.xlsx
│   └── embeddings/
└── reports/
    └── generated/
```

---

### 10. Deployment Plan
- **Phase 1:** Local development (FastAPI backend + Streamlit frontend)
- **Phase 2:** Cloud deployment (Render / Vercel / AWS EC2)
- **Phase 3:** Database & KB integration
- **Phase 4:** PDF report + GPT-5 prompt tuning

---

### 11. Security & Validation
- SSL encryption for all endpoints.
- File size limits (max 20MB per upload).
- OCR text validation for anomalies.
- Strict GPT-5 prompting with guardrails: if missing KB data → return `"Not enough data."`
- Audit logs for every recommendation.

---

### 12. Future Integration
- LLM fine-tuning for domain-specific guidance.
- KB auto-refresh from LinkedIn + O*NET.
- Integration with resume parsing modules.
- Placement analytics dashboard for institutions.

---

### 13. Version Control
- Version: **v1.0 (Architecture Blueprint)**
- Maintainer: **Abdul Jameel A M**
- Update Cycle: Annual / Major milestone updates.

---

