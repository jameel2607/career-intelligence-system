## **Career Readiness Scoring Framework - Design, Logic, and Implementation Plan (Updated)**

## **1\. Introduction**

The **Career Readiness Scoring Framework** defines the detailed method used to calculate the **Career Readiness Score (CRS)** for each student.

It answers:

- What data do we use?  

- How do we transform that data into numbers?  

- How do these numbers combine into a final 0-100 score?  

- How do we ensure fairness, resistance to gaming, and explainability?  

This framework is designed for:

- Product design and logic  

- Backend implementation  

- Faculty and stakeholders who want to understand the scoring logic  

## **2\. Purpose of the Career Readiness Score**

The CRS is created to:

- Provide a **standard, objective scale** of job readiness (0-100).  

- Highlight how well the student currently matches **real job market requirements**.  

- Identify **missing skills, certificates, or experiences**.  

- Guide **next steps** for the student (courses, projects, internships).  

- Help institutions monitor overall readiness trends across batches.  

It is not a permanent label. It is a **snapshot + roadmap**.

## **3\. Conceptual Overview of Scoring**

The CRS is computed in **three stages**:

| **Stage** | **Name** | **Purpose** |
| --- | --- | --- |
| 1   | Core Readiness | Measure the student's current abilities and evidence (skills + soft skills + practice) |
| --- | --- | --- |
| 2   | Market Alignment | Adjust readiness based on demand and difficulty of chosen roles |
| --- | --- | --- |
| 3   | Confidence & Completeness | Adjust based on how reliable and complete the data is |
| --- | --- | --- |

Final flow:

Raw capability → adjusted for market → adjusted for evidence confidence  
→ scaled to **0-100**.

## **4\. Key Inputs (Detailed)**

### **A. Student Profile Data**

- Degree and specialization (e.g., B.Com, B.Sc CS, BBA, BCA, etc.)  

- Year of graduation or "currently pursuing"  

- Mode of study:  
  - Full-time  

  - Part-time  

  - Distance / Online  

- Work experience (if any):  
  - Internship  

  - Part-time  

  - Full-time  

  - Duration and basic description  

- (Optional) Higher study intent:  
  - "Plan for PG in India"  

  - "Plan for PG Abroad"  

  - "Not sure yet"  

### **B. Extracted Evidence Data**

From certificates and documents (via OCR + NLP):

- Technical / domain skills mentioned  

- Soft skill descriptions (for example: "Teamwork", "Communication", "Leadership")  

- Certificate provider name (Coursera, IBM, college, local institute, etc.)  

- Certificate issue date  

- Any verification link or ID if present  

From projects and practical work:

- Project titles and descriptions  

- Tools used (e.g., Excel, Python, Canva, Power BI)  

- Type of outcome (report, dashboard, website, campaign, teaching plan, etc.)  

From extra-curriculars:

- Sports participation  

- Cultural events  

- Volunteering / social service  

- Event coordination  

- Leadership positions (club head, class representative, etc.)  

### **C. Market Knowledge Base Data**

From your Excel-based Job Role Knowledge Base:

- Required technical and domain skills for each role  

- Expected soft skills  

- Role demand (High / Medium / Low)  

- Difficulty level  

- Typical experience range  

The Knowledge Base is always treated as the **"source of truth"** for what jobs demand.

### **D. Data Quality and Confidence Data**

- OCR confidence of extracted text  

- Clarity of provider names and skill lists  

- Verification of certificates (if link available)  

- Whether core profile details are filled or missing  

These values affect the **MetaFactor** (final confidence adjustment).

## **5\. Scoring Components (Structure)**

We define three main component groups:

### **5.1 Layer 1 - Core Readiness Factors**

These measure **what the student currently has**.

| **Component** | **Symbol** | **Range** | **Description** |
| --- | --- | --- | --- |
| Soft Skill Score | SS  | 0-1 | Derived from certificates and your 10 soft skill courses |
| --- | --- | --- | --- |
| Domain/Technical Score | DS  | 0-1 | Skill match with required tech/domain skills of targeted roles |
| --- | --- | --- | --- |
| Practical Evidence Score | P   | 0-1 | Quality and quantity of internships, projects, and applied work |
| --- | --- | --- | --- |

We combine these using your chosen weights:

- Soft skills = 60%  

- Domain/Technical = 25%  

- Practical = 15%  

### **5.2 Layer 2 - Market & Industry Alignment**

| **Component** | **Symbol** | **Range** | **Description** |
| --- | --- | --- | --- |
| Role Demand | RD  | 0-1 | Demand level for selected roles (High > Medium > Low) |
| --- | --- | --- | --- |
| Role Difficulty | RDf | 0-1 | Complexity of role (higher value = harder role) |
| --- | --- | --- | --- |

We combine these into a **MarketFactor**.

### **5.3 Layer 3 - Confidence & Completeness**

| **Component** | **Symbol** | **Range** | **Description** |
| --- | --- | --- | --- |
| Evidence Confidence | EC  | 0-1 | How reliable certificates and extracted evidence are |
| --- | --- | --- | --- |
| Data Completeness | DC  | 0-1 | How much of the required profile is filled |
| --- | --- | --- | --- |

We combine these into a **MetaFactor**.

## **6\. Step-by-Step Calculation Logic**

### **Step 1: Compute Soft Skill Score (SS)**

Soft skills are the **heart** of this system.

We use two sources:

- **Certificates & Experience (Base Soft Skill Evidence)  
    **
  - Scan all certificates and project descriptions for soft skill phrases like:  
        "Communication", "Presentation", "Team Leadership", "Teamwork", "Customer handling", etc.  

  - Assign small contributions for each confirmed soft skill evidence, based on:  
    - Provider quality (e.g., well-known vs low-known)  

    - Recency (new certificates count more)  

  - Combine these to form a **Base Soft Skill Score** (SS_base ∈ \[0, 0.7\]).  

- **Soft Skill Courses in Your Platform (Soft Skill Boost)  
    **
  - The student enrolls in and completes your **10 structured soft skill courses**.  

  - Each course contributes a fixed portion of the **maximum soft skill score**.  

  - After all 10 courses are completed, SS approaches **0.99**.  

A simple representation:

SS_base = soft skills from certificates and activities (max 0.7)

SS_course = (number of soft skill courses completed / 10) × 0.29

SS = min(SS_base + SS_course, 0.99)

This ensures:

- Certificates alone cannot give the maximum score  

- Your 10-course soft skill track holds real weight  

### **Step 2: Compute Domain/Technical Score (DS)**

For each target role (from KB):

- Get the list of required domain/technical skills (S_req).  

- From evidence, build a set of student skills (S_have).  

- Compute:  

Coverage = |S_req ∩ S_have| / |S_req|

- Based on the quality of certificates and recency, slightly weight up or down.  

- Normalize DS to a range between 0 and 1.  

If multiple roles are considered, DS can be:

- The average across top-matching roles  

- Or computed specifically per role if CRS is role-specific  

### **Step 3: Compute Practical Evidence Score (P)**

We measure practice, not just theory.

Inputs:

- Number of internships  

- Number and quality of projects  

- Relevance to target roles  

- Availability of actual artifacts (reports, GitHub links, dashboards, etc.)  

We use a simple rubric-like logic:

- 0 internships & no clear projects → P close to 0  

- 1 basic project or mini-internship → moderate P  

- Multiple role-relevant projects/internships → higher P  

We map P into \[0, 1\].

### **Step 4: Compute Core Capability Score**

Once SS, DS, and P are computed:

CoreScore = (0.60 × SS) + (0.25 × DS) + (0.15 × P)

CoreScore ∈ \[0, 1\]

This is the student's **internal capability score** before considering market and confidence.

### **Step 5: Compute MarketFactor (Demand & Difficulty)**

From the Knowledge Base:

- RD = Role demand (High = closer to 1.0, Medium ≈ 0.6, Low ≈ 0.3)  

- RDf = Role difficulty (Entry-level roles lower; advanced roles higher)  

We compute:

MarketFactor = (0.60 × RD) + (0.40 × (1 − RDf))

Interpretation:

- High demand, low difficulty → MarketFactor closer to 1  

- Low demand, high difficulty → MarketFactor smaller  

If roles are not specific yet, we can use generic entry-level assumptions.

### **Step 6: Compute MetaFactor (Confidence & Completeness)**

From evidence and profile:

- EC: EvidenceConfidence (OCR quality, certificate verification) ∈ \[0, 1\]  

- DC: DataCompleteness (fraction of required fields filled) ∈ \[0, 1\]  

We compute:

MetaFactor = (0.80 × EC) + (0.20 × DC)

If:

- EC is low (unverified certificates, poor scans)  

- DC is low (many blank profile fields)  
    then MetaFactor will be lower, reducing trust in CRS.  

### **Step 7: Final Career Readiness Score**

Combine everything:

AdjustedScore = CoreScore × MarketFactor × MetaFactor

CRS = round(100 × AdjustedScore)

Clamp CRS between 0 and 100.

This gives the final Career Readiness Score shown to the student.

## **7\. Example: How It Works in Practice (Simplified)**

### **Example Student**

- B.Com student, final year  

- Certificates:  
  - "Excel for Business" (good provider, recent)  

  - "Communication Skills Workshop" (local provider)  

- One internship in a local firm (basic finance tasks)  

- Wants to target: "Junior Financial Analyst" (High demand, medium difficulty)  

Assume after processing:

- SS ≈ 0.55  

- DS ≈ 0.45  

- P ≈ 0.40  

Then:

CoreScore = 0.60\*0.55 + 0.25\*0.45 + 0.15\*0.40

\= 0.33 + 0.1125 + 0.06

\= 0.5025

From KB:

- RD (demand) = 0.8  

- RDf (difficulty) = 0.5  

MarketFactor = 0.60\*0.8 + 0.40\*(1−0.5)

\= 0.48 + 0.20

\= 0.68

Evidence and profile:

- EC = 0.85 (good OCR and some verification)  

- DC = 0.90 (profile mostly filled)  

MetaFactor = 0.80\*0.85 + 0.20\*0.90

\= 0.68 + 0.18

\= 0.86

Final:

AdjustedScore = 0.5025 × 0.68 × 0.86 ≈ 0.294

CRS ≈ 29 / 100

Interpretation:

- The student has started well but is still in **Developing** range.  

- Action plan:  
  - Complete soft skill courses (to push SS closer to 0.99)  

  - Add 1-2 finance-related projects  

  - Aim for at least one more strong certification.  

## **8\. Handling Non-Technical Domains**

The same logic works across all domains.

The only change is **what counts as practical evidence** and **what is in DS**:

- HR / Management → HR plans, recruitment process tasks, event management  

- Commerce / Finance → financial models, reports, audits  

- Education → teaching plans, recorded lessons, classroom engagement activities  

- Arts / Media → portfolios, shows, content samples  

- Marketing / Operations → campaigns, market research, process improvements  

The structure of CRS remains unchanged.

## **9\. Handling Different Student Pathways**

The framework is flexible to common real-world scenarios:

- **UG with no experience  
    **
  - P is low; CRS driven mainly by SS and DS  

  - Suggestions focus on projects + soft skill courses  

- **UG + Internship  
    **
  - P is higher; readiness increases  

  - System encourages: "Now deepen technical/domain certifications"  

- **UG + Work Experience + PG  
    **
  - Experience is reflected via P and DS  

  - MarketFactor may direct towards more advanced roles in the future  

- **Distance/Online Education  
    **
  - No penalty in scoring  

  - Only skills and evidence matter  

## **10\. Soft Skill Courses - Scoring Role**

Your 10 soft skill courses are central to this system.

- Before courses:  
  - Soft skills are approximate, based mainly on certificates and activities  

  - SS cannot exceed 0.7  

- After courses:  
  - Soft skills get a strong boost  

  - With all 10 completed, SS → up to 0.99  

This guarantees **real value** for your internal content and creates a clear incentive for students to follow the complete track.

## **11\. Anti-Gaming & Fraud Resistance**

The system reduces gaming through:

- **Provider trust levels  
    **
  - Well-known providers → higher weight  

  - Low-known sources → lower weight  

- **Certificate verification  
    **
  - Presence of valid URLs/IDs → higher EC  

  - Missing or suspicious data → lower EC  

- **Diminishing returns  
    **
  - Many small, low-value certificates do not keep increasing the score indefinitely.  

- **Incomplete data handling  
    **
  - If DC (completeness) is below a threshold, the system can warn:  
    - "Not enough data to compute a reliable score. Please add more details."  

## **12\. Explainability & UI**

For each student, the system can show:

- CRS (0-100)  

- A short text like: "You are currently in the _Progressing_ stage."  

- Top positive contributors (e.g., "Good communication evidence", "Relevant internship")  

- Top gaps limiting score (e.g., "Low domain skill coverage", "No clear project evidence")  

- Suggested improvement steps with estimated score gain.  

This makes the scoring system **transparent and actionable**, not a black box.

## **13\. Future Enhancement Plan**

Later, when enough data is available:

- Use machine learning to refine weights  

- Validate which components most strongly predict successful placement  

- Adjust formulas (but keep them explainable)  

- Add more advanced analytics dashboards for institutions  

The current deterministic framework is a **strong starting point** that is:

- Implementable immediately  

- Easy to communicate  

- Easy to review and audit  

## **14\. Conclusion**

This updated **Career Readiness Scoring Framework**:

- Respects your new priorities:  
  - **Soft skills at 60% weight  
        **
  - Technical at 25%  

  - Practical at 15%  

- Keeps everything rooted in **certificates, projects, and your own soft skill courses  
    **
- Is detailed enough for implementation, but simple enough for faculty and students to understand.  

It fits cleanly inside your **AI-Powered Student Career Intelligence & Guidance System** and connects directly with the Career Intelligence Engine and Knowledge Base.