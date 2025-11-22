## **Career Readiness Score - Logic (High-Level, Updated)**

### **Design Goals (Updated)**

The **Career Readiness Score (CRS)** is designed with the following goals:

- **Deterministic & Explainable  
    **Anyone should be able to understand how the score is calculated from the inputs.  
    For every student, we can show:  
  - What data was used  

  - How much each component contributed  

  - What they should do to improve.  

- **Soft Skill-First and India-Relevant  
    **The score reflects the reality that, especially in India, employers strongly value communication, teamwork, adaptability, and work ethic.  
    Therefore, **soft skills contribute 60%** to the score, with technical/domain skills and practical exposure forming the rest.  

- **Dynamic & Updatable  
    **The score is **not fixed**. It should update automatically when the student:  
  - Uploads new certificates  

  - Completes soft skill courses  

  - Adds internships or project experience  

  - Updates their profile.  

- **Simple to Use, Deep in Logic  
    **Students and colleges should see only **one number** (0-100) and a clear explanation.  
    The internal logic can be detailed, but the output must be straightforward.  

- **Robust to Missing / Noisy Data  
    **Not all students will have all details filled or high-quality certificates.  
    The system should:  
  - Use defaults when required  

  - Reduce confidence (not randomly inflate scores) when data is weak.  

- **Resistant to Gaming  
    **Students should not be able to unfairly boost their score by:  
  - Uploading many low-quality certificates  

  - Adding irrelevant or fake documents.  
        The system must use:  

  - Verification checks  

  - Diminishing returns  

  - Trust levels for providers.  

- **Fairness-Aware and Non-Discriminatory  
    **CRS should not favor:  
  - Only "top" colleges  

  - Only full-time courses  

  - Specific regions or backgrounds.  
        It should evaluate **skills + evidence**, not social or demographic factors.  

## **1 - What the Career Readiness Score Represents**

The **Career Readiness Score (CRS)** is a single number between **0 and 100**.

It answers one core question:

"Given the student's current skills, certificates, projects, and the job market,  
**how ready are they to start applying for suitable roles?**"

Score ranges:

- **0-30 → Developing  
    **
  - The student needs foundational development.  

  - Focus on soft skills, one or two strong certificates, and basic projects.  

- **31-60 → Progressing / Employable with Support  
    **
  - The student is partially ready.  

  - With targeted upskilling and 1-2 focused internships/projects, they can become job-ready.  

- **61-100 → Job-Ready / Industry-Aligned  
    **
  - The student's profile matches the requirements of real entry-level roles.  

  - They can participate actively in placements and job applications.  

This score is **not a judgment**. It is a **progress indicator** with a clear learning roadmap.

## **2 - Inputs Used for the Score**

The CRS uses three main input categories:

- **Profile (Static)  
    **
  - Degree and specialization  

  - Year of study or graduation  

  - Mode of study: full-time, part-time, distance, online  

  - Work experience (if any): internships, part-time roles, full-time roles  

- **Evidence (Certificates & Projects)  
    **
  - Certificates (technical, domain, soft skill, workshops, etc.)  

  - Extracted skills from certificates via OCR + text analysis  

  - Projects, reports, portfolios, internships, or case studies  

  - Extra-curriculars (sports, volunteering, leadership roles)  

- **Market (Job Role Knowledge Base)  
    **
  - Skills needed for targeted roles  

  - Demand level (High / Medium / Low)  

  - Difficulty level (entry / tougher roles)  

  - Typical experience requirement for that role  

Additionally, two meta-factors are considered:

- **Evidence Confidence** - How much we can trust the extracted certificate and project data  

- **Data Completeness** - How much of the profile is filled  

These do not add "marks" but influence how much we **trust** the score.

## **3 - Soft Skills in the Updated System**

Soft skills are central to this version of CRS.

### **3.1 Soft Skills as 60% of Readiness**

Internally, we treat soft skills as the largest contributor to readiness:

- Communication  

- Teamwork and collaboration  

- Problem-solving  

- Adaptability  

- Time management  

- Professional behavior  

- Leadership (if any evidence is present)  

In the final formula, **SoftSkillScore (SS)** contributes **60%** of the **Core Readiness Score**.

### **3.2 Two Phases for Soft Skill Score**

Soft skills are derived in two steps, based on where the student is in your system:

- **Before completing your 10 soft skill courses  
    **
  - SS is based mainly on:  
    - What we can detect from certificates (for example, courses mentioning "communication", "teamwork", etc.)  

    - Evidence from internships/projects that mention presentations, coordination, or similar.  

  - SS here is **capped** at a moderate level to avoid overestimating purely from text.  

- **After completing all 10 soft skill courses (on your platform)  
    **
  - We treat this as **strong, structured evidence** of soft skill training.  

  - The student's SoftSkillScore (SS) is then boosted towards a maximum of **0.99** (99%).  

  - We intentionally avoid 100% to keep it realistic.  

This approach ensures:

- Certificates alone cannot max out soft skills.  

- Your own soft skill course path has **real value** and impact.  

## **4 - Component Weights (Soft = 60%, Tech = 25%, Practical = 15%)**

Internally, CRS is built from three main capability components:

| **Component** | **Symbol** | **Weight** | **Description** |
| --- | --- | --- | --- |
| Soft Skill Score | SS  | 0.60 | Communication, teamwork, adaptability, etc. |
| --- | --- | --- | --- |
| Domain/Technical Match | DS  | 0.25 | Match with required technical/domain skills of target roles |
| --- | --- | --- | --- |
| Practical Experience | P   | 0.15 | Projects, internships, fieldwork, or applied work |
| --- | --- | --- | --- |

These three components are combined into a **CoreScore** (0-1).  
Then, CoreScore is adjusted by:

- Job role **demand  
    **
- Job role **difficulty  
    **
- Evidence **confidence  
    **
- Profile **completeness  
    **

to produce the **final CRS** (0-100).

## **5 - Intuitive Scoring Flow**

Instead of thinking in formulas, we can think of CRS in **three stages**:

- **Stage 1 - What the student already has  
    **
  - How strong are their soft skills (SS)?  

  - How well do their technical/domain skills match the roles (DS)?  

  - How much real-world practice have they had (P)?  

- **Stage 2 - How this fits the market  
    **
  - Are they aiming for roles with **high demand** or very niche/rare ones?  

  - Are they trying for roles that are **too advanced**, based on typical experience levels?  

- **Stage 3 - How much we trust the data  
    **
  - Are most certificates **verifiable**?  

  - Is the profile mostly complete or very empty?  

The final score is:

**Core capability × Market alignment × Data confidence**,  
scaled to 0-100.

## **6 - Score Ranges and Interpretation**

- **0-30 (Developing)  
    **Student is at the beginning of their journey.  
    Recommended focus:  
  - Complete 2-3 soft skill courses  

  - Do at least one basic project or mini-internship  

  - Obtain at least one relevant certificate  

- **31-60 (Progressing)  
    **Student is partially ready.  
    Recommended focus:  
  - Finish all 10 soft skill courses over time  

  - Add one strong internship or project  

  - Add targeted domain certificates (for chosen roles)  

- **61-100 (Job-Ready)  
    **Student's profile aligns well with entry-level roles.  
    Recommended focus:  
  - Interview preparation  

  - Resume polishing  

  - Role-specific small improvements  

## **7 - How Students Improve CRS in Practice**

The system shows **concrete actions** with approximate score impact, such as:

- "Complete Soft Skill Course 1 (Communication Basics) → +5 to +8 points expected"  

- "Add one verified domain certificate (e.g., Tally, Power BI, Java) → +4 to +6 points"  

- "Do one internship or guided project → +8 to +12 points"  

This makes CRS **actionable**, not just informational.

## **8 - Fairness**

CRS follows clear fairness principles:

- **No penalty** for:  
  - Studying via distance or online mode  

  - Having gaps in education  

  - Belonging to a lesser-known college  

- **Only skills and evidence** affect the score.  

Where data is incomplete, the system does **not lie**. Instead, it lowers confidence and highlights what is missing.

## **9 - Future Improvements (High-Level)**

Later versions of CRS can:

- Learn from real placement outcomes  

- Adjust internal weights based on actual hiring success  

- Provide deeper analytics at the institution level  

- Support program-level changes (e.g., "this batch needs more soft skill focus")