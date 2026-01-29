# Codebase Walkthrough

This document provides a detailed explanation of how the My Personal Agent codebase is organized and how all components work together.

## Table of Contents

1. [Entry Points](#entry-points)
2. [Configuration System](#configuration-system)
3. [Core RAG Components](#core-rag-components)
4. [Feature Modules](#feature-modules)
5. [Utilities](#utilities)
6. [Authentication](#authentication)
7. [CLI Interface](#cli-interface)
8. [Data Flow Examples](#data-flow-examples)

## Entry Points

### `src/main.py`

The main entry point that simply imports and runs the CLI:

```python
from src.my_personal_agent.cli import main
if __name__ == "__main__":
    main()
```

This allows the application to be run as:
```bash
python src/main.py
# or
python -m src.my_personal_agent.cli
```

### `src/my_personal_agent/cli.py`

The command-line interface that handles user interactions. It:
- Parses command-line arguments using `argparse`
- Routes commands to appropriate handlers
- Provides user-friendly output formatting
- Manages authentication state

**Key Classes**:
- `PersonalAgentCLI`: Main CLI class that orchestrates all modules

## Configuration System

### `src/my_personal_agent/config.py`

Centralized configuration management using Pydantic settings:

**Purpose**: Loads all configuration from environment variables and provides type-safe access throughout the application.

**Key Features**:
- Validates required environment variables
- Provides defaults for optional settings
- Creates necessary directories on initialization
- Supports `.env` file loading

**Important Settings**:
- `openai_api_key`: Required for LLM operations
- `secret_key`: Required for authentication
- `vector_db_path`: Where ChromaDB stores data
- `default_llm_provider`: Which LLM to use by default
- Feature flags for enabling/disabling features

## Core RAG Components

### 1. `core/llm_client.py`

**Purpose**: Abstraction layer for multiple LLM providers.

**Key Classes**:

#### `BaseLLMClient` (Abstract)
Defines the interface that all LLM clients must implement:
- `chat_completion()`: Standard text generation
- `vision_completion()`: Image + text generation
- `get_embeddings()`: Text embedding generation

#### `OpenAILLMClient`
Implements OpenAI API:
- Uses `openai` library
- Supports GPT-4, GPT-4 Vision
- Handles embeddings with `text-embedding-3-small`

#### `AnthropicLLMClient`
Implements Anthropic Claude API:
- Uses `anthropic` library
- Supports Claude 3 Opus with vision
- Note: Anthropic doesn't provide embeddings API

#### `LLMClient` (Wrapper)
Unified interface that:
- Initializes both providers
- Routes calls to the active provider
- Always uses OpenAI for embeddings (since Anthropic doesn't provide them)

**Design Pattern**: Strategy pattern - easy to add new providers without changing application code.

### 2. `core/vector_store.py`

**Purpose**: Manages document embeddings and similarity search.

**Key Class**: `VectorStore`

**How it works**:
1. Uses ChromaDB as the underlying storage
2. Takes text documents and generates embeddings using LLM client
3. Stores embeddings with metadata
4. Provides similarity search functionality

**Key Methods**:
- `add_documents()`: Add texts to the vector store (generates embeddings)
- `search()`: Find similar documents to a query
- `get_collection_info()`: Get statistics about stored documents

**Storage**: ChromaDB uses a persistent client, so data survives application restarts.

### 3. `core/rag_engine.py`

**Purpose**: Combines retrieval (vector store) with generation (LLM).

**Key Class**: `RAGEngine`

**How RAG Works**:
1. **Query Phase**: User asks a question
2. **Retrieval Phase**: Vector store finds relevant documents
3. **Context Building**: Retrieved documents are formatted as context
4. **Generation Phase**: LLM generates answer using context + question

**Key Methods**:
- `query()`: Standard RAG query with text
- `vision_query()`: Vision-based query (no retrieval, direct image analysis)
- `add_knowledge()`: Add documents to the knowledge base

**Example Flow**:
```
User Question: "What is machine learning?"
  ↓
RAGEngine.query()
  ↓
VectorStore.search() → Finds relevant docs about ML
  ↓
Build context: "Context: [retrieved docs]\n\nQuestion: What is machine learning?"
  ↓
LLMClient.chat_completion() → Generates answer
  ↓
Return answer + sources
```

## Feature Modules

### 1. `modules/vehicle_diagnostics.py`

**Purpose**: Analyze vehicle dashboard images and provide solutions.

**Key Class**: `VehicleDiagnostics`

**Workflow**:
1. Takes image path and optional description
2. Uses `RAGEngine.vision_query()` to analyze image
3. Post-processes LLM response to extract:
   - Diagnosis
   - Recommended actions
   - Safety warnings
4. Adds emergency contact information if needed
5. Provides detailed step-by-step solutions

**Emergency Contacts**: Hardcoded list of roadside assistance providers (AAA, etc.) that are suggested based on the diagnosis.

**Solution Generation**: For common issues (battery, tires), provides detailed step-by-step instructions.

### 2. `modules/resume_analyzer.py`

**Purpose**: Analyze resume against job description with ATS optimization.

**Key Class**: `ResumeAnalyzer`

**Analysis Pipeline**:

1. **Text Extraction**: Uses `FileHandler` to extract text from resume PDF/DOCX
2. **Keyword Matching**: Uses `TextProcessor` to compare keywords between resume and JD
3. **Skill Extraction**: Extracts skills from both documents
4. **LLM Analysis**: Uses RAG engine for detailed, nuanced feedback
5. **ATS Scoring**: Calculates compatibility score (0-100) based on:
   - Keyword match (40% weight)
   - Skill match (30% weight)
   - Section presence (20% weight)
   - Format quality (10% weight)
6. **Recommendations**: Generates actionable improvement suggestions

**Output Structure**:
- ATS score and status
- Keyword analysis (common, missing, extra)
- Skills analysis (match percentage, missing skills)
- Detailed LLM feedback
- Specific recommendations

### 3. `modules/resume_builder.py`

**Purpose**: Generate ATS-optimized resumes from structured data.

**Key Class**: `ResumeBuilder`

**Building Process**:

1. **Input Processing**: Takes structured JSON with:
   - Experiences (title, company, duration, description)
   - Skills (list of strings)
   - Education (degree, institution, year, details)
   - Portfolio items (optional)
   - Target job description (optional)

2. **Optimization** (if target job provided):
   - Uses LLM to optimize content for the specific job
   - Suggests keyword additions
   - Highlights relevant experiences

3. **Summary Generation**:
   - Uses LLM to generate professional summary
   - Based on experiences, skills, and target job

4. **Document Creation**:
   - `_create_docx_resume()`: Creates formatted DOCX using `python-docx`
   - `_create_txt_resume()`: Creates plain text version
   - Applies professional formatting

**Output**: Saves resume file and returns metadata.

## Utilities

### 1. `utils/file_handler.py`

**Purpose**: Handle file operations for documents.

**Key Class**: `FileHandler`

**Capabilities**:
- Extract text from PDF, DOCX, TXT files
- Save uploaded files with user organization
- Generate output files (TXT, DOCX)
- Manage upload and output directories

**Text Extraction**:
- PDF: Uses `pdfplumber` (preferred) with `PyPDF2` fallback
- DOCX: Uses `python-docx` to extract text from paragraphs and tables
- TXT: Direct file reading

### 2. `utils/text_processor.py`

**Purpose**: Text analysis and processing utilities.

**Key Class**: `TextProcessor` (static methods)

**Key Methods**:
- `extract_keywords()`: Extract keywords, filtering stop words
- `extract_skills()`: Identify technical skills in text
- `calculate_keyword_match()`: Compare keyword overlap between texts
- `extract_sections()`: Parse resume into sections (Experience, Education, etc.)

**Use Cases**:
- Resume analysis keyword matching
- Skill extraction from job descriptions
- Resume section parsing

## Authentication

### `auth/user_manager.py`

**Purpose**: User authentication and session management.

**Key Class**: `UserManager`

**Database Schema**:
- `users` table: id, username, email, password_hash, timestamps
- `sessions` table: session_id, user_id, expiration

**Key Methods**:
- `create_user()`: Register new user (hashes password)
- `authenticate_user()`: Verify credentials
- `create_session()`: Generate session token
- `validate_session()`: Check if session is valid
- `delete_session()`: Invalidate session

**Security**:
- Passwords hashed with SHA-256 (consider bcrypt for production)
- Session tokens with expiration
- SQLite database for storage

## CLI Interface

### Command Structure

The CLI uses `argparse` with subcommands:

```
python -m src.my_personal_agent.cli <command> [options]
```

**Commands**:
1. `vehicle`: Vehicle diagnostics
2. `analyze-resume`: Resume analysis
3. `build-resume`: Resume building
4. `auth`: Authentication (register/login/logout)

**Command Handlers**:
Each command has a corresponding handler method in `PersonalAgentCLI`:
- `handle_vehicle_diagnosis()`
- `handle_resume_analysis()`
- `handle_resume_build()`
- `handle_auth()`

**Output Formatting**:
- Uses emojis for visual appeal (✅, ❌, 📊, etc.)
- Structured output with sections
- JSON export option for detailed results

## Data Flow Examples

### Example 1: Vehicle Diagnostics

```
User: python cli.py vehicle --image dashboard.jpg
  ↓
CLI.handle_vehicle_diagnosis()
  ↓
VehicleDiagnostics.diagnose(image_path="dashboard.jpg")
  ↓
RAGEngine.vision_query(question="Analyze vehicle...", image_path="dashboard.jpg")
  ↓
LLMClient.vision_completion() → OpenAI/Anthropic Vision API
  ↓
LLM Response: "The battery appears dead..."
  ↓
VehicleDiagnostics._extract_diagnosis() → "Battery is dead"
VehicleDiagnostics._extract_actions() → ["Check battery voltage", "Use jumper cables"]
VehicleDiagnostics._get_relevant_contacts() → AAA contact info
VehicleDiagnostics._generate_detailed_solution() → Step-by-step jump-start instructions
  ↓
Return structured result → CLI formats and displays
```

### Example 2: Resume Analysis

```
User: python cli.py analyze-resume --resume resume.pdf --job-description "Software Engineer..."
  ↓
CLI.handle_resume_analysis()
  ↓
FileHandler.extract_text("resume.pdf") → Resume text
  ↓
ResumeAnalyzer.analyze(resume_text, jd_text)
  ↓
TextProcessor.calculate_keyword_match(resume, jd) → Keyword scores
TextProcessor.extract_skills() → Skills lists
  ↓
RAGEngine.query("Analyze resume against job...") → LLM detailed feedback
  ↓
ResumeAnalyzer._calculate_ats_score() → 0-100 score
ResumeAnalyzer._generate_recommendations() → Actionable suggestions
  ↓
Return analysis result → CLI formats and displays
```

### Example 3: Resume Building

```
User: python cli.py build-resume --input-file data.json
  ↓
CLI.handle_resume_build()
  ↓
Load JSON: {experiences, skills, education, portfolio, target_job}
  ↓
ResumeBuilder.build_resume(data)
  ↓
If target_job: ResumeBuilder._optimize_for_job() → LLM optimization
ResumeBuilder._generate_summary() → LLM-generated summary
  ↓
ResumeBuilder._create_docx_resume() → python-docx document creation
  ↓
Save to data/outputs/resume.docx
  ↓
Return file path → CLI displays success message
```

## Key Design Decisions

### Why ChromaDB?
- Local-first (no external service needed)
- Persistent storage
- Easy to use
- Good for personal/small-scale use

### Why Multiple LLM Providers?
- Flexibility for users
- Cost optimization (different providers for different tasks)
- Resilience (fallback options)
- Learning opportunity (understanding different APIs)

### Why Modular Architecture?
- Easy to add new features
- Clear separation of concerns
- Testable components
- Maintainable codebase

### Why CLI First?
- Quick to implement
- Works on any system
- Easy to automate
- Good for portfolio demonstration
- Can add web UI later

## Extending the Codebase

### Adding a New LLM Provider

1. Create a new client class in `core/llm_client.py` inheriting from `BaseLLMClient`
2. Implement the three required methods
3. Add provider initialization in `LLMClient.__init__()`
4. Add configuration in `config.py`

### Adding a New Feature Module

1. Create new file in `modules/`
2. Create class that uses `RAGEngine` or `LLMClient`
3. Add CLI command in `cli.py`
4. Add handler method
5. Update documentation

### Adding a New Document Format

1. Add extraction method to `FileHandler`
2. Update `SUPPORTED_EXTENSIONS`
3. Add to `extract_text()` method

## Testing Strategy

Current tests cover:
- Configuration loading
- Text processing utilities

To expand testing:
- Add integration tests for RAG engine
- Mock LLM API calls for unit tests
- Test file handlers with sample documents
- Test CLI with mock inputs

## Conclusion

This codebase demonstrates:
- **Modern Python**: Type hints, async-ready patterns
- **AI Engineering**: RAG, embeddings, LLM integration
- **Software Architecture**: Clean design, modularity
- **Practical Applications**: Real-world use cases
- **Professional Development**: Documentation, testing, structure

The architecture is designed to be:
- **Extensible**: Easy to add features
- **Maintainable**: Clear structure and documentation
- **Testable**: Modular components
- **Portable**: Works on any Python 3.9+ system
- **Scalable**: Can be extended to web/cloud deployment

