# Career Guidance UI + System Flow Document

───────────────

## 1. Purpose of the UI & Flow Design

The Career Guidance UI ensures:

Smooth onboarding → scoring → guidance → upskilling → placement flow

High clarity with simple screens but powerful logic behind

Every student receives outcomes even with incomplete data

Motivation-driven UX where students see improvement in real time

This document describes end-to-end user journey + interface modules + backend triggers to implement the platform effectively.

## 2. User Journey Overview

A 5-stage journey where each stage unlocks the next

| Stage | Module | What Happens | System Output |
| --- | --- | --- | --- |
| 1️ | Profile Onboarding | Student fills academics & preferences | Initial Interest Mapping |
| 2️ | Upload & Verification | Certificates & achievements uploaded | Skills extracted + Soft Skills baseline |
| 3️ | CRS Generation | System processes Skill, Domain, Practical data | Career Readiness Score (0–100) |
| 4️ | Pathway Navigation | Show job roles, alternates, higher studies, entrepreneurship | Guided pathways |
| 5️ | Improvement Actions | Soft skill courses + targeted certification suggestions | Score upgrades in real-time |

This aligns fully with the core architecture defined previously

AI-Powered Student Career Intel…

## 3. Detailed UI Modules

### 3.1 Home / Dashboard

**Primary Objectives:**

Welcome user

Show journey status

Encourage them to finish missing steps

**Key UI Components:**

| Component | Description |
| --- | --- |
| Progress Tracker | 0% to 100% completion of onboarding |
| CTA Buttons | “Complete Profile”, “Upload Certificates”, “Generate Score” |
| Recent Activities | Latest uploads or completed courses |
| Notification Panel | Alerts (e.g., “Add internship details”) |

Visual Example:
A vertical stepper with 5 milestones representing journey stages

Encouraging messages: “You are just 1 step away from your readiness score!”

### 3.2 Smart Profile Builder

Collect:

Personal info

Education details

Language fluency

Experience if any

Preferred career direction:

Job

Higher studies (India/Abroad)

Entrepreneurship

Not Sure Yet → auto-matched guidance

Special fields:

Medium of instruction (10th & 12th)

GPA/percentile (optional)

LinkedIn / GitHub (for portfolio import)

UX Strengths:

Tooltips explain why each field matters

Pre-filled college details if connected to institution login

### 3.3 Document Upload & Extraction

Supports:

PDF, JPG, PNG certificates

Project files / links

Internship letters

Backend performs:

OCR (Google Vision/Tesseract)

Skill extraction (NLP)

Verification check

**UI Status Types:**

| Status Tag | Meaning |
| --- | --- |
| Verified | Provider recognized + valid details detected |
| Low Trust | Provider unknown or text unclear |
| Needs Action | Missing data → Requires manual edit |

Student sees:

Extracted skills list

Option to confirm/edit if minor error

This matches Document Intelligence Engine design

AI-Powered Student Career Intel…

### 3.4 Career Readiness Score Screen

The most important UX screen.

**Elements Displayed:**

Final CRS (0–100)

Readiness Category (Developing / Progressing / Job-Ready)

Visual meter (speedometer / gauge)

**Under that:**

| Section | Content |
| --- | --- |
| Strengths | Data-driven highlights (+points) |
| Gaps | Missing skills reducing score (–points) |
| Quick Wins | Exact actions with expected score boost |
| Confidence Indicator | Profile completeness + evidence trust meter |

Example:
“Complete Soft Skill Course 2 → +7 points expected”

### 3.5 Career Pathway Navigation

This is where the magic happens

**Tabs:**

| Tab | Contains |
| --- | --- |
| Primary Roles | Roles with High Skill + Degree match |
| Alternate Roles | Roles with Strong transferable skills |
| Higher Studies | If selected in profile → dual pathway shown |
| Entrepreneurship | Guided only if interested |

Each role card includes:

Role name

Why recommended (Skill match %)

Salary range (from KB)

Required certifications

2–3 day tasks to get started

Supports skill-first recommendation as per your rule.

### 3.6 Upskilling & Course Recommendations

Connection between CRS → pathway → skills needed

| Feature | Purpose |
| --- | --- |
| 10 Soft Skill Courses | Maximize SS component up to 99% |
| Role-Based Domain Courses | Direct gap-closing |
| Suggested Projects | Must-do practical experience |
| Micro-actions | Daily tasks for consistent improvement |

Progress indicators update CRS in real time

### 3.7 Career Intelligence Report (PDF + Web)

Report includes:

Profile summary

Extracted certificates & skills

CRS explanation & breakdown

Recommended roles (primary + alternate)

Higher study fit

Entrepreneurship ideas

Action roadmap (short, medium, long)

Consistent with system goals

AI-Powered Student Career Intel…

## 4. System Flow — End-to-End Journey

[Dashboard]
   ↓
[Profile Completion]
   ↓
[Doc Upload + Skill Extraction]
   ↓
CRS Calculation Engine
   ↓
[Show Score + Breakdown + Gaps]
   ↓
Career Pathway Recommendation Engine
   ↓
[Primary / Alternate / PG / Entrepreneurship]
   ↓
Upskilling Suggestions + Progress Visualization
   ↓
[Download Career Intelligence Report]

Backend communication:

Profile + Evidence → Knowledge Base matching

CRS → Pathway logic → Recommended outcomes

Upskilling → CRS recalculation → Updated pathways

## 5. Motivational Experience Design

Psychology-based nudges built-in:

Progress bar increases with every action

“+Possible Score Increase” labels

Celebrations on reaching 50 and 60 CRS

Monthly growth report:
“ You improved 12 points this month — great pace!”

Goal:
Convert students into active career owners — not passive job seekers

## 6. Accessibility & Fairness UX Factors

Multi-language support (English + Regional)

Low-data usage mode for mobile users

No required GPA/percentage fields → optional

No discrimination based on:

College brand

Study mode

City/town

This aligns with your No Partiality policy.

## 7. Future UI Enhancements

| Feature | Benefit |
| --- | --- |
| In-platform mock interview with AI | Practice employability |
| Auto-resume creation | Ready to apply instantly |
| Placement job board | One-click apply |
| AI Mentor Chat | Conversational self-discovery |

