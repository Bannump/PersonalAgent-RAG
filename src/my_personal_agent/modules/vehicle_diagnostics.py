"""
Vehicle Diagnostics Module - Analyzes car dashboard images and provides solutions
"""
from typing import Dict, Any, Optional
from pathlib import Path
import re
from src.my_personal_agent.core.rag_engine import RAGEngine
from src.my_personal_agent.core.llm_client import LLMClient


class VehicleDiagnostics:
    """Vehicle diagnostics using vision AI and knowledge base"""
    
    # Common emergency contacts
    EMERGENCY_CONTACTS = {
        "aaa": {
            "name": "AAA Roadside Assistance",
            "phone": "1-800-AAA-HELP (1-800-222-4357)",
            "website": "https://www.aaa.com",
            "services": ["Towing", "Battery jump-start", "Tire change", "Lockout service", "Fuel delivery"]
        },
        "state_farm": {
            "name": "State Farm Roadside Assistance",
            "phone": "1-800-SF-CLAIM (1-800-732-5246)",
            "services": ["24/7 roadside assistance"]
        },
        "geico": {
            "name": "GEICO Emergency Road Service",
            "phone": "1-800-841-3000",
            "services": ["Roadside assistance"]
        },
    }
    
    def __init__(self, rag_engine: Optional[RAGEngine] = None):
        self.rag_engine = rag_engine or RAGEngine()
    
    def diagnose(
        self,
        image_path: str,
        user_description: Optional[str] = None,
        include_contacts: bool = True,
    ) -> Dict[str, Any]:
        """
        Diagnose vehicle issue from dashboard image
        
        Args:
            image_path: Path to the dashboard/car image
            user_description: Optional description of what happened
            include_contacts: Whether to include emergency contact information
        
        Returns:
            Dictionary with diagnosis, solution, and contacts
        """
        # Build diagnostic question
        question = self._build_diagnostic_question(user_description)
        
        # System prompt for vehicle diagnostics
        system_prompt = """You are an expert automotive mechanic and roadside assistance advisor. 
Analyze vehicle dashboard images and provide:
1. Clear diagnosis of the issue (e.g., "Battery is dead" or "Low tire pressure")
2. Immediate action steps (in numbered format)
3. Safety considerations
4. Whether professional help is needed

Be specific and actionable. If you see warning lights, identify them. If the battery is dead, 
suggest using jumper cables and provide instructions, or recommend calling roadside assistance."""
        
        # Get vision analysis
        analysis = self.rag_engine.vision_query(
            question=question,
            image_path=image_path,
            system_prompt=system_prompt,
        )
        
        # Extract diagnosis and solution
        result = {
            "diagnosis": self._extract_diagnosis(analysis),
            "full_analysis": analysis,
            "recommended_actions": self._extract_actions(analysis),
            "needs_professional_help": self._check_needs_professional(analysis),
        }
        
        # Add emergency contacts if needed
        if include_contacts and result["needs_professional_help"]:
            result["emergency_contacts"] = self._get_relevant_contacts(result["diagnosis"])
        
        # Add specific solutions based on diagnosis
        result["detailed_solution"] = self._generate_detailed_solution(result["diagnosis"], analysis)
        
        return result
    
    def _build_diagnostic_question(self, user_description: Optional[str]) -> str:
        """Build the diagnostic question"""
        base_question = (
            "Analyze this vehicle dashboard image. Identify any warning lights, "
            "error messages, or indicators. Provide a diagnosis of what's wrong "
            "and what steps should be taken immediately."
        )
        
        if user_description:
            base_question += f"\n\nAdditional context: {user_description}"
        
        return base_question
    
    def _extract_diagnosis(self, analysis: str) -> str:
        """Extract the main diagnosis from analysis"""
        # Try to find diagnosis in first few sentences
        sentences = analysis.split(". ")
        if sentences:
            # Look for patterns like "The battery is dead" or "Diagnosis: ..."
            for sentence in sentences[:3]:
                sentence_lower = sentence.lower()
                if any(keyword in sentence_lower for keyword in [
                    "battery", "dead", "low", "pressure", "warning", "issue", "problem"
                ]):
                    return sentence.strip()
        
        return sentences[0].strip() if sentences else analysis[:200]
    
    def _extract_actions(self, analysis: str) -> list:
        """Extract action steps from analysis"""
        actions = []
        
        # Look for numbered lists
        lines = analysis.split("\n")
        for line in lines:
            # Match patterns like "1.", "2.", "- ", "* "
            if re.match(r'^\s*[\d\.\-*]\s+', line):
                action = re.sub(r'^\s*[\d\.\-*]+\s+', '', line).strip()
                if action:
                    actions.append(action)
        
        # If no numbered list found, extract from sentences with action verbs
        if not actions:
            sentences = analysis.split(". ")
            for sentence in sentences[:5]:
                sentence = sentence.strip()
                if any(verb in sentence.lower() for verb in [
                    "check", "call", "use", "connect", "start", "replace", "add"
                ]):
                    actions.append(sentence)
        
        return actions[:5]  # Return top 5 actions
    
    def _check_needs_professional(self, analysis: str) -> bool:
        """Check if professional help is recommended"""
        analysis_lower = analysis.lower()
        professional_keywords = [
            "call", "tow", "mechanic", "service", "repair shop",
            "roadside assistance", "professional", "technician"
        ]
        return any(keyword in analysis_lower for keyword in professional_keywords)
    
    def _get_relevant_contacts(self, diagnosis: str) -> list:
        """Get relevant emergency contacts based on diagnosis"""
        diagnosis_lower = diagnosis.lower()
        
        # Determine relevant services
        if "battery" in diagnosis_lower or "dead" in diagnosis_lower:
            service_type = "Battery jump-start or towing"
        elif "tire" in diagnosis_lower or "flat" in diagnosis_lower:
            service_type = "Tire change or towing"
        elif "lockout" in diagnosis_lower or "locked" in diagnosis_lower:
            service_type = "Lockout service"
        elif "fuel" in diagnosis_lower or "gas" in diagnosis_lower:
            service_type = "Fuel delivery"
        else:
            service_type = "General roadside assistance"
        
        # Return AAA as primary (most comprehensive)
        contacts = [{
            **self.EMERGENCY_CONTACTS["aaa"],
            "service_type": service_type,
            "recommended": True,
        }]
        
        return contacts
    
    def _generate_detailed_solution(self, diagnosis: str, analysis: str) -> Dict[str, Any]:
        """Generate detailed solution with step-by-step instructions"""
        diagnosis_lower = diagnosis.lower()
        
        solution = {
            "quick_fix_available": False,
            "steps": [],
            "safety_warnings": [],
        }
        
        # Battery-related solutions
        if "battery" in diagnosis_lower or "dead" in diagnosis_lower:
            solution["quick_fix_available"] = True
            solution["steps"] = [
                "Locate jumper cables and a working vehicle",
                "Position the working vehicle close to your car (not touching)",
                "Turn off both vehicles and engage parking brakes",
                "Connect red jumper cable to positive (+) terminal of dead battery",
                "Connect other end of red cable to positive (+) terminal of working battery",
                "Connect black jumper cable to negative (-) terminal of working battery",
                "Connect other end of black cable to unpainted metal surface on dead car (not battery)",
                "Start the working vehicle and let it run for a few minutes",
                "Try starting the dead vehicle",
                "Once started, remove cables in reverse order",
            ]
            solution["safety_warnings"] = [
                "Never connect negative cable directly to dead battery's negative terminal",
                "Ensure cables don't touch each other during connection",
                "If battery is damaged or leaking, do not attempt jump-start",
            ]
        
        # Tire-related solutions
        elif "tire" in diagnosis_lower or "pressure" in diagnosis_lower:
            solution["quick_fix_available"] = True
            solution["steps"] = [
                "Check tire pressure with a gauge",
                "If low, find nearest gas station with air pump",
                "Add air to recommended PSI (check driver's door jamb)",
                "If flat, use spare tire if available",
            ]
            solution["safety_warnings"] = [
                "Do not drive on severely underinflated tires",
                "Replace spare tire at first opportunity",
            ]
        
        return solution

