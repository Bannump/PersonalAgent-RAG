"""
Configuration management for My Personal Agent
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


# Detect if running on Vercel (serverless environment)
IS_VERCEL = os.environ.get("VERCEL", "") == "1" or os.environ.get("VERCEL_ENV") is not None

# Find project root (directory containing .env file)
# config.py is at: RAG/src/my_personal_agent/config.py
# .env is at: RAG/.env
_config_file_path = Path(__file__).resolve()
# Go up 3 levels: config.py -> my_personal_agent -> src -> RAG
_project_root = _config_file_path.parent.parent.parent
_env_file_path = _project_root / ".env"

# Use /tmp for writable directories on Vercel
_default_data_dir = "/tmp/data" if IS_VERCEL else "./data"
_default_uploads_dir = "/tmp/data/uploads" if IS_VERCEL else "./data/uploads"
_default_output_dir = "/tmp/data/outputs" if IS_VERCEL else "./data/outputs"
_default_vector_db = "/tmp/vector_db" if IS_VERCEL else "./data/vector_db"
_default_db_path = "/tmp/data/users.db" if IS_VERCEL else "./data/users.db"


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys (with defaults for graceful degradation)
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    
    # Vector Database
    vector_db_path: str = Field(default=_default_vector_db, env="VECTOR_DB_PATH")
    use_pinecone: bool = Field(False, env="USE_PINECONE")
    pinecone_api_key: Optional[str] = Field(None, env="PINECONE_API_KEY")
    pinecone_environment: Optional[str] = Field(None, env="PINECONE_ENVIRONMENT")
    pinecone_index_name: Optional[str] = Field(None, env="PINECONE_INDEX_NAME")
    
    # Application Settings
    secret_key: str = Field(default="default-secret-key-change-in-production", env="SECRET_KEY")
    database_path: str = Field(default=_default_db_path, env="DATABASE_PATH")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Model Configuration
    default_llm_provider: str = Field("openai", env="DEFAULT_LLM_PROVIDER")
    default_model: str = Field("gpt-4o", env="DEFAULT_MODEL")
    embedding_model: str = Field("text-embedding-3-small", env="EMBEDDING_MODEL")
    
    # Paths (use /tmp on Vercel)
    data_dir: str = Field(default=_default_data_dir, env="DATA_DIR")
    uploads_dir: str = Field(default=_default_uploads_dir, env="UPLOADS_DIR")
    output_dir: str = Field(default=_default_output_dir, env="OUTPUT_DIR")
    
    # Feature Flags
    enable_auth: bool = Field(True, env="ENABLE_AUTH")
    enable_image_analysis: bool = Field(True, env="ENABLE_IMAGE_ANALYSIS")
    enable_resume_builder: bool = Field(True, env="ENABLE_RESUME_BUILDER")
    
    class Config:
        env_file = str(_env_file_path) if _env_file_path.exists() else None
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist (use try/except for read-only filesystems)
        for dir_path in [self.data_dir, self.uploads_dir, self.output_dir, self.vector_db_path]:
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            except (OSError, PermissionError):
                # Directory creation failed (e.g., read-only filesystem)
                pass


# Global settings instance
settings = Settings()

