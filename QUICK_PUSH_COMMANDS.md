# Quick Commands to Push to GitHub

## ⚠️ IMPORTANT: Check Before Pushing!

**NEVER commit these files:**
- `.env` (contains your API keys!)
- `venv/` (virtual environment)
- `data/` (data files)
- Personal resume/PDF files

## Quick Commands (Copy & Paste)

Run these commands in your WSL terminal:

```bash
# 1. Navigate to project directory
cd /mnt/c/Users/sarat/OneDrive/Documents/self_learning/RAG/RAG

# 2. Check current status
git status

# 3. Make sure .env is NOT in the list! If it is, skip step 4 and fix it first.

# 4. Add all files (respects .gitignore)
git add .

# 5. Verify .env is NOT staged (run this and make sure .env is NOT listed)
git status

# 6. Commit with a message
git commit -m "Initial commit: My Personal Agent RAG application

Features:
- Core RAG engine with ChromaDB
- Vehicle diagnostics with vision AI
- Resume analyzer with ATS optimization
- Resume builder
- User authentication
- CLI interface
- Comprehensive documentation"

# 7. Push to GitHub (if remote is already set up)
git push origin main

# OR if you need to set up remote first:
# git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
# git push -u origin main
```

## If .env Accidentally Gets Staged

If you see `.env` in `git status`, remove it:

```bash
# Remove from staging
git reset HEAD .env

# Verify it's removed
git status
```

## Create New GitHub Repository

If you need to create a new repository:

1. Go to https://github.com/new
2. Repository name: `my-personal-agent` (or your choice)
3. Description: "A RAG-based personal AI assistant for vehicle diagnostics and resume optimization"
4. Choose Public or Private
5. **DO NOT** initialize with README, .gitignore, or license (you already have these)
6. Click "Create repository"
7. Then run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/my-personal-agent.git
git push -u origin main
```

## Verify Everything is Pushed

After pushing, visit your GitHub repository and verify:
- ✅ All source code files are there
- ✅ Documentation is there
- ❌ `.env` file is NOT there
- ❌ `venv/` directory is NOT there
- ❌ `data/` directory is NOT there

## What Should Be on GitHub

✅ **Should be committed:**
- `src/` - All source code
- `docs/` - Documentation
- `tests/` - Tests
- `examples/` - Example files (but maybe not personal resumes)
- `README.md`, `QUICKSTART.md`, etc.
- `requirements.txt`
- `setup.py`
- `LICENSE`
- `env.example` (template, no real keys)
- `.gitignore`

❌ **Should NOT be committed:**
- `.env` - Contains API keys
- `venv/` - Virtual environment
- `data/` - Data files
- `resume/` - Personal files (already in .gitignore)
- `jds/` - Personal job descriptions (already in .gitignore)
- `*.pdf` - Personal documents (already in .gitignore)

