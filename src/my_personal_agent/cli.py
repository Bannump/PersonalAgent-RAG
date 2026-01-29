"""
Command-line interface for My Personal Agent
"""
import argparse
import sys
from pathlib import Path
from typing import Optional
import json

from src.my_personal_agent.core.rag_engine import RAGEngine
from src.my_personal_agent.modules.vehicle_diagnostics import VehicleDiagnostics
from src.my_personal_agent.modules.resume_analyzer import ResumeAnalyzer
from src.my_personal_agent.modules.resume_builder import ResumeBuilder
from src.my_personal_agent.auth.user_manager import UserManager
from src.my_personal_agent.config import settings


class PersonalAgentCLI:
    """Command-line interface for My Personal Agent"""
    
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.vehicle_diagnostics = VehicleDiagnostics(self.rag_engine)
        self.resume_analyzer = ResumeAnalyzer(self.rag_engine)
        self.resume_builder = ResumeBuilder(self.rag_engine)
        self.user_manager = UserManager() if settings.enable_auth else None
        self.current_user_id: Optional[str] = None
    
    def handle_vehicle_diagnosis(self, args):
        """Handle vehicle diagnosis command"""
        if not args.image:
            print("Error: --image argument is required for vehicle diagnosis")
            return
        
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: Image file not found: {args.image}")
            return
        
        print("Analyzing vehicle image...")
        print("=" * 60)
        
        try:
            result = self.vehicle_diagnostics.diagnose(
                image_path=str(image_path),
                user_description=args.description,
                include_contacts=args.include_contacts,
            )
            
            print("\n🔍 DIAGNOSIS:")
            print("-" * 60)
            print(result["diagnosis"])
            
            print("\n📋 RECOMMENDED ACTIONS:")
            print("-" * 60)
            for i, action in enumerate(result["recommended_actions"], 1):
                print(f"{i}. {action}")
            
            if result.get("detailed_solution") and result["detailed_solution"].get("steps"):
                print("\n🛠️ DETAILED SOLUTION:")
                print("-" * 60)
                for i, step in enumerate(result["detailed_solution"]["steps"], 1):
                    print(f"{i}. {step}")
                
                if result["detailed_solution"].get("safety_warnings"):
                    print("\n⚠️ SAFETY WARNINGS:")
                    print("-" * 60)
                    for warning in result["detailed_solution"]["safety_warnings"]:
                        print(f"• {warning}")
            
            if result.get("emergency_contacts"):
                print("\n📞 EMERGENCY CONTACTS:")
                print("-" * 60)
                for contact in result["emergency_contacts"]:
                    print(f"\n{contact['name']}")
                    print(f"  Phone: {contact['phone']}")
                    if contact.get("website"):
                        print(f"  Website: {contact['website']}")
                    print(f"  Services: {', '.join(contact.get('services', []))}")
            
            if args.output:
                output_path = Path(args.output)
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2, default=str)
                print(f"\n✅ Full analysis saved to: {output_path}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def handle_resume_analysis(self, args):
        """Handle resume analysis command"""
        if not args.resume:
            print("Error: --resume argument is required")
            return
        
        resume_path = Path(args.resume)
        if not resume_path.exists():
            print(f"Error: Resume file not found: {args.resume}")
            return
        
        jd_text = None
        jd_path = None
        
        if args.job_description:
            jd_path = Path(args.job_description)
            if jd_path.exists():
                from src.my_personal_agent.utils.file_handler import FileHandler
                jd_text = FileHandler().extract_text(str(jd_path))
            else:
                # Treat as text
                jd_text = args.job_description
        
        if not jd_text:
            print("Error: Job description required (use --job-description)")
            return
        
        print("Analyzing resume against job description...")
        print("=" * 60)
        
        try:
            result = self.resume_analyzer.analyze(
                resume_path=str(resume_path),
                job_description_text=jd_text,
            )
            
            print("\n📊 ATS SCORE:")
            print("-" * 60)
            print(f"{result['ats_score']}/100")
            
            if result["ats_score"] >= 80:
                status = "✅ Excellent"
            elif result["ats_score"] >= 60:
                status = "⚠️ Good"
            elif result["ats_score"] >= 40:
                status = "🔶 Needs Improvement"
            else:
                status = "❌ Poor"
            print(f"Status: {status}")
            
            print("\n🔑 KEYWORD ANALYSIS:")
            print("-" * 60)
            ka = result["keyword_analysis"]
            print(f"Match Score: {ka['match_score']:.1f}%")
            print(f"Common Keywords: {len(ka['common_keywords'])}")
            print(f"Missing Keywords: {len(ka['missing_keywords'])}")
            
            if ka["missing_keywords"]:
                print("\nTop Missing Keywords:")
                for keyword in ka["missing_keywords"][:10]:
                    print(f"  • {keyword}")
            
            print("\n💼 SKILLS ANALYSIS:")
            print("-" * 60)
            sa = result["skills_analysis"]
            print(f"Resume Skills: {len(sa['resume_skills'])}")
            print(f"Job Skills: {len(sa['job_skills'])}")
            print(f"Common Skills: {len(sa['common_skills'])}")
            print(f"Skill Match: {sa['skill_match_percentage']:.1f}%")
            
            if sa["missing_skills"]:
                print("\nMissing Skills:")
                for skill in sa["missing_skills"][:10]:
                    print(f"  • {skill}")
            
            print("\n💡 RECOMMENDATIONS:")
            print("-" * 60)
            for i, rec in enumerate(result["recommendations"], 1):
                print(f"{i}. {rec}")
            
            if args.output:
                output_path = Path(args.output)
                with open(output_path, "w") as f:
                    json.dump(result, f, indent=2, default=str)
                print(f"\n✅ Full analysis saved to: {output_path}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def handle_resume_build(self, args):
        """Handle resume building command"""
        # Load data from file or use defaults
        if args.input_file:
            input_path = Path(args.input_file)
            if not input_path.exists():
                print(f"Error: Input file not found: {args.input_file}")
                return
            
            with open(input_path, "r") as f:
                data = json.load(f)
        else:
            # Interactive mode or use command-line args
            print("Resume builder requires an input JSON file with your information.")
            print("Use --input-file to provide a JSON file.")
            print("\nExample JSON structure:")
            print(json.dumps({
                "experiences": [
                    {
                        "title": "Software Engineer",
                        "company": "Tech Corp",
                        "duration": "2020-2024",
                        "description": "Developed web applications..."
                    }
                ],
                "skills": ["Python", "JavaScript", "React"],
                "education": [
                    {
                        "degree": "BS Computer Science",
                        "institution": "University",
                        "year": "2020",
                        "details": "GPA: 3.8"
                    }
                ],
                "portfolio": [
                    {
                        "name": "Project Name",
                        "description": "Project description..."
                    }
                ],
                "target_job": "Software Engineer"
            }, indent=2))
            return
        
        experiences = data.get("experiences", [])
        skills = data.get("skills", [])
        education = data.get("education", [])
        portfolio = data.get("portfolio", [])
        target_job = data.get("target_job")
        
        print("Building optimized resume...")
        print("=" * 60)
        
        try:
            result = self.resume_builder.build_resume(
                experiences=experiences,
                skills=skills,
                education=education,
                portfolio_items=portfolio,
                target_job=target_job,
                output_format=args.format or "docx",
                user_id=self.current_user_id,
            )
            
            print(f"\n✅ Resume created successfully!")
            print(f"📄 File: {result['file_path']}")
            print(f"📊 Format: {result['format']}")
            
            if args.output:
                output_path = Path(args.output)
                with open(output_path, "w") as f:
                    json.dump({
                        "file_path": result["file_path"],
                        "format": result["format"],
                        "resume_data": result["resume_data"],
                    }, f, indent=2, default=str)
                print(f"📋 Metadata saved to: {output_path}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def handle_auth(self, args):
        """Handle authentication commands"""
        if not self.user_manager:
            print("Authentication is disabled")
            return
        
        if args.action == "register":
            try:
                user = self.user_manager.create_user(
                    username=args.username,
                    password=args.password,
                    email=args.email,
                )
                print(f"✅ User created: {user['username']}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
        
        elif args.action == "login":
            user = self.user_manager.authenticate_user(
                username=args.username,
                password=args.password,
            )
            if user:
                session_id = self.user_manager.create_session(user["user_id"])
                self.current_user_id = user["user_id"]
                print(f"✅ Logged in as: {user['username']}")
                print(f"Session ID: {session_id}")
            else:
                print("❌ Invalid username or password")
        
        elif args.action == "logout":
            self.current_user_id = None
            print("✅ Logged out")
    
    def run(self):
        """Run the CLI"""
        parser = argparse.ArgumentParser(
            description="My Personal Agent - Your AI-powered personal assistant",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Vehicle diagnostics
  python -m src.my_personal_agent.cli vehicle --image car_dashboard.jpg --description "Car won't start"
  
  # Resume analysis
  python -m src.my_personal_agent.cli analyze-resume --resume my_resume.pdf --job-description "Software Engineer position..."
  
  # Build resume
  python -m src.my_personal_agent.cli build-resume --input-file resume_data.json
            """
        )
        
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Vehicle diagnostics
        vehicle_parser = subparsers.add_parser("vehicle", help="Diagnose vehicle issues from images")
        vehicle_parser.add_argument("--image", required=True, help="Path to vehicle/dashboard image")
        vehicle_parser.add_argument("--description", help="Additional description of the issue")
        vehicle_parser.add_argument("--include-contacts", action="store_true", default=True, help="Include emergency contacts")
        vehicle_parser.add_argument("--output", help="Save full analysis to JSON file")
        
        # Resume analysis
        analyze_parser = subparsers.add_parser("analyze-resume", help="Analyze resume against job description")
        analyze_parser.add_argument("--resume", required=True, help="Path to resume file (PDF/DOCX/TXT)")
        analyze_parser.add_argument("--job-description", required=True, help="Job description text or file path")
        analyze_parser.add_argument("--output", help="Save analysis to JSON file")
        
        # Resume builder
        build_parser = subparsers.add_parser("build-resume", help="Build optimized resume from data")
        build_parser.add_argument("--input-file", required=True, help="JSON file with experiences, skills, education")
        build_parser.add_argument("--format", choices=["docx", "txt"], default="docx", help="Output format")
        build_parser.add_argument("--output", help="Save metadata to JSON file")
        
        # Authentication
        if settings.enable_auth:
            auth_parser = subparsers.add_parser("auth", help="User authentication")
            auth_parser.add_argument("action", choices=["register", "login", "logout"], help="Authentication action")
            auth_parser.add_argument("--username", help="Username")
            auth_parser.add_argument("--password", help="Password")
            auth_parser.add_argument("--email", help="Email (for registration)")
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        # Route to appropriate handler
        if args.command == "vehicle":
            self.handle_vehicle_diagnosis(args)
        elif args.command == "analyze-resume":
            self.handle_resume_analysis(args)
        elif args.command == "build-resume":
            self.handle_resume_build(args)
        elif args.command == "auth":
            self.handle_auth(args)
        else:
            parser.print_help()


def main():
    """Main entry point"""
    cli = PersonalAgentCLI()
    cli.run()


if __name__ == "__main__":
    main()

