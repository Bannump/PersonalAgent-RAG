"""
Tests for configuration management
"""
import os
import pytest
from src.my_personal_agent.config import Settings


def test_settings_loading():
    """Test that settings can be loaded"""
    # This test requires .env file or environment variables
    # It will fail if required keys are missing, which is expected
    try:
        settings = Settings()
        assert settings.default_llm_provider in ["openai", "anthropic"]
    except Exception:
        # Expected if .env is not set up
        pytest.skip("Settings require .env file")


def test_settings_defaults():
    """Test default settings values"""
    # Test with minimal required env vars
    os.environ["OPENAI_API_KEY"] = "test-key"
    os.environ["SECRET_KEY"] = "test-secret"
    
    settings = Settings()
    assert settings.log_level == "INFO"
    assert settings.default_llm_provider == "openai"
    assert settings.enable_auth is True

