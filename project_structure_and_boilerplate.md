# 📁 Project Structure & Boilerplate Code
## AI-Powered Student Career Intelligence & Guidance System

---

## Complete Project Structure

```
career_intelligence_system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── config.py               # Configuration settings
│   │   ├── database.py             # Database connection
│   │   └── dependencies.py         # Dependency injection
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Authentication endpoints
│   │   │   ├── students.py         # Student profile endpoints
│   │   │   ├── documents.py        # Document processing endpoints
│   │   │   ├── career.py           # Career intelligence endpoints
│   │   │   ├── reports.py          # Report generation endpoints
│   │   │   └── knowledge_base.py   # KB management endpoints
│   │   └── dependencies.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                 # User model
│   │   ├── student.py              # Student profile model
│   │   ├── document.py             # Document model
│   │   ├── certificate.py          # Certificate model
│   │   ├── career_score.py         # Career score model
│   │   ├── job_recommendation.py   # Job recommendation model
│   │   └── report.py               # Report model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py                 # User schemas
│   │   ├── student.py              # Student schemas
│   │   ├── document.py             # Document schemas
│   │   ├── career.py               # Career schemas
│   │   └── report.py               # Report schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py         # Authentication service
│   │   ├── student_service.py      # Student profile service
│   │   ├── document_service.py     # Document processing service
│   │   ├── ocr_service.py            # OCR service
│   │   ├── nlp_service.py            # NLP service
│   │   ├── scoring_service.py        # Career scoring service
│   │   ├── rag_service.py            # RAG service
│   │   ├── gpt_service.py              # GPT-5 integration service
│   │   ├── report_service.py           # Report generation service
│   │   └── knowledge_base_service.py   # KB management service
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── security.py               # Security utilities
│   │   ├── file_handler.py           # File handling utilities
│   │   ├── validators.py             # Input validation
│   │   ├── embeddings.py             # Vector embedding utilities
│   │   ├── pdf_generator.py          # PDF generation utilities
│   │   └── excel_parser.py           # Excel parsing utilities
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                 # Core configuration
│   │   ├── constants.py              # Application constants
│   │   ├── exceptions.py             # Custom exceptions
│   │   └── logging.py                # Logging configuration
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py               # Test configuration
│   │   ├── test_auth.py              # Authentication tests
│   │   ├── test_students.py          # Student tests
│   │   ├── test_documents.py         # Document tests
│   │   ├── test_career.py            # Career tests
│   │   └── test_reports.py             # Report tests
│   │
│   ├── alembic/                      # Database migrations
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-dev.txt            # Development dependencies
│   ├── .env.example                    # Environment variables template
│   ├── Dockerfile                      # Docker configuration
│   └── docker-compose.yml              # Docker compose
│
├── frontend/
│   ├── public/
│   │   ├── index.html                  # HTML template
│   │   ├── favicon.ico                 # Site icon
│   │   └── manifest.json               # Web app manifest
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header.jsx          # App header
│   │   │   │   ├── Footer.jsx          # App footer
│   │   │   │   ├── LoadingSpinner.jsx  # Loading indicator
│   │   │   │   └── ErrorBoundary.jsx   # Error handler
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.jsx       # Login component
│   │   │   │   ├── RegisterForm.jsx    # Registration component
│   │   │   │   └── ProtectedRoute.jsx  # Route protection
│   │   │   ├── student/
│   │   │   │   ├── ProfileForm.jsx     # Profile creation
│   │   │   │   ├── ProfileView.jsx     # Profile display
│   │   │   │   └── ProfileEdit.jsx     # Profile editing
│   │   │   ├── documents/
│   │   │   │   ├── FileUpload.jsx      # File upload component
│   │   │   │   ├── DocumentList.jsx    # Document listing
│   │   │   │   ├── DocumentPreview.jsx # Document preview
│   │   │   │   └── UploadProgress.jsx  # Upload progress
│   │   │   ├── career/
│   │   │   │   ├── CareerScore.jsx     # Score display
│   │   │   │   ├── JobRecommendations.jsx # Job suggestions
│   │   │   │   ├── SkillGapAnalysis.jsx   # Skill gap display
│   │   │   │   └── CareerRoadmap.jsx      # Career path
│   │   │   └── reports/
│   │   │       ├── ReportViewer.jsx      # Report display
│   │   │       ├── ReportDownload.jsx    # Report download
│   │   │       └── ReportHistory.jsx     # Report history
│   │   │
│   │   ├── pages/
│   │   │   ├── HomePage.jsx              # Landing page
│   │   │   ├── LoginPage.jsx             # Login page
│   │   │   ├── RegisterPage.jsx          # Registration page
│   │   │   ├── DashboardPage.jsx         # Main dashboard
│   │   │   ├── ProfilePage.jsx           # Profile management
│   │   │   ├── DocumentsPage.jsx         # Document management
│   │   │   ├── CareerAnalysisPage.jsx    # Career analysis
│   │   │   ├── ReportPage.jsx            # Report generation
│   │   │   └── NotFoundPage.jsx          # 404 page
│   │   │
│   │   ├── services/
│   │   │   ├── api.js                    # API client
│   │   │   ├── authService.js            # Authentication service
│   │   │   ├── studentService.js         # Student service
│   │   │   ├── documentService.js        # Document service
│   │   │   ├── careerService.js          # Career service
│   │   │   └── reportService.js          # Report service
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.js                # Authentication hook
│   │   │   ├── useApi.js                 # API hook
│   │   │   ├── useFileUpload.js          # File upload hook
│   │   │   └── useCareerData.js          # Career data hook
│   │   │
│   │   ├── utils/
│   │   │   ├── constants.js              # App constants
│   │   │   ├── helpers.js                # Helper functions
│   │   │   ├── validators.js             # Input validation
│   │   │   └── formatters.js             # Data formatters
│   │   │
│   │   ├── styles/
│   │   │   ├── globals.css               # Global styles
│   │   │   ├── components.css            # Component styles
│   │   │   └── variables.css             # CSS variables
│   │   │
│   │   ├── App.jsx                         # Main app component
│   │   ├── App.css                         # App styles
│   │   └── index.js                        # App entry point
│   │
│   ├── tests/
│   │   ├── components/                     # Component tests
│   │   ├── pages/                          # Page tests
│   │   ├── services/                       # Service tests
│   │   └── utils/                          # Utility tests
│   │
│   ├── package.json                        # Node.js dependencies
│   ├── package-lock.json                   # Dependency lock
│   ├── .env.example                        # Environment variables
│   ├── vite.config.js                      # Vite configuration
│   ├── tailwind.config.js                  # Tailwind CSS config
│   ├── postcss.config.js                   # PostCSS config
│   ├── jest.config.js                      # Jest test config
│   └── .gitignore                          # Git ignore rules
│
├── knowledge_base/
│   ├── career_intelligence_kb.xlsx       # Main KB Excel file
│   ├── embeddings/                         # Vector embeddings
│   │   ├── job_roles.index                 # FAISS index
│   │   └── embeddings.npy                  # Embedding vectors
│   └── templates/
│       └── kb_template.xlsx                # KB template for updates
│
├── reports/
│   ├── templates/
│   │   ├── career_report_template.html     # HTML report template
│   │   └── career_report_styles.css        # Report styles
│   ├── generated/                          # Generated reports
│   └── temp/                               # Temporary files
│
├── scripts/
│   ├── setup_dev.sh                        # Development setup
│   ├── setup_prod.sh                       # Production setup
│   ├── generate_embeddings.py              # Embedding generation
│   ├── process_kb.py                       # KB processing
│   └── deploy.sh                           # Deployment script
│
├── docs/
│   ├── API.md                              # API documentation
│   ├── DEPLOYMENT.md                       # Deployment guide
│   ├── TESTING.md                          # Testing guide
│   └── TROUBLESHOOTING.md                  # Troubleshooting
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                          # CI/CD pipeline
│   │   └── tests.yml                       # Test automation
│   └── ISSUE_TEMPLATE/                     # Issue templates
│
├── .env.example                            # Root environment variables
├── .gitignore                              # Global git ignore
├── README.md                               # Project documentation
├── LICENSE                                 # Project license
└── docker-compose.yml                      # Full stack deployment
```

---

## Key Boilerplate Code Files

### Backend - Main FastAPI Application

```python
# backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.v1 import auth, students, documents, career, reports, knowledge_base
from app.core.config import settings
from app.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Career Intelligence System...")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down Career Intelligence System...")

# Create FastAPI app
app = FastAPI(
    title="Career Intelligence System API",
    description="AI-Powered Student Career Intelligence & Guidance System",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(career.router, prefix="/api/v1/career", tags=["Career Intelligence"])
app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(knowledge_base.router, prefix="/api/v1/kb", tags=["Knowledge Base"])

@app.get("/")
async def root():
    return {"message": "Welcome to Career Intelligence System API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "career-intelligence-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

### Backend - Configuration

```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Career Intelligence System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/career_db")
    
    # CORS settings
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File upload settings
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 20 * 1024 * 1024  # 20MB
    ALLOWED_FILE_TYPES: List[str] = [".pdf", ".jpg", ".jpeg", ".png"]
    
    # AI/ML settings
    GPT5_API_KEY: str = os.getenv("GPT5_API_KEY", "")
    GPT5_MODEL: str = "gpt-5"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # OCR settings
    OCR_ENGINE: str = "tesseract"  # or "google_vision"
    GOOGLE_VISION_API_KEY: Optional[str] = os.getenv("GOOGLE_VISION_API_KEY")
    
    # Knowledge Base settings
    KB_FILE_PATH: str = "knowledge_base/career_intelligence_kb.xlsx"
    EMBEDDINGS_DIR: str = "knowledge_base/embeddings"
    
    # Report generation settings
    REPORT_TEMPLATE_DIR: str = "reports/templates"
    REPORT_OUTPUT_DIR: str = "reports/generated"
    
    # Redis settings (for caching)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Email settings (for notifications)
    SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()
```

### Frontend - Main App Component

```jsx
// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './hooks/useAuth';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Common components
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import ErrorBoundary from './components/common/ErrorBoundary';

// Pages
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ProfilePage from './pages/ProfilePage';
import DocumentsPage from './pages/DocumentsPage';
import CareerAnalysisPage from './pages/CareerAnalysisPage';
import ReportPage from './pages/ReportPage';
import NotFoundPage from './pages/NotFoundPage';

// Protected Route
import ProtectedRoute from './components/auth/ProtectedRoute';

// Styles
import './App.css';
import './styles/globals.css';

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <Router>
          <div className="App min-h-screen bg-gray-50 flex flex-col">
            <Header />
            <main className="flex-grow container mx-auto px-4 py-8">
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                
                {/* Protected Routes */}
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                } />
                <Route path="/profile" element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                } />
                <Route path="/documents" element={
                  <ProtectedRoute>
                    <DocumentsPage />
                  </ProtectedRoute>
                } />
                <Route path="/career-analysis" element={
                  <ProtectedRoute>
                    <CareerAnalysisPage />
                  </ProtectedRoute>
                } />
                <Route path="/reports" element={
                  <ProtectedRoute>
                    <ReportPage />
                  </ProtectedRoute>
                } />
                
                {/* 404 Route */}
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </main>
            <Footer />
            <ToastContainer
              position="top-right"
              autoClose={3000}
              hideProgressBar={false}
              newestOnTop={false}
              closeOnClick
              rtl={false}
              pauseOnFocusLoss
              draggable
              pauseOnHover
            />
          </div>
        </Router>
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
```

### Frontend - API Service

```javascript
// frontend/src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Docker Configuration

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create upload directory
RUN mkdir -p uploads reports/generated knowledge_base/embeddings

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Environment Variables Template

```bash
# .env.example
# Application
SECRET_KEY=your-secret-key-here
DEBUG=false
APP_ENV=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/career_db

# Redis
REDIS_URL=redis://localhost:6379

# AI/ML Services
GPT5_API_KEY=your-gpt5-api-key
GOOGLE_VISION_API_KEY=your-google-vision-key

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=20971520

# Email (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000
```

---

## Quick Start Commands

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Database setup
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Docker Setup
```bash
# Full stack with Docker
docker-compose up -d

# Or individual services
docker-compose up backend
docker-compose up frontend
```

This complete project structure provides a solid foundation for building the AI-Powered Student Career Intelligence & Guidance System. The boilerplate code includes all the essential components needed to start development immediately.