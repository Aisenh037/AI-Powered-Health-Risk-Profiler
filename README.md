# 🏥 AI-Powered Health Risk Profiler

> **Live Demo (Backend API)**: [https://ai-powered-health-risk-profiler-isvm.onrender.com/docs](https://ai-powered-health-risk-profiler-isvm.onrender.com/docs)
> **Live Demo (Frontend App)**: [Streamlit Cloud Link]

![Project Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.25%2B-red)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

## 📌 Project Overview
**AI-Powered Health Risk Profiler** is a comprehensive full-stack application designed to predict the risk of cardiovascular diseases (heart attack, stroke) using machine learning.

It moves beyond simple prediction by offering an **end-to-end solution**:

1.  **Synthetic Data Generation**: Creates a realistic dataset of patient health records.
2.  **ML Model Training**: Trains an ensemble of models (Random Forest, XGBoost, Neural Network) for high accuracy.
3.  **FastAPI Backend**: Serves predictions via a high-performance REST API.
4.  **Streamlit Frontend**: Provides a user-friendly interface for doctors/patients using a **modular component-based architecture**.
5.  **Dockerized Deployment**: Ensures consistency across environments.

---

## 📖 Essential Documentation
| Document | Purpose |
|----------|---------|
| [**PROJECT_SHOWCASE.md**](docs/PROJECT_SHOWCASE.md) | **Read First** - The "Product Pitch" & Features |
| [**INTERVIEW_PITCH.md**](docs/INTERVIEW_PITCH.md) | **For You** - Exact scripts for interviews |
| [**PROJECT_ARCHITECTURE.md**](docs/PROJECT_ARCHITECTURE.md) | **System Design** - Map of every file & folder |
| [**DEPLOYMENT_CHECKLIST.md**](docs/DEPLOYMENT_CHECKLIST.md) | DevOps & Cloud setup guide |

---

## 🏗️ Project Structure
This project follows a **Microservices-Ready** architecture:

```text
health-risk-profiles/
├── app/                 # 🧠 Backend API (FastAPI)
│   ├── main.py          # Gateway & Endpoints
│   └── services.py      # Business Logic & OCR
├── frontend/            # 💻 Frontend UI (Streamlit)
│   ├── main.py          # Entry Point
│   └── components/      # Modular UI Widgets (Charts, Forms)
├── ml_models/           # 🤖 Machine Learning Pipeline
├── docs/                # 📚 Documentation & Guides
├── tests/               # 🧪 Automated Test Suite
└── docker-compose.yml   # 🐳 Container Orchestration
```

---

## 🚀 Quick Start

### 1. Run with Docker (Recommended)
This starts both services in one command.
```bash
docker-compose up --build
```
- **API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend**: [http://localhost:8501](http://localhost:8501)

### 2. Manual Setup

**Step A: Backend (Terminal 1)**
```bash
# Install backend reqs
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

**Step B: Frontend (Terminal 2)**
```bash
# Install frontend reqs (if different)
pip install -r frontend/requirements.txt

# Run modular frontend
streamlit run frontend/main.py
```

---

## 🛠️ Tech Stack
- **Backend**: FastAPI, Python 3.9+, Pydantic
- **Frontend**: Streamlit, Plotly, Mermaid.js
- **ML**: scikit-learn, XGBoost, Neural Network (MLP)
- **Deployment**: Docker, Render.com

---

## 👤 Author
**Aisenh037**
- GitHub: [@Aisenh037](https://github.com/Aisenh037)

---
**Built with ❤️ for learning and demonstrating production ML engineering**
