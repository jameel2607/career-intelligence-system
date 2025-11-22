# 🧠 Product Requirements Document (PRD)
## Project: AI-Powered Student Career Intelligence & Guidance System

---

### 1. Objective
To build an AI-driven platform that analyzes student data, extracts evidence from certificates, and generates a complete **Career Intelligence Report** that includes:
- Career Readiness Score (CRS)
- Job Recommendations
- Skill Gaps
- Personalized Roadmap

---

### 2. Target Users
- College students (UG / PG)
- Career counselors
- Training & placement cells

---

### 3. Core Features
1. **Student Profile Analyzer**
2. **Document Intelligence Engine (OCR + NLP)**
3. **Career Intelligence Engine (GPT-5 + RAG)**
4. **Career Readiness Scoring Framework**
5. **Excel-based Knowledge Base**
6. **Report Generator (PDF/HTML)**
7. **(Optional)** AI Chat Career Advisor

---

### 4. Key Functional Requirements
| Module | Description |
|--------|--------------|
| Student Intake | Form input + document upload |
| Document Parsing | OCR + NLP skill extraction |
| Profile Fusion | Merge profile + certificates + skills |
| Readiness Scoring | Compute CRS (0–100) |
| Role Recommendation | GPT-5 + RAG query against KB |
| Report Generation | Summary + Skills + Recommendations |
| KB Management | Annual manual update system |

---

### 5. Non-Functional Requirements
- **Scalability:** Should handle thousands of users concurrently.
- **Accuracy:** Must cite KB sources, zero hallucination.
- **Explainability:** Every recommendation traceable.
- **Data Privacy:** Secure storage, no public sharing.
- **Extensibility:** Easy to add new clusters/roles.

---

### 6. Technical Stack
| Layer | Tech | Purpose |
|--------|------|----------|
| Frontend | React.js / Streamlit | UI |
| Backend | FastAPI / Express.js | API |
| DB | MongoDB / PostgreSQL | Storage |
| OCR | Google Vision / Tesseract | Extraction |
| AI | GPT-5 / GPT-5-mini | NLP & reasoning |
| Vector Store | FAISS / Pinecone | RAG search |
| Report | jsPDF / ReportLab | Output |
| KB | Excel | Trusted dataset |

---

### 7. Data Flow
```
Student Uploads → Document Intelligence → Data Fusion → Scoring → RAG Role Match → Report
```

---

### 8. Knowledge Base Schema
| Field | Description |
|--------|--------------|
| Cluster | Domain group |
| Job Family | Sub-domain |
| Job Role | Occupation |
| Level | Entry / Mid / Senior |
| Qualifications / Degrees | Degree paths |
| Technical Skills | Tools/software |
| Soft Skills | Behavioral skills |
| Domain / Functional Skills | Job-specific skills |
| Experience Range | Years required |
| Job Index / ID | O*NET / NSDC / ESCO code |
| Job Description Summary | Short role definition |
| Salary | India / Global |
| Data Sources | URLs for references |

---

### 9. Career Readiness Scoring Logic
**Formula Summary:**
```
Raw = (0.12×D)+(0.08×E)+(0.30×CSC)+(0.15×CQ)+(0.10×P)+(0.05×SS)
MarketFactor = (0.6×RD)+(0.2×SF)+(0.2×(1−RDf))
MetaFactor = (0.8×EC)+(0.2×DC)
Final Score = round(100 × Raw × MarketFactor × MetaFactor)
```
**Range:**
- 0–30 → Beginner  
- 31–60 → Progressing  
- 61–100 → Job-Ready

---

### 10. Output Example (Report Sections)
1. Profile Summary  
2. Certificates & Skills Extracted  
3. Career Readiness Score + Confidence Band  
4. Top 5 Job Roles  
5. Skill Gaps & Recommendations  
6. Salary Outlook (India + Global)  
7. AI Summary with References

---

### 11. Future Enhancements
- Automated Knowledge Base updater (GPT-5 web-assist)
- Placement prediction (supervised model)
- Resume & Skill Pathway builder
- Conversational career assistant (Chat RAG)

---

### 12. Success Metrics
| Metric | Goal |
|--------|------|
| Accuracy | 90%+ match with verified KB |
| Explainability | 100% traceable outputs |
| Scalability | 100k+ users |
| Update Frequency | Annual KB refresh |

---

### 13. Project Deliverables
1. Full backend and API architecture  
2. Integration-ready front-end skeleton  
3. Knowledge Base ingestion + RAG setup  
4. Career Readiness scoring engine  
5. Report generator templates  

---

### 14. Owner & Versioning
- **Owner:** Abdul Jameel A M  
- **Version:** v1.0 (2025-11)  
- **Update Frequency:** Annual  
- **KB Source:** Verified Excel Dataset

---