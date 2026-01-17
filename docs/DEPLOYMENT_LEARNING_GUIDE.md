# Render Deployment - Complete Learning Guide

## 📚 What You'll Learn

By the end of this guide, you'll understand:
- ✅ How cloud deployment works
- ✅ What Render.com does (Platform as a Service)
- ✅ Environment variables vs hardcoded config
- ✅ Build vs Start commands
- ✅ How servers handle dynamic ports
- ✅ Cold starts and scaling
- ✅ Monitoring and logs

**Time to complete**: 45-60 minutes  
**Cost**: Free tier or $7/month Starter plan

---

## 🎯 Step 1: Understanding What We're Deploying

### What is deployment?

**Before deployment** (Local):
```
Your Computer → localhost:8000 → Only you can access
```

**After deployment** (Cloud):
```
Render Server → https://your-app.onrender.com → Anyone can access
```

### What platform should I use?

| Platform | Best For | Cost |
|----------|----------|------|
| **Render** | Python APIs, simple setup | Free/$7/mo |
| Railway | Quick deploy, auto-config | $5 credit |
| Heroku | Industry standard | $7/mo min |
| AWS EC2 | Full control, learning | Complex |
| Vercel | Frontend/Next.js | Free |

**We're using Render** because:
- ✅ Easy for beginners
- ✅ Good documentation
- ✅ Free tier available
- ✅ Auto-deploys from GitHub
- ✅ Good for FastAPI/Python

---

## 🎓 Key Concepts to Understand

### 1. PaaS vs IaaS vs Serverless

**IaaS (Infrastructure as a Service)** - AWS EC2, DigitalOcean
- You get: A computer (virtual machine)
- You manage: OS, dependencies, server, code
- Example: Renting a raw computer

**PaaS (Platform as a Service)** - Render, Heroku, Railway
- You get: Platform that runs your code
- You manage: Just your code
- Example: Renting a furnished apartment

**Serverless** - AWS Lambda, Google Cloud Functions
- You get: Code execution on demand
- You manage: Individual functions
- Example: Paying per use (like Airbnb)

**Render is PaaS** = You just provide code, they handle everything else.

---

### 2. Build Command vs Start Command

**Build Command**: Runs ONCE when deploying
```bash
pip install -r requirements.txt
python ml_models/dataset_generator.py
python ml_models/model_trainer.py
```
- Installs dependencies
- Trains ML models
- Prepares your app

**Start Command**: Runs EVERY TIME server starts
```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
- Starts the web server
- Handles incoming requests
- Keeps running 24/7

**Analogy**:
- Build = Cooking ingredients (once)
- Start = Serving food (ongoing)

---

### 3. Dynamic Port (`$PORT`)

**Local**:
```python
# You control the port
uvicorn app.main:app --port 8000  # Always 8000
```

**Cloud (Render)**:
```python
# Render controls the port
uvicorn app.main:app --port $PORT  # Could be 10000, 8080, etc.
```

**Why?**: Cloud providers assign ports dynamically to avoid conflicts.

**`$PORT`** = Environment variable set by Render

**Understanding Environment Variables**:
```bash
# Local
PORT=8000

# Render sets it automatically
PORT=10000
```

Code reads it:
```python
import os
port = os.getenv("PORT", 8000)  # Use Render's port or default to 8000
```

---

### 4. `--host 0.0.0.0` vs `127.0.0.1`

**Local Development** (`127.0.0.1`):
```
Your computer only → 127.0.0.1:8000 → localhost
```

**Production** (`0.0.0.0`):
```
Any IP address → 0.0.0.0:8000 → Accessible from internet
```

**Why?**:
- `127.0.0.1` = "loopback" = only this machine
- `0.0.0.0` = "any interface" = external access allowed

**Security**: Render handles firewall, so it's safe.

---

## 🚀 Step 2: Create Render Account (5 minutes)

### What is Render?

Render is a **cloud platform** that:
- Hosts your code on their servers
- Automatically builds and deploys
- Provides a public URL
- Monitors your app
- Handles SSL/HTTPS automatically

### Steps:

1. **Go to [render.com](https://render.com)**
   - Render is a modern PaaS (launched 2019)
   - Alternative to Heroku

2. **Click "Get Started for Free"**
   - No credit card required for free tier!

3. **Sign up with GitHub**
   - Click "GitHub"
   - This connects Render to your repos
   
   **Why GitHub sign-in?**
   - Render can access your code
   - Auto-deploys when you push
   - No manual code upload

4. **Authorize Render**
   - Render asks permission to read your repos
   - Click "Authorize Render"
   
   **What Render can see:**
   - Your public repositories
   - (Optionally) Private repositories if you allow

5. **You're in!**
   - You'll see Render Dashboard

**✅ Checkpoint**: You should be on Render Dashboard with "New +" button.

---

## 🔧 Step 3: Create Web Service (10 minutes)

### Understanding "Web Service"

Render offers different service types:

| Type | Use Case | Example |
|------|----------|---------|
| **Web Service** | APIs, websites that respond to HTTP | Your FastAPI app ✅ |
| Background Worker | Long-running tasks | ML training jobs |
| Cron Job | Scheduled tasks | Daily reports |
| Static Site | HTML/JS only | React/Vue apps |

**We need Web Service** because FastAPI responds to HTTP requests.

### Steps:

1. **Click "New +" → "Web Service"**

2. **Connect Repository**
   
   You'll see list of your GitHub repos.
   
   Find and click: `AI-Powered-Health-Risk-Profiler`
   
   **What happens**: Render clones your GitHub repo

3. **Configure Service**

   **Name**: `health-risk-profiler`
   - This becomes your URL subdomain
   - URL will be: `health-risk-profiler-XXXX.onrender.com`
   - Choose short, descriptive name
   
   **Region**: Select closest to you
   - Options: Oregon (US West), Ohio (US East), Frankfurt (EU), Singapore (Asia)
   - **Why?** Lower latency (faster response)
   
   **Branch**: `main`
   - Which git branch to deploy
   - Every push to `main` triggers redeploy
   
   **Root Directory**: Leave blank
   - If code is in subfolder, specify here
   - Your code is at root, so blank
   
   **Environment**: `Python 3`
   - Render auto-detects from `requirements.txt`
   - Uses Python 3.9+ automatically

4. **Build Command** (IMPORTANT!)

   ```bash
   pip install -r requirements.txt && python ml_models/dataset_generator.py && python ml_models/model_trainer.py
   ```
   
   **Breaking it down**:
   
   **Part 1**: `pip install -r requirements.txt`
   - Installs all Python packages
   - From your requirements.txt file
   - scikit-learn, xgboost, fastapi, etc.
   
   **Part 2**: `&&` (AND operator)
   - Runs next command ONLY if previous succeeded
   - If pip fails, stops here
   
   **Part 3**: `python ml_models/dataset_generator.py`
   - Generates 10,000 synthetic health records
   - Creates `data/processed/health_dataset.csv`
   - Takes ~10-20 seconds
   
   **Part 4**: `&& python ml_models/model_trainer.py`
   - Trains 3 ML models
   - Saves models to `saved_models/`
   - Takes ~2-3 minutes
   
   **Why run training during build?**
   - ✅ Always fresh models
   - ✅ Reproducible
   - ✅ No need to commit large model files
   
   **Alternative** (if models already in GitHub):
   ```bash
   pip install -r requirements.txt
   ```
   (Skip training, use pre-existing models)

5. **Start Command** (IMPORTANT!)

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   
   **Breaking it down**:
   
   **`uvicorn`**: ASGI server
   - Runs Python async web apps
   - FastAPI requires ASGI (not WSGI like Flask)
   
   **`app.main:app`**: Module path
   - `app` = directory
   - `.main` = main.py file
   - `:app` = FastAPI instance named 'app'
   - Python import: `from app.main import app`
   
   **`--host 0.0.0.0`**: Listen on all interfaces
   - Allows external connections
   - Required for cloud deployment
   
   **`--port $PORT`**: Use Render's port
   - Render sets $PORT environment variable
   - Could be 10000, 8080, etc.
   - DO NOT hardcode port!

6. **Instance Type** (CRITICAL DECISION!)

   **Free Tier** (512 MB RAM):
   - Cost: $0/month
   - RAM: 512 MB
   - CPU: 0.1 shared CPU
   - **Spins down** after 15 min inactivity
   - **First request** after spin-down: 30-60 seconds
   
   **Will it work?**
   - ⚠️ Tight for 3 ML models
   - Each model ~50-80 MB
   - Total: ~200-300 MB just for models
   - Plus FastAPI, Python runtime: ~200 MB
   - **Total**: ~400-500 MB
   - **Verdict**: Might work, might crash
   
   **Starter** ($7/month, 512 MB):
   - Same RAM as free
   - NO spin-down (always on)
   - Better CPU (0.5 CPU)
   - **Verdict**: Borderline
   
   **Standard** ($25/month, 2 GB RAM):
   - Plenty of RAM
   - Full CPU core
   - **Verdict**: Safe choice ✅

   **My Recommendation for Learning**:
   
   **Option A**: Try Free Tier first
   - If it crashes, modify code (see below)
   - Upgrade to Starter if needed
   
   **Option B**: Start with Starter ($7/mo)
   - Guaranteed to work
   - Worth it for portfolio project

7. **Advanced Options** (Optional)

   Expand "Advanced" if you want to see:
   
   **Auto-Deploy**: ON (default)
   - Redeploys on every git push
   - Turn OFF if you want manual control
   
   **Environment Variables**: Leave empty for now
   - For secrets like API keys
   - We don't need any yet
   
   **Health Check Path**: `/health`
   - Render pings this endpoint
   - If fails 3 times, restarts service
   - Our app has `/health` endpoint ✅

8. **Click "Create Web Service"**

---

## ⏳ Step 4: Monitor Deployment (5-10 minutes)

### What happens now?

Render performs these steps automatically:

```
1. Clone Git Repo from GitHub
   └─ Downloads your code

2. Build (run build command)
   ├─ Install Python dependencies (pip install)
   ├─ Generate dataset (10,000 records)
   └─ Train models (RF, XGBoost, NN)
   
3. Create Container (Docker-like)
   └─ Packages your app with dependencies

4. Deploy
   ├─ Start uvicorn server
   ├─ Health check (ping /health)
   └─ Route traffic to your service

5. Success!
   └─ App is live at https://health-risk-profiler-XXXX.onrender.com
```

### Watch the Logs

You'll see real-time build output:

```
Building...
==> Cloning from https://github.com/Aisenh037/AI-Powered-Health-Risk-Profiler
==> Running 'pip install -r requirements.txt'
Collecting fastapi==0.111.0
Collecting xgboost==2.0.3
...
Successfully installed 25 packages

==> Running 'python ml_models/dataset_generator.py'
INFO:__main__:Generating 10000 synthetic health records
INFO:__main__:Dataset saved to data/processed/health_dataset.csv

==> Running 'python ml_models/model_trainer.py'
INFO:__main__:Training Random Forest...
INFO:__main__:Training XGBoost...
INFO:__main__:Training Neural Network...
Best Model: neural_network (F1: 0.9586)

==> Build succeeded in 4m32s

==> Deploying...
Starting service with 'uvicorn app.main:app --host 0.0.0.0 --port 10000'
INFO:     Uvicorn running on http://0.0.0.0:10000
INFO:     Application startup complete
==> Service is live 🎉
```

**What to watch for**:

✅ **Good signs**:
```
Successfully installed X packages
✓ Model trained successfully
uvicorn running on...
Application startup complete
```

❌ **Warning signs**:
```
ModuleNotFoundError: No module named 'app'
→ Missing __init__.py

Killed
→ Out of memory (upgrade instance or use fewer models)

Error loading models
→ Models not found (check training ran)
```

### Troubleshooting Common Issues

**Issue: Out of Memory (OOM)**

```
Building...
Training Random Forest...
Training XGBoost...
Killed
```

**Why?**: Training all 3 models uses >512 MB

**Solution 1**: Use pre-trained models
- Uncomment models in .gitignore
- Add saved_models to GitHub
- Remove training from build command

**Solution 2**: Load only Neural Network
See fix below (Step 8)

**Solution 3**: Upgrade to Standard tier

---

**Issue: Module Not Found**

```
ModuleNotFoundError: No module named 'app'
```

**Why?**: Missing `app/__init__.py`

**Solution**:
```bash
# On your local computer
cd c:\Users\ASUS\Desktop\Intership_Tasks\health-risk-profiles
echo. > app/__init__.py
git add app/__init__.py
git commit -m "Add app package init"
git push origin main
```

Render auto-redeploys after push.

---

## ✅ Step 5: Test Your Live API (5 minutes)

### Get Your URL

After deployment succeeds, Render shows:

```
Your service is live at:
https://health-risk-profiler-abcd1234.onrender.com
```

**Understanding the URL**:
- `health-risk-profiler`: Your service name
- `abcd1234`: Random identifier (prevents conflicts)
- `onrender.com`: Render's domain
- **HTTPS**: Free SSL certificate (secure) ✅

### Test Health Check

Open your browser or use curl:

```bash
curl https://health-risk-profiler-abcd1234.onrender.com/health
```

**Expected response**:
```json
{
  "status": "healthy",
  "ml_available": true
}
```

**What this means**:
- ✅ Server is running
- ✅ ML models loaded successfully
- ✅ API is responding

### Test API Documentation

Visit in browser:
```
https://health-risk-profiler-abcd1234.onrender.com/docs
```

**You'll see**: Swagger UI (interactive API docs)

**Try it**:
1. Click POST `/predict`
2. Click "Try it out"
3. Enter test data:
```json
{
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
}
```
4. Click "Execute"
5. See prediction with 91%+ confidence!

### Test All Endpoints

```bash
# Health check
curl https://YOUR-URL.onrender.com/health

# Model info
curl https://YOUR-URL.onrender.com/model-info

# ML prediction
curl -X POST "https://YOUR-URL.onrender.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"age": 55, "bmi": 32.0, "systolic_bp": 160, "cholesterol": 260, "smoker": true, "exercise": "never", "diet": "high fat", "family_history": true, "sleep_hours": 5.0, "alcohol": "heavy", "stress_level": 9}'
```

---

## 📊 Step 6: Understanding Monitoring (10 minutes)

### Render Dashboard

Click on your service to see:

**Metrics Tab**:
- CPU usage
- Memory usage
- Request rate
- Response times

**Logs Tab**:
- Real-time logs
- Every API request logged
- Error tracking

**Example Log**:
```
INFO:     127.0.0.1:45678 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:45679 - "POST /predict HTTP/1.1" 200 OK
INFO:     Prediction for age=55: high risk (confidence: 0.92)
```

**Settings Tab**:
- Environment variables
- Auto-deploy ON/OFF
- Custom domain
- Health check config

---

## 🔄 Step 7: Understanding Auto-Deploy (5 minutes)

### How it works:

```
You push to GitHub → GitHub webhook → Render detects change → Auto-rebuild → Deploy
```

**Try it**:

1. Edit README.md locally:
```markdown
## 🌐 Live Demo

**API**: https://health-risk-profiler-abcd1234.onrender.com
**Docs**: https://health-risk-profiler-abcd1234.onrender.com/docs
```

2. Commit and push:
```bash
git add README.md
git commit -m "Add live demo URL"
git push origin main
```

3. **Watch Render dashboard**:
   - Detects new commit
   - Starts rebuilding
   - ~5 minutes later: deployed!

**Blue-Green Deployment**:
- Render builds new version
- Keeps old version running
- Only switches when new version is healthy
- = Zero downtime! ✅

---

## 🛠️ Step 8: Optimization for Free Tier (15 minutes)

### Problem: Too much memory

If deployment crashes with free tier:

### Solution: Use only Neural Network (best model)

**Why?**:
- Neural Network: 95.86% accuracy (best)
- Random Forest: 88.2% accuracy
- XGBoost: 93.25% accuracy

**Trade-off**: Lose ensemble, but save ~100 MB RAM

**Edit `ml_models/risk_classifier.py`**:

```python
# Around line 26-51, modify load_models():

def load_models(self):
    """Load only Neural Network to save memory"""
    try:
        # Load only Neural Network (best model)
        nn_path = os.path.join(self.models_dir, "neural_network_latest.pkl")
        if os.path.exists(nn_path):
            self.models['neural_network'] = joblib.load(nn_path)
            logger.info("Loaded Neural Network model")
        else:
            logger.warning("Neural Network model not found")
        
        # COMMENTED OUT: Random Forest and XGBoost
        # rf_path = os.path.join(self.models_dir, "random_forest_latest.pkl")
        # if os.path.exists(rf_path):
        #     self.models['random_forest'] = joblib.load(rf_path)
        
        # xgb_path = os.path.join(self.models_dir, "xgboost_latest.pkl")
        # if os.path.exists(xgb_path):
        #     self.models['xgboost'] = joblib.load(xgb_path)
        
        # Load label encoder
        le_path = os.path.join(self.models_dir, "label_encoder.pkl")
        if os.path.exists(le_path):
            self.label_encoder = joblib.load(le_path)
            logger.info("Loaded label encoder")
```

**Edit ensemble weights (around line 111)**:

```python
# Simplified weights for single model
weights = {
    'neural_network': 1.0  # 100% weight to NN
}
```

**Commit changes**:

```bash
git add ml_models/risk_classifier.py
git commit -m "Optimize memory: use only Neural Network model"
git push origin main
```

Render auto-redeploys with lower memory usage!

---

## 🌐 Step 9: Custom Domain (Optional, 10 minutes)

### Add your own domain

**If you own a domain** (e.g., `yourdomain.com`):

1. **In Render**: Settings → Custom Domain
2. Add: `api.yourdomain.com`
3. **In your domain registrar** (Namecheap, GoDaddy):
   - Add CNAME record:
     - Host: `api`
     - Value: `health-risk-profiler-abcd1234.onrender.com`
4. **Wait 5-60 minutes** for DNS propagation
5. **Done!** Now accessible at `https://api.yourdomain.com`

**Render provides free SSL** for custom domains too!

---

## 📈 Step 10: Final Checklist & Best Practices

### ✅ Deployment Checklist

- [ ] Service deployed successfully
- [ ] `/health` returns 200 OK
- [ ] `/docs` shows Swagger UI
- [ ] `/predict` works with test data
- [ ] `/model-info` shows all models
- [ ] Logs show no errors
- [ ] README updated with live URL
- [ ] Auto-deploy tested (push triggers redeploy)

### 📝 Best Practices

**1. Environment Variables for Secrets**

Don't hardcode:
```python
# BAD
API_KEY = "abc123secret"
```

Use environment variables:
```python
# GOOD
import os
API_KEY = os.getenv("API_KEY")
```

Add in Render: Settings → Environment Variables

**2. Monitoring**

Set up monitoring:
- UptimeRobot: Ping every 14 min (prevent free tier spin-down)
- Sentry: Error tracking
- LogTail: Log aggregation

**3. Rate Limiting**

Protect API from abuse:
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/predict")
@limiter.limit("10/minute")
async def predict():
    ...
```

**4. Caching**

Cache predictions:
```python
import redis

@app.post("/predict")
async def predict(data: MLPredictionInput):
    cache_key = hash(data)
    cached = redis.get(cache_key)
    if cached:
        return cached
    
    result = model.predict(data)
    redis.set(cache_key, result, ex=3600)  # Cache 1 hour
    return result
```

---

## 🎓 Concepts You've Learned

### Cloud Deployment
- ✅ PaaS vs IaaS vs Serverless
- ✅ Build vs Start commands
- ✅ Dynamic ports (`$PORT`)
- ✅ Host binding (`0.0.0.0`)
- ✅ Environment variables
- ✅ Auto-deployment from Git

### Production Considerations
- ✅ Memory management
- ✅ Blue-green deployment
- ✅ Health checks
- ✅ Logs and monitoring
- ✅ SSL/HTTPS automatic
- ✅ Zero-downtime deploys

### DevOps Practices
- ✅ Git-based deployment
- ✅ Continuous deployment (CD)
- ✅ Infrastructure as Code (config in repo)
- ✅ Observability (logs, metrics)

---

## 🚀 You're Live!

**Congratulations!** Your ML API is now:
- 🌍 Accessible worldwide
- 🔒 Secured with HTTPS
- 📊 Monitored 24/7
- ⚡ Auto-deploying from GitHub
- 💪 Production-ready

**Share it**:
- Add to resume
- Share with recruiters
- Include in portfolio
- Demo in interviews

---

## 📚 Further Learning

### Next Steps:
1. Add PostgreSQL database (Render offers addon)
2. Implement Redis caching
3. Add monitoring (Sentry, UptimeRobot)  
4. Set up CI/CD (GitHub Actions)
5. Add authentication (JWT tokens)

### Resources:
- Render Docs: https://render.com/docs
- FastAPI Deployment: https://fastapi.tiangolo.com/deployment/
- 12 Factor App: https://12factor.net/

---

**You now understand production deployment like a pro engineer!** 🎉
