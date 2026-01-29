"""
Resume Builder Module - Build optimized resumes from experiences, skills, and portfolio
"""
from typing import Dict, Any, List, Optional
from pathlib import Path
import re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from src.my_personal_agent.core.rag_engine import RAGEngine
from src.my_personal_agent.utils.file_handler import FileHandler
from src.my_personal_agent.utils.text_processor import TextProcessor


class ResumeBuilder:
    """Build ATS-optimized resumes from user inputs"""
    
    def __init__(self, rag_engine: Optional[RAGEngine] = None):
        self.rag_engine = rag_engine or RAGEngine()
        self.file_handler = FileHandler()
        self.text_processor = TextProcessor()
    
    def build_resume(
        self,
        experiences: List[Dict[str, Any]],
        skills: List[str],
        education: List[Dict[str, Any]],
        portfolio_items: Optional[List[Dict[str, Any]]] = None,
        target_job: Optional[str] = None,
            output_format: str = "pdf",
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Build a resume from provided information
        
        Args:
            experiences: List of work experiences with keys: title, company, duration, description
            skills: List of skills
            education: List of education entries with keys: degree, institution, year, details
            portfolio_items: Optional list of portfolio projects
            target_job: Optional target job title/description for optimization
            output_format: "docx", "txt", or "pdf"
            user_id: Optional user ID for file organization
        
        Returns:
            Dictionary with resume content and file path
        """
        # Generate optimized content using LLM if target_job provided
        if target_job:
            optimized_content = self._optimize_for_job(
                experiences, skills, education, portfolio_items, target_job
            )
            experiences = optimized_content.get("experiences", experiences)
            skills = optimized_content.get("skills", skills)
        
        # Generate professional summary
        summary = self._generate_summary(experiences, skills, target_job)
        
        # Build resume sections
        resume_data = {
            "summary": summary,
            "experiences": experiences,
            "skills": skills,
            "education": education,
            "portfolio": portfolio_items or [],
        }
        
        # Create resume document
        if output_format in ["tex", "pdf"]:
            file_path = self._create_latex_resume(resume_data, user_id, output_format)
        elif output_format == "docx":
            file_path = self._create_docx_resume(resume_data, user_id)
        elif output_format == "txt":
            file_path = self._create_txt_resume(resume_data, user_id)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        # Generate resume text for analysis
        resume_text = self._generate_resume_text(resume_data)
        
        return {
            "resume_data": resume_data,
            "resume_text": resume_text,
            "file_path": file_path,
            "format": output_format,
        }
    
    def _optimize_for_job(
        self,
        experiences: List[Dict[str, Any]],
        skills: List[str],
        education: List[Dict[str, Any]],
        portfolio_items: Optional[List[Dict[str, Any]]],
        target_job: str,
    ) -> Dict[str, Any]:
        """Optimize resume content for a target job using LLM while maintaining authenticity"""
        # Optimize experiences one by one to maintain authenticity
        optimized_experiences = []
        for exp in experiences:
            optimized_exp = self._optimize_experience(exp, target_job)
            optimized_experiences.append(optimized_exp)
        
        # Optimize skills - suggest additional relevant skills without fabricating
        optimized_skills = self._optimize_skills(skills, target_job)
        
        # Reorder experiences by relevance to job description
        optimized_experiences = self._reorder_experiences_by_relevance(optimized_experiences, target_job)
        
        return {
            "experiences": optimized_experiences,
            "skills": optimized_skills,
        }
    
    def _optimize_experience(self, experience: Dict[str, Any], job_description: str) -> Dict[str, Any]:
        """Optimize a single experience description to match job description while maintaining authenticity"""
        title = experience.get("title", "")
        company = experience.get("company", "")
        duration = experience.get("duration", "")
        original_description = experience.get("description", "")
        
        # Skip if no description to optimize
        if not original_description:
            return experience
        
        system_prompt = """You are an expert resume writer and ATS optimization specialist. 
Your task is to reframe existing work experience descriptions to better match job requirements 
while maintaining 100% authenticity and truthfulness. 

CRITICAL RULES:
- DO NOT add experiences, technologies, or achievements that weren't mentioned
- DO NOT change dates, companies, or job titles
- DO reframe existing work using relevant keywords from the job description
- DO highlight aspects of the work that match the job requirements
- DO use industry-standard terminology that matches the job description
- DO emphasize quantifiable achievements and impact
- DO make descriptions more ATS-friendly by including relevant keywords naturally

Maintain the core facts but optimize the language and emphasis."""
        
        prompt = f"""Job Description:
{job_description[:2000]}

Original Experience:
Title: {title}
Company: {company}
Duration: {duration}
Description: {original_description}

Reframe the description above to better match the job description requirements. 
Keep ALL facts the same - same company, same role, same work done.
Only modify how it's described to:
1. Include relevant keywords from the job description
2. Emphasize aspects that match the job requirements
3. Use terminology that matches the job description
4. Make it more ATS-friendly

Return ONLY the optimized description text (2-4 concise bullet points, each max 120 characters). 
Do NOT change title, company, or duration - only optimize the description."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        
        try:
            optimized_description = self.rag_engine.llm_client.chat_completion(messages=messages)
            optimized_description = optimized_description.strip()
            
            # Fallback to original if optimization fails or is empty
            if not optimized_description or len(optimized_description) < 10:
                optimized_description = original_description
            
            return {
                "title": title,
                "company": company,
                "duration": duration,
                "description": optimized_description,
            }
        except Exception as e:
            # On error, return original experience
            return experience
    
    def _optimize_skills(self, skills: List[str], job_description: str) -> List[str]:
        """Optimize skills list by adding relevant skills from job description (if related to existing skills)"""
        # Extract skills/technologies from job description
        skill_keywords = self.text_processor.extract_keywords(job_description, min_length=2)
        # Limit to top 50 keywords
        skill_keywords = skill_keywords[:50]
        
        # Filter to only include technical/professional skills (exclude common words)
        technical_words = {
            "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust", "ruby",
            "react", "angular", "vue", "node", "django", "flask", "fastapi", "spring",
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
            "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
            "git", "jenkins", "ci/cd", "devops", "agile", "scrum",
            "machine learning", "ai", "llm", "nlp", "computer vision",
            "rest", "graphql", "grpc", "microservices", "api",
        }
        
        # Find relevant skills from job description that are related to existing skills
        relevant_new_skills = []
        existing_skills_lower = [s.lower() for s in skills]
        
        for keyword in skill_keywords:
            keyword_lower = keyword.lower()
            # Only add if it's a technical skill and not already in the list
            if (keyword_lower in technical_words or len(keyword) >= 3) and keyword_lower not in existing_skills_lower:
                # Check if it's related to existing skills (same technology family)
                is_related = any(
                    keyword_lower in existing or existing in keyword_lower 
                    for existing in existing_skills_lower
                ) or any(
                    # Check for technology families
                    keyword_lower.startswith(existing[:3]) or existing.startswith(keyword_lower[:3])
                    for existing in existing_skills_lower
                    if len(existing) >= 3
                )
                
                if is_related:
                    relevant_new_skills.append(keyword)
        
        # Limit new skills to avoid overstuffing (max 3-5 new relevant skills)
        relevant_new_skills = relevant_new_skills[:5]
        
        # Combine original skills with relevant new ones
        optimized_skills = list(skills) + relevant_new_skills
        
        return optimized_skills
    
    def _reorder_experiences_by_relevance(self, experiences: List[Dict[str, Any]], job_description: str) -> List[Dict[str, Any]]:
        """Reorder experiences by relevance to job description (most relevant first)"""
        if not job_description or len(experiences) <= 1:
            return experiences
        
        # Extract keywords from job description
        jd_keywords_list = self.text_processor.extract_keywords(job_description.lower(), min_length=3)
        jd_keywords = set(jd_keywords_list[:30])  # Limit to top 30
        
        # Score each experience by keyword overlap
        scored_experiences = []
        for exp in experiences:
            exp_text = f"{exp.get('title', '')} {exp.get('company', '')} {exp.get('description', '')}".lower()
            exp_keywords_list = self.text_processor.extract_keywords(exp_text, min_length=3)
            exp_keywords = set(exp_keywords_list[:20])  # Limit to top 20
            
            # Calculate relevance score (overlap)
            overlap = len(jd_keywords.intersection(exp_keywords))
            scored_experiences.append((overlap, exp))
        
        # Sort by relevance (highest first)
        scored_experiences.sort(key=lambda x: x[0], reverse=True)
        
        # Return experiences in relevance order
        return [exp for _, exp in scored_experiences]
    
    def _generate_summary(
        self,
        experiences: List[Dict[str, Any]],
        skills: List[str],
        target_job: Optional[str],
    ) -> str:
        """Generate professional summary"""
        system_prompt = """You are an expert resume writer. Write concise, impactful professional summaries."""
        
        # Extract key information
        experience_summary = "\n".join([
            f"- {exp.get('title', 'N/A')} at {exp.get('company', 'N/A')}: {exp.get('description', '')[:100]}"
            for exp in experiences[:3]
        ])
        
        top_skills = ", ".join(skills[:10])
        
        prompt = f"""Write a professional summary (2-3 sentences) for a resume.

Key Experiences:
{experience_summary}

Top Skills: {top_skills}

Target Job: {target_job if target_job else "General"}
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
        
        summary = self.rag_engine.llm_client.chat_completion(messages=messages)
        return summary.strip()
    
    def _create_docx_resume(
        self,
        resume_data: Dict[str, Any],
        user_id: Optional[str],
    ) -> str:
        """Create a DOCX resume document"""
        doc = Document()
        
        # Configure styles
        style = doc.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)
        
        # Title (Name would go here - placeholder)
        title = doc.add_paragraph()
        title_run = title.add_run("PROFESSIONAL RESUME")
        title_run.bold = True
        title_run.font.size = Pt(16)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        doc.add_paragraph()  # Spacing
        
        # Professional Summary
        if resume_data.get("summary"):
            doc.add_paragraph("PROFESSIONAL SUMMARY", style='Heading 1')
            summary_para = doc.add_paragraph(resume_data["summary"])
            doc.add_paragraph()  # Spacing
        
        # Skills
        if resume_data.get("skills"):
            doc.add_paragraph("SKILLS", style='Heading 1')
            skills_text = " • ".join(resume_data["skills"])
            doc.add_paragraph(skills_text)
            doc.add_paragraph()  # Spacing
        
        # Experience
        if resume_data.get("experiences"):
            doc.add_paragraph("PROFESSIONAL EXPERIENCE", style='Heading 1')
            
            for exp in resume_data["experiences"]:
                # Job title and company
                job_header = doc.add_paragraph()
                job_title_run = job_header.add_run(exp.get("title", "N/A"))
                job_title_run.bold = True
                job_header.add_run(f" | {exp.get('company', 'N/A')}")
                
                # Duration
                if exp.get("duration"):
                    duration_para = doc.add_paragraph(exp["duration"])
                    duration_para.paragraph_format.left_indent = Inches(0.25)
                
                # Description
                if exp.get("description"):
                    desc_para = doc.add_paragraph(exp["description"])
                    desc_para.paragraph_format.left_indent = Inches(0.25)
                
                doc.add_paragraph()  # Spacing
        
        # Education
        if resume_data.get("education"):
            doc.add_paragraph("EDUCATION", style='Heading 1')
            
            for edu in resume_data["education"]:
                edu_para = doc.add_paragraph()
                degree_run = edu_para.add_run(edu.get("degree", "N/A"))
                degree_run.bold = True
                edu_para.add_run(f" | {edu.get('institution', 'N/A')}")
                
                if edu.get("year"):
                    year_para = doc.add_paragraph(edu["year"])
                    year_para.paragraph_format.left_indent = Inches(0.25)
                
                if edu.get("details"):
                    details_para = doc.add_paragraph(edu["details"])
                    details_para.paragraph_format.left_indent = Inches(0.25)
                
                doc.add_paragraph()  # Spacing
        
        # Portfolio/Projects (optional)
        if resume_data.get("portfolio"):
            doc.add_paragraph("PROJECTS", style='Heading 1')
            
            for project in resume_data["portfolio"]:
                proj_para = doc.add_paragraph()
                proj_name_run = proj_para.add_run(project.get("name", "N/A"))
                proj_name_run.bold = True
                
                if project.get("description"):
                    desc_para = doc.add_paragraph(project["description"])
                    desc_para.paragraph_format.left_indent = Inches(0.25)
                
                doc.add_paragraph()  # Spacing
        
        # Save document
        filename = "resume.docx"
        if user_id:
            output_path = self.file_handler.output_dir / user_id / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.file_handler.output_dir / filename
        
        doc.save(str(output_path))
        return str(output_path)
    
    def _create_txt_resume(
        self,
        resume_data: Dict[str, Any],
        user_id: Optional[str],
    ) -> str:
        """Create a TXT resume document"""
        lines = []
        
        lines.append("=" * 60)
        lines.append("PROFESSIONAL RESUME")
        lines.append("=" * 60)
        lines.append("")
        
        # Summary
        if resume_data.get("summary"):
            lines.append("PROFESSIONAL SUMMARY")
            lines.append("-" * 60)
            lines.append(resume_data["summary"])
            lines.append("")
        
        # Skills
        if resume_data.get("skills"):
            lines.append("SKILLS")
            lines.append("-" * 60)
            lines.append(" • ".join(resume_data["skills"]))
            lines.append("")
        
        # Experience
        if resume_data.get("experiences"):
            lines.append("PROFESSIONAL EXPERIENCE")
            lines.append("-" * 60)
            
            for exp in resume_data["experiences"]:
                lines.append(f"{exp.get('title', 'N/A')} | {exp.get('company', 'N/A')}")
                if exp.get("duration"):
                    lines.append(f"  {exp['duration']}")
                if exp.get("description"):
                    lines.append(f"  {exp['description']}")
                lines.append("")
        
        # Education
        if resume_data.get("education"):
            lines.append("EDUCATION")
            lines.append("-" * 60)
            
            for edu in resume_data["education"]:
                lines.append(f"{edu.get('degree', 'N/A')} | {edu.get('institution', 'N/A')}")
                if edu.get("year"):
                    lines.append(f"  {edu['year']}")
                if edu.get("details"):
                    lines.append(f"  {edu['details']}")
                lines.append("")
        
        # Portfolio
        if resume_data.get("portfolio"):
            lines.append("PROJECTS")
            lines.append("-" * 60)
            
            for project in resume_data["portfolio"]:
                lines.append(project.get("name", "N/A"))
                if project.get("description"):
                    lines.append(f"  {project['description']}")
                lines.append("")
        
        resume_text = "\n".join(lines)
        
        # Save file
        filename = "resume.txt"
        file_path = self.file_handler.save_output(resume_text, filename, user_id)
        
        return file_path
    
    def _generate_resume_text(self, resume_data: Dict[str, Any]) -> str:
        """Generate plain text version of resume for analysis"""
        text_parts = []
        
        if resume_data.get("summary"):
            text_parts.append(resume_data["summary"])
        
        if resume_data.get("skills"):
            text_parts.append(" ".join(resume_data["skills"]))
        
        if resume_data.get("experiences"):
            for exp in resume_data["experiences"]:
                exp_text = f"{exp.get('title', '')} {exp.get('company', '')} {exp.get('description', '')}"
                text_parts.append(exp_text)
        
        if resume_data.get("education"):
            for edu in resume_data["education"]:
                edu_text = f"{edu.get('degree', '')} {edu.get('institution', '')} {edu.get('details', '')}"
                text_parts.append(edu_text)
        
        return "\n".join(text_parts)
    
    def _create_latex_resume(
        self,
        resume_data: Dict[str, Any],
        user_id: Optional[str],
        output_format: str = "tex",
    ) -> str:
        """Create a LaTeX resume document using the main.tex template"""
        # Load the template
        template_path = Path(__file__).parent.parent.parent.parent / "examples" / "main.tex"
        
        if not template_path.exists():
            raise FileNotFoundError(f"LaTeX template not found at {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Extract user info - for now use placeholders, but in production would come from user profile
        # For now, try to extract name from first experience or use placeholder
        name = "Your Name"  # Placeholder - would come from user profile in full implementation
        contact_info = "Phone: (XXX) XXX-XXXX | Email: email@example.com | Location: City, State"
        tagline = self._extract_tagline(resume_data) or "Professional"
        
        # Build LaTeX content sections
        header = self._build_latex_header(name, contact_info, tagline)
        summary = self._build_latex_summary(resume_data.get("summary", ""))
        experience = self._build_latex_experience(resume_data.get("experiences", []))
        projects = self._build_latex_projects(resume_data.get("portfolio", []))
        skills = self._build_latex_skills(resume_data.get("skills", []))
        education = self._build_latex_education(resume_data.get("education", []))
        
        # Replace template sections - replace content between markers, keep markers
        # Use function-based replacement to avoid regex escape issues with LaTeX backslashes
        latex_content = template
        
        # Replace header section (content between %----------HEADER---------- and %----------SUMMARY----------)
        def replace_header(match):
            return f"{match.group(1)}\n{header}\n{match.group(3)}"
        header_pattern = rf"(%----------HEADER----------)(.*?)(%----------SUMMARY----------)"
        latex_content = re.sub(header_pattern, replace_header, latex_content, flags=re.DOTALL)
        
        # Replace summary section (content between %----------SUMMARY---------- and %-----------EXPERIENCE-----------)
        def replace_summary(match):
            return f"{match.group(1)}\n{summary}\n{match.group(3)}"
        summary_pattern = rf"(%----------SUMMARY----------)(.*?)(%-----------EXPERIENCE-----------)"
        latex_content = re.sub(summary_pattern, replace_summary, latex_content, flags=re.DOTALL)
        
        # Replace experience section (content between %-----------EXPERIENCE----------- and %-----------PROJECTS-----------)
        def replace_experience(match):
            return f"{match.group(1)}\n{experience}\n{match.group(3)}"
        exp_pattern = rf"(%-----------EXPERIENCE-----------)(.*?)(%-----------PROJECTS-----------)"
        latex_content = re.sub(exp_pattern, replace_experience, latex_content, flags=re.DOTALL)
        
        # Replace projects section (content between %-----------PROJECTS----------- and %-----------TECHNICAL SKILLS-----------)
        def replace_projects(match):
            return f"{match.group(1)}\n{projects}\n{match.group(3)}"
        proj_pattern = rf"(%-----------PROJECTS-----------)(.*?)(%-----------TECHNICAL SKILLS-----------)"
        latex_content = re.sub(proj_pattern, replace_projects, latex_content, flags=re.DOTALL)
        
        # Replace skills section (content between %-----------TECHNICAL SKILLS----------- and %-----------EDUCATION-----------)
        def replace_skills(match):
            return f"{match.group(1)}\n{skills}\n{match.group(3)}"
        skills_pattern = rf"(%-----------TECHNICAL SKILLS-----------)(.*?)(%-----------EDUCATION-----------)"
        latex_content = re.sub(skills_pattern, replace_skills, latex_content, flags=re.DOTALL)
        
        # Replace education section (content between %-----------EDUCATION----------- and %-------------------------------------------)
        def replace_education(match):
            return f"{match.group(1)}\n{education}\n{match.group(3)}"
        edu_pattern = rf"(%-----------EDUCATION-----------)(.*?)(%-------------------------------------------)"
        latex_content = re.sub(edu_pattern, replace_education, latex_content, flags=re.DOTALL)
        
        # Save LaTeX file
        filename = "resume.tex"
        if user_id:
            output_path = self.file_handler.output_dir / user_id / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
        else:
            output_path = self.file_handler.output_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # If PDF format requested, compile LaTeX to PDF
        if output_format == "pdf":
            pdf_path = self._compile_latex_to_pdf(output_path)
            if pdf_path and pdf_path.exists():
                return str(pdf_path)
            # If compilation fails, return .tex file
            return str(output_path)
        
        return str(output_path)
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        if not text:
            return ""
        text = str(text)
        # Escape special LaTeX characters
        replacements = {
            '\\': r'\textbackslash{}',
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '^': r'\textasciicircum{}',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text
    
    def _build_latex_header(self, name: str, contact: str, tagline: str) -> str:
        """Build LaTeX header section"""
        escaped_name = self._escape_latex(name)
        escaped_tagline = self._escape_latex(tagline)
        
        # Parse contact info (simple parsing - in production would be more robust)
        contact_parts = contact.split('|')
        phone = contact_parts[0].strip() if len(contact_parts) > 0 else ""
        email = contact_parts[1].strip() if len(contact_parts) > 1 else ""
        location = contact_parts[2].strip() if len(contact_parts) > 2 else ""
        
        return f"""\\begin{{center}}
    {{\\Huge \\scshape {escaped_name}}} \\\\ \\vspace{{4pt}}
    \\small 
    \\faPhone\\ {phone} \\hspace{{10pt}}
    \\faEnvelope\\ \\href{{mailto:{email}}}{{\\underline{{{email}}}}} \\hspace{{10pt}}
    \\faMapMarker\\ {location} \\\\
    \\vspace{{2pt}} \\textit{{{escaped_tagline}}}
\\end{{center}}"""
    
    def _build_latex_summary(self, summary: str) -> str:
        """Build LaTeX summary section"""
        escaped_summary = self._escape_latex(summary)
        # Ensure summary is concise (max 2-3 sentences for 1-page resume)
        sentences = escaped_summary.split('.')
        if len(sentences) > 3:
            escaped_summary = '. '.join(sentences[:3]) + '.'
        
        return f"""\\vspace{{-6pt}}
\\begin{{center}}
    \\small
    {escaped_summary}
\\end{{center}}
\\vspace{{-6pt}}"""
    
    def _build_latex_experience(self, experiences: List[Dict[str, Any]]) -> str:
        """Build LaTeX experience section - limited to fit 1 page"""
        if not experiences:
            return ""
        
        # Limit to 2-3 most relevant experiences for 1-page resume
        experiences = experiences[:3]
        
        latex = "\\section{Professional Experience}\n  \\resumeSubHeadingListStart\n\n"
        
        for exp in experiences:
            title = self._escape_latex(exp.get("title", "N/A"))
            company = self._escape_latex(exp.get("company", "N/A"))
            duration = self._escape_latex(exp.get("duration", ""))
            description = exp.get("description", "")
            
            # Extract location if available (e.g., "Company | Location" format)
            if '|' in company:
                parts = company.split('|', 1)
                company = parts[0].strip()
                location = self._escape_latex(parts[1].strip())
            else:
                location = ""  # Default location
            
            # Parse description into bullet points (limit to 3-4 per experience for 1-page)
            bullets = self._parse_description_to_bullets(description, max_bullets=4)
            
            latex += f"    \\resumeSubheading\n"
            latex += f"      {{{title}}}{{{duration}}}\n"
            if location:
                latex += f"      {{\\textit{{\\small {company}}}}}{{\\textit{{\\small {location}}}}}\n"
            else:
                latex += f"      {{\\textit{{\\small {company}}}}}{{}}\n"
            
            if bullets:
                latex += "      \\resumeItemListStart\n"
                for bullet in bullets:
                    escaped_bullet = self._escape_latex(bullet)
                    latex += f"        \\resumeItem{{{escaped_bullet}}}\n"
                latex += "      \\resumeItemListEnd\n"
        
        latex += "\n  \\resumeSubHeadingListEnd"
        return latex
    
    def _build_latex_projects(self, portfolio: List[Dict[str, Any]]) -> str:
        """Build LaTeX projects section - limited for 1-page resume"""
        if not portfolio:
            return ""
        
        # Limit to 2 most relevant projects for 1-page resume
        portfolio = portfolio[:2]
        
        latex = "\\section{Systems \\& AI Projects}\n    \\resumeSubHeadingListStart\n\n"
        
        for project in portfolio:
            name = self._escape_latex(project.get("name", "N/A"))
            description = project.get("description", "")
            # Extract date if available, otherwise use placeholder
            date = "Present"  # Would extract from portfolio data if available
            
            bullets = self._parse_description_to_bullets(description, max_bullets=3)
            
            latex += f"      \\resumeProjectHeading\n"
            latex += f"          {{\\textbf{{{name}}}}}{{{date}}}\n"
            
            if bullets:
                latex += "          \\resumeItemListStart\n"
                for bullet in bullets:
                    escaped_bullet = self._escape_latex(bullet)
                    latex += f"            \\resumeItem{{{escaped_bullet}}}\n"
                latex += "          \\resumeItemListEnd\n"
        
        latex += "\n    \\resumeSubHeadingListEnd"
        return latex
    
    def _build_latex_skills(self, skills: List[str]) -> str:
        """Build LaTeX skills section - organized by category"""
        if not skills:
            return ""
        
        # Categorize skills for better organization (industry standard)
        categories = {
            "AI \\& Machine Learning": [],
            "Systems \\& Languages": [],
            "Networking \\& Low Level": [],
            "Cloud Infrastructure": [],
            "Tools \\& Platforms": [],
        }
        
        # Simple categorization (in production, use more sophisticated logic)
        skill_keywords = {
            "AI \\& Machine Learning": ["ai", "ml", "llm", "gpt", "openai", "pytorch", "tensorflow", "langchain", "rag"],
            "Systems \\& Languages": ["c++", "c ", "go", "python", "java", "rust", "sql"],
            "Networking \\& Low Level": ["tcp", "udp", "socket", "grpc", "network", "linux"],
            "Cloud Infrastructure": ["aws", "kubernetes", "docker", "terraform", "azure", "gcp", "eks"],
            "Tools \\& Platforms": ["git", "jenkins", "grafana", "wireshark", "linux", "ubuntu"],
        }
        
        uncategorized = []
        for skill in skills:
            skill_lower = skill.lower()
            categorized = False
            for category, keywords in skill_keywords.items():
                if any(keyword in skill_lower for keyword in keywords):
                    categories[category].append(skill)
                    categorized = True
                    break
            if not categorized:
                uncategorized.append(skill)
        
        # Add uncategorized to a default category (limit for 1-page)
        if uncategorized:
            categories["Systems \\& Languages"].extend(uncategorized[:5])
        
        # Build LaTeX
        latex = "\\section{Technical Skills}\n \\begin{itemize}[leftmargin=0.15in, label={}]\n    \\small{\\item{\n"
        
        skill_lines = []
        for category, skill_list in categories.items():
            if skill_list:
                # Limit skills per category for 1-page resume
                skill_list = skill_list[:8]
                skill_str = ", ".join([self._escape_latex(s) for s in skill_list])
                skill_lines.append(f"     \\textbf{{{category}}}{{}}: {skill_str}")
        
        latex += "     \\\\\n     ".join(skill_lines)
        latex += "\n    }}\n \\end{itemize}"
        
        return latex
    
    def _build_latex_education(self, education: List[Dict[str, Any]]) -> str:
        """Build LaTeX education section"""
        if not education:
            return ""
        
        latex = "\\section{Education}\n  \\resumeSubHeadingListStart\n"
        
        for edu in education[:2]:  # Limit to 2 entries for 1-page
            degree = self._escape_latex(edu.get("degree", "N/A"))
            institution = self._escape_latex(edu.get("institution", "N/A"))
            year = self._escape_latex(edu.get("year", ""))
            details = self._escape_latex(edu.get("details", ""))
            
            # Format degree with details if available
            if details:
                degree_full = f"{degree} ({details})"
            else:
                degree_full = degree
            
            latex += f"    \\resumeSubheading\n"
            latex += f"      {{{institution}}}{{{year}}}\n"
            latex += f"      {{{degree_full}}}{{}}\n"
        
        latex += "  \\resumeSubHeadingListEnd"
        return latex
    
    def _parse_description_to_bullets(self, description: str, max_bullets: int = 4) -> List[str]:
        """Parse description text into bullet points, ensuring concise format for 1-page resume"""
        if not description:
            return []
        
        # Split by common separators
        bullets = re.split(r'[•\n•\-]\s*|\n\s*[-•]\s*', description)
        bullets = [b.strip() for b in bullets if b.strip()]
        
        # If no clear bullets, split by sentences
        if len(bullets) <= 1:
            sentences = re.split(r'[.!?]+', description)
            bullets = [s.strip() + '.' for s in sentences if s.strip()][:max_bullets]
        else:
            bullets = bullets[:max_bullets]
        
        # Ensure bullets are concise (max 120 chars for 1-page resume)
        concise_bullets = []
        for bullet in bullets:
            if len(bullet) > 120:
                # Truncate and add ellipsis
                bullet = bullet[:117] + "..."
            concise_bullets.append(bullet)
        
        return concise_bullets
    
    def _extract_tagline(self, resume_data: Dict[str, Any]) -> str:
        """Extract tagline from experiences and skills"""
        # Generate tagline from most relevant experience
        experiences = resume_data.get("experiences", [])
        if experiences:
            first_exp = experiences[0]
            title = first_exp.get("title", "")
            # Extract primary role/title for tagline
            if "|" in title:
                title = title.split("|")[0].strip()
            return title
        return "Professional"
    
    def _compile_latex_to_pdf(self, tex_path: Path) -> Optional[Path]:
        """Compile LaTeX file to PDF using pdflatex (if available)"""
        try:
            import subprocess
            import shutil
            
            # Check if pdflatex is available
            pdflatex_path = shutil.which('pdflatex')
            if not pdflatex_path:
                print(f"WARNING: pdflatex not found in PATH. PDF compilation skipped.")
                return None  # pdflatex not installed
            
            # Compile LaTeX to PDF (run twice for references)
            output_dir = tex_path.parent
            
            # First compilation
            result1 = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            # Log any errors from first compilation
            if result1.returncode != 0:
                print(f"WARNING: pdflatex first run failed with return code {result1.returncode}")
                print(f"Error output: {result1.stderr[:500] if result1.stderr else 'No error output'}")
            
            # Second compilation (for references)
            result2 = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory', str(output_dir), str(tex_path)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            pdf_path = output_dir / tex_path.with_suffix('.pdf').name
            
            # Check if PDF was created successfully
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                # Clean up auxiliary files
                for ext in ['.aux', '.log', '.out']:
                    aux_file = output_dir / tex_path.with_suffix(ext).name
                    if aux_file.exists():
                        try:
                            aux_file.unlink()
                        except Exception:
                            pass
                print(f"Successfully compiled LaTeX to PDF: {pdf_path}")
                return pdf_path
            else:
                print(f"WARNING: PDF file was not created at {pdf_path}")
                if result2.stderr:
                    print(f"Error output: {result2.stderr[:500]}")
                return None
            
        except subprocess.TimeoutExpired:
            print(f"WARNING: pdflatex compilation timed out after 30 seconds")
            return None
        except FileNotFoundError:
            print(f"WARNING: pdflatex command not found")
            return None
        except Exception as e:
            print(f"WARNING: pdflatex compilation failed with error: {str(e)}")
            return None

