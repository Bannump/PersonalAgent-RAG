"""
Text processing utilities for resume and document analysis
"""
import re
from typing import List, Dict, Set, Any
from collections import Counter


class TextProcessor:
    """Text processing utilities for resume analysis"""
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 4) -> List[str]:
        """Extract ATS-relevant technical keywords from text (filters out generic words)"""
        # Remove special characters and split
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Comprehensive stop words list for ATS matching
        # Focuses on filtering out generic English words to highlight technical terms
        stop_words = {
            # Basic articles and prepositions
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "must", "can", "this", "that",
            "these", "those", "i", "you", "he", "she", "it", "we", "they",
            # Common verbs
            "get", "got", "use", "used", "work", "worked", "make", "made", "take", "took",
            "see", "saw", "know", "knew", "think", "thought", "come", "came", "go", "went",
            "want", "like", "said", "say", "need", "try", "tried", "help", "call", "called",
            "apply", "applies", "applied", "application", "applications", "provide", "provides", "provided",
            "create", "creates", "created", "develop", "develops", "developing", "built",
            "build", "builds", "design", "designs", "designed", "implement", "implements",
            "implemented", "manage", "manages", "managed", "lead", "leads", "led",
            # Common adjectives and adverbs
            "able", "about", "according", "accurately", "actually", "addition", "affordable",
            "agency", "agents", "all", "always", "among", "analytical", "any", "anyone",
            "anything", "appropriate", "around", "available", "back", "before", "being",
            "below", "between", "beyond", "better", "best", "big", "both", "each", "early",
            "either", "enough", "even", "ever", "every", "everyone", "everything", "except",
            "few", "first", "following", "further", "general", "given", "good", "great",
            "high", "how", "important", "instead", "into", "its", "itself", "last", "later",
            "least", "little", "long", "many", "more", "most", "much", "new", "next",
            "old", "once", "only", "onto", "other", "over", "own", "part", "perhaps",
            "rather", "right", "same", "several", "since", "some", "someone", "something",
            "still", "such", "than", "their", "them", "then", "there", "these", "they",
            "this", "those", "through", "throughout", "time", "together", "too", "toward",
            "towards", "two", "under", "until", "upon", "usually", "very", "well", "what",
            "when", "where", "which", "who", "will", "within", "without", "year",
            # Generic business/process words that don't add technical value
            "ability", "academic", "access", "account", "achieve", "action", "active",
            "activity", "address", "advance", "advantage", "advertise", "affect",
            "after", "again", "against", "agree", "allow", "almost", "along", "already",
            "also", "although", "amount", "another", "answer", "appear", "approach",
            "area", "argue", "around", "arrive", "article", "ask", "assume", "author",
            "avoid", "away", "baby", "back", "bad", "bag", "ball", "bank", "base",
            "basic", "battle", "bear", "beat", "beautiful", "because", "become",
            "bed", "begin", "behavior", "behind", "believe", "belong", "below",
            "benefit", "best", "better", "between", "beyond", "bill", "billion",
            "bit", "black", "blood", "blue", "board", "body", "book", "born",
            "both", "boy", "break", "bring", "brother", "budget", "build", "building",
            "bunch", "business", "busy", "but", "buy", "by", "call", "camera",
            "campaign", "can", "cancer", "candidate", "capital", "car", "card",
            "care", "career", "carry", "case", "cash", "cast", "cat", "catch",
            "cause", "cell", "center", "central", "century", "certain", "certainly",
            "chair", "challenge", "chance", "change", "character", "charge", "check",
            "child", "choice", "choose", "church", "citizen", "city", "civil",
            "claim", "class", "clear", "clearly", "close", "coach", "cold",
            "collection", "college", "color", "come", "commercial", "common",
            "community", "company", "compare", "computer", "concern", "condition",
            "conference", "Congress", "consider", "consumer", "contain", "continue",
            "control", "cost", "could", "country", "couple", "course", "court",
            "cover", "create", "crime", "cultural", "culture", "cup", "current",
            "cut", "dark", "data", "daughter", "day", "dead", "deal", "death",
            "debate", "decade", "decide", "decision", "deep", "defense", "degree",
            "Democrat", "democratic", "describe", "design", "despite", "detail",
            "determine", "develop", "development", "die", "difference", "different",
            "difficult", "dinner", "direction", "director", "discover", "discuss",
            "discussion", "disease", "do", "doctor", "dog", "door", "down", "draw",
            "dream", "drive", "drop", "drug", "during", "each", "early", "east",
            "easy", "eat", "economic", "economy", "edge", "education", "effect",
            "effort", "eight", "either", "election", "else", "employee", "end",
            "energy", "enjoy", "enough", "enter", "entire", "environment", "environmental",
            "especially", "establish", "even", "evening", "event", "ever", "every",
            "everybody", "everyone", "everything", "evidence", "exactly", "example",
            "executive", "exist", "expect", "experience", "expert", "explain", "eye",
            "face", "fact", "factor", "fail", "fall", "family", "far", "fast",
            "father", "fear", "federal", "feel", "feeling", "few", "field", "fight",
            "figure", "fill", "film", "final", "finally", "financial", "find",
            "fine", "finger", "finish", "fire", "firm", "first", "fish", "five",
            "floor", "fly", "focus", "follow", "food", "foot", "for", "force",
            "foreign", "forget", "form", "former", "forward", "four", "free",
            "friend", "from", "front", "full", "fund", "future", "game", "garden",
            "gas", "general", "generation", "get", "girl", "give", "glass", "go",
            "goal", "good", "government", "great", "green", "ground", "group",
            "grow", "growth", "guess", "gun", "guy", "hair", "half", "hand",
            "hang", "happen", "happy", "hard", "have", "he", "head", "health",
            "hear", "heart", "heat", "heavy", "help", "her", "here", "herself",
            "hi", "high", "him", "himself", "his", "history", "hit", "hold",
            "home", "hope", "hospital", "hot", "hotel", "hour", "house", "how",
            "however", "huge", "human", "hundred", "husband", "I", "idea", "identify",
            "if", "image", "imagine", "impact", "important", "improve", "in",
            "include", "including", "increase", "indeed", "indicate", "individual",
            "industry", "information", "inside", "instead", "institution", "interest",
            "interesting", "international", "interview", "into", "investment", "involve",
            "issue", "it", "item", "its", "itself", "job", "join", "just", "keep",
            "key", "kid", "kill", "kind", "kitchen", "know", "knowledge", "land",
            "language", "large", "last", "late", "later", "laugh", "law", "lawyer",
            "lay", "lead", "leader", "learn", "least", "leave", "left", "leg",
            "legal", "less", "let", "letter", "level", "lie", "life", "light",
            "like", "likely", "line", "list", "listen", "little", "live", "local",
            "long", "look", "lose", "loss", "lot", "love", "low", "machine",
            "magazine", "main", "maintain", "major", "majority", "make", "man",
            "manage", "management", "manager", "many", "market", "marriage", "material",
            "matter", "may", "maybe", "me", "mean", "measure", "media", "medical",
            "meet", "meeting", "member", "memory", "mention", "message", "method",
            "middle", "might", "military", "million", "mind", "minute", "miss",
            "mission", "model", "modern", "moment", "money", "month", "more",
            "morning", "most", "mother", "mouth", "move", "movement", "movie",
            "Mr", "Mrs", "much", "music", "must", "my", "myself", "name", "nation",
            "national", "natural", "nature", "near", "nearly", "necessary", "need",
            "network", "never", "new", "news", "newspaper", "next", "nice", "night",
            "nine", "no", "none", "nor", "north", "not", "note", "nothing", "notice",
            "now", "n't", "number", "occur", "of", "off", "offer", "office",
            "officer", "official", "often", "oh", "oil", "ok", "old", "on", "once",
            "one", "only", "onto", "open", "operation", "opportunity", "option",
            "or", "order", "organization", "other", "others", "our", "out", "outside",
            "over", "own", "owner", "page", "pain", "paint", "painting", "pair",
            "paper", "parent", "part", "participant", "particular", "particularly",
            "partner", "party", "pass", "past", "patient", "pattern", "pay",
            "peace", "people", "per", "perform", "performance", "perhaps", "period",
            "person", "personal", "phone", "physical", "pick", "picture", "piece",
            "place", "plan", "plant", "play", "player", "PM", "point", "police",
            "policy", "political", "politics", "poor", "popular", "population",
            "position", "positive", "possible", "power", "practice", "prepare",
            "present", "president", "pressure", "pretty", "prevent", "price",
            "private", "probably", "problem", "process", "produce", "product",
            "production", "program", "project", "property", "protect", "prove",
            "provide", "public", "pull", "purpose", "push", "put", "quality",
            "question", "quickly", "quite", "race", "radio", "raise", "range",
            "rate", "rather", "reach", "read", "ready", "real", "reality", "realize",
            "really", "reason", "receive", "recent", "recently", "recognize",
            "record", "red", "reduce", "reflect", "region", "relate", "relationship",
            "religious", "remain", "remember", "remove", "report", "represent",
            "Republican", "require", "research", "resource", "respond", "response",
            "responsibility", "rest", "result", "return", "reveal", "rich", "right",
            "rise", "risk", "road", "rock", "role", "room", "rule", "run", "safe",
            "same", "save", "say", "scene", "school", "science", "scientist",
            "score", "sea", "season", "seat", "second", "section", "security",
            "see", "seek", "seem", "sell", "send", "senior", "sense", "series",
            "serious", "serve", "service", "set", "seven", "several", "sex",
            "sexual", "shake", "shall", "shape", "share", "she", "shoot", "short",
            "shot", "should", "shoulder", "show", "side", "sign", "significant",
            "similar", "simple", "simply", "since", "sing", "single", "sister",
            "sit", "site", "situation", "six", "size", "skill", "skin", "small",
            "smile", "so", "social", "society", "soldier", "some", "somebody",
            "someone", "something", "sometimes", "son", "song", "soon", "sort",
            "sound", "source", "south", "southern", "space", "speak", "special",
            "specific", "speech", "spend", "sport", "spring", "staff", "stage",
            "stand", "standard", "star", "start", "state", "statement", "station",
            "stay", "step", "still", "stock", "stop", "store", "story", "strategy",
            "street", "strong", "structure", "student", "study", "stuff", "style",
            "subject", "success", "successful", "such", "suddenly", "suffer",
            "suggest", "summer", "support", "sure", "surface", "system", "table",
            "take", "talk", "task", "tax", "teach", "teacher", "team", "technology",
            "television", "tell", "ten", "tend", "term", "test", "than", "thank",
            "that", "the", "their", "them", "themselves", "then", "theory", "there",
            "these", "they", "thing", "think", "third", "this", "those", "though",
            "thought", "thousand", "threat", "three", "through", "throughout",
            "throw", "thus", "time", "to", "today", "together", "tonight", "too",
            "top", "total", "tough", "toward", "towards", "town", "trade", "traditional",
            "training", "travel", "treat", "treatment", "tree", "trial", "trip",
            "trouble", "true", "truth", "try", "turn", "TV", "two", "type", "under",
            "understand", "unit", "until", "up", "upon", "us", "use", "usually",
            "value", "various", "very", "victim", "view", "violence", "visit",
            "voice", "vote", "wait", "walk", "wall", "want", "war", "watch",
            "water", "way", "we", "weapon", "wear", "week", "weight", "well",
            "west", "western", "what", "whatever", "when", "where", "whether",
            "which", "while", "white", "who", "whole", "whom", "whose", "why",
            "wide", "wife", "will", "win", "wind", "window", "wish", "with",
            "within", "without", "woman", "wonder", "word", "work", "worker",
            "world", "worry", "would", "write", "writer", "wrong", "yard", "yeah",
            "year", "yes", "yet", "you", "young", "your", "yourself"
        }
        
        # Filter: minimum length 4, not in stop words, and contains at least one letter
        keywords = [
            word for word in words 
            if len(word) >= min_length 
            and word not in stop_words
            and word.isalpha()
        ]
        
        return keywords
    
    @staticmethod
    def extract_skills(text: str) -> List[str]:
        """Extract potential skills from text"""
        # Common skill patterns
        skill_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:development|programming|engineering|analysis|design|management|administration)\b',
            r'\b(?:Python|Java|JavaScript|C\+\+|C#|SQL|HTML|CSS|React|Angular|Vue|Node\.js|Docker|Kubernetes|AWS|Azure|GCP)\b',
        ]
        
        skills = set()
        text_lower = text.lower()
        
        # Extract common technical skills
        common_skills = [
            "python", "java", "javascript", "sql", "html", "css", "react", "angular",
            "vue", "node.js", "docker", "kubernetes", "aws", "azure", "gcp",
            "machine learning", "deep learning", "data science", "agile", "scrum",
            "project management", "git", "linux", "rest api", "graphql", "mongodb",
            "postgresql", "mysql", "redis", "elasticsearch", "tensorflow", "pytorch",
            "pandas", "numpy", "scikit-learn", "tableau", "power bi", "excel",
        ]
        
        for skill in common_skills:
            if skill in text_lower:
                skills.add(skill.title())
        
        # Use regex patterns
        for pattern in skill_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            skills.update(matches)
        
        return sorted(list(skills))
    
    @staticmethod
    def calculate_keyword_match(text1: str, text2: str) -> Dict[str, Any]:
        """Calculate keyword matching between two texts"""
        keywords1 = set(TextProcessor.extract_keywords(text1))
        keywords2 = set(TextProcessor.extract_keywords(text2))
        
        common = keywords1.intersection(keywords2)
        unique_to_text1 = keywords1 - keywords2
        unique_to_text2 = keywords2 - keywords1
        
        match_score = len(common) / len(keywords2) * 100 if keywords2 else 0
        
        return {
            "match_score": round(match_score, 2),
            "common_keywords": sorted(list(common)),
            "missing_keywords": sorted(list(unique_to_text2)),
            "extra_keywords": sorted(list(unique_to_text1)),
            "total_keywords_text1": len(keywords1),
            "total_keywords_text2": len(keywords2),
        }
    
    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """Extract sections from resume text"""
        sections = {}
        current_section = "header"
        current_content = []
        
        lines = text.split("\n")
        
        # Common section headers
        section_patterns = [
            r'^(?:experience|work experience|employment history)',
            r'^(?:education|academic background)',
            r'^(?:skills|technical skills|core competencies)',
            r'^(?:projects|project experience)',
            r'^(?:certifications|certificates)',
            r'^(?:summary|professional summary|objective)',
            r'^(?:achievements|accomplishments)',
        ]
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            is_section_header = False
            for pattern in section_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    # Save previous section
                    if current_content:
                        sections[current_section] = "\n".join(current_content)
                    
                    # Start new section
                    current_section = re.sub(r'[^a-z\s]', '', line.lower()).strip()
                    current_content = []
                    is_section_header = True
                    break
            
            if not is_section_header:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = "\n".join(current_content)
        
        return sections

