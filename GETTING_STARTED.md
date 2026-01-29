# Getting Started with My Personal Agent

Welcome! This guide will help you understand and use your new RAG application.

## 📚 Documentation Overview

Your project includes comprehensive documentation:

1. **README.md** - Main project overview and features
2. **QUICKSTART.md** - Fast setup instructions
3. **PROJECT_SUMMARY.md** - High-level project summary for portfolio
4. **docs/architecture.md** - Detailed system architecture
5. **docs/api_reference.md** - API documentation
6. **docs/CODEBASE_WALKTHROUGH.md** - Detailed code explanation

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Environment

1. Copy the example environment file:
```bash
cp env.example .env
```

2. Edit `.env` and add your OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-key-here
SECRET_KEY=your-random-secret-key-here
```

3. Generate a secret key (optional):
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Test Installation

```bash
python -m src.my_personal_agent.cli --help
```

If you see the help message, you're ready to go! 🎉

## 📖 Understanding the Project Structure

```
RAG/
├── src/my_personal_agent/    # Main application code
│   ├── core/                  # RAG engine (the brain)
│   │   ├── rag_engine.py      # Main RAG logic
│   │   ├── vector_store.py    # Vector database (ChromaDB)
│   │   └── llm_client.py      # LLM API clients (OpenAI/Anthropic)
│   ├── modules/               # Feature modules
│   │   ├── vehicle_diagnostics.py    # Car diagnostics
│   │   ├── resume_analyzer.py        # Resume analysis
│   │   └── resume_builder.py         # Resume generation
│   ├── utils/                 # Helper utilities
│   │   ├── file_handler.py    # File operations
│   │   └── text_processor.py  # Text analysis
│   ├── auth/                  # User authentication
│   ├── config.py              # Configuration management
│   └── cli.py                 # Command-line interface
├── tests/                     # Unit tests
├── docs/                      # Documentation
├── examples/                  # Example files
└── data/                      # Data storage (auto-created)
```

## 🎯 Three Main Features Explained

### 1. Vehicle Diagnostics

**What it does**: Analyzes car dashboard images using AI vision and provides solutions.

**How to use**:
```bash
python -m src.my_personal_agent.cli vehicle \
    --image path/to/your/dashboard.jpg \
    --description "Car won't start, lights are dim"
```

**What happens**:
1. Image is analyzed using GPT-4 Vision or Claude Vision
2. AI identifies the issue (e.g., dead battery)
3. Provides step-by-step solution
4. Suggests emergency contacts (AAA, etc.)

**Use case**: Your car stops, you take a dashboard photo, get instant diagnosis and help!

### 2. Resume Analysis

**What it does**: Compares your resume against a job description and provides ATS optimization feedback.

**How to use**:
```bash
python -m src.my_personal_agent.cli analyze-resume \
    --resume my_resume.pdf \
    --job-description "We are looking for a Software Engineer..."
```

**What happens**:
1. Resume and job description are analyzed
2. Keywords are matched
3. Skills are compared
4. ATS compatibility score is calculated (0-100)
5. Specific recommendations are provided

**Use case**: Before applying to a job, optimize your resume to pass ATS systems!

### 3. Resume Builder

**What it does**: Generates an ATS-optimized resume from your experiences, skills, and portfolio.

**How to use**:

1. Create a JSON file (see `examples/resume_data_example.json`):
```json
{
  "experiences": [
    {
      "title": "Software Engineer",
      "company": "Tech Corp",
      "duration": "2020-2024",
      "description": "Developed web applications..."
    }
  ],
  "skills": ["Python", "JavaScript", "React"],
  "education": [
    {
      "degree": "BS Computer Science",
      "institution": "University",
      "year": "2020"
    }
  ],
  "target_job": "Software Engineer position..."
}
```

2. Run the builder:
```bash
python -m src.my_personal_agent.cli build-resume \
    --input-file my_data.json \
    --format docx
```

**What happens**:
1. Data is processed and optimized for target job (if provided)
2. Professional summary is generated using AI
3. Formatted resume is created (DOCX or TXT)
4. Saved to `data/outputs/`

**Use case**: Build a tailored resume for each job application automatically!

## 🔧 How the RAG System Works

**RAG = Retrieval-Augmented Generation**

1. **Knowledge Base**: Documents are stored as embeddings in ChromaDB
2. **Query**: User asks a question
3. **Retrieval**: System finds relevant documents using similarity search
4. **Augmentation**: Retrieved context is added to the query
5. **Generation**: LLM generates answer using context + query

**Why RAG?**: 
- More accurate than LLM alone
- Can use your own documents/knowledge
- Provides sources for answers
- Reduces hallucination

## 🎓 Key Concepts to Understand

### Vector Store (ChromaDB)
- Stores text as numerical vectors (embeddings)
- Enables semantic search (finds similar meaning, not just keywords)
- Think of it as the "memory" of your AI

### LLM Client
- Abstraction over different AI providers (OpenAI, Anthropic)
- Handles API calls, error handling, formatting
- Makes it easy to switch providers

### Embeddings
- Convert text to numbers that capture meaning
- Similar texts have similar embeddings
- Used for finding relevant documents

### ATS (Applicant Tracking System)
- Software used by companies to filter resumes
- Looks for keywords and formatting
- Your resume needs to be ATS-friendly to pass screening

## 🔐 Authentication (Optional)

The system includes user authentication:

```bash
# Register
python -m src.my_personal_agent.cli auth register \
    --username myuser \
    --password mypass \
    --email my@email.com

# Login
python -m src.my_personal_agent.cli auth login \
    --username myuser \
    --password mypass
```

Files are organized by user ID when authenticated.

## 📝 Example Workflows

### Workflow 1: Car Trouble

```bash
# 1. Take photo of dashboard
# 2. Run diagnostics
python -m src.my_personal_agent.cli vehicle \
    --image dashboard.jpg \
    --description "Car won't start"

# 3. Follow the step-by-step instructions
# 4. Call AAA if needed (contact info provided)
```

### Workflow 2: Job Application

```bash
# 1. Analyze current resume
python -m src.my_personal_agent.cli analyze-resume \
    --resume current_resume.pdf \
    --job-description job.txt \
    --output analysis.json

# 2. Review recommendations
# 3. Build optimized resume
python -m src.my_personal_agent.cli build-resume \
    --input-file updated_resume_data.json \
    --format docx

# 4. Submit optimized resume!
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Make sure `.env` file exists in project root
- Check that it contains `OPENAI_API_KEY=sk-...`

### "ModuleNotFoundError"
- Activate your virtual environment
- Run `pip install -r requirements.txt`

### "ChromaDB connection error"
- The `data/` directory will be created automatically
- Check file permissions if issues persist

### Import errors
- Make sure you're running from the project root
- Use `python -m src.my_personal_agent.cli` (not `python cli.py`)

## 🎯 Next Steps

1. **Try Each Feature**: Run all three main features with sample data
2. **Read the Code**: Start with `core/rag_engine.py` to understand RAG
3. **Modify & Experiment**: Add your own features or improvements
4. **Add to GitHub**: This project is ready to publish!

## 💡 Tips for Portfolio

When showcasing this project:

1. **Highlight the RAG Architecture**: Explain how retrieval + generation works
2. **Show Real Examples**: Use actual resume analysis or vehicle diagnostics
3. **Demonstrate AI Integration**: Show OpenAI/Anthropic API usage
4. **Explain Use Cases**: Why each feature is valuable
5. **Mention Scalability**: How it could be extended (web UI, cloud deployment)

## 📚 Learning Resources

To deepen your understanding:

- **RAG**: Read about retrieval-augmented generation
- **Vector Databases**: Learn about embeddings and similarity search
- **LLM APIs**: OpenAI and Anthropic documentation
- **Document Processing**: PyPDF2, python-docx libraries

## 🤝 Contributing to Yourself

This is your project! Ideas for enhancements:

- Add web interface (Streamlit or FastAPI)
- Support more file formats
- Add more LLM providers
- Improve ATS scoring algorithm
- Add resume templates
- Build knowledge base management UI

## ✅ Checklist

- [ ] Installed dependencies
- [ ] Configured .env file
- [ ] Tested CLI help command
- [ ] Tried vehicle diagnostics (if you have a car image)
- [ ] Tested resume analysis (if you have a resume)
- [ ] Read the architecture documentation
- [ ] Understood the code structure
- [ ] Ready to customize and extend!

---

**Happy coding! 🚀**

Remember: This is a portfolio-worthy project that demonstrates:
- AI/ML engineering (RAG, embeddings, LLMs)
- Software architecture (clean code, modularity)
- Practical problem-solving (real-world use cases)
- Professional development (documentation, structure)

You've built something impressive! Now make it your own. 💪

