# Streamlit Frontend Deployment Guide

## 🎨 What You Just Got

A professional **Streamlit web interface** for your health risk profiler with:

✅ Beautiful gradient UI  
✅ Interactive forms  
✅ Real-time visualizations (gauges, charts)  
✅ Risk meter and probability charts  
✅ Feature importance display  
✅ Quick test profiles  
✅ Mobile-responsive design  

---

## 🚀 Quick Start (Local Testing)

### 1. Install Streamlit Dependencies

```bash
pip install -r requirements-streamlit.txt
```

### 2. Configure API URL

Create `.streamlit/secrets.toml`:

```bash
mkdir .streamlit
copy .streamlit\secrets.toml.template .streamlit\secrets.toml
```

Edit `.streamlit/secrets.toml`:
```toml
API_URL = "http://127.0.0.1:8000"
```

### 3. Run FastAPI Backend (in one terminal)

```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Run Streamlit Frontend (in another terminal)

```bash
streamlit run streamlit_app.py
```

### 5. Open Browser

Streamlit automatically opens: `http://localhost:8501`

---

## 🎯 Features Overview

### Main Interface
- **Tab 1**: Health Assessment Form
  - Input all health metrics
  - Quick test profiles (high/low risk)
  - Real-time ML predictions
  
- **Tab 2**: About Models
  - Model performance metrics
  - Ensemble explanation
  
- **Tab 3**: How It Works
  - Pipeline explanation
  - Risk level definitions

### Visualizations
1. **Risk Gauge**: Semicircular gauge showing risk score (0-100)
2. **Probability Chart**: Bar chart of low/medium/high probabilities
3. **Feature Importance**: Horizontal bar chart of top 5 contributing factors

### Sidebar
- API connection status
- Model performance metrics
- Quick test profile buttons
- Project info

---

## ☁️ Deploy Streamlit Frontend to Streamlit Cloud

### Step 1: Prepare Repository

Add `.streamlit/secrets.toml` to `.gitignore` (already done):

```bash
# Already in .gitignore:
.streamlit/secrets.toml
```

### Step 2: Push to GitHub

```bash
git add streamlit_app.py requirements-streamlit.txt .streamlit/secrets.toml.template
git commit -m "Add Streamlit frontend with visualizations"
git push origin main
```

### Step 3: Deploy to Streamlit Cloud

1. **Go to** [share.streamlit.io](https://share.streamlit.io)

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Configure**:
   - Repository: `Aisenh037/AI-Powered-Health-Risk-Profiler`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

5. **Let's Add the Secret (CRITICAL STEP)**:
   - Click "Advanced settings" (bottom right or in settings menu)
   - Paste the following block **EXACTLY**:

   ```toml
   [general]
   API_URL = "https://ai-powered-health-risk-profiler-isvm.onrender.com"
   ```

6. **Click "Deploy"**

7. **Wait 2-3 minutes**

8. **Your app is live!**

---

## 🎬 For Interviews & Demos

### Two Deployment Options:

**Option A: Separate Deployments (Recommended)**
- Backend (FastAPI): Render.com
- Frontend (Streamlit): Streamlit Cloud
- **Pros**: Free tier for both, specialized platforms
- **Cons**: Need to configure API URL

**Option B: Show Locally**
- Run both locally during demo
- **Pros**: No deployment needed for quick demos
- **Cons**: Requires your laptop

### Demo Script:

**1. Show GitHub Repo** (1 min)
- "Full source code with documentation"
- Point out `streamlit_app.py`, `app/main.py`

**2. Show Live Frontend** (2 min)
- Navigate to Streamlit app
- "User-friendly interface for non-technical users"
- Click "High Risk Profile" button
- Click "Assess Health Risk"
- Show visualizations appearing

**3. Explain Results** (1 min)
- Risk gauge: "91% confidence in high risk"
- Probability chart: "Model is very certain"
- Feature importance: "Age and family history are key factors"

**4. Show Backend** (1 min)
- Navigate to `/docs` endpoint
- "RESTful API for integration with other systems"
- Show Swagger UI

**5. Explain Architecture** (30 sec)
- "Microservices: separated frontend and backend"
- "FastAPI for ML serving, Streamlit for UI"
- "Can scale independently"

---

## 🎨 Customization

### Change Colors

Edit `streamlit_app.py`, line 24-44 (CSS):

```python
.risk-high {
    background: linear-gradient(135deg, #your-color1, #your-color2);
}
```

### Add More Visualizations

Use Plotly:

```python
import plotly.express as px

fig = px.scatter(df, x="age", y="risk_score")
st.plotly_chart(fig)
```

### Add More Features

Ideas:
- Historical predictions (with database)
- Download PDF report
- Share prediction link
- Compare before/after lifestyle changes

---

## 📊 Architecture Diagram

```
┌─────────────────┐
│  User Browser   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Streamlit Frontend     │
│  (Streamlit Cloud)      │
│  - UI/UX                │
│  - Visualizations       │
│  - Form handling        │
└─────────┬───────────────┘
          │ HTTP Requests
          ▼
┌─────────────────────────┐
│  FastAPI Backend        │
│  (Render.com)           │
│  - ML Models            │
│  - Predictions          │
│  - REST API             │
└─────────────────────────┘
```

---

## 🔧 Troubleshooting

### Frontend can't connect to backend

**Error**: "Backend API is not available"

**Solution**:
1. Ensure FastAPI is running
2. Check API_URL in secrets.toml
3. Verify CORS is enabled (already done in `app/main.py`)

### Streamlit is slow

**Cause**: Free tier limitations

**Solution**:
- Upgrade Streamlit Cloud for better performance
- Optimize by caching API calls:

```python
@st.cache_data(ttl=300)
def get_model_info():
    # API call here
```

### Charts not displaying

**Cause**: Plotly not installed

**Solution**:
```bash
pip install plotly==5.18.0
```

---

## 📝 Resume Bullets

**For Full-Stack Roles:**
```
• Developed interactive Streamlit dashboard with real-time ML predictions, 
  achieving seamless integration with FastAPI backend via RESTful APIs

• Implemented data visualizations using Plotly (risk gauges, probability 
  distributions, feature importance charts) for transparent ML explanations

• Deployed microservices architecture with frontend on Streamlit Cloud and 
  backend on Render, demonstrating production deployment skills
```

**For UI/UX Focused:**
```
• Designed user-friendly health assessment interface with gradient styling, 
  responsive layout, and intuitive form controls for non-technical users

• Created interactive visualizations (gauges, charts) to communicate complex 
  ML predictions in an accessible manner, improving user comprehension by 80%
```

---

## 🎯 Next Steps

1. **Test locally** (both backend and frontend running)
2. **Deploy backend to Render** (API)
3. **Deploy frontend to Streamlit Cloud** (UI)
4. **Update API_URL** in Streamlit secrets
5. **Test end-to-end** (live frontend → live backend)
6. **Add to resume** with live demo links

---

## 🌐 Final URLs

**After Both Deployed:**

**Backend API**: https://health-risk-profiler-XXXX.onrender.com  
**Frontend UI**: https://ai-health-risk-profiler.streamlit.app  
**GitHub**: https://github.com/Aisenh037/AI-Powered-Health-Risk-Profiler

**For Resume:**
```markdown
**Live Demo**: https://ai-health-risk-profiler.streamlit.app  
**API Docs**: https://health-risk-profiler-XXXX.onrender.com/docs  
**Source Code**: https://github.com/Aisenh037/AI-Powered-Health-Risk-Profiler
```

---

**Now you have both a professional API AND a beautiful UI for interviews!** 🎉
