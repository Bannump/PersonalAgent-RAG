# Architecture Documentation

## Overview

My Personal Agent is a RAG (Retrieval-Augmented Generation) application built with Python that provides intelligent assistance for daily tasks including vehicle diagnostics, resume analysis, and resume building.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│                    (CLI / Future: Web UI)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Application Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Vehicle    │  │   Resume     │  │   Resume     │     │
│  │ Diagnostics  │  │   Analyzer   │  │   Builder    │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
└─────────┼──────────────────┼──────────────────┼──────────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼──────────────┐
│                      Core RAG Engine                          │
│  ┌────────────────────────────────────────────────────┐     │
│  │              RAGEngine                              │     │
│  │  • Query Processing                                 │     │
│  │  • Context Retrieval                                │     │
│  │  • LLM Integration                                  │     │
│  └────────────┬──────────────────────┬─────────────────┘     │
│               │                      │                        │
│  ┌────────────▼──────────┐  ┌───────▼──────────────┐       │
│  │    VectorStore        │  │    LLMClient         │       │
│  │  • ChromaDB           │  │  • OpenAI            │       │
│  │  • Embeddings         │  │  • Anthropic         │       │
│  │  • Similarity Search  │  │  • Vision AI         │       │
│  └───────────────────────┘  └──────────────────────┘       │
└──────────────────────────────────────────────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────────────┐
│                   Data & Storage Layer                         │
│  • SQLite (User Management)                                    │
│  • ChromaDB (Vector Storage)                                   │
│  • File System (Documents, Images, Outputs)                    │
└────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. RAG Engine (`core/rag_engine.py`)

The heart of the application, responsible for:
- **Query Processing**: Understanding user queries and context
- **Context Retrieval**: Finding relevant information from vector store
- **Response Generation**: Combining retrieved context with LLM capabilities

**Key Methods**:
- `query()`: Standard RAG query with text
- `vision_query()`: Vision-based queries with images
- `add_knowledge()`: Add documents to knowledge base

### 2. Vector Store (`core/vector_store.py`)

Manages document embeddings and similarity search:
- Uses ChromaDB for persistent vector storage
- Generates embeddings using OpenAI's embedding models
- Provides semantic search capabilities

**Key Features**:
- Persistent storage (survives restarts)
- Metadata filtering
- Cosine similarity search

### 3. LLM Client (`core/llm_client.py`)

Abstraction layer for multiple LLM providers:
- **OpenAI**: GPT-4, GPT-4 Vision, Embeddings
- **Anthropic**: Claude (future expansion)

**Design Pattern**: Strategy pattern allows switching providers without changing application code

### 4. Specialized Modules

#### Vehicle Diagnostics (`modules/vehicle_diagnostics.py`)
- Vision AI integration for image analysis
- Emergency contact information
- Step-by-step solutions

#### Resume Analyzer (`modules/resume_analyzer.py`)
- ATS compatibility scoring
- Keyword matching
- Skill gap analysis
- LLM-powered detailed feedback

#### Resume Builder (`modules/resume_builder.py`)
- ATS-optimized resume generation
- Multiple output formats (DOCX, TXT)
- Job-specific optimization

### 5. Utilities

#### File Handler (`utils/file_handler.py`)
- Document extraction (PDF, DOCX, TXT)
- File upload management
- Output file generation

#### Text Processor (`utils/text_processor.py`)
- Keyword extraction
- Skill extraction
- Section parsing
- Matching algorithms

### 6. Authentication (`auth/user_manager.py`)
- User registration and authentication
- Session management
- SQLite-based storage

## Data Flow

### Vehicle Diagnosis Flow

```
1. User uploads image → FileHandler
2. Image path → VehicleDiagnostics.diagnose()
3. Vision query → RAGEngine.vision_query()
4. LLM analyzes image → Returns analysis
5. Post-processing → Extract contacts, solutions
6. Return structured result → User
```

### Resume Analysis Flow

```
1. User uploads resume + JD → FileHandler (extract text)
2. Text extraction → ResumeAnalyzer.analyze()
3. Keyword matching → TextProcessor
4. LLM detailed analysis → RAGEngine.query()
5. ATS scoring → Calculate scores
6. Generate recommendations → Return results
```

### Resume Building Flow

```
1. User provides JSON data → ResumeBuilder.build_resume()
2. Optional job optimization → LLM optimization
3. Generate summary → LLM
4. Build document → Create DOCX/TXT
5. Save file → FileHandler
6. Return file path → User
```

## Technology Choices

### Why ChromaDB?
- **Local-first**: No external service needed
- **Persistent**: Data survives restarts
- **Easy to use**: Simple Python API
- **Flexible**: Supports metadata filtering

### Why Multiple LLM Providers?
- **Flexibility**: Users can choose preferred provider
- **Cost optimization**: Different providers for different use cases
- **Resilience**: Fallback options
- **Future-proof**: Easy to add new providers

### Why SQLite for Auth?
- **Simple**: No separate database server
- **Sufficient**: For personal/small-scale use
- **Portable**: Single file database
- **Upgradeable**: Can migrate to PostgreSQL later

## Configuration Management

All configuration is managed through environment variables and `config.py`:
- API keys (OpenAI, Anthropic)
- Database paths
- Feature flags
- Model selection

## Security Considerations

1. **API Keys**: Stored in environment variables, never in code
2. **Password Hashing**: SHA-256 (consider bcrypt for production)
3. **Session Management**: Token-based with expiration
4. **File Uploads**: User-specific directories, path validation

## Scalability Considerations

Current design is optimized for personal use. For production scaling:

1. **Vector Database**: Migrate to Pinecone or Weaviate
2. **Database**: PostgreSQL for user management
3. **Caching**: Redis for frequent queries
4. **API**: FastAPI for REST API
5. **Background Jobs**: Celery for async processing
6. **Storage**: S3/Cloud Storage for files

## Future Enhancements

1. **Web Interface**: Streamlit or FastAPI + React
2. **More LLM Providers**: Google Gemini, local models
3. **Advanced RAG**: Multi-hop reasoning, re-ranking
4. **Knowledge Base Management**: UI for managing documents
5. **Analytics**: Usage tracking, performance metrics
6. **Multi-language Support**: Internationalization

