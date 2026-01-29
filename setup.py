"""
Setup script for My Personal Agent
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="my-personal-agent",
    version="1.0.0",
    description="A RAG-based personal assistant for daily tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/my-personal-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "openai>=1.6.1",
        "anthropic>=0.8.1",
        "chromadb>=0.4.18",
        "tiktoken>=0.5.2",
        "PyPDF2>=3.0.1",
        "pdfplumber>=0.10.3",
        "python-docx>=1.1.0",
        "Pillow>=10.2.0",
        "opencv-python>=4.8.1.78",
        "requests>=2.31.0",
        "sqlalchemy>=2.0.23",
    ],
    entry_points={
        "console_scripts": [
            "personal-agent=src.my_personal_agent.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

