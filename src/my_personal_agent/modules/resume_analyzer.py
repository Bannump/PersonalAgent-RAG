"""
Resume Analyzer Module - Analyzes resume against job description with ATS optimization
"""
from typing import Dict, Any, List, Optional
from src.my_personal_agent.core.rag_engine import RAGEngine
from src.my_personal_agent.utils.file_handler import FileHandler
from src.my_personal_agent.utils.text_processor import TextProcessor


class ResumeAnalyzer:
    """Analyze resume against job description with ATS optimization"""
    
    def __init__(self, rag_engine: Optional[RAGEngine] = None):
        self.rag_engine = rag_engine or RAGEngine()
        self.file_handler = FileHandler()
        self.text_processor = TextProcessor()
    
    def analyze(
        self,
        resume_path: str,
        job_description_path: Optional[str] = None,
        job_description_text: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze resume against job description
        
        Args:
            resume_path: Path to resume file (PDF, DOCX, or TXT)
            job_description_path: Optional path to job description file
            job_description_text: Optional job description as text string
        
        Returns:
            Dictionary with analysis results, scores, and recommendations
        """
        # Extract text from resume
        resume_text = self.file_handler.extract_text(resume_path)
        
        # Get job description
        if job_description_text:
            jd_text = job_description_text
        elif job_description_path:
            jd_text = self.file_handler.extract_text(job_description_path)
        else:
            raise ValueError("Either job_description_path or job_description_text must be provided")
        
        # Perform keyword matching
        keyword_analysis = self.text_processor.calculate_keyword_match(resume_text, jd_text)
        
        # Extract skills
        resume_skills = self.text_processor.extract_skills(resume_text)
        jd_skills = self.text_processor.extract_skills(jd_text)
        
        # Skill matching
        common_skills = set(resume_skills).intersection(set(jd_skills))
        missing_skills = set(jd_skills) - set(resume_skills)
        
        # Use LLM for detailed analysis
        detailed_analysis = self._get_llm_analysis(resume_text, jd_text)
        
        # Extract sections
        resume_sections = self.text_processor.extract_sections(resume_text)
        
        # Calculate ATS score
        ats_score = self._calculate_ats_score(
            keyword_analysis,
            len(common_skills),
            len(jd_skills),
            resume_sections,
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            keyword_analysis,
            missing_skills,
            detailed_analysis,
            ats_score,
        )
        
        return {
            "ats_score": ats_score,
            "keyword_analysis": keyword_analysis,
            "skills_analysis": {
                "resume_skills": resume_skills,
                "job_skills": jd_skills,
                "common_skills": sorted(list(common_skills)),
                "missing_skills": sorted(list(missing_skills)),
                "skill_match_percentage": round(len(common_skills) / len(jd_skills) * 100, 2) if jd_skills else 0,
            },
            "detailed_analysis": detailed_analysis,
            "resume_sections": resume_sections,
            "recommendations": recommendations,
            "summary": self._generate_summary(ats_score, keyword_analysis, len(missing_skills)),
        }
    
    def _get_llm_analysis(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Get detailed analysis using LLM"""
        system_prompt = """You are an expert resume reviewer and ATS (Applicant Tracking System) specialist. 
Analyze resumes and job descriptions to provide actionable feedback."""
        
        analysis_prompt = f"""Analyze this resume against the job description.

Job Description:
{jd_text[:2000]}

Resume:
{resume_text[:2000]}

Provide:
1. Overall fit assessment (1-10 scale)
2. Strengths that match the job
3. Gaps or weaknesses
4. Specific suggestions for improvement
5. ATS compatibility concerns

Format your response in a structured way."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": analysis_prompt},
        ]
        
        response = self.rag_engine.llm_client.chat_completion(messages=messages)
        
        return {
            "llm_analysis": response,
            "structured_feedback": self._parse_llm_response(response),
        }
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        # Try to extract structured information
        import re
        
        structured = {
            "fit_score": None,
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
        }
        
        # Extract fit score
        score_match = re.search(r'(\d+)[-/]10', response)
        if score_match:
            structured["fit_score"] = int(score_match.group(1))
        
        # Extract sections (basic parsing)
        lines = response.split("\n")
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            if "strength" in line_lower and ":" in line:
                current_section = "strengths"
            elif "weakness" in line_lower or "gap" in line_lower:
                current_section = "weaknesses"
            elif "suggestion" in line_lower or "improvement" in line_lower:
                current_section = "suggestions"
            elif line.strip().startswith(("-", "•", "*", "1.", "2.", "3.")):
                if current_section and current_section in structured:
                    item = re.sub(r'^[\s\-\*•\d\.]+\s*', '', line).strip()
                    if item:
                        structured[current_section].append(item)
        
        return structured
    
    def _calculate_ats_score(
        self,
        keyword_analysis: Dict[str, Any],
        common_skills_count: int,
        total_jd_skills: int,
        resume_sections: Dict[str, str],
    ) -> float:
        """Calculate ATS compatibility score (0-100)"""
        score = 0.0
        
        # Keyword match (40% weight)
        keyword_score = keyword_analysis["match_score"]
        score += keyword_score * 0.4
        
        # Skill match (30% weight)
        if total_jd_skills > 0:
            skill_match = (common_skills_count / total_jd_skills) * 100
            score += skill_match * 0.3
        else:
            score += 30  # Full points if no skills specified
        
        # Section presence (20% weight)
        required_sections = {"experience", "education", "skills"}
        present_sections = set(resume_sections.keys())
        section_score = (len(required_sections.intersection(present_sections)) / len(required_sections)) * 100
        score += section_score * 0.2
        
        # Format and structure (10% weight - assume good if sections are present)
        if resume_sections:
            score += 10
        
        return round(min(score, 100), 2)
    
    def _generate_recommendations(
        self,
        keyword_analysis: Dict[str, Any],
        missing_skills: set,
        detailed_analysis: Dict[str, Any],
        ats_score: float,
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Keyword recommendations
        if keyword_analysis["match_score"] < 60:
            top_missing = keyword_analysis["missing_keywords"][:10]
            if top_missing:
                recommendations.append(
                    f"Add these keywords naturally: {', '.join(top_missing[:5])}"
                )
        
        # Skill recommendations
        if missing_skills:
            recommendations.append(
                f"Consider adding these skills: {', '.join(list(missing_skills)[:5])}"
            )
        
        # ATS score recommendations
        if ats_score < 70:
            recommendations.append("Overall ATS score is below optimal. Review and incorporate missing keywords and skills.")
        
        if ats_score < 50:
            recommendations.append("Resume needs significant improvement to pass ATS screening.")
        
        # Add LLM suggestions
        llm_suggestions = detailed_analysis.get("structured_feedback", {}).get("suggestions", [])
        recommendations.extend(llm_suggestions[:3])
        
        return recommendations
    
    def _generate_summary(
        self,
        ats_score: float,
        keyword_analysis: Dict[str, Any],
        missing_skills_count: int,
    ) -> str:
        """Generate summary of analysis"""
        if ats_score >= 80:
            status = "Excellent"
        elif ats_score >= 60:
            status = "Good"
        elif ats_score >= 40:
            status = "Needs Improvement"
        else:
            status = "Poor"
        
        summary = f"ATS Score: {ats_score}/100 ({status})\n"
        summary += f"Keyword Match: {keyword_analysis['match_score']:.1f}%\n"
        summary += f"Missing Skills: {missing_skills_count}\n"
        
        return summary

