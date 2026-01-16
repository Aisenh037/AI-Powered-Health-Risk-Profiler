# Deploying to Render.com

## Prerequisites

- GitHub account with your repository
- Render account (free tier available at [render.com](https://render.com))
- Project pushed to GitHub

---

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure these files are in your repo:
- ✅ `requirements.txt`
- ✅ `Dockerfile`  
- ✅ `app/main.py`
- ✅ ML model files or training scripts

### 2. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 3. Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure service:

   **Basic Settings:**
   - **Name**: `health-risk-profiler`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your primary branch)
   - **Root Directory**: Leave blank
   - **Environment**: `Python 3`

   **Build & Deploy:**
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python ml_models/dataset_generator.py && python ml_models/model_trainer.py
     ```
   
   - **Start Command**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

   **Instance Type:**
   - Free tier (512MB RAM) - might be tight for ML models
   - Starter ($7/month, 512MB)
   - **Recommended**: Standard ($25/month, 2GB) for ML workloads

4. Click **"Create Web Service"**

### 4. Environment Variables (Optional)

If you need environment variables:

1. Go to **"Environment"** tab
2. Add variables:
   ```
   PYTHON_VERSION=3.9.18
   ```

### 5. Monitor Deployment

Watch the build logs. First deployment takes 5-10 minutes:

```
Building...
✓ Installing requirements
✓ Generating dataset
✓ Training models
✓ Starting server
🎉 Deploy successful!
```

### 6. Access Your API

Your API will be available at:
```
https://health-risk-profiler-XXXX.onrender.com
```

Test it:
```bash
curl https://health-risk-profiler-XXXX.onrender.com/health
```

API Docs:
```
https://health-risk-profiler-XXXX.onrender.com/docs
```

---

## Important Notes

### Memory Considerations

Free tier (512MB) might crash with 3 ML models. Solutions:

**Option 1**: Use only best model (Neural Network)
```python
# In risk_classifier.py, load only NN:
if os.path.exists(nn_path):
    self.models['neural_network'] = joblib.load(nn_path)
# Comment out RF and XGBoost loading
```

**Option 2**: Upgrade to Starter/Standard plan

**Option 3**: Use model quantization (advanced)

### Cold Starts

Free tier spins down after 15 min inactivity:
- First request: 30-60 seconds
- Subsequent requests: normal speed

Solution: Use [UptimeRobot](https://uptimerobot.com/) to ping every 14 minutes

### Build Time

Including model training in build:
- ✅ Pros: Models always up-to-date
- ❌ Cons: Slow builds (5-10 min)

Alternative: Pre-trained models in repo:
```bash
# Build Command (faster):
pip install -r requirements.txt

# Add saved_models/ to git (if < 100MB each)
```

---

## Alternative: Docker Deployment

If you prefer Docker on Render:

1. Select **"Docker"** as environment
2. Build Command: Leave blank
3. Render will use your `Dockerfile`

**Dockerfile should include**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate data and train models during build
RUN python ml_models/dataset_generator.py
RUN python ml_models/model_trainer.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
```

---

## Troubleshooting

### Issue: Build Fails

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**: Ensure `app/` is a package with `__init__.py`

```bash
# In app/__init__.py
# Can be empty or:
from .main import app
```

### Issue: Out of Memory

**Error**: `Killed` during model training

**Solutions**:
1. Reduce dataset size: `n_samples=5000` in dataset_generator.py
2. Use lighter models (remove Neural Network)
3. Upgrade Render plan

### Issue: Slow Start

**Error**: Health check timeout

**Solution**: Increase timeout in Render settings:
- Dashboard → Settings → Health Check Path: `/health`
- Health Check Timeout: 300 seconds (for first cold start)

### Issue: Models Not Found

**Error**: `FileNotFoundError: saved_models/ not found`

**Solution**:
1. Ensure training runs in build command
2. Check build logs for errors
3. Verify `saved_models/` directory created

---

## Monitoring

### Health Check

Render automatically monitors `/health` endpoint.

If it fails 3 times, Render restarts the service.

### Logs

View logs in real-time:
1. Go to your service dashboard
2. Click **"Logs"** tab
3. See all requests and errors

### Metrics

Available on paid plans:
- CPU usage
- Memory usage  
- Request rate
- Response times

---

## Custom Domain

### Add Your Domain

1. Buy domain (Namecheap, Google Domains, etc.)
2. In Render:
   - Go to **"Settings"** → **"Custom Domain"**
   - Add your domain (`api.yourdomain.com`)
3. Update DNS:
   - **CNAME**: `api` → `health-risk-profiler-XXXX.onrender.com`
4. SSL auto-configured by Render ✅

---

## CI/CD with GitHub

Render auto-deploys on git push:

1. Push to `main` branch
2. Render detects change
3. Automatically rebuilds and deploys
4. Zero downtime (blue-green deployment)

**Disable auto-deploy**:
Settings → Auto-Deploy → Off

**Manual deploy**:
Click "Manual Deploy" → "Deploy latest commit"

---

## Cost Optimization

### Free Tier Limits
- 750 hours/month free (enough for 1 service running 24/7)
- Spins down after 15 min inactivity
- 100GB bandwidth/month

### Tips
1. Use only necessary models (1 instead of 3)
2. Cache predictions (Redis)
3. Reduce dataset size in training
4. Use pre-trained models (skip training in build)

---

## Alternative Platforms

If Render doesn't work:

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Railway** | $5 credit | Easy, fast | Credit runs out |
| **Fly.io** | 3 VMs free | Great for small apps | Complex config |
| **Heroku** | $7/month min | Popular | No free tier anymore |
| **AWS EC2** | 12 months free | Full control | Complex setup |
| **Google Cloud Run** | Always free tier | Serverless, scales to 0 | Cold starts |

---

## Success Checklist

Before going public:

- [ ] Models trained successfully
- [ ] All endpoints working (`/health`, `/predict`, `/model-info`)
- [ ] API docs accessible at `/docs`
- [ ] Response times acceptable (<2 seconds)
- [ ] Error handling tested
- [ ] README updated with live URL
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] GitHub repo public

---

## Live Example

After deployment, update README:

```markdown
## 🌐 Live Demo

API Base URL: https://health-risk-profiler.onrender.com

Try it:
- Health Check: https://health-risk-profiler.onrender.com/health
- Interactive Docs: https://health-risk-profiler.onrender.com/docs
```

---

**Deployment Time**: 10-15 minutes  
**Difficulty**: ⭐⭐⚪⚪⚪ (Easy)  
**Cost**: Free to $25/month depending on tier

🎉 **Your ML API is now live and accessible worldwide!**
