#!/bin/bash
# Quick script to push project to GitHub
# Run this from the RAG directory

echo "🚀 Preparing to push My Personal Agent to GitHub..."
echo ""

# Check if .env exists and warn
if [ -f .env ]; then
    echo "⚠️  WARNING: .env file found!"
    echo "   Make sure .env is in .gitignore (it should NOT be committed)"
    read -p "   Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check git status
echo "📊 Current git status:"
git status --short
echo ""

# Check if .env is staged (it shouldn't be!)
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "❌ ERROR: .env file is staged for commit!"
    echo "   Removing .env from staging..."
    git reset HEAD .env
    echo "✅ Removed .env from staging"
    echo ""
fi

# Add all files (respecting .gitignore)
echo "📦 Adding files to git..."
git add .
echo ""

# Show what will be committed
echo "📋 Files staged for commit:"
git status --short
echo ""

# Ask for confirmation
read -p "📝 Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial commit: My Personal Agent RAG application

- Core RAG engine with ChromaDB vector store
- Vehicle diagnostics module with vision AI  
- Resume analyzer with ATS optimization
- Resume builder with job-specific optimization
- User authentication system
- CLI interface
- Comprehensive documentation"
fi

# Commit
echo ""
echo "💾 Committing changes..."
git commit -m "$commit_msg"

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    echo ""
    echo "🔗 Remote 'origin' exists"
    echo "📤 Pushing to GitHub..."
    git push origin main
    echo ""
    echo "✅ Successfully pushed to GitHub!"
else
    echo ""
    echo "⚠️  No remote 'origin' configured"
    echo "   To add a remote repository:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git"
    echo "   git push -u origin main"
fi

echo ""
echo "✨ Done!"

