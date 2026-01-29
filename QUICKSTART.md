# Quick Start Guide

Get up and running with My Personal Agent in minutes!

## Prerequisites

- Python 3.9 or higher
- OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation Steps

### 1. Clone or Navigate to Project

```bash
cd RAG
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp env.example .env

# Edit .env and add your API key
OPENAI_API_KEY=sk-your-actual-api-key-here
SECRET_KEY=generate-a-random-secret-key-here
```

**Generate a secret key** (optional but recommended):
```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Verify Installation

```bash
python -m src.my_personal_agent.cli --help
```

## Usage Examples

### Example 1: Vehicle Diagnostics

1. Take a photo of your car dashboard when there's an issue
2. Save it as `car_issue.jpg`
3. Run:

```bash
python -m src.my_personal_agent.cli vehicle \
    --image car_issue.jpg \
    --description "Car won't start, dashboard lights are dim"
```

### Example 2: Resume Analysis

1. Have your resume ready (PDF, DOCX, or TXT)
2. Have a job description ready
3. Run:

```bash
# If job description is in a file
python -m src.my_personal_agent.cli analyze-resume \
    --resume my_resume.pdf \
    --job-description job_description.txt

# If job description is text
python -m src.my_personal_agent.cli analyze-resume \
    --resume my_resume.pdf \
    --job-description "We are looking for a Software Engineer with Python experience..."
```

### Example 3: Build a Resume

1. Create a JSON file with your information (see `examples/resume_data_example.json`)
2. Run:

```bash
python -m src.my_personal_agent.cli build-resume \
    --input-file my_resume_data.json \
    --format docx
```

The generated resume will be saved in `data/outputs/resume.docx`

## Common Issues

### Issue: "OPENAI_API_KEY not found"

**Solution**: Make sure your `.env` file is in the project root and contains:
```
OPENAI_API_KEY=sk-your-key-here
```

### Issue: "ModuleNotFoundError"

**Solution**: Make sure you're in the virtual environment and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "ChromaDB connection error"

**Solution**: The vector database directory will be created automatically. If issues persist, check write permissions for the `data/` directory.

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [docs/architecture.md](docs/architecture.md) to understand the system design
- See [docs/api_reference.md](docs/api_reference.md) for API documentation
- Explore the example files in the `examples/` directory

## Getting Help

- Check the documentation in the `docs/` folder
- Review example files in the `examples/` folder
- Open an issue on GitHub if you encounter bugs

Happy using! 🚀

