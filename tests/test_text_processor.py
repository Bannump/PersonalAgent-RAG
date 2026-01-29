"""
Tests for text processing utilities
"""
from src.my_personal_agent.utils.text_processor import TextProcessor


def test_extract_keywords():
    """Test keyword extraction"""
    text = "Python is a programming language. JavaScript is also popular."
    keywords = TextProcessor.extract_keywords(text)
    
    assert "python" in keywords
    assert "javascript" in keywords
    assert "programming" in keywords
    assert "is" not in keywords  # Stop word should be filtered


def test_extract_skills():
    """Test skill extraction"""
    text = "I know Python, JavaScript, React, and AWS cloud services."
    skills = TextProcessor.extract_skills(text)
    
    assert len(skills) > 0
    # Should find at least some skills
    skill_text_lower = " ".join([s.lower() for s in skills])
    assert "python" in skill_text_lower or "javascript" in skill_text_lower


def test_calculate_keyword_match():
    """Test keyword matching"""
    text1 = "Python developer with experience in React and AWS"
    text2 = "Looking for a Python developer with AWS skills"
    
    result = TextProcessor.calculate_keyword_match(text1, text2)
    
    assert "match_score" in result
    assert result["match_score"] > 0
    assert "common_keywords" in result
    assert "python" in [kw.lower() for kw in result["common_keywords"]]


def test_extract_sections():
    """Test section extraction from resume text"""
    resume_text = """
    John Doe
    
    Experience
    Software Engineer at Tech Corp (2020-2024)
    Developed web applications
    
    Education
    BS Computer Science, University (2020)
    """
    
    sections = TextProcessor.extract_sections(resume_text)
    
    assert len(sections) > 0
    # Should extract experience and education sections

