# 🧠 Career Intelligence System

An AI-Powered Student Career Intelligence & Guidance System that analyzes student data, extracts evidence from certificates, and generates comprehensive Career Intelligence Reports with personalized recommendations.

## 🌟 Features

### Core Functionality
- **Student Profile Analysis** - Comprehensive profile management with skills, education, and experience tracking
- **Document Intelligence Engine** - OCR + NLP powered certificate and document analysis
- **Career Readiness Scoring** - Advanced algorithm following PRD specifications (0-100 scale)
- **AI-Powered Recommendations** - GPT-4 integration with RAG for intelligent career guidance
- **Professional Report Generation** - Beautiful PDF reports with charts and detailed analysis
- **Knowledge Base Management** - Comprehensive job roles database with 26+ roles across 7 industry clusters

### Advanced Features
- **Real-time Career Analysis** - Interactive dashboard with live scoring
- **Skills Gap Analysis** - Identify missing skills for target roles
- **Market Insights** - AI-powered market trends and salary information
- **Modern UI/UX** - Professional interface with animations and responsive design
- **Comprehensive Error Handling** - Robust error management and user feedback

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Configuration and exceptions
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # FastAPI application
├── alembic/             # Database migrations
└── requirements.txt     # Python dependencies
```

### Frontend (React + Vite)
```
frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/          # Application pages
│   ├── services/       # API services
│   └── styles/         # CSS styles
├── package.json        # Node dependencies
└── vite.config.js      # Vite configuration
```

### Knowledge Base
```
knowledge_base/
├── career_intelligence_kb.xlsx  # Job roles database
└── embeddings/                  # Vector embeddings for RAG
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (optional, SQLite by default)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd career-intelligence-system
python scripts/setup_system.py
```

### 2. Setup Local AI (Recommended)
```bash
# Install Ollama (see OLLAMA_SETUP.md for detailed instructions)
# Windows: Download from https://ollama.ai/download
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama2
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Configuration is already optimized for local AI
uvicorn app.main:app --reload
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 5. Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- System Status: http://localhost:8000/api/v1/system/status

## 📊 Career Readiness Scoring

The system implements a comprehensive scoring algorithm based on the PRD specifications:

### Formula
```
Raw Score = (0.12×D) + (0.08×E) + (0.30×CSC) + (0.15×CQ) + (0.10×P) + (0.05×SS)
Market Factor = (0.6×RD) + (0.2×SF) + (0.2×(1−RDf))
Meta Factor = (0.8×EC) + (0.2×DC)
Final Score = round(100 × Raw × Market Factor × Meta Factor)
```

### Components
- **D**: Degree Score (Educational qualifications)
- **E**: Experience Score (Work experience)
- **CSC**: Skill Coverage Score (Technical skills alignment)
- **CQ**: Certificate Quality (Certification assessment)
- **P**: Practical Evidence (Portfolio and projects)
- **SS**: Soft Skills Score (Interpersonal abilities)
- **RD**: Role Demand (Market demand for target roles)
- **SF**: Salary Fit (Salary expectations vs market)
- **RDf**: Role Difficulty (Complexity of target role)
- **EC**: Evidence Confidence (OCR and data quality)
- **DC**: Data Completeness (Profile completeness)

### Score Interpretation
- **0-30**: Beginner (Getting Started)
- **31-60**: Progressing (Good Progress)
- **61-100**: Job-Ready (Excellent!)

## 🤖 AI Integration

### Local AI with Ollama (Recommended)
- **Privacy-first**: All AI processing happens locally
- **Cost-effective**: No API costs or usage limits
- **Offline capable**: Works without internet connection
- **Models supported**: Llama 2, Code Llama, Mistral, and more
- **Easy setup**: See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for installation guide

### OpenAI GPT-4 Integration (Fallback)
- Structured career recommendations
- Market insights and trends
- Personalized learning paths
- Professional guidance
- Automatic fallback when Ollama is unavailable

### RAG (Retrieval-Augmented Generation)
- FAISS vector database for job role matching
- Sentence-BERT embeddings
- Context-aware recommendations
- Source attribution and references

### OCR Processing
- **EasyOCR (Primary)**: Superior accuracy for document processing
- **Tesseract (Fallback)**: Reliable open-source OCR engine
- **Multi-format support**: PDF, JPG, PNG, TIFF, BMP
- **Confidence scoring**: Quality assessment for extracted text

## 📈 Knowledge Base

The system includes a comprehensive knowledge base with:

### Job Roles (26+)
- **Technology**: Frontend/Backend Developers, AI Engineers, DevOps, Cybersecurity
- **Data**: Data Analysts, Data Scientists, ML Engineers
- **Design**: UX/UI Designers, Visual Designers
- **Business**: Product Managers, Project Managers, Sales, Marketing
- **Finance**: Financial Analysts
- **Healthcare**: Health Informatics Specialists
- **Education**: Instructional Designers

### Data Schema
- Cluster and Job Family classification
- Technical and soft skills requirements
- Experience ranges and salary information
- Market sources and references
- O*NET job index integration

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Database
DATABASE_URL=sqlite:///./career.db

# AI Configuration (Ollama preferred, OpenAI fallback)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama2
GPT5_API_KEY=your_openai_api_key_optional
GPT5_MODEL=gpt-4

# OCR Configuration
OCR_ENGINE=easyocr
GOOGLE_VISION_API_KEY=your_google_vision_key_optional

# Security
SECRET_KEY=your_secret_key

# File Upload
MAX_FILE_SIZE=20971520  # 20MB
ALLOWED_FILE_TYPES=.pdf,.jpg,.jpeg,.png

# CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
```

### Database Migration
```bash
cd backend
alembic upgrade head
```

## 📱 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login

### Student Profile
- `GET /api/v1/students/me` - Get profile
- `POST /api/v1/students/me` - Create profile
- `PUT /api/v1/students/me` - Update profile

### Documents
- `POST /api/v1/documents/upload` - Upload documents
- `POST /api/v1/documents/{id}/ocr` - Extract text from document
- `POST /api/v1/documents/extract-skills` - Extract skills from documents

### Career Analysis
- `GET /api/v1/career/score` - Get career readiness score
- `GET /api/v1/career/recommendations` - Get job recommendations
- `GET /api/v1/career/ai-recommendations` - Get AI-powered insights

### Reports
- `POST /api/v1/reports/generate` - Generate comprehensive report
- `GET /api/v1/reports/{id}/download` - Download report

### Knowledge Base
- `POST /api/v1/kb/upload` - Upload knowledge base
- `POST /api/v1/kb/query` - Search job roles

## 🎨 UI Components

### Modern Design Features
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Animations** - Framer Motion for smooth interactions
- **Charts & Visualizations** - Recharts for data visualization
- **Icons** - Lucide React for consistent iconography
- **File Upload** - React Dropzone for document handling
- **Forms** - React Hook Form for validation

### Key Pages
- **Dashboard** - Overview with career score and activity
- **Profile Management** - Comprehensive profile editing
- **Document Upload** - Drag-and-drop file handling
- **Career Analysis** - Interactive scoring and recommendations
- **Report Generation** - Professional PDF reports
- **Knowledge Base** - Job role exploration

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Docker Deployment
```bash
# Backend
cd backend
docker build -t career-intelligence-api .
docker run -p 8000:8000 career-intelligence-api

# Frontend
cd frontend
docker build -t career-intelligence-ui .
docker run -p 3000:3000 career-intelligence-ui
```

### Production Considerations
- Use PostgreSQL for production database
- Configure proper CORS settings
- Set up SSL certificates
- Use environment-specific configurations
- Implement proper logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Owner**: Abdul Jameel A M
- **Version**: v1.0 (2025-11)
- **Update Frequency**: Annual

## 🆘 Support

For support and questions:
1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [Architecture Document](career_intelligence_architecture.md)
3. Read the [PRD](career_intelligence_prd.md)
4. Open an issue in the repository

## 🔮 Future Enhancements

- Automated Knowledge Base updater (GPT-5 web-assist)
- Placement prediction (supervised model)
- Resume & Skill Pathway builder
- Conversational career assistant (Chat RAG)
- Mobile application
- Integration with job portals
- Advanced analytics dashboard
- Multi-language support

---

**Built with ❤️ for empowering student career development**
