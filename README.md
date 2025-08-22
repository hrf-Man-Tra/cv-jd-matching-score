# CV-JD Matching Score API

🚀 **AI-powered CV and Job Description Matching System** - A FastAPI-based application that analyzes the compatibility between CVs and Job Descriptions using OpenAI's language models.

## 📁 Project Structure

```
cv-jd-matching-score/
├── 📁 src/
│   ├── 📁 api/
│   │   └── 📄 routes.py          # API endpoints
│   ├── 📁 extractors/
│   │   ├── 📄 cv_extractor.py    # CV processing logic
│   │   └── 📄 jd_loader.py       # JD processing logic
│   └── 📁 matching/
│       └── 📄 matching_engine.py # Matching algorithm
├── 📁 data/
│   ├── 📁 input/
│   │   ├── 📁 CV/               # Sample CV files
│   │   └── 📁 JD/               # Sample JD files
│   └── 📁 output/               # Processing results
├── 📄 main.py                   # Application entry point
├── 📄 test_client.py            # API testing client
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example             # Environment template
├── 📄 run_server.sh            # Server startup script
├── 📄 dev.sh                   # Development script
└── 📄 README.md                # This file
```
## ✨ Features

- **📄 CV Extraction**: Extract structured information from PDF CVs
- **📝 JD Processing**: Process job descriptions from text files
- **🎯 Matching Algorithm**: Calculate compatibility scores between CVs and JDs
- **🔗 RESTful API**: Easy-to-use HTTP endpoints
- **📊 Detailed Analysis**: Comprehensive matching reports with breakdowns
- **🔄 Multiple Input Methods**: Support file uploads and direct data input
- **📚 Auto Documentation**: Interactive API documentation with Swagger UI

## 🚀 Usage

### Start the Server

```bash
python main.py
```

### Access the API

Once the server is running, you can access:

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Input | Output |
|--------|----------|-------------|-------|--------|
| `GET` | `/` | Root endpoint | - | Welcome message |
| `GET` | `/health` | Health check | - | Service status |
| `POST` | `/extract-cv` | Extract CV info | PDF file | Structured CV data |
| `POST` | `/load-jd` | Load job description | TXT file | JD content |
| `POST` | `/match-cv-jd` | Match CV with JD | PDF + TXT files | Matching score |
