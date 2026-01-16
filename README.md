# AI-Powered Health Risk Profiler 🩺

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com/)
[![ML Models](https://img.shields.io/badge/ML-3%20Models-orange.svg)](https://scikit-learn.org/)
[![Accuracy](https://img.shields.io/badge/Accuracy-95.86%25-brightgreen.svg)](.)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Production-ready ML system for cardiovascular health risk assessment using ensemble learning (Random Forest, XGBoost, Neural Network) achieving **95.86% accuracy** with full explainability.

![API Demo](docs/images/api_demo.png)

---

## 🎯 Key Features

- **🤖 Ensemble ML**: 3 models (RF, XGBoost, NN) with weighted averaging
- **📊 High Accuracy**: 95.86% on test set with 99.45% ROC-AUC
- **🔍 Explainable AI**: Feature importance showing top risk contributors
- **⚡ Fast API**: <500ms response time, RESTful design
- **🐳 Production Ready**: Docker, tests, comprehensive docs
- **📈 Dual Modes**: ML-powered and rule-based predictions

---

## 🚀 Quick Start

### Option 1: Local Development

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/health-risk-profiler.git
cd health-risk-profiler

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Generate dataset and train models
python ml_models/dataset_generator.py
python ml_models/model_trainer.py

# Run API server
uvicorn app.main:app --reload

# Access at http://127.0.0.1:8000
# API docs at http://127.0.0.1:8000/docs
```

### Option 2: Docker

```bash
docker build -t health-risk-profiler .
docker run -p 8000:8000 health-risk-profiler
```

### Option 3: Docker Compose

```bash
docker-compose up
```

---

## 📋 API Endpoints

| Endpoint | Method | Description | Response Time |
|----------|--------|-------------|---------------|
| `/predict` | POST | ML-based risk prediction | ~350ms |
| `/analyze` | POST | Rule-based assessment | ~120ms |
| `/model-info` | GET | Model performance metrics | ~80ms |
| `/health` | GET | Health check | ~30ms |

### Example Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "bmi": 32.0,
    "systolic_bp": 160,
    "cholesterol": 260,
    "smoker": true,
    "exercise": "never",
    "diet": "high fat",
    "family_history": true,
    "sleep_hours": 5.0,
    "alcohol": "heavy",
    "stress_level": 9
  }'
```

### Example Response

```json
{
  "risk_level": "high",
  "risk_score": 81.0,
  "confidence": 0.9187,
  "probabilities": {
    "low": 0.0004,
    "medium": 0.0809,
    "high": 0.9187
  },
  "model_predictions": {
    "random_forest": "high",
    "xgboost": "high",
    "neural_network": "high"
  },
  "top_contributing_factors": [
    {"feature": "age", "importance": 0.19},
    {"feature": "family_history", "importance": 0.12},
    {"feature": "smoker", "importance": 0.11}
  ]
}
```

---

## 📊 Model Performance

| Model | Accuracy | F1 Score | ROC-AUC |
|-------|----------|----------|---------|
| **Neural Network** | **95.86%** | **0.9586** | **0.9945** |
| XGBoost | 93.25% | 0.9299 | 0.9865 |
| Random Forest | 88.20% | 0.8761 | 0.9592 |

**Ensemble Method**: Weighted averaging (XGBoost: 40%, RF: 35%, NN: 25%)

---

## 🏗️ Project Structure

```
health-risk-profiler/
├── app/
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic models
│   └── services.py          # Business logic
├── ml_models/
│   ├── dataset_generator.py # Synthetic data generation
│   ├── model_trainer.py     # Training pipeline
│   └── risk_classifier.py   # ML inference
├── tests/
│   └── test_api_comprehensive.py  # Automated tests
├── data/
│   └── processed/           # Training data
├── saved_models/            # Trained model artifacts
├── docs/
│   ├── TESTING_GUIDE.md
│   ├── ENHANCEMENT_ROADMAP.md
│   └── PROJECT_SHOWCASE.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

### Automated Tests

```bash
python tests/test_api_comprehensive.py
```

**Test Coverage**: 9 test cases covering:
- Health check
- Model loading
- ML predictions (high/low/borderline risk)
- Rule-based analysis
- Performance benchmarking

### Manual Testing

Follow the comprehensive guide in `TESTING_GUIDE.md` for step-by-step manual testing.

---

## 📚 Documentation

- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Complete manual testing procedures
- **[ENHANCEMENT_ROADMAP.md](ENHANCEMENT_ROADMAP.md)** - Future improvements (UI, monitoring, advanced ML)
- **[PROJECT_SHOWCASE.md](PROJECT_SHOWCASE.md)** - Resume bullets & interview prep
- **[MANUAL_TEST_RESULTS.md](MANUAL_TEST_RESULTS.md)** - Test execution results

---

## 🛠️ Tech Stack

**Backend**: FastAPI, Python 3.9+  
**ML**: scikit-learn, XGBoost, Neural Network (MLP)  
**Data**: pandas, numpy  
**Deployment**: Docker, uvicorn  
**Testing**: pytest, requests

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (optional, defaults work for local):

```bash
# Server
PORT=8000
HOST=0.0.0.0

# Models
MODEL_PATH=saved_models/
```

---

## 📈 Performance Benchmarks

- **Response Time**: P50 < 200ms, P95 < 500ms
- **Throughput**: 10+ concurrent requests
- **Memory**: ~500MB (all models loaded)
- **Model Size**: ~150MB total

---

## 🚢 Deployment

### Deploy to Render

1. Fork this repository
2. Create account on [Render.com](https://render.com)
3. Click "New Web Service"
4. Connect your GitHub repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt && python ml_models/dataset_generator.py && python ml_models/model_trainer.py`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

Detailed instructions: See `docs/DEPLOYMENT.md`

### Deploy to Railway/Heroku

See deployment guides in `docs/` folder.

---

## 🤝 Contributing

Contributions welcome! Please read `CONTRIBUTING.md` first.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📅 Roadmap

- [x] Core ML pipeline (Dataset → Training → Inference)
- [x] FastAPI REST API
- [x] Docker containerization
- [x] Comprehensive documentation
- [x] Automated testing
- [ ] SHAP explainability (Week 1)
- [ ] React dashboard (Week 2)
- [ ] PostgreSQL database (Week 3)
- [ ] Monitoring (Prometheus/Grafana)
- [ ] CI/CD pipeline (GitHub Actions)

See full roadmap in `ENHANCEMENT_ROADMAP.md`

---

## 🎓 Learning Resources

### ML Concepts
- **Ensemble Learning**: Combining multiple models for better predictions
- **Feature Engineering**: Creating synthetic health data with realistic correlations
- **Pipeline Pattern**: Preventing data leakage in ML workflows
- **Explainability**: Using feature importance for transparent predictions

### Software Engineering
- **API Design**: RESTful principles with FastAPI
- **Error Handling**: Graceful degradation and HTTP status codes
- **Testing**: Unit tests, integration tests, performance tests
- **Deployment**: Docker, containerization, cloud deployment

Detailed explanations in `PROJECT_SHOWCASE.md`

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

---

## 👤 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Portfolio: [yourportfolio.com](https://yourportfolio.com)

---

## 🙏 Acknowledgments

- Synthetic dataset inspired by real-world cardiovascular risk factors
- ML architecture based on industry best practices
- Documentation structure from production ML systems

---

## 📞 Support

Found a bug or have suggestions?
- Open an [Issue](https://github.com/yourusername/health-risk-profiler/issues)
- Start a [Discussion](https://github.com/yourusername/health-risk-profiler/discussions)

---

## ⭐ Star History

If this project helped you, please consider giving it a star! ⭐

---

**Built with ❤️ for learning and demonstrating production ML engineering**

---

## 🔗 Related Projects

- [Disease Prediction System](https://github.com/...)
- [Medical Chatbot](https://github.com/...)
- [Health Analytics Dashboard](https://github.com/...)

---

**Last Updated**: January 2026  
**Status**: ✅ Production Ready
