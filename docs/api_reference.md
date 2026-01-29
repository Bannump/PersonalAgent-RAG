# API Reference

## Core Classes

### RAGEngine

Main RAG engine class.

#### Methods

##### `query(question, context_collection=None, max_context_docs=5, temperature=0.7, system_prompt=None)`

Perform a RAG query.

**Parameters**:
- `question` (str): User's question
- `context_collection` (str, optional): Collection name for context
- `max_context_docs` (int): Maximum documents to retrieve
- `temperature` (float): LLM temperature
- `system_prompt` (str, optional): System prompt

**Returns**: `Dict` with keys:
- `answer`: Generated answer
- `sources`: List of source documents
- `metadata`: Query metadata

##### `vision_query(question, image_path, system_prompt=None, temperature=0.7)`

Query with image using vision AI.

**Parameters**:
- `question` (str): Question about the image
- `image_path` (str): Path to image file
- `system_prompt` (str, optional): System prompt
- `temperature` (float): LLM temperature

**Returns**: `str` - Generated answer

---

### VehicleDiagnostics

Vehicle diagnostics module.

#### Methods

##### `diagnose(image_path, user_description=None, include_contacts=True)`

Diagnose vehicle issue from image.

**Parameters**:
- `image_path` (str): Path to vehicle image
- `user_description` (str, optional): Additional context
- `include_contacts` (bool): Include emergency contacts

**Returns**: `Dict` with keys:
- `diagnosis`: Main diagnosis
- `recommended_actions`: List of actions
- `emergency_contacts`: Contact information
- `detailed_solution`: Step-by-step solution

---

### ResumeAnalyzer

Resume analysis module.

#### Methods

##### `analyze(resume_path, job_description_path=None, job_description_text=None)`

Analyze resume against job description.

**Parameters**:
- `resume_path` (str): Path to resume file
- `job_description_path` (str, optional): Path to JD file
- `job_description_text` (str, optional): JD as text

**Returns**: `Dict` with keys:
- `ats_score`: ATS compatibility score (0-100)
- `keyword_analysis`: Keyword matching results
- `skills_analysis`: Skills comparison
- `recommendations`: Improvement suggestions
- `detailed_analysis`: LLM-generated analysis

---

### ResumeBuilder

Resume building module.

#### Methods

##### `build_resume(experiences, skills, education, portfolio_items=None, target_job=None, output_format="docx", user_id=None)`

Build optimized resume.

**Parameters**:
- `experiences` (List[Dict]): Work experience list
- `skills` (List[str]): Skills list
- `education` (List[Dict]): Education entries
- `portfolio_items` (List[Dict], optional): Portfolio projects
- `target_job` (str, optional): Target job for optimization
- `output_format` (str): "docx" or "txt"
- `user_id` (str, optional): User ID for organization

**Returns**: `Dict` with keys:
- `resume_data`: Structured resume data
- `resume_text`: Plain text version
- `file_path`: Path to generated file
- `format`: Output format

**Experience Dict Format**:
```python
{
    "title": "Software Engineer",
    "company": "Tech Corp",
    "duration": "2020-2024",
    "description": "Job description..."
}
```

**Education Dict Format**:
```python
{
    "degree": "BS Computer Science",
    "institution": "University Name",
    "year": "2020",
    "details": "Additional details..."
}
```

---

### UserManager

User authentication and management.

#### Methods

##### `create_user(username, password, email=None)`

Create a new user.

**Returns**: `Dict` with user information

##### `authenticate_user(username, password)`

Authenticate user.

**Returns**: `Dict` with user info if successful, `None` otherwise

##### `create_session(user_id, expiration_hours=24)`

Create a session.

**Returns**: `str` - Session ID

##### `validate_session(session_id)`

Validate session.

**Returns**: `str` - User ID if valid, `None` otherwise

---

## CLI Commands

### Vehicle Diagnosis

```bash
python -m src.my_personal_agent.cli vehicle \
    --image path/to/image.jpg \
    --description "Car won't start" \
    --output analysis.json
```

### Resume Analysis

```bash
python -m src.my_personal_agent.cli analyze-resume \
    --resume path/to/resume.pdf \
    --job-description "Job description text or file path" \
    --output analysis.json
```

### Build Resume

```bash
python -m src.my_personal_agent.cli build-resume \
    --input-file resume_data.json \
    --format docx \
    --output metadata.json
```

### Authentication

```bash
# Register
python -m src.my_personal_agent.cli auth register \
    --username myuser \
    --password mypass \
    --email user@example.com

# Login
python -m src.my_personal_agent.cli auth login \
    --username myuser \
    --password mypass

# Logout
python -m src.my_personal_agent.cli auth logout
```

## Configuration

All configuration is done through environment variables (see `.env.example`):

- `OPENAI_API_KEY`: OpenAI API key (required)
- `ANTHROPIC_API_KEY`: Anthropic API key (optional)
- `VECTOR_DB_PATH`: Path to vector database
- `SECRET_KEY`: Secret key for sessions
- `DEFAULT_LLM_PROVIDER`: "openai" or "anthropic"
- `DEFAULT_MODEL`: Model name (e.g., "gpt-4-turbo-preview")

