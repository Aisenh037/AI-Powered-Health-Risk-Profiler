# GitHub Setup and Push Guide

## Prerequisites

- Git installed on your system
- GitHub account created
- Project is ready to push

---

## Step 1: Initialize Git Repository

Open terminal in your project directory and run:

```bash
cd c:\Users\ASUS\Desktop\Intership_Tasks\health-risk-profiles

# Initialize git (if not already initialized)
git init

# Check status
git status
```

---

## Step 2: Create GitHub Repository

### Option A: Via GitHub Website

1. Go to [github.com](https://github.com)
2. Click **"+"** → **"New repository"**
3. Settings:
   - **Repository name**: `AI-Health-Risk-Profiler` or `health-risk-profiler`
   - **Description**: `ML-powered health risk assessment with 95.86% accuracy using ensemble learning`
   - **Visibility**: Public (for portfolio/resume)
   - **Initialize**: ❌ Do NOT add README, .gitignore, or license (we have them)
4. Click **"Create repository"**

### Option B: Via GitHub CLI (if installed)

```bash
gh repo create AI-Health-Risk-Profiler --public --description "ML-powered health risk profiler"
```

---

## Step 3: Clean Up Unnecessary Files

### Remove These Directories/Files:

```bash
# Remove test artifacts
del test_results.json
rmdir /s ".gemini"

# Remove temporary files
del *.tmp
del *.log
```

### What to Keep:

✅ **Essential Files:**
```
app/
ml_models/
tests/
data/.gitkeep
saved_models/         # Keep models OR train during deployment
docs/
requirements.txt
Dockerfile
docker-compose.yml
README.md
.gitignore
TESTING_GUIDE.md
ENHANCEMENT_ROADMAP.md
PROJECT_SHOWCASE.md
```

❌ **Don't Commit:**
- `__pycache__/` - Cached Python files
- `.venv/` or `venv/` - Virtual environment
- `.idea/`, `.vscode/` - IDE settings
- `*.log` - Log files
- Test artifacts - `.png`, `.webp`

---

## Step 4: Stage Files for Commit

```bash
# Add all files (respects .gitignore)
git add .

# Or add specific files/folders
git add app/
git add ml_models/
git add requirements.txt
git add README.md
git add Dockerfile
git add docker-compose.yml
git add docs/
git add tests/
git add .gitignore

# Check what will be committed
git status
```

**You should see**:
```
Changes to be committed:
  new file:   app/main.py
  new file:   ml_models/dataset_generator.py
  new file:   requirements.txt
  ...
```

---

## Step 5: Create Initial Commit

```bash
git commit -m "Initial commit: ML-powered health risk profiler

- Ensemble ML models (RF, XGBoost, Neural Network) with 95.86% accuracy
- FastAPI REST API with 4 endpoints
- Comprehensive testing suite
- Docker deployment configuration
- Full documentation for development and learning"
```

---

## Step 6: Connect to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/AI-Health-Risk-Profiler.git

# Verify remote
git remote -v
```

**Expected output:**
```
origin  https://github.com/YOUR_USERNAME/AI-Health-Risk-Profiler.git (fetch)
origin  https://github.com/YOUR_USERNAME/AI-Health-Risk-Profiler.git (push)
```

---

## Step 7: Push to GitHub

```bash
# Rename branch to main (if currently master)
git branch -M main

# Push code
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use **Personal Access Token** (NOT your GitHub password)

### Creating Personal Access Token:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control of private repositories)
4. Copy token (save it somewhere safe!)
5. Use token as password when pushing

---

## Step 8: Verify Upload

1. Go to `https://github.com/YOUR_USERNAME/AI-Health-Risk-Profiler`
2. You should see all your files
3. README.md should display nicely

---

## Step 9: Add Topics/Tags

On GitHub repository page:

1. Click **⚙️ (settings gear)** next to "About"
2. Add topics:
   ```
   machine-learning
   fastapi
   ensemble-learning
   health-tech
   neural-networks
   xgboost
   python
   api
   explainable-ai
   docker
   ```
3. Save changes

---

## Step 10: Create Releases (Optional but Professional)

```bash
# Tag your first release
git tag -a v1.0.0 -m "Release v1.0.0: Production-ready ML health risk profiler"
git push origin v1.0.0
```

On GitHub:
1. Go to **"Releases"**
2. Click **"Draft a new release"**
3. Settings:
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Production Release`
   - Description:
     ```markdown
     ## Features
     - ✅ 95.86% accuracy ensemble ML model
     - ✅ FastAPI REST API
     - ✅ Explainable AI with feature importance
     - ✅ Docker deployment
     - ✅ Comprehensive documentation

     ## What's Included
     - 3 trained models (Random Forest, XGBoost, Neural Network)
     - 10,000 sample synthetic dataset
     - Automated test suite
     - Deployment guides for Render, Railway, Docker
     ```
4. Click **"Publish release"**

---

## File Structure That Will Be Pushed

```
AI-Health-Risk-Profiler/
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── services.py
├── ml_models/
│   ├── __init__.py
│   ├── dataset_generator.py
│   ├── model_trainer.py
│   └── risk_classifier.py
├── tests/
│   ├── __init__.py
│   └── test_api_comprehensive.py
├── data/
│   ├── .gitkeep
│   └── processed/
│       └── .gitkeep
├── saved_models/          # Optional: Include or train during deployment
│   ├── *.pkl
│   └── training_results.json
└── docs/
    ├── DEPLOYMENT.md
    ├── TESTING_GUIDE.md
    ├── ENHANCEMENT_ROADMAP.md
    ├── PROJECT_SHOWCASE.md
    └── MANUAL_TEST_RESULTS.md
```

---

## Model Files Decision

### Option 1: Include Models in Repo (Easier Setup)

**Pros:**
- Users can immediately run predictions
- No training needed
- Faster deployment

**Cons:**
- Large files (~150MB total)
- Repo size increases
- Git LFS recommended for files >50MB

**How:**
```bash
# Ensure saved_models/ is NOT in .gitignore
git add saved_models/
git commit -m "Add pre-trained models"
git push
```

### Option 2: Train During Setup (Reproducible)

**Pros:**
- Smaller repo size
- Users learn complete pipeline
- Reproducible training

**Cons:**
- Longer setup time (5 min)
- Requires computational resources

**How:**
```bash
# Ensure saved_models/ is in .gitignore
# Users run:
python ml_models/dataset_generator.py
python ml_models/model_trainer.py
```

**Recommended:** Option 2 (train during setup) for learning projects

---

## Troubleshooting

### Issue: Large Files

```
error: failed to push some refs
file is 128MB; this exceeds GitHub's file size limit of 100.00 MB
```

**Solution:**

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "saved_models/*.pkl"
git add .gitattributes
git commit -m "Track model files with Git LFS"
git push
```

Or exclude models:
```bash
# Add to .gitignore:
echo "saved_models/*.pkl" >> .gitignore
```

### Issue: Authentication Failed

**Solution:** Use Personal Access Token, not password

### Issue: Files Not Ignored

Check `.gitignore` is correct and run:
```bash
git rm -r --cached .
git add .
git commit -m "Fix .gitignore"
git push
```

---

## Best Practices

### Commit Messages

**Good:**
```
✅ "Add SHAP explainability feature"
✅ "Fix memory leak in model loading"
✅ "Update docs with deployment guide"
```

**Bad:**
```
❌ "Update"
❌ "Fix bug"
❌ "Changes"
```

### Branch Strategy

For solo project:
```bash
# Main branch for stable code
git checkout -b main

# Feature branches for experiments
git checkout -b feature/shap-integration
git checkout -b feature/react-dashboard
```

### Regular Commits

```bash
# Commit working changes frequently
git add .
git commit -m "Descriptive message"
git push
```

---

## Adding Collaborators

If working in a team:

1. Repository page → **Settings** → **Collaborators**
2. Add collaborators by username/email
3. They can now push to your repo

---

## GitHub Actions (CI/CD) - Optional

Create `.github/workflows/tests.yml`:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python tests/test_api_comprehensive.py
```

This automatically runs tests on every push!

---

## Success Checklist

- [ ] Repository created on GitHub
- [ ] All relevant files committed
- [ ] Pushed to `main` branch successfully
- [ ] README displays correctly on GitHub
- [ ] Topics/tags added
- [ ] No sensitive data committed (.env, keys)
- [ ] `.gitignore` working properly
- [ ] Repository is public (for portfolio)

---

**🎉 Your project is now on GitHub and ready to share!**

**Repository URL**: `https://github.com/YOUR_USERNAME/AI-Health-Risk-Profiler`

**Next Step**: Deploy to Render using `docs/DEPLOYMENT.md`
