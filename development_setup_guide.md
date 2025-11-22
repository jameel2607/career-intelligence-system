# 🚀 Development Setup & Deployment Guide
## AI-Powered Student Career Intelligence & Guidance System

---

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: Minimum 8GB, Recommended 16GB
- **Storage**: 20GB free space
- **Internet**: Required for API calls and package downloads

### Development Tools
- **Python**: 3.11+ (Backend)
- **Node.js**: 18+ (Frontend)
- **PostgreSQL**: 14+ (Database)
- **Redis**: 7+ (Caching)
- **Git**: Latest version
- **Docker**: Latest version (Optional but recommended)

---

## Development Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd career_intelligence_system
```

### 2. Backend Setup

#### Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Backend Requirements (`requirements.txt`)
```
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0

# Database
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
alembic==1.12.1

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# AI/ML
openai==1.3.7
transformers==4.35.2
torch==2.1.1
sentence-transformers==2.2.2
faiss-cpu==1.7.4

# OCR
pytesseract==0.3.10
pdf2image==1.16.3
Pillow==10.1.0
opencv-python==4.8.1.78

# Data Processing
pandas==2.1.3
numpy==1.25.2
openpyxl==3.1.2

# Utilities
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-magic==0.4.27
aiofiles==23.2.1

# PDF Generation
reportlab==4.0.7
jinja2==3.1.2

# Caching
redis==5.0.1

# Development
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
black==23.11.0
flake8==6.1.0
```

#### Create Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Database Setup
```bash
# Create PostgreSQL database
createdb career_db

# Run database migrations
alembic upgrade head

# Create initial data (if needed)
python scripts/init_db.py
```

#### Test Backend Installation
```bash
# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test API endpoints
curl http://localhost:8000/health
```

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd ../frontend
npm install
```

#### Frontend Dependencies (`package.json`)
```json
{
  "name": "career-intelligence-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint src --ext .js,.jsx,.ts,.tsx --fix"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "axios": "^1.6.2",
    "react-hook-form": "^7.47.0",
    "react-dropzone": "^14.2.3",
    "react-query": "^3.39.3",
    "react-toastify": "^9.1.3",
    "lucide-react": "^0.292.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.1.1",
    "vite": "^4.5.0",
    "tailwindcss": "^3.3.5",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "eslint": "^8.53.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "jest": "^29.7.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/jest-dom": "^6.1.4"
  }
}
```

#### Create Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

#### Test Frontend Installation
```bash
# Run development server
npm run dev

# Build for production
npm run build
```

### 4. Redis Setup

#### Install Redis
```bash
# On macOS
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# On Windows (using WSL)
sudo apt-get install redis-server
sudo service redis-server start
```

#### Test Redis Connection
```bash
redis-cli ping
# Should return: PONG
```

### 5. Knowledge Base Setup

#### Download Sample Knowledge Base
```bash
# Create KB directory
mkdir -p knowledge_base/embeddings

# Place your Excel file here
# knowledge_base/career_intelligence_kb.xlsx
```

#### Generate Vector Embeddings
```bash
cd backend
python scripts/generate_embeddings.py
```

---

## AI Service Configuration

### 1. OpenAI GPT-5 Setup

#### Get API Key
1. Sign up at [OpenAI Platform](https://platform.openai.com)
2. Generate API key
3. Add to `.env` file:
```
GPT5_API_KEY=your-api-key-here
```

#### Test GPT-5 Integration
```python
# backend/scripts/test_gpt5.py
import openai
import os

openai.api_key = os.getenv("GPT5_API_KEY")

response = openai.ChatCompletion.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Hello, can you help with career guidance?"}]
)

print(response.choices[0].message.content)
```

### 2. Google Vision API Setup (Optional)

#### Enable Google Vision API
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable Vision API
4. Create service account and download credentials

#### Configure Environment
```bash
# Add to .env
GOOGLE_VISION_API_KEY=your-google-vision-key
OCR_ENGINE=google_vision  # or 'tesseract' for local
```

---

## Development Workflow

### 1. Git Workflow
```bash
# Create feature branch
git checkout -b feature/student-profile-enhancement

# Make changes and commit
git add .
git commit -m "feat: enhance student profile form with validation"

# Push and create PR
git push origin feature/student-profile-enhancement
```

### 2. Code Quality

#### Backend (Python)
```bash
# Format code
black .

# Lint code
flake8 .

# Run tests
pytest

# Type checking
mypy .
```

#### Frontend (JavaScript/React)
```bash
# Lint code
npm run lint

# Fix linting issues
npm run lint:fix

# Run tests
npm test

# Type checking (if using TypeScript)
npm run type-check
```

### 3. Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "Add student profile table"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Testing Strategy

### 1. Unit Tests

#### Backend Tests
```bash
# Run all tests
cd backend && pytest

# Run specific test file
pytest tests/test_students.py

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_auth.py::test_user_registration -v
```

#### Frontend Tests
```bash
# Run all tests
npm test

# Run in watch mode
npm run test:watch

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- --testPathPattern=LoginForm.test.jsx
```

### 2. Integration Tests

#### API Integration Tests
```bash
# Run API integration tests
pytest tests/integration/

# Test with real database
pytest tests/integration/ --use-real-db
```

#### End-to-End Tests
```bash
# Install Cypress (if using)
npm install --save-dev cypress

# Run E2E tests
npx cypress open  # Interactive mode
npx cypress run     # Headless mode
```

### 3. Load Testing

#### Using Apache JMeter
```bash
# Download JMeter
wget https://downloads.apache.org//jmeter/binaries/apache-jmeter-5.6.2.zip

# Run load tests
jmeter -n -t tests/load/career_system_load.jmx -l results.jtl
```

#### Using Locust (Python)
```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class CareerSystemUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_api_health(self):
        self.client.get("/health")
    
    @task
    def test_student_registration(self):
        self.client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "testpassword123",
            "name": "Test User"
        })

# Run Locust
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

---

## Docker Development Environment

### 1. Docker Compose Configuration

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: career_db
      POSTGRES_USER: career_user
      POSTGRES_PASSWORD: career_pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - career_network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - career_network

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://career_user:career_pass@postgres:5432/career_db
      REDIS_URL: redis://redis:6379
      GPT5_API_KEY: ${GPT5_API_KEY}
      GOOGLE_VISION_API_KEY: ${GOOGLE_VISION_API_KEY}
    volumes:
      - ./backend:/app
      - ./uploads:/app/uploads
      - ./reports:/app/reports
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - career_network

  frontend:
    build: ./frontend
    environment:
      REACT_APP_API_URL: http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - career_network

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./uploads:/var/www/uploads
      - ./reports:/var/www/reports
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
      - frontend
    networks:
      - career_network

volumes:
  postgres_data:
  redis_data:

networks:
  career_network:
    driver: bridge
```

### 2. Start Docker Environment
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild specific service
docker-compose build backend
docker-compose up -d backend
```

---

## Production Deployment

### 1. Cloud Infrastructure (AWS)

#### Infrastructure Setup
```bash
# Install AWS CLI
pip install awscli
aws configure

# Create VPC and subnets
aws cloudformation create-stack --stack-name career-system-infra --template-body file://infrastructure/aws-infra.yaml

# Create RDS PostgreSQL
aws rds create-db-instance \
  --db-instance-identifier career-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password your-password \
  --allocated-storage 20
```

#### Application Deployment
```bash
# Build and push Docker images
docker build -t career-backend ./backend
docker build -t career-frontend ./frontend

# Tag for ECR
docker tag career-backend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/career-backend:latest
docker tag career-frontend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/career-frontend:latest

# Push to ECR
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/career-backend:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/career-frontend:latest

# Deploy with ECS
aws ecs create-service --cluster career-cluster --service-name career-backend --task-definition career-backend:1 --desired-count 2
```

### 2. Alternative: Render.com Deployment

#### Backend Deployment
```yaml
# render.yaml
services:
  - type: web
    name: career-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        sync: false
      - key: GPT5_API_KEY
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

#### Frontend Deployment
```yaml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  REACT_APP_API_URL = "https://career-backend.onrender.com"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## Monitoring and Logging

### 1. Application Monitoring

#### Setup Prometheus + Grafana
```yaml
# monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

#### Application Metrics
```python
# backend/app/middleware/metrics.py
from prometheus_client import Counter, Histogram, generate_latest
import time

# Define metrics
request_count = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
request_duration = Histogram('app_request_duration_seconds', 'Request duration')

@app.middleware("http")
async def track_metrics(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    request_count.labels(method=request.method, endpoint=request.url.path).inc()
    request_duration.observe(duration)
    
    return response
```

### 2. Log Aggregation

#### Setup ELK Stack
```yaml
# logging/docker-compose.yml
version: '3.8'

services:
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"

  logstash:
    image: logstash:8.11.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf
    ports:
      - "5044:5044"

  kibana:
    image: kibana:8.11.0
    ports:
      - "5601:5601"
```

---

## Security Best Practices

### 1. Environment Security
- Use environment variables for sensitive data
- Never commit `.env` files to version control
- Rotate API keys regularly
- Use strong passwords and 2FA

### 2. Application Security
- Implement rate limiting
- Use HTTPS everywhere
- Validate all inputs
- Sanitize file uploads
- Implement proper CORS policies

### 3. Database Security
- Use connection pooling
- Implement proper access controls
- Regular backups
- Encrypt sensitive data at rest

### 4. API Security
```python
# backend/app/middleware/security.py
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import time

class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window
        self.requests = {}
    
    async def check_rate_limit(self, client_ip: str):
        now = time.time()
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.window
        ]
        
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.requests[client_ip].append(now)

# Apply to routes
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    await rate_limiter.check_rate_limit(client_ip)
    response = await call_next(request)
    return response
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. PostgreSQL Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -h localhost -U career_user -d career_db

# Reset PostgreSQL password
sudo -u postgres psql
ALTER USER career_user PASSWORD 'new_password';
```

#### 2. Redis Connection Issues
```bash
# Check Redis status
redis-cli ping

# Check Redis logs
tail -f /var/log/redis/redis-server.log

# Reset Redis
redis-cli FLUSHALL
```

#### 3. OCR Issues
```bash
# Check Tesseract installation
tesseract --version

# Install additional language packs
sudo apt-get install tesseract-ocr-[lang]

# Test OCR
convert input.pdf -density 300 output.png
tesseract output.png output
```

#### 4. GPT-5 API Issues
```python
# Test GPT-5 connection
import openai
openai.api_key = "your-key"

try:
    response = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print("GPT-5 is working")
except Exception as e:
    print(f"GPT-5 error: {e}")
```

#### 5. Memory Issues with Large Files
```python
# Increase upload size limit
# backend/app/main.py
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_upload_size=50 * 1024 * 1024  # 50MB
)
```

---

## Performance Optimization

### 1. Database Optimization
```sql
-- Create indexes for better performance
CREATE INDEX idx_student_email ON users(email);
CREATE INDEX idx_document_student ON documents(student_id);
CREATE INDEX idx_certificate_document ON extracted_certificates(document_id);
CREATE INDEX idx_score_student ON career_scores(student_id);
```

### 2. Caching Strategy
```python
# backend/app/services/cache_service.py
import redis
import json
from typing import Optional

class CacheService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
    
    async def get(self, key: str) -> Optional[dict]:
        data = self.redis_client.get(key)
        return json.loads(data) if data else None
    
    async def set(self, key: str, data: dict, expire: int = 3600):
        self.redis_client.setex(key, expire, json.dumps(data))
    
    async def delete(self, key: str):
        self.redis_client.delete(key)

# Use in services
cache = CacheService()

async def get_career_score(student_id: str):
    cache_key = f"career_score:{student_id}"
    cached_data = await cache.get(cache_key)
    
    if cached_data:
        return cached_data
    
    # Calculate score
    score = await calculate_career_score(student_id)
    await cache.set(cache_key, score, expire=1800)  # 30 minutes
    
    return score
```

### 3. Async Processing
```python
# backend/app/services/async_service.py
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

async def process_document_async(document_id: str):
    loop = asyncio.get_event_loop()
    
    # Run OCR in thread pool
    ocr_result = await loop.run_in_executor(
        executor, 
        process_document_ocr, 
        document_id
    )
    
    # Process in background
    asyncio.create_task(extract_skills_async(ocr_result))
    
    return {"status": "processing", "document_id": document_id}
```

This comprehensive development setup guide provides everything needed to get the AI-Powered Student Career Intelligence & Guidance System up and running for development and production deployment.