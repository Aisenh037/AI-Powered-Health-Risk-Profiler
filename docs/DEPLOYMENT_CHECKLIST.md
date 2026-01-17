# Quick Deployment Checklist

## ✅ GitHub Push - COMPLETE!

Your repository is live at:
**https://github.com/Aisenh037/AI-Powered-Health-Risk-Profiler**

---

## 🚀 Next: Deploy to Render.com

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Click "Get Started"
3. Sign up with GitHub
4. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click **"New +"** → **"Web Service"**
2. Find and select: `Aisenh037/AI-Powered-Health-Risk-Profiler`
3. Click "Connect"

### Step 3: Configure Service

**Basic Settings:**
```
Name: health-risk-profiler
Region: Oregon (US West) or closest to you
Branch: main
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command:
pip install -r requirements.txt && python ml_models/dataset_generator.py && python ml_models/model_trainer.py

Start Command:
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
- ⚠️ Free tier (512MB) - Will likely crash with 3 ML models
- ✅ **Recommended**: Starter ($7/month, 512MB) or Standard ($25/month, 2GB)

### Step 4: Deploy!
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for first deployment
3. Watch build logs for progress

### Step 5: Test Your Live API

Once deployed, you'll get a URL like:
```
https://health-risk-profiler-XXXX.onrender.com
```

Test it:
```bash
# Health check
curl https://health-risk-profiler-XXXX.onrender.com/health

# API docs
https://health-risk-profiler-XXXX.onrender.com/docs
```

---

## 💡 Important Notes

### Memory Issue on Free Tier

If free tier crashes, **quick fix**:

Edit `ml_models/risk_classifier.py` to load only Neural Network:

```python
# Load only best model to save memory
def load_models(self):
    try:
        # Load only Neural Network (best performing)
        nn_path = os.path.join(self.models_dir, "neural_network_latest.pkl")
        if os.path.exists(nn_path):
            self.models['neural_network'] = joblib.load(nn_path)
            logger.info("Loaded Neural Network model")
        
        # Comment out RF and XGBoost
        # rf_path = ...
        # xgb_path = ...
        
        # ... rest of code
```

Then adjust ensemble:
```python
# In predict() method
# weights = {'neural_network': 1.0}  # 100% weight to NN
ensemble_proba = probabilities['neural_network']
```

Commit and push the change - Render will auto-redeploy.

### Cold Starts (Free Tier)

Free tier spins down after 15 minutes:
- Solution: Use [UptimeRobot](https://uptimerobot.com/) to ping every 14 minutes

---

## 🎯 Alternative: Railway.app (Easier)

If Render is too complex:

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select `AI-Powered-Health-Risk-Profiler`
5. Railway auto-detects Python and deploys!

**Pros:**
- Easier setup
- $5 free credit
- Deploy in 2 clicks

**Cons:**
- Credit runs out
- Need to add payment after trial

---

## 📝 After Deployment

### Update README with Live URL

Add to top of README.md:
```markdown
## 🌐 Live Demo

**API Base URL**: https://health-risk-profiler-XXXX.onrender.com

**Try it:**
- Health Check: [/health](https://health-risk-profiler-XXXX.onrender.com/health)
- API Docs: [/docs](https://health-risk-profiler-XXXX.onrender.com/docs)
- Model Info: [/model-info](https://health-risk-profiler-XXXX.onrender.com/model-info)
```

Then commit and push:
```bash
git add README.md
git commit -m "Add live deployment URL"
git push origin main
```

---

## 🎉 Success Checklist

- [x] ✅ Code pushed to GitHub
- [ ] Render account created
- [ ] Web service configured
- [ ] First deployment successful
- [ ] API accessible publicly
- [ ] Health check endpoint working
- [ ] README updated with live URL
- [ ] Tested all endpoints

---

## 🆘 Troubleshooting

### Build Fails

**Error**: `No module named 'app'`

**Solution**: Verify `app/__init__.py` exists. If not:
```bash
# Create it (can be empty)
echo. > app/__init__.py
git add app/__init__.py
git commit -m "Add app package init"
git push
```

### Out of Memory

**Error**: `Killed` during training

**Solutions**:
1. Load only Neural Network model (see above)
2. Reduce dataset: `n_samples=5000` in dataset_generator.py
3. Upgrade to paid tier

### Cannot Access API

**Error**: 503 Service Unavailable

**Check**:
1. Render dashboard → Logs tab
2. Look for errors in logs
3. Verify `/health` endpoint returns 200

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **GitHub Issues**: Open issue in your repo
- **Status**: Check Render status page

---

**Estimated Time**: 
- Render setup: 15 minutes
- First deployment: 5-10 minutes
- Testing: 5 minutes

**Total**: ~30 minutes to go live! 🚀
