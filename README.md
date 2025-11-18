# 🎬 CineMood

AI-powered movie recommendation system that understands your mood. Built with FastAPI, React, Ollama (Llama 3.1), and vector search using sentence transformers.

## ✨ Features

- 🤖 **AI Intent Parsing**: Natural language understanding powered by Llama 3.1 via Ollama
- 🔍 **Vector Similarity Search**: Semantic movie search using sentence transformers (paraphrase-multilingual-mpnet-base-v2)
- 🎭 **Mood-Based Recommendations**: 5 quick mood shortcuts (輕鬆/療癒/刺激/平靜/深度)
- 🎯 **Intelligent Reasoning**: AI-generated explanations for each recommendation
- 🎬 **Similar Movies**: Vector-based similarity calculation for movie discovery
- 🖼️ **TMDB Integration**: High-quality movie posters and metadata
- ⚡ **Modern Tech Stack**: FastAPI backend + React frontend with TypeScript

## 🏗️ Architecture

```
CineMood/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic (AI, vector search)
│   │   └── core/           # Configuration
│   ├── data/               # Vector store & embeddings
│   └── scripts/            # Utility scripts
│
└── frontend/               # React Frontend
    ├── src/
    │   ├── api/           # API client layer
    │   ├── hooks/         # Custom React hooks
    │   ├── components/    # Reusable components
    │   ├── pages/         # Page components
    │   └── types/         # TypeScript definitions
    └── public/
```

## 🚀 Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **LLM**: Ollama (Llama 3.1:8b)
- **Embeddings**: Sentence Transformers (paraphrase-multilingual-mpnet-base-v2)
- **Vector Store**: Custom pickle-based implementation (768-dim)

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 7.2.2
- **Styling**: TailwindCSS v4
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Architecture**: pilot_x layered design

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Ollama with Llama 3.1 model

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run database migrations
alembic upgrade head

# Sync embeddings (optional, if vector store not present)
python scripts/sync_embeddings.py

# Start backend server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# VITE_API_BASE_URL=http://localhost:8000

# Start development server
npm run dev
```

## 🎯 Usage

1. **Start Backend**: `http://localhost:8000`
2. **Start Frontend**: `http://localhost:5173`
3. **API Docs**: `http://localhost:8000/docs`

### Example Queries

- "我心情不好，想看療癒的電影"
- "輕鬆搞笑的週末電影"
- "關於時間旅行的科幻片"
- "刺激的動作冒險片"
- "讓人思考的深度劇情"

## 🔧 API Endpoints

### Movies
- `GET /api/v1/movies` - Get movie list (with pagination & filters)
- `GET /api/v1/movies/{id}` - Get movie details
- `GET /api/v1/genres` - Get all genres

### AI Recommendations
- `POST /api/v1/ai/recommend` - AI-powered recommendations with intent parsing
- `POST /api/v1/ai/search` - Semantic vector search
- `GET /api/v1/ai/similar/{movie_id}` - Get similar movies

## 🎨 UI/UX Highlights

- **Dark Mode Design**: Slate-based color scheme optimized for movie browsing
- **Smooth Animations**: fadeInUp, pulse-ai, card-hover effects
- **Responsive Layout**: Mobile-first design with Tailwind breakpoints
- **Auto-scroll**: Smooth navigation between movie details
- **Loading States**: Skeleton screens and spinners for better UX

## 📊 Data

- **Movie Database**: 212 TMDB movies with Chinese metadata
- **Vector Dimensions**: 768-dimensional embeddings
- **Supported Languages**: Traditional Chinese (繁體中文) + English

## 🛠️ Development

### Backend Development
```bash
# Run tests
pytest

# Format code
black app/

# Type checking
mypy app/
```

### Frontend Development
```bash
# Build for production
npm run build

# Lint code
npm run lint

# Type checking
npm run type-check
```

## 📝 Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost:5432/cinemood
OLLAMA_BASE_URL=http://localhost:11434
EMBEDDING_MODEL=paraphrase-multilingual-mpnet-base-v2
LLM_MODEL=llama3.1:8b
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🎓 Key Features Explained

### 1. AI Intent Parsing
Uses Llama 3.1 to extract mood, genres, and keywords from natural language queries.

### 2. Vector Similarity Search
Converts movie metadata into embeddings and finds similar movies using cosine similarity.

### 3. Hybrid Recommendation
Combines LLM understanding with vector search for intelligent, contextual recommendations.

## 📚 Documentation

### Project Documentation
- [Requirements](docs/Requirements.md) - Project requirements and specifications
- [Technical Specification](docs/Technical-Specification.md) - Detailed technical specifications
- [Development Roadmap](docs/DEVELOPMENT_ROADMAP.md) - Project phases and milestones

### Architecture & Design
- [Backend Architecture](docs/BACKEND_ARCHITECTURE.md) - Backend system architecture
- [Database ER Diagram](docs/DATABASE_ER_DIAGRAM.md) - Database schema and relationships
  - [ER Diagram (SVG)](docs/database/ER_Diagram.svg) - Visual database schema
  - [Database Models (DBML)](docs/database/models.dbml) - DBML schema definition
- [Architecture Dependency Audit](docs/ARCHITECTURE_DEPENDENCY_AUDIT.md) - Dependency analysis
- [UI/UX Design Guide](docs/UI_UX_DESIGN.md) - Complete design system and wireframes

### Phase Documentation
- [Phase 1: Data Layer](docs/PHASE1_DATA_LAYER.md) - Database setup and TMDB integration
- [Phase 2: API Layer](docs/PHASE2_API_LAYER.md) - RESTful API implementation
- [Phase 3: AI Layer](docs/PHASE3_AI_LAYER.md) - LLM and vector search implementation
- [Phase 3: Test Report](docs/PHASE3_TEST_REPORT.md) - AI system testing results

### Setup Guides
- [Backend Startup Guide](docs/BACKEND_STARTUP_GUIDE.md) - Step-by-step backend setup

### Hardware & Infrastructure
- [Hardware Assessment](docs/Hardware-Assessment.md) - System requirements analysis
- [OMEN Specification](docs/OMEN_Specification.md) - Development machine specifications

## 📄 License

MIT License

## 👤 Author

**franklin77543**

## 🙏 Acknowledgments

- TMDB for movie data and images
- Ollama for local LLM inference
- Sentence Transformers for multilingual embeddings
- FastAPI and React communities

---

⭐ If you find this project useful, please consider giving it a star!
