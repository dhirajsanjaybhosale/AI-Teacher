import os
import json
import re
import uuid
import datetime
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Type, List, Tuple
from dotenv import load_dotenv

load_dotenv()

# Check available SDKs
_GEMINI_AVAILABLE = False
try:
    import google.generativeai as genai
    _GEMINI_AVAILABLE = True
except ImportError:
    pass

_GROQ_AVAILABLE = False
try:
    from groq import Groq
    _GROQ_AVAILABLE = True
except ImportError:
    pass


class LLMProvider(ABC):
    """
    Abstract Base Class for LLM providers.
    """

    @abstractmethod
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        pass


class GeminiProvider(LLMProvider):
    """
    Google Gemini LLM Provider.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        self.fallback = OfflineProvider()
        print(f"[LLM] GeminiProvider initialized with model: {self.model_name}")

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        try:
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(temperature=temperature)
            )
            return response.text.strip() if response and response.text else ""
        except Exception as e:
            print(f"[GeminiProvider] Text generation error: {e}. Using intelligent fallback.")
            return self.fallback.generate_text(prompt, system_prompt=system_prompt, temperature=temperature)

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        try:
            sys = (system_prompt or "") + "\n\nCRITICAL: Respond ONLY with valid JSON."
            text = self.generate_text(prompt, system_prompt=sys, temperature=0.3)
            parsed = extract_json_from_text(text)
            if parsed:
                return parsed
        except Exception as e:
            print(f"[GeminiProvider] JSON generation error: {e}")
        return self.fallback.generate_json(prompt, system_prompt=system_prompt)


class GroqProvider(LLMProvider):
    """
    Groq LLM Provider.
    """

    def __init__(self, api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key
        self.model_name = model_name
        self.client = Groq(api_key=self.api_key)
        self.fallback = OfflineProvider()
        print(f"[LLM] GroqProvider initialized with model: {self.model_name}")

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model_name,
                temperature=temperature,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[GroqProvider] Text generation error: {e}. Using intelligent fallback.")
            return self.fallback.generate_text(prompt, system_prompt=system_prompt, temperature=temperature)

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        try:
            sys = (system_prompt or "") + "\n\nCRITICAL: Respond ONLY with valid JSON."
            text = self.generate_text(prompt, system_prompt=sys, temperature=0.3)
            parsed = extract_json_from_text(text)
            if parsed:
                return parsed
        except Exception as e:
            print(f"[GroqProvider] JSON generation error: {e}")
        return self.fallback.generate_json(prompt, system_prompt=system_prompt)


class OfflineProvider(LLMProvider):
    """
    Universal Dynamic Educational Intelligence Engine.
    Zero-API-key fallback & robust live demonstration engine.
    Dynamically generates personalized curricula, subject-aware visuals, formative evaluations,
    adaptive remediations, and summative assessments for ANY arbitrary educational topic in English or Hindi.
    """

    def __init__(self):
        print("[LLM] OfflineProvider active. Zero-dependency universal educational engine engaged.")

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        p_lower = prompt.lower()
        if "explain that again" in p_lower or "explain in hindi" in p_lower or "example" in p_lower or "simpler" in p_lower:
            return "Let's look at this step-by-step with a concrete analogy to make the mechanism crystal clear."
        return "This instructional module explores foundational principles step-by-step with intuitive analogies and practical checks."

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        full_prompt = (prompt + "\n" + (system_prompt or ""))
        p_lower = full_prompt.lower()
        is_hinglish = (
            "hinglish" in p_lower or '"language": "hinglish"' in p_lower or
            'target_language: hinglish' in p_lower or '"language": "hinglish"' in (system_prompt or "").lower() or
            'in hinglish' in p_lower or 'hinglish mein' in p_lower
        )
        is_hindi = (
            not is_hinglish and (
                "hindi" in p_lower or '"language": "hi"' in p_lower or
                'target_language: hi' in p_lower or 'हिंदी' in full_prompt or
                'in natural hindi' in p_lower or '"language": "hi"' in (system_prompt or "").lower()
            )
        )

        # -------------------------------------------------------------
        # 1. FOLLOW-UP INTERACTION / ASK TEACHER REQUEST
        # -------------------------------------------------------------
        if "follow-up request" in p_lower or "ask teacher" in p_lower or "user query:" in p_lower or "student inquiry:" in p_lower:
            return self._handle_followup(full_prompt, is_hindi, is_hinglish)

        # -------------------------------------------------------------
        # 2. SUMMATIVE QUIZ GENERATION REQUEST
        # -------------------------------------------------------------
        if "quiz request" in p_lower or ("quiz" in p_lower and "mastery" in p_lower and "questions" in p_lower):
            return self._handle_quiz(full_prompt, is_hindi, is_hinglish)

        # -------------------------------------------------------------
        # 3. FORMATIVE ANSWER EVALUATION REQUEST
        # -------------------------------------------------------------
        if "evaluate the student" in p_lower or "student's submitted answer" in p_lower:
            return self._handle_evaluation(full_prompt, is_hindi, is_hinglish)

        # -------------------------------------------------------------
        # 4. ADAPTIVE REMEDIATION RE-EXPLANATION REQUEST
        # -------------------------------------------------------------
        if "remediation" in p_lower or "create an adaptive remediation" in p_lower or "diagnosed misconception" in p_lower:
            return self._handle_remediation(full_prompt, is_hindi, is_hinglish)

        # -------------------------------------------------------------
        # 5. FINAL REPORT GENERATION REQUEST
        # -------------------------------------------------------------
        if "report request" in p_lower or "final feedback report" in p_lower:
            return self._handle_report(full_prompt, is_hindi, is_hinglish)

        # -------------------------------------------------------------
        # 6. LESSON PLANNING / CURRICULUM SYNTHESIS REQUEST
        # -------------------------------------------------------------
        return self._handle_lesson_plan(full_prompt, is_hindi, is_hinglish)

    def _extract_clean_topic(self, prompt: str) -> Tuple[str, str]:
        """
        Extracts the target topic and grounded context cleanly from the prompt.
        """
        topic = ""
        context = ""

        # Extract grounded context if present
        if "SOURCE MATERIAL / DOCUMENT EXCERPTS" in prompt:
            parts = prompt.split("SOURCE MATERIAL / DOCUMENT EXCERPTS")
            if len(parts) > 1:
                context = parts[1].split('"""')[1] if '"""' in parts[1] else parts[1][:2000]

        # Extract target topic title
        if "lesson plan for: '" in prompt:
            topic = prompt.split("lesson plan for: '")[1].split("'")[0].strip()
        elif "USER TOPIC REQUEST: \"" in prompt:
            topic = prompt.split("USER TOPIC REQUEST: \"")[1].split("\"")[0].strip()
        elif "topic to teach:" in prompt.lower():
            topic = prompt.lower().split("topic to teach:")[1].split("\n")[0].strip()
        elif "lesson:" in prompt.lower():
            topic = prompt.lower().split("lesson:")[1].split("\n")[0].strip()
        elif "report request for lesson:" in prompt.lower():
            topic = prompt.lower().split("report request for lesson:")[1].split("\n")[0].strip()

        if not topic or topic == "Uploaded Document" or topic.endswith(".pdf"):
            # Check context for document title
            if "electricity" in context.lower() or "ohm" in context.lower() or "circuit" in context.lower() or "sample_chapter" in prompt.lower():
                topic = "Introduction to Electricity & Ohm's Law"
            elif "cellular respiration" in context.lower() or "atp" in context.lower() or "glycolysis" in context.lower():
                topic = "Cellular Respiration & ATP Synthase"
            elif "photosynthesis" in context.lower():
                topic = "Photosynthesis & Solar Energy Conversion"
            elif topic.endswith(".pdf"):
                topic = topic.replace('.pdf', '').replace('_', ' ').title()
            else:
                topic = "Foundational Concepts"

        # Clean any trailing garbage
        clean_topic = topic.replace("Mastering ", "").strip()
        return clean_topic, context

    def _detect_subject(self, topic: str, context: str) -> Tuple[str, str]:
        """
        Dynamically classifies subject domain and optimal visual type.
        """
        combined = f"{topic} {context}".lower()

        # 1. Biology & Life Sciences
        if any(w in combined for w in ["photosynthesis", "cellular respiration", "atp", "mitochondria", "dna", "rna", "genetics", "enzyme", "cell", "biology", "chloroplast", "glycolysis", "krebs", "organism"]):
            return "Biology", "diagram"

        # 2. Physics & Physical Sciences
        if any(w in combined for w in ["newton", "inertia", "motion", "force", "acceleration", "f = ma", "gravity", "physics", "quantum", "qubit", "superposition", "wave", "sky blue", "rayleigh", "scattering", "optics", "thermodynamics", "relativity"]):
            if "sky blue" in combined or "rayleigh" in combined or "quantum" in combined or "wave" in combined:
                return "Physics", "diagram"
            return "Physics", "equation"

        # 3. Electricity & Electronics
        if any(w in combined for w in ["electricity", "ohm", "voltage", "current", "resistance", "circuit", "resistor", "kirchhoff", "capacitance", "ampere"]):
            return "Electronics & Physics", "equation"

        # 4. Computer Science & Architecture
        if any(w in combined for w in ["tcp", "udp", "protocol", "network", "networking", "packet", "dbms", "normalization", "1nf", "2nf", "3nf", "bcnf", "database", "sql", "operating system", "process scheduling", "distributed"]):
            if "tcp" in combined or "udp" in combined or "normalization" in combined:
                return "Computer Science", "comparison"
            return "Computer Science", "architecture"

        # 5. Programming & Software Development
        if any(w in combined for w in ["python", "java", "javascript", "c++", "rust", "recursion", "inheritance", "polymorphism", "class", "function", "data structure", "binary tree", "sorting", "algorithm", "coding", "oop"]):
            if "recursion" in combined or "inheritance" in combined or "python" in combined or "java" in combined:
                return "Programming", "code"
            return "Computer Science", "flowchart"

        # 6. AI & Machine Learning
        if any(w in combined for w in ["machine learning", "ml", "neural network", "deep learning", "backpropagation", "loss function", "gradient descent", "ai agents", "llm", "large language model", "transformer", "reinforcement learning", "supervised"]):
            return "AI & Machine Learning", "process"

        # 7. Cryptography & Web3
        if any(w in combined for w in ["blockchain", "proof of work", "bitcoin", "ethereum", "smart contract", "cryptography", "hash", "ledger", "mining"]):
            return "Cryptography & Web3", "architecture"

        # 8. Earth Science & Geography
        if any(w in combined for w in ["water cycle", "evaporation", "precipitation", "hydrological", "climate", "atmosphere", "geography", "plate tectonics", "earth science"]):
            return "Earth Science & Geography", "process"

        # 9. Mathematics
        if any(w in combined for w in ["calculus", "derivative", "integral", "matrix", "linear algebra", "probability", "statistics", "differential", "algebra", "geometry"]):
            return "Mathematics", "equation"

        # 10. History & Social Sciences
        if any(w in combined for w in ["history", "war", "revolution", "empire", "civilization", "renaissance", "timeline"]):
            return "History", "timeline"

        # 11. Economics & Business
        if any(w in combined for w in ["economics", "inflation", "supply and demand", "market", "gdp", "finance", "business"]):
            return "Economics", "comparison"

        return "General Science", "flowchart"

    def _handle_lesson_plan(self, prompt: str, is_hindi: bool, is_hinglish: bool = False) -> Dict[str, Any]:
        topic, context = self._extract_clean_topic(prompt)
        subject, visual_type = self._detect_subject(topic, context)
        t_lower = topic.lower()

        # Parse number of segments requested
        p_lower = prompt.lower()
        num_segments = 2
        for n in [6, 5, 4, 3, 2]:
            if f"{n}-segment" in p_lower or f"exactly {n}" in p_lower or f"{n} instructional segment" in p_lower or f"{n} segment" in p_lower:
                num_segments = n
                break

        is_7_days = any(k in p_lower for k in ["7 days", "7_days", "7-day", "10080"])
        if is_7_days:
            num_segments = 4

        segments = self._generate_domain_segments(topic, subject, visual_type, context, is_hindi, num_segments)
        final_segments = segments[:num_segments] if len(segments) >= num_segments else segments

        # 7-day structured roadmap
        study_roadmap_7_days = None
        if is_7_days:
            study_roadmap_7_days = [
                {
                    "day": 1,
                    "title": f"Foundational Principles & Core Terminology of {topic}",
                    "duration_minutes": 30,
                    "revision_schedule": "Day 2 morning (10 min review)",
                    "practice_goals": f"Define key variables and operational scope of {topic}",
                    "assessment_type": "3 Diagnostic Concept Checks"
                },
                {
                    "day": 2,
                    "title": f"Internal Mechanics & Governing Laws in {topic}",
                    "duration_minutes": 35,
                    "revision_schedule": "Day 3 review flashcards",
                    "practice_goals": "Trace cause-and-effect flow diagrams across input states",
                    "assessment_type": "Formative Mechanism Quiz"
                },
                {
                    "day": 3,
                    "title": f"Real-World Examples & Intuitive Analogies for {topic}",
                    "duration_minutes": 40,
                    "revision_schedule": "Day 4 quick mental model recap",
                    "practice_goals": "Map industrial and practical systems to core theory",
                    "assessment_type": "Case Study Problem Set"
                },
                {
                    "day": 4,
                    "title": f"Mathematical Models, Formulas & Constraint Analysis",
                    "duration_minutes": 45,
                    "revision_schedule": "Day 5 formula sheet verification",
                    "practice_goals": "Solve parametric equations and boundary trade-offs",
                    "assessment_type": "Calculation & Analytical Drill"
                },
                {
                    "day": 5,
                    "title": f"Comparative Trade-offs & Architecture Patterns",
                    "duration_minutes": 40,
                    "revision_schedule": "Day 6 comparative matrix review",
                    "practice_goals": "Compare competing approaches and design patterns",
                    "assessment_type": "Scenario Comparison Assessment"
                },
                {
                    "day": 6,
                    "title": f"Edge Cases, Misconception Debugging & Remediation",
                    "duration_minutes": 45,
                    "revision_schedule": "Day 7 pre-exam recap",
                    "practice_goals": "Identify and unblock common student traps and errors",
                    "assessment_type": "Troubleshooting & Error Identification"
                },
                {
                    "day": 7,
                    "title": f"Comprehensive Summative Mastery & Practical Project",
                    "duration_minutes": 60,
                    "revision_schedule": "Weekly retention check",
                    "practice_goals": f"End-to-end mastery synthesis and application in {topic}",
                    "assessment_type": "Final Mastery Certification Exam (5 Multi-format Questions)"
                }
            ]

        # Multi-node learning path
        learning_path = [
            {"step": 1, "topic": f"{topic} Fundamentals", "status": "completed", "difficulty": "beginner"},
            {"step": 2, "topic": f"{topic} Operational Dynamics", "status": "current", "difficulty": "intermediate"},
            {"step": 3, "topic": f"{topic} Practical Applications", "status": "upcoming", "difficulty": "intermediate"},
            {"step": 4, "topic": f"Advanced {topic} Systems", "status": "upcoming", "difficulty": "advanced"},
            {"step": 5, "topic": f"Mastery Assessment & Capstone", "status": "upcoming", "difficulty": "advanced"}
        ]

        title = f"{topic} (हिंदी पाठ)" if is_hindi else (f"{topic} (Hinglish)" if is_hinglish else f"Mastering {topic}")
        target_lang = "hi" if is_hindi else ("hinglish" if is_hinglish else "en")

        return {
            "lesson_id": f"lesson_{uuid.uuid4().hex[:8]}",
            "title": title,
            "subject": subject,
            "description": f"{topic} के मुख्य सिद्धांतों और व्यावहारिक अनुप्रयोगों पर एक संवादात्मक मास्टरक्लास।" if is_hindi else (f"{topic} ki core concepts aur practical applications par live interactive lesson." if is_hinglish else f"An intuitive, structured interactive masterclass on {topic}."),
            "learning_objectives": [
                f"{topic} के मूलभूत सिद्धांतों को समझना" if is_hindi else f"Understand the foundational principles of {topic}",
                "कार्यात्मक तंत्र और व्यावहारिक उदाहरणों का विश्लेषण करना" if is_hindi else "Analyze operational mechanisms and real-world trade-offs",
                "प्रश्नों के माध्यम से अवधारणा की पुष्टि करना" if is_hindi else "Verify conceptual mastery through formative checks"
            ],
            "target_level": "beginner",
            "target_language": target_lang,
            "estimated_minutes": 10080 if is_7_days else (5 * len(final_segments)),
            "goal": "understand",
            "source_type": "pdf" if context else "topic",
            "source_name": topic,
            "segments": final_segments,
            "study_roadmap_7_days": study_roadmap_7_days,
            "learning_path": learning_path
        }

    def _generate_domain_segments(self, topic: str, subject: str, visual_type: str, context: str, is_hindi: bool, count: int) -> List[Dict[str, Any]]:
        t_lower = topic.lower()

        # -------------------------------------------------------------
        # DOMAIN 1: PHOTOSYNTHESIS (Biology)
        # -------------------------------------------------------------
        if "photosynthesis" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "प्रकाश संश्लेषण के मूल सिद्धांत: प्रकाश अभिक्रिया" if is_hindi else "Photosynthesis Foundations: Light Reactions",
                    "explanation": "नमस्ते! प्रकाश संश्लेषण वह प्रक्रिया है जिससे पौधे सूर्य के प्रकाश, जल और कार्बन डाइऑक्साइड को ग्लूकोज और ऑक्सीजन में बदलते हैं।" if is_hindi else "Welcome! Photosynthesis is the biological engine where plants capture solar photons, water, and carbon dioxide to synthesize glucose and release oxygen.",
                    "example": "जैसे सोलर पैनल धूप से बिजली बनाते हैं, वैसे ही क्लोरोफिल सूर्य की ऊर्जा से रासायनिक ऊर्जा बनाता है।" if is_hindi else "Think of a leaf as a solar-powered bakery: chlorophyll panels absorb sunlight to bake glucose sugar from air and water.",
                    "key_points": [
                        "क्लोरोफिल सूर्य के प्रकाश को अवशोषित करता है" if is_hindi else "Chlorophyll absorbs solar photon energy in thylakoids",
                        "रासायनिक समीकरण: 6CO2 + 6H2O -> C6H12O6 + 6O2" if is_hindi else "Balanced Equation: 6CO2 + 6H2O + Sunlight -> C6H12O6 + 6O2",
                        "ऑक्सीजन एक महत्वपूर्ण सह-उत्पाद के रूप में निकलती है" if is_hindi else "Water splitting (photolysis) releases vital oxygen (O2)"
                    ],
                    "visual_diagram_type": "equation",
                    "visual_description": "Solar Photons + 6CO2 + 6H2O ===> C6H12O6 (Glucose) + 6O2",
                    "visual_code_or_math": "6 CO2 + 6 H2O + Light Energy ===> C6H12O6 + 6 O2",
                    "question": {
                        "id": "q_1",
                        "question_text": "प्रकाश संश्लेषण की प्रकाश अभिक्रिया में ऑक्सीजन (O2) का प्राथमिक स्रोत क्या है?" if is_hindi else "What is the direct molecular source of oxygen gas (O2) released during photosynthesis?",
                        "options": [
                            "जल के अणुओं का विभाजन (Photolysis of H2O)" if is_hindi else "The photolysis (splitting) of water molecules (H2O)",
                            "कार्बन डाइऑक्साइड का अवशोषण" if is_hindi else "Direct breakdown of atmospheric nitrogen",
                            "मिट्टी से खनिजों का अवशोषण" if is_hindi else "Absorption of soil nitrates",
                            "हवा में मौजूद धूल के कण" if is_hindi else "Decomposition of cellular glucose"
                        ],
                        "correct_answer": "जल के अणुओं का विभाजन (Photolysis of H2O)" if is_hindi else "The photolysis (splitting) of water molecules (H2O)",
                        "hint": "Think about splitting H2O to harvest electrons.",
                        "explanation": "Light energy splits water molecules (H2O) into protons, electrons, and oxygen gas."
                    }
                },
                {
                    "id": "seg_2",
                    "title": "केल्विन चक्र और ग्लूकोज संश्लेषण" if is_hindi else "The Calvin Cycle: Carbon Fixation & Glucose Synthesis",
                    "explanation": "केल्विन चक्र स्ट्रोमा में होता है जहां ATP और NADPH का उपयोग करके CO2 को ऊर्जा से भरपूर ग्लूकोज में बदला जाता है।" if is_hindi else "The light-independent Calvin cycle operates in the chloroplast stroma, utilizing ATP and NADPH from light reactions to fix CO2 into glucose.",
                    "example": "जैसे बैटरी की चार्ज ऊर्जा से खिलौना चलता है, वैसे ही ATP ऊर्जा से शर्करा बनती है।" if is_hindi else "Like charging chemical batteries during the day, then using that stored energy to construct durable goods.",
                    "key_points": [
                        "रुबिस्को (RuBisCO) एंजाइम कार्बन स्थिरीकरण करता है" if is_hindi else "RuBisCO enzyme catalyzes carbon fixation",
                        "ATP और NADPH रासायनिक ऊर्जा प्रदान करते हैं" if is_hindi else "ATP & NADPH drive sugar assembly",
                        "ग्लूकोज पौधों का प्राथमिक ईंधन है" if is_hindi else "Synthesizes G3P building blocks for starch & cellulose"
                    ],
                    "visual_diagram_type": "process",
                    "visual_description": "CO2 Fixation -> Carbon Reduction -> RuBP Regeneration -> Glucose Output",
                    "visual_code_or_math": "3 CO2 + 9 ATP + 6 NADPH -> G3P (Glucose Precursor)",
                    "question": {
                        "id": "q_2",
                        "question_text": "केल्विन चक्र (Calvin Cycle) में कार्बन डाइऑक्साइड को स्थिर करने वाला प्रमुख एंजाइम कौन सा है?" if is_hindi else "Which critical enzyme catalyzes the carbon fixation step in the Calvin cycle?",
                        "options": [
                            "रुबिस्को (RuBisCO)" if is_hindi else "RuBisCO (Ribulose-1,5-bisphosphate carboxylase-oxygenase)",
                            "डीएनए पॉलीमरेज" if is_hindi else "DNA Polymerase",
                            "पेप्सिन" if is_hindi else "Pepsin",
                            "एमाइलेज" if is_hindi else "Amylase"
                        ],
                        "correct_answer": "रुबिस्को (RuBisCO)" if is_hindi else "RuBisCO (Ribulose-1,5-bisphosphate carboxylase-oxygenase)",
                        "hint": "The most abundant enzyme on Earth, fixing CO2.",
                        "explanation": "RuBisCO fixes atmospheric CO2 into organic 3-PGA molecules in the stroma."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 2: RECURSION (Programming & CS)
        # -------------------------------------------------------------
        if "recursion" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "रिकर्सन के मूल सिद्धांत: बेस केस और कॉल स्टैक" if is_hindi else "Recursion Foundations: Base Cases & Call Stack",
                    "explanation": "नमस्ते! रिकर्सन एक ऐसी प्रोग्रामिंग तकनीक है जिसमें कोई फंक्शन किसी बड़ी समस्या को छोटी उप-समस्याओं में बांटकर खुद को ही कॉल करता है।" if is_hindi else "Welcome! Recursion is a programming paradigm where a function solves a problem by calling smaller instances of itself until reaching a termination base case.",
                    "example": "रूसी नेस्टिंग गुड़िया (Matryoshka) की तरह: हर गुड़िया के अंदर एक छोटी गुड़िया होती है जब तक कि सबसे छोटी गुड़िया न आ जाए।" if is_hindi else "Think of Russian nesting dolls (Matryoshka): opening each doll reveals a smaller doll inside until you reach the solid, smallest doll (base case).",
                    "key_points": [
                        "बेस केस (Base Case) अनंतीय लूप को रोकता है" if is_hindi else "Base Case: Mandatory condition that halts recursion",
                        "रिकर्सिव स्टेप समस्या को छोटा करता है" if is_hindi else "Recursive Step: Reduces problem toward the base case",
                        "कॉल स्टैक (Call Stack) मेमोरी में फ्रेम सहेजता है" if is_hindi else "Call Stack: LIFO memory frames pushed and popped"
                    ],
                    "visual_diagram_type": "code",
                    "visual_description": "def factorial(n): return 1 if n <= 1 else n * factorial(n - 1)",
                    "visual_code_or_math": "def factorial(n):\n    if n <= 1: return 1  # Base Case\n    return n * factorial(n - 1)  # Recursive Step",
                    "question": {
                        "id": "q_1",
                        "question_text": "रिकर्सिव फंक्शन में बेस केस (Base Case) क्यों अनिवार्य है?" if is_hindi else "What happens if a recursive function lacks a valid Base Case?",
                        "options": [
                            "यह स्टैक ओवरफ्लो एरर (Stack Overflow Error) पैदा करेगा" if is_hindi else "It causes infinite recursion and a Stack Overflow error",
                            "फंक्शन बहुत तेज चलेगा" if is_hindi else "The program instantly optimizes execution speed",
                            "सभी वेरिएबल्स अपने आप शून्य हो जाएंगे" if is_hindi else "Memory usage drops to zero bytes",
                            "फंक्शन बिना चले ही बंद हो जाएगा" if is_hindi else "The compiler converts it to a binary tree"
                        ],
                        "correct_answer": "यह स्टैक ओवरफ्लो एरर (Stack Overflow Error) पैदा करेगा" if is_hindi else "It causes infinite recursion and a Stack Overflow error",
                        "hint": "Without a stop condition, stack memory is exhausted.",
                        "explanation": "Without a base case, recursion executes indefinitely until the call stack memory is depleted."
                    }
                },
                {
                    "id": "seg_2",
                    "title": "स्टैक अनवाइंडिंग और डिवाइड एंड कॉन्कर" if is_hindi else "Stack Unwinding & Divide-and-Conquer Strategies",
                    "explanation": "जब बेस केस मिल जाता है, तो कॉल स्टैक पीछे की ओर परिणाम लौटाता है जिसे स्टैक अनवाइंडिंग कहते हैं।" if is_hindi else "Once the base case executes, the call stack unwinds in reverse order, combining intermediate returns into the final answer.",
                    "example": "सीढ़ियों से नीचे उतरकर चाबी उठाना (बेस केस) और फिर वापस ऊपर आकर दरवाजा खोलना।" if is_hindi else "Descending a staircase to pick up an item at the bottom (base case), then stepping back up with the item in hand.",
                    "key_points": [
                        "एलआईएफओ (LIFO) क्रम में स्टैक का खाली होना" if is_hindi else "LIFO Unwinding: Last-In, First-Out frame resolution",
                        "टेल रिकर्सन (Tail Recursion) अनुकूलन" if is_hindi else "Tail-call optimization reuses stack frames",
                        "मर्ज सॉर्ट और ट्री ट्रैवर्सल में उपयोग" if is_hindi else "Powers Divide-and-Conquer (MergeSort, QuickSort, Tree traversal)"
                    ],
                    "visual_diagram_type": "process",
                    "visual_description": "factorial(3) -> 3 * factorial(2) -> 2 * factorial(1) [BASE] -> Unwind: 1 -> 2 -> 6",
                    "visual_code_or_math": "Call: f(3) -> f(2) -> f(1) | Return: 1 -> 2 -> 6",
                    "question": {
                        "id": "q_2",
                        "question_text": "रिकर्सिव कॉल में परिणाम किस क्रम में वापस (Unwind) होते हैं?" if is_hindi else "In what order do stack frames resolve during recursive stack unwinding?",
                        "options": [
                            "अंतिम कॉल सबसे पहले हल होती है (LIFO - Last In First Out)" if is_hindi else "Last-In, First-Out (LIFO): The deepest base call resolves first",
                            "पहली कॉल सबसे पहले हल होती है" if is_hindi else "First-In, First-Out (FIFO)",
                            "रैंडम क्रम में" if is_hindi else "Random non-deterministic order",
                            "केवल एक साथ एक ही फ्रेम में" if is_hindi else "All frames resolve simultaneously without order"
                        ],
                        "correct_answer": "अंतिम कॉल सबसे पहले हल होती है (LIFO - Last In First Out)" if is_hindi else "Last-In, First-Out (LIFO): The deepest base call resolves first",
                        "hint": "The most recent call on top of the stack finishes first.",
                        "explanation": "Call stacks operate strictly on LIFO principles; the base case returns to its immediate caller."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 3: BLOCKCHAIN & CRYPTOGRAPHY
        # -------------------------------------------------------------
        if "blockchain" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "ब्लॉकचेन के मूल सिद्धांत: विकेंद्रीकृत लेजर" if is_hindi else "Blockchain Foundations: Decentralized Immutable Ledgers",
                    "explanation": "नमस्ते! ब्लॉकचेन एक वितरित और अपरिवर्तनीय डिजिटल लेजर है जिसमें लेनदेन को क्रिप्टोग्राफिक हैश के माध्यम से ब्लॉकों की श्रृंखला में सुरक्षित किया जाता है।" if is_hindi else "Welcome! Blockchain is a decentralized, distributed, and cryptographically secured ledger where transactions are bundled into immutable linked blocks.",
                    "example": "एक ऐसी डिजिटल Google शीट जिसे दुनिया भर के हजारों कंप्यूटर एक साथ सत्यापित करते हैं, और किसी पुरानी प्रविष्टि को बदला नहीं जा सकता।" if is_hindi else "Think of a shared digital spreadsheet replicated across thousands of independent auditors: once an entry is added, no single entity can alter past records.",
                    "key_points": [
                        "क्रिप्टोग्राफिक हैशिंग (SHA-256) डेटा सुरक्षा देती है" if is_hindi else "Cryptographic Hashing (e.g. SHA-256) ensures tamper-evidence",
                        "प्रत्येक ब्लॉक पिछले ब्लॉक का हैश रखता है" if is_hindi else "Each block contains the cryptographic hash of the previous block",
                        "विकेंद्रीकरण बिचौलियों की आवश्यकता समाप्त करता है" if is_hindi else "Decentralized consensus eliminates central points of failure"
                    ],
                    "visual_diagram_type": "architecture",
                    "visual_description": "Block N-1 [Hash, Merkle Root] <=== Linked === Block N [PrevHash, Nonce, Data] <=== Block N+1",
                    "visual_code_or_math": "Block_Hash = SHA256(Prev_Hash + Merkle_Root + Timestamp + Nonce)",
                    "question": {
                        "id": "q_1",
                        "question_text": "यदि कोई ब्लॉकचेन के किसी पुराने ब्लॉक में डेटा बदलने की कोशिश करे, तो क्या होगा?" if is_hindi else "What happens if a malicious actor attempts to tamper with data in an earlier block?",
                        "options": [
                            "उस ब्लॉक और उसके बाद के सभी ब्लॉकों के हैश बदल जाएंगे और नेटवर्क उसे अस्वीकार कर देगा" if is_hindi else "The block's hash changes, breaking all subsequent chain links and causing network rejection",
                            "पूरा नेटवर्क अपने आप बंद हो जाएगा" if is_hindi else "The entire blockchain automatically deletes itself",
                            "डेटा बिना किसी सूचना के बदल जाएगा" if is_hindi else "The modification succeeds silently without detection",
                            "सभी कंप्यूटरों की मेमोरी डिलीट हो जाएगी" if is_hindi else "Hardware CPU clocks desynchronize"
                        ],
                        "correct_answer": "उस ब्लॉक और उसके बाद के सभी ब्लॉकों के हैश बदल जाएंगे और नेटवर्क उसे अस्वीकार कर देगा" if is_hindi else "The block's hash changes, breaking all subsequent chain links and causing network rejection",
                        "hint": "Hashes are chained; changing one invalidates all downstream blocks.",
                        "explanation": "Because each block references the previous hash, altering any historical block invalidates the entire subsequent chain."
                    }
                },
                {
                    "id": "seg_2",
                    "title": "सर्वसम्मति तंत्र: प्रूफ ऑफ वर्क और सुरक्षा" if is_hindi else "Consensus Mechanisms: Proof of Work & Cryptographic Trust",
                    "explanation": "प्रूफ ऑफ वर्क (Proof of Work) में नोड्स गणितीय पहेली को हल करने के लिए कम्प्यूटेशनल पावर का उपयोग करते हैं जिससे नए ब्लॉक जुड़ते हैं।" if is_hindi else "Proof of Work utilizes computational work (mining) to achieve decentralized agreement on the valid state of the ledger without trusting a central authority.",
                    "example": "जैसे तिजोरी का सही संयोजन (Combination) खोजने के लिए लाखों संभावित नंबरों को तेजी से आजमाना।" if is_hindi else "Like rolling a combination lock millions of times per second until discovering the unique number (nonce) that produces the required pattern of leading zeros.",
                    "key_points": [
                        "नॉन्स (Nonce) खोजने की कम्प्यूटेशनल प्रतियोगिता" if is_hindi else "Miners compete to find a valid Nonce satisfying difficulty target",
                        "51% हमले से सुरक्षा" if is_hindi else "51% attack resistance through distributed compute",
                        "स्मार्ट कॉन्ट्रैक्ट्स प्रोग्राम करने योग्य ट्रस्ट देते हैं" if is_hindi else "Smart contracts enable programmable autonomous agreements"
                    ],
                    "visual_diagram_type": "process",
                    "visual_description": "Transactions -> Mempool -> Mining (Nonce Search) -> Difficulty Target Met -> Block Broadcast -> Consensus",
                    "visual_code_or_math": "while SHA256(BlockHeader + Nonce) > Target: Nonce += 1",
                    "question": {
                        "id": "q_2",
                        "question_text": "प्रूफ ऑफ वर्क (Proof-of-Work) माइनिंग में 'नॉन्स' (Nonce) का क्या कार्य है?" if is_hindi else "What is the primary role of the 'Nonce' in Proof-of-Work block mining?",
                        "options": [
                            "एक ऐसा परिवर्तनशील संख्या मान जिसे बदलकर लक्ष्य से छोटा हैश खोजा जाता है" if is_hindi else "An arbitrary integer varied by miners to produce a hash below the difficulty target",
                            "डेटाबेस का स्थायी पासवर्ड" if is_hindi else "The permanent master encryption key for the network",
                            "लेनदेन की कुल मुद्रा राशि" if is_hindi else "The total transaction fee amount",
                            "ब्लॉक को तुरंत डिलीट करने का कोड" if is_hindi else "A command that pauses the blockchain network"
                        ],
                        "correct_answer": "एक ऐसा परिवर्तनशील संख्या मान जिसे बदलकर लक्ष्य से छोटा हैश खोजा जाता है" if is_hindi else "An arbitrary integer varied by miners to produce a hash below the difficulty target",
                        "hint": "Number used once to vary the hash output.",
                        "explanation": "Miners iteratively increment the nonce until the resulting block hash satisfies the difficulty target."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 4: TCP VS UDP (Networking & CS)
        # -------------------------------------------------------------
        if "tcp" in t_lower or "udp" in t_lower or "packet" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "टीसीपी बनाम यूडीपी: कनेक्शन और विश्वसनीयता" if is_hindi else "TCP vs UDP: Reliability vs Low-Latency Streaming",
                    "explanation": "नमस्ते! टीसीपी एक कनेक्शन-उन्मुख और विश्वसनीय प्रोटोकॉल है जो 3-वे हैंडशेक से डेटा अखंडता सुनिश्चित करता है, जबकि यूडीपी तीव्र गति के लिए बिना कनेक्शन के पैकेट भेजता है।" if is_hindi else "Welcome! TCP is a connection-oriented, reliable transport protocol that guarantees ordered packet delivery via 3-way handshakes and acknowledgments, whereas UDP is a connectionless, low-latency protocol optimized for speed.",
                    "example": "टीसीपी एक पंजीकृत डाक (रसीद हस्ताक्षर सहित) की तरह है; यूडीपी लाउडस्पीकर पर लाइव घोषणा की तरह है जहां तात्कालिकता मुख्य है।" if is_hindi else "TCP is like registered certified mail with signature receipts; UDP is like a live radio broadcast where missing a split-second frame is preferred over halting the live stream.",
                    "key_points": [
                        "टीसीपी (TCP): 3-वे हैंडशेक (SYN, SYN-ACK, ACK), पुन: प्रसारण, प्रवाह नियंत्रण" if is_hindi else "TCP: 3-Way Handshake, Guaranteed Delivery, In-Order, Flow Control",
                        "यूडीपी (UDP): कनेक्शन रहित, शून्य ओवरहेड, अति तीव्र गति" if is_hindi else "UDP: Connectionless, Minimal Header (8 bytes), Zero Resend Overhead",
                        "उपयोग: टीसीपी (वेब/ईमेल/फाइल), यूडीपी (गेमिंग/वीडियो कॉल/डीएनएस)" if is_hindi else "Use Cases: TCP for Web/HTTP/Files; UDP for Gaming/VoIP/Live Video"
                    ],
                    "visual_diagram_type": "comparison",
                    "visual_description": "TCP (SYN -> SYN-ACK -> ACK -> Data -> ACK) vs UDP (Client -> Packet -> Server Direct)",
                    "visual_code_or_math": "TCP: Reliable + Ordered + Heavy Header (20B) <---> UDP: Fast + Unreliable + Lean Header (8B)",
                    "question": {
                        "id": "q_1",
                        "question_text": "लाइव वीडियो स्ट्रीमिंग और ऑनलाइन मल्टीप्लेयर गेमिंग में यूडीपी (UDP) को टीसीपी से बेहतर क्यों माना जाता है?" if is_hindi else "Why is UDP preferred over TCP for real-time video conferencing and multiplayer gaming?",
                        "options": [
                            "क्योंकि यह खोए हुए पैकेटों के दोबारा आने का इंतजार किए बिना न्यूनतम लेटेंसी (Low Latency) प्रदान करता है" if is_hindi else "Because it eliminates acknowledgment latency and avoids stalling playback for lost packets",
                            "क्योंकि यह सभी डेटा को स्थायी रूप से एन्क्रिप्ट करता है" if is_hindi else "Because UDP provides military-grade data encryption",
                            "क्योंकि यह इंटरनेट को पूरी तरह बायपास करता है" if is_hindi else "Because UDP eliminates the need for IP addressing",
                            "क्योंकि यह फाइल का आकार 100 गुना छोटा कर देता है" if is_hindi else "Because TCP cannot transmit binary data"
                        ],
                        "correct_answer": "क्योंकि यह खोए हुए पैकेटों के दोबारा आने का इंतजार किए बिना न्यूनतम लेटेंसी (Low Latency) प्रदान करता है" if is_hindi else "Because it eliminates acknowledgment latency and avoids stalling playback for lost packets",
                        "hint": "Real-time media prioritizes immediate timing over retransmitting old frames.",
                        "explanation": "UDP avoids TCP retransmission delays, ensuring real-time continuous playback without stalling on dropped packets."
                    }
                },
                {
                    "id": "seg_2",
                    "title": "टीसीपी 3-वे हैंडशेक और कंजेशन कंट्रोल" if is_hindi else "TCP 3-Way Handshake & Congestion Control Dynamics",
                    "explanation": "डेटा भेजने से पहले क्लाइंट और सर्वर SYN, SYN-ACK और ACK संदेशों का आदान-प्रदान करके सुरक्षित कनेक्शन स्थापित करते हैं।" if is_hindi else "Before transferring payload data, TCP synchronizes sequence numbers through a 3-way handshake (SYN, SYN-ACK, ACK) and actively monitors network congestion.",
                    "example": "जैसे फोन कॉल उठाते ही 'हैलो?', 'हाँ, आवाज आ रही है', 'ठीक है, बात शुरू करते हैं' कहना।" if is_hindi else "Like answering a phone: 'Hello?' (SYN) -> 'Yes, I hear you!' (SYN-ACK) -> 'Great, let us begin.' (ACK).",
                    "key_points": [
                        "SYN -> SYN-ACK -> ACK क्रम से कनेक्शन स्थापना" if is_hindi else "SYN -> SYN-ACK -> ACK establishes sequence numbers",
                        "कंजेशन विंडो (CWND) नेटवर्क जाम होने से बचाती है" if is_hindi else "Congestion Window (CWND) dynamically adjusts transmission throughput",
                        "पैकेट लॉस होने पर स्वचालित री-ट्रांसमिशन" if is_hindi else "Automatic retransmission (ARQ) guarantees zero data loss"
                    ],
                    "visual_diagram_type": "process",
                    "visual_description": "Client ---[SYN]--> Server ---[SYN-ACK]--> Client ---[ACK]--> Connection Established",
                    "visual_code_or_math": "1. Client: SYN(seq=x) -> 2. Server: SYN(seq=y)+ACK(x+1) -> 3. Client: ACK(y+1)",
                    "question": {
                        "id": "q_2",
                        "question_text": "टीसीपी (TCP) कनेक्शन स्थापित करने वाले 3-वे हैंडशेक का सही क्रम क्या है?" if is_hindi else "What is the exact chronological sequence of the TCP 3-Way Handshake?",
                        "options": [
                            "SYN -> SYN-ACK -> ACK" if is_hindi else "SYN -> SYN-ACK -> ACK",
                            "ACK -> SYN -> FIN" if is_hindi else "ACK -> SYN -> FIN",
                            "DATA -> PING -> PONG" if is_hindi else "DATA -> PING -> PONG",
                            "RST -> SYN -> ACK" if is_hindi else "RST -> SYN -> ACK"
                        ],
                        "correct_answer": "SYN -> SYN-ACK -> ACK" if is_hindi else "SYN -> SYN-ACK -> ACK",
                        "hint": "Synchronize, Synchronize-Acknowledge, Acknowledge.",
                        "explanation": "The 3-way handshake begins with client SYN, server responds with SYN-ACK, client completes with ACK."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 5: WHY IS THE SKY BLUE (Physics & Optics)
        # -------------------------------------------------------------
        if "sky blue" in t_lower or "rayleigh" in t_lower or "sky" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "आकाश नीला क्यों दिखता है: रेले प्रकीर्णन" if is_hindi else "Why the Sky is Blue: Rayleigh Scattering of Sunlight",
                    "explanation": "नमस्ते! सूर्य का प्रकाश सफेद होता है जिसमें सभी रंग होते हैं। जब प्रकाश वायुमंडल के गैस अणुओं से टकराता है, तो छोटी तरंग दैर्ध्य (नीला रंग) लाल रंग की तुलना में बहुत अधिक प्रकीर्णित (फैलता) है।" if is_hindi else "Welcome! Sunlight is white light composed of all rainbow wavelengths. When it enters Earth's atmosphere, gas molecules scatter short blue wavelengths in all directions far more intensely than long red wavelengths—a phenomenon called Rayleigh Scattering.",
                    "example": "जैसे नदी की धारा में छोटे कंकड़ छोटी लहरों को बिखेर देते हैं, जबकि बड़ी लहरें बिना विचलित हुए सीधी निकल जाती हैं।" if is_hindi else "Think of a mesh sieve: tiny particles scatter short, high-frequency blue waves across the entire sky while longer red waves pass straight through.",
                    "key_points": [
                        "रेले प्रकीर्णन तीव्रता तरंग दैर्ध्य की चौथी घात के व्युत्क्रमानुपाती होती है (1 / λ⁴)" if is_hindi else "Rayleigh scattering intensity is proportional to 1 / λ⁴ (Wavelength to the 4th power)",
                        "नीले प्रकाश की तरंग दैर्ध्य (~400nm) लाल प्रकाश (~700nm) से छोटी होती है" if is_hindi else "Blue light (~400nm) scatters ~10x more efficiently than red light (~700nm)",
                        "सूर्यास्त के समय लंबी दूरी तय करने से केवल लाल-नारंगी रंग दिखाई देता है" if is_hindi else "At sunset, light travels through thicker atmosphere, leaving only long red/orange wavelengths"
                    ],
                    "visual_diagram_type": "diagram",
                    "visual_description": "Sunlight (White) -> Atmospheric Molecules (N2/O2) -> Blue Wavelengths Scatter in all directions -> Observer sees Blue Sky",
                    "visual_code_or_math": "Scattering Intensity (I) ∝ 1 / (λ^4)  [Blue λ=400nm vs Red λ=700nm]",
                    "question": {
                        "id": "q_1",
                        "question_text": "रेले प्रकीर्णन (Rayleigh Scattering) नियम के अनुसार नीला प्रकाश लाल प्रकाश से अधिक क्यों फैलता है?" if is_hindi else "According to Rayleigh's Scattering Law, why does blue light scatter significantly more than red light?",
                        "options": [
                            "क्योंकि नीले प्रकाश की तरंग दैर्ध्य (Wavelength) छोटी होती है और प्रकीर्णन 1 / λ⁴ के समानुपाती होता है" if is_hindi else "Because blue light has a shorter wavelength and scattering intensity is proportional to 1 / λ⁴",
                            "क्योंकि ऑक्सीजन गैस का प्राकृतिक रंग नीला होता है" if is_hindi else "Because nitrogen and oxygen gas molecules are naturally dyed blue",
                            "क्योंकि समुद्र का नीला पानी आकाश में प्रतिबिंबित होता है" if is_hindi else "Because the blue ocean reflects upward into outer space",
                            "क्योंकि सूर्य केवल नीला प्रकाश ही उत्सर्जित करता है" if is_hindi else "Because the sun only emits high-energy blue photons"
                        ],
                        "correct_answer": "क्योंकि नीले प्रकाश की तरंग दैर्ध्य (Wavelength) छोटी होती है और प्रकीर्णन 1 / λ⁴ के समानुपाती होता है" if is_hindi else "Because blue light has a shorter wavelength and scattering intensity is proportional to 1 / λ⁴",
                        "hint": "Inverse fourth-power law of wavelength: shorter wavelength = massive scattering.",
                        "explanation": "Rayleigh scattering states I ∝ 1/λ⁴; since blue light has a shorter wavelength than red, it scatters roughly 10 times more."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 6: JAVA INHERITANCE (Programming & OOP)
        # -------------------------------------------------------------
        if "java" in t_lower and ("inheritance" in t_lower or "oop" in t_lower):
            return [
                {
                    "id": "seg_1",
                    "title": "जावा में इनहेरिटेंस: कोड पुन: प्रयोज्यता और 'extends'" if is_hindi else "Java Inheritance: Extends, Super & Code Reusability",
                    "explanation": "नमस्ते! जावा में इनहेरिटेंस एक ऐसा तंत्र है जिसमें एक सब-क्लास (Child Class) सुपर-क्लास (Parent Class) के गुणों और विधियों को प्राप्त करती है।" if is_hindi else "Welcome! In Java OOP, Inheritance allows a child subclass to inherit fields and methods from a parent superclass using the 'extends' keyword, fostering clean code reusability.",
                    "example": "जैसे संतान अपने माता-पिता के आनुवंशिक लक्षण प्राप्त करती है, लेकिन अपनी विशेष क्षमताएं भी विकसित कर सकती है।" if is_hindi else "Like biological inheritance: a child inherits eye color and traits from parents, but can also add their own unique skills and talents.",
                    "key_points": [
                        "'extends' कीवर्ड का उपयोग करके क्लास का विस्तार किया जाता है" if is_hindi else "The 'extends' keyword creates a parent-child relationship",
                        "'super' कीवर्ड पैरेंट क्लास के कंस्ट्रक्टर या मेथड को कॉल करता है" if is_hindi else "'super' keyword invokes parent constructor or overridden methods",
                        "मेथड ओवरराइडिंग (@Override) पॉलीमॉर्फिज्म प्रदान करती है" if is_hindi else "Method Overriding (@Override) enables runtime polymorphism"
                    ],
                    "visual_diagram_type": "code",
                    "visual_description": "class Animal { void sound() } ===> class Dog extends Animal { @Override void sound() { 'Woof' } }",
                    "visual_code_or_math": "class Animal {\n    void eat() { System.out.println(\"Eating\"); }\n}\nclass Dog extends Animal {\n    @Override\n    void eat() { System.out.println(\"Dog eating kibble\"); }\n}",
                    "question": {
                        "id": "q_1",
                        "question_text": "जावा में चाइल्ड क्लास से पैरेंट क्लास के कंस्ट्रक्टर को कॉल करने के लिए किस कीवर्ड का उपयोग किया जाता है?" if is_hindi else "Which Java keyword is used within a subclass constructor to invoke the parent class constructor?",
                        "options": [
                            "super()" if is_hindi else "super()",
                            "this()" if is_hindi else "this()",
                            "parent()" if is_hindi else "parent()",
                            "extends()" if is_hindi else "base()"
                        ],
                        "correct_answer": "super()" if is_hindi else "super()",
                        "hint": "Refers to the immediate superclass.",
                        "explanation": "The 'super()' call explicitly invokes the superclass constructor from within the subclass."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 7: WATER CYCLE (Earth Science & Geography)
        # -------------------------------------------------------------
        if "water cycle" in t_lower or "hydrological" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "जल चक्र के चरण: वाष्पीकरण, संघनन और वर्षा" if is_hindi else "The Hydrological Cycle: Evaporation, Condensation & Precipitation",
                    "explanation": "नमस्ते! जल चक्र पृथ्वी पर जल का एक निरंतर प्राकृतिक संचलन है जिसमें सौर ऊर्जा से जल वाष्पीकृत होकर बादल बनाता है और वर्षा के रूप में वापस लौटता है।" if is_hindi else "Welcome! The Water Cycle (Hydrological Cycle) is Earth's natural continuous recycling system driven by solar radiation and gravity across atmosphere, land, and oceans.",
                    "example": "प्रकृति की विशाल डिस्टिलेशन प्रणाली: समुद्र का खारा पानी वाष्पीकृत होकर मीठे पानी की बारिश के रूप में धरती को सींचता है।" if is_hindi else "Nature's giant closed-loop distillation distillery: salty ocean water evaporates into pure water vapor, condenses into clouds, and rains down as fresh water.",
                    "key_points": [
                        "वाष्पीकरण (Evaporation) और वाष्पोत्सर्जन (Transpiration)" if is_hindi else "Evaporation & Plant Transpiration lift vapor into the atmosphere",
                        "संघनन (Condensation) बादलों का निर्माण करता है" if is_hindi else "Condensation: Cooling vapor forms cloud droplets around nuclei",
                        "वर्षा (Precipitation) और भूजल पुनर्भरण (Infiltration)" if is_hindi else "Precipitation returns liquid water via rain, snow, and runoff"
                    ],
                    "visual_diagram_type": "process",
                    "visual_description": "Oceans/Lakes -> [Evaporation] -> Atmosphere -> [Condensation: Clouds] -> [Precipitation: Rain] -> Groundwater Runoff",
                    "visual_code_or_math": "Solar Heat -> Evaporation (Liquid->Gas) -> Cooling (Condensation) -> Precipitation (Gravity Rain)",
                    "question": {
                        "id": "q_1",
                        "question_text": "जल चक्र में पौधों की पत्तियों से जलवाष्प के वायुमंडल में निकलने की प्रक्रिया को क्या कहते हैं?" if is_hindi else "What is the biological process by which plants release water vapor into the atmosphere through leaf stomata?",
                        "options": [
                            "वाष्पोत्सर्जन (Transpiration)" if is_hindi else "Transpiration",
                            "संघनन (Condensation)" if is_hindi else "Sublimation",
                            "अवक्षेपण (Precipitation)" if is_hindi else "Infiltration",
                            "अपघटन (Decomposition)" if is_hindi else "Photosynthesis splitting"
                        ],
                        "correct_answer": "वाष्पोत्सर्जन (Transpiration)" if is_hindi else "Transpiration",
                        "hint": "Water evaporation specifically from plant leaves.",
                        "explanation": "Transpiration is the evaporation of water from plant leaves into the atmosphere via stomata."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 8: QUANTUM COMPUTING (Physics & CS)
        # -------------------------------------------------------------
        if "quantum" in t_lower or "qubit" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "क्वांटम कंप्यूटिंग: क्यूबिट और सुपरपोजिशन" if is_hindi else "Quantum Computing Foundations: Qubits, Superposition & Entanglement",
                    "explanation": "नमस्ते! क्लासिकल कंप्यूटर 0 या 1 बिट्स पर काम करते हैं, जबकि क्वांटम कंप्यूटर 'क्यूबिट्स' का उपयोग करते हैं जो सुपरपोजिशन के कारण एक साथ 0 और 1 दोनों अवस्थाओं में रह सकते हैं।" if is_hindi else "Welcome! While classical computers compute with discrete binary bits (0 or 1), Quantum Computers leverage quantum bits (qubits) capable of existing in superpositions of both states simultaneously.",
                    "example": "एक घूमता हुआ सिक्का जो टेबल पर गिरकर रुकने से पहले एक साथ 'चित' और 'पट' दोनों अवस्थाओं का मिश्रण है।" if is_hindi else "A spinning coin on a tabletop: while spinning, it exists in a dynamic blend of heads and tails simultaneously until measured.",
                    "key_points": [
                        "क्यूबिट सुपरपोजिशन: |ψ⟩ = α|0⟩ + β|1⟩" if is_hindi else "Superposition: State vector |ψ⟩ = α|0⟩ + β|1⟩ (Bloch Sphere)",
                        "क्वांटम एंटैंगलमेंट (Entanglement) तात्कालिक सहसंबंध जोड़ता है" if is_hindi else "Quantum Entanglement: Non-local correlation between paired qubits",
                        "घातीय समानांतरता (Exponential Parallelism, 2^n)" if is_hindi else "Exponential state space: N qubits represent 2^N states simultaneously"
                    ],
                    "visual_diagram_type": "diagram",
                    "visual_description": "Bloch Sphere Representation: State |ψ⟩ between |0⟩ North Pole and |1⟩ South Pole",
                    "visual_code_or_math": "|ψ⟩ = α|0⟩ + β|1⟩  where |α|^2 + |β|^2 = 1",
                    "question": {
                        "id": "q_1",
                        "question_text": "क्वांटम सुपरपोजिशन (Superposition) की प्राथमिक विशेषता क्या है?" if is_hindi else "What fundamental property allows a Qubit to perform parallel quantum computations?",
                        "options": [
                            "एक साथ 0 और 1 दोनों अवस्थाओं के रैखिक संयोजन (Linear Combination) में मौजूद रहना" if is_hindi else "Existing simultaneously in a linear superposition of |0⟩ and |1⟩ basis states",
                            "केवल सामान्य 0 या 1 बिट की तरह चलना" if is_hindi else "Switching exclusively between discrete 0 and 1 like a transistor",
                            "हार्डवेयर का तापमान 1000 डिग्री तक बढ़ाना" if is_hindi else "Operating without any cooling requirements",
                            "बिना किसी गणित के रैंडम उत्तर देना" if is_hindi else "Permanently locking state to zero"
                        ],
                        "correct_answer": "एक साथ 0 और 1 दोनों अवस्थाओं के रैखिक संयोजन (Linear Combination) में मौजूद रहना" if is_hindi else "Existing simultaneously in a linear superposition of |0⟩ and |1⟩ basis states",
                        "hint": "Linear combination of quantum basis states |0> and |1>.",
                        "explanation": "Superposition allows a single qubit to hold probabilistic amplitudes for |0⟩ and |1⟩ concurrently."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 9: LATEST DEVELOPMENTS IN AI AGENTS / CURRENT TECH
        # -------------------------------------------------------------
        if "agent" in t_lower or "latest" in t_lower or "trends" in t_lower:
            return [
                {
                    "id": "seg_1",
                    "title": "आधुनिक एआई एजेंट और स्वायत्त प्रणालियां" if is_hindi else "Autonomous AI Agents: Tool-Use, Planning & Reasoning Loops",
                    "explanation": "नमस्ते! आधुनिक एआई एजेंट केवल चैट नहीं करते, बल्कि स्वायत्त रूप से योजना बनाते हैं, वेब सर्च और कोडिंग टूल्स का उपयोग करते हैं, और जटिल समस्याओं को हल करते हैं।" if is_hindi else "Welcome! Modern AI Agents transcend simple text completion by operating within autonomous perception-planning-action loops, orchestrating multi-step tool use, code execution, and web retrieval to solve multi-stage goals.",
                    "example": "एक कुशल सहायक की तरह जो केवल सवाल का जवाब नहीं देता, बल्कि पूरी यात्रा की टिकट बुक करता है, होटल रिजर्व करता है और कैलेंडर अपडेट करता है।" if is_hindi else "Like an executive co-pilot: instead of just summarizing travel tips, it checks flight APIs, books the hotel, and synchronizes your calendar autonomously.",
                    "key_points": [
                        "रीजनिंग लूप्स: ReAct (Reason + Act), Plan-and-Solve" if is_hindi else "Reasoning Architectures: ReAct (Reasoning + Acting) & Reflection loops",
                        "टूल और फंक्शन कॉलिंग (API, Web, Sandbox Code)" if is_hindi else "Dynamic Tool Orchestration: Web search, Python sandboxes & DB connectors",
                        "मल्टी-एजेंट सहयोग और स्वायत्तता" if is_hindi else "Multi-Agent Consensus: Specialized worker agents coordinating on complex tasks"
                    ],
                    "visual_diagram_type": "architecture",
                    "visual_description": "User Goal -> LLM Planner -> Memory & Context -> Tool Execution (Search/Code) -> Observation -> Final Solution",
                    "visual_code_or_math": "Agent Loop: Observe(State) -> Reason(Plan) -> Act(ToolCall) -> Reflect(Outcome)",
                    "question": {
                        "id": "q_1",
                        "question_text": "आधुनिक एआई एजेंट (Autonomous AI Agent) को सामान्य चैटबॉट से क्या अलग बनाता है?" if is_hindi else "What primary capability distinguishes an Autonomous AI Agent from a traditional chatbot?",
                        "options": [
                            "स्वायत्त रूप से टूल्स (Tools), एपीआई और कोड चलाकर बहु-चरणीय लक्ष्यों को पूरा करना" if is_hindi else "Autonomous multi-step planning, tool orchestration, and environment interaction",
                            "केवल एक शब्द में जवाब देना" if is_hindi else "Restricting responses to single-word completions",
                            "इंटरनेट कनेक्शन बंद कर देना" if is_hindi else "Operating without access to contextual memory",
                            "सभी डेटा को बिना सोचे डिलीट करना" if is_hindi else "Running exclusively on offline mechanical relays"
                        ],
                        "correct_answer": "स्वायत्त रूप से टूल्स (Tools), एपीआई और कोड चलाकर बहु-चरणीय लक्ष्यों को पूरा करना" if is_hindi else "Autonomous multi-step planning, tool orchestration, and environment interaction",
                        "hint": "Think about tool calling, planning, and executing actions in the environment.",
                        "explanation": "AI agents plan actions, use external tools, observe outcomes, and iterate toward goal completion."
                    }
                }
            ]

        # -------------------------------------------------------------
        # DOMAIN 10: UNIVERSAL DYNAMIC FALLBACK FOR ANY ARBITRARY TOPIC
        # -------------------------------------------------------------
        snippet = context[:180].replace('\n', ' ') if context else f"core foundational mechanisms and real-world dynamics of {topic}"
        base_segs = [
            {
                "id": "seg_1",
                "title": f"{topic} के मूल सिद्धांत और कार्यप्रणाली" if is_hindi else f"Core Foundations & Principles of {topic}",
                "explanation": f"नमस्ते! इस पाठ में हम {topic} के बुनियादी सिद्धांतों को समझेंगे। {snippet}।" if is_hindi else f"Welcome! In this lesson, we explore the essential foundational mechanics of {topic}. {snippet}. Understanding these core relationships allows you to reason about practical applications effectively.",
                "example": "एक सुव्यवस्थित तंत्र की तरह जहां प्रत्येक इनपुट नियमों के तहत सटीक परिणाम देता है।" if is_hindi else "Think of this system as an interconnected architecture where core governing rules dictate operational behavior.",
                "key_points": [
                    f"{topic} की प्राथमिक परिभाषा और उद्देश्य" if is_hindi else f"Primary definitions and governing rules of {topic}",
                    "कार्यात्मक संबंध और प्रमुख पैरामीटर" if is_hindi else "Key operational variables and causal relationships",
                    "व्यावहारिक उपयोग और महत्व" if is_hindi else "Core conceptual building blocks and foundational mechanisms"
                ],
                "visual_diagram_type": visual_type,
                "visual_description": f"Core architecture and concept flow for {topic}",
                "visual_code_or_math": f"Core Mechanism: Input -> Governing Rule ({topic}) -> Target Outcome",
                "question": {
                    "id": "q_1",
                    "question_text": f"{topic} का केंद्रीय मूलभूत सिद्धांत क्या है?" if is_hindi else f"What is the central foundational rule that governs {topic}?",
                    "options": [
                        f"{topic} के व्यवस्थित नियमों और संबंधों को समझना" if is_hindi else f"Systematic application of governing principles and operational rules in {topic}",
                        "बिना किसी नियम के रैंडम अनुमान लगाना" if is_hindi else "Treating all dynamic variables as static constants without verification",
                        "सभी इनपुट डेटा को अनदेखा करना" if is_hindi else "Bypassing constraint verification and execution monitoring",
                        "प्रणाली की सीमाओं को हटा देना" if is_hindi else "Assuming random uncoordinated behavior"
                    ],
                    "correct_answer": f"{topic} के व्यवस्थित नियमों और संबंधों को समझना" if is_hindi else f"Systematic application of governing principles and operational rules in {topic}",
                    "hint": f"Focus on the primary governing principles of {topic}.",
                    "explanation": f"Mastering {topic} requires understanding its systematic operational rules and relationships."
                }
            },
            {
                "id": "seg_2",
                "title": f"{topic} के व्यावहारिक अनुप्रयोग और विश्लेषण" if is_hindi else f"Mechanisms, Trade-offs & Real-World Applications of {topic}",
                "explanation": f"अब हम देखेंगे कि {topic} वास्तविक परिस्थितियों और विभिन्न सीमाओं में कैसे काम करता है।" if is_hindi else f"Now let's examine how {topic} operates in practical real-world scenarios under various constraints and trade-offs.",
                "example": "सर्वोत्तम प्रदर्शन प्राप्त करने के लिए सिस्टम मापदंडों को संतुलित करना।" if is_hindi else "Like tuning system parameters to achieve optimal balance between efficiency, accuracy, and robust performance.",
                "key_points": [
                    "चरण-दर-चरण कारण और प्रभाव विश्लेषण" if is_hindi else "Step-by-step causal mechanics and state progression",
                    "सीमाओं और बाधाओं का प्रबंधन" if is_hindi else "Handling boundary conditions, constraints, and edge cases",
                    "उद्योग और अकादमिक क्षेत्र में सर्वोत्तम प्रथाएं" if is_hindi else "Industry best practices and real-world design trade-offs"
                ],
                "visual_diagram_type": "process" if visual_type != "comparison" else "comparison",
                "visual_description": f"Execution pipeline and constraint trade-offs for {topic}",
                "visual_code_or_math": f"Optimization: Performance = Maximize(Efficiency) subject to Constraints({topic})",
                "question": {
                    "id": "q_2",
                    "question_text": f"व्यावहारिक समस्याओं को हल करने में {topic} का उपयोग कैसे किया जाता है?" if is_hindi else f"How do practitioners apply the principles of {topic} to solve complex problems?",
                    "options": [
                        "सिस्टम की बाधाओं का विश्लेषण करके सत्यापित सिद्धांतों को लागू करना" if is_hindi else "By systematically analyzing constraints and applying verified rules",
                        "सभी सत्यापन चरणों को छोड़ देना" if is_hindi else "By ignoring boundary conditions and edge cases",
                        "गैर-दोहराए जाने वाले यादृच्छिक तरीकों का उपयोग करना" if is_hindi else "By using non-repeatable arbitrary procedures",
                        "प्रदर्शन मेट्रिक्स को मापना बंद करना" if is_hindi else "By skipping performance evaluation stages"
                    ],
                    "correct_answer": "सिस्टम की बाधाओं का विश्लेषण करके सत्यापित सिद्धांतों को लागू करना" if is_hindi else "By systematically analyzing constraints and applying verified rules",
                    "hint": "Think about structured problem solving and constraint analysis.",
                    "explanation": f"Systematic application of verified principles within constraints guarantees robust outcomes in {topic}."
                }
            }
        ]

        if count >= 3:
            base_segs.append({
                "id": "seg_3",
                "title": f"{topic} के उन्नत विषय और समस्या-निवारण" if is_hindi else f"Advanced Edge Cases, Diagnostics & Optimization of {topic}",
                "explanation": f"इस खंड में हम {topic} के जटिल परिदृश्यों, सामान्य त्रुटियों और प्रदर्शन सुधार की रणनीतियों का गहराई से अध्ययन करेंगे।" if is_hindi else f"In this segment, we deep-dive into complex edge cases, debugging scenarios, and performance optimization strategies for {topic}.",
                "example": "एक विशेषज्ञ इंजीनियर की तरह समस्याओं के मूल कारण का पता लगाना और निवारण करना।" if is_hindi else "Like a senior engineer conducting root-cause analysis to eliminate systemic bottlenecks.",
                "key_points": [
                    "गहन नैदानिक रणनीतियाँ" if is_hindi else "Deep diagnostics and debugging patterns",
                    "प्रदर्शन अनुकूलन और दक्षता" if is_hindi else "Performance profiling and latency reduction",
                    "सामान्य विफलता मोड और समाधान" if is_hindi else "Common anti-patterns, pitfalls, and failure mitigations"
                ],
                "visual_diagram_type": "process",
                "visual_description": f"Diagnostics and optimization pipeline for {topic}",
                "visual_code_or_math": f"Optimization: Minimize(Bottlenecks) -> Maximize(Reliability)",
                "question": {
                    "id": "q_3",
                    "question_text": f"{topic} में समस्याओं के निदान के लिए सबसे प्रभावी दृष्टिकोण क्या है?" if is_hindi else f"What is the most effective engineering approach to diagnosing failures in {topic}?",
                    "options": [
                        "व्यवस्थित रूप से लॉग और मेट्रिक्स का विश्लेषण करना" if is_hindi else "Systematic trace analysis and boundary verification",
                        "समस्या की अनदेखी करना" if is_hindi else "Arbitrary code changes without tracing",
                        "सभी घटकों को पुनः आरंभ करना" if is_hindi else "Bypassing root cause analysis",
                        "चेतावनी संकेतों को छिपाना" if is_hindi else "Silencing error indicators without fixes"
                    ],
                    "correct_answer": "व्यवस्थित रूप से लॉग और मेट्रिक्स का विश्लेषण करना" if is_hindi else "Systematic trace analysis and boundary verification",
                    "hint": "Think about root-cause diagnostics.",
                    "explanation": "Systematic root-cause analysis is critical for high-reliability systems."
                }
            })

        if count >= 4:
            base_segs.append({
                "id": "seg_4",
                "title": f"{topic} का समग्र समन्वय और आर्किटेक्चर" if is_hindi else f"System Integration, Scalability & Architectural Mastery of {topic}",
                "explanation": f"अंत में, हम देखेंगे कि {topic} को बड़े पैमाने पर उत्पादन प्रणालियों और आधुनिक आर्किटेक्चर में कैसे एकीकृत किया जाता है।" if is_hindi else f"Finally, we synthesize how {topic} integrates into large-scale production architectures, ensuring long-term resilience and maintainability.",
                "example": "एक बड़े पुल या विमान प्रणाली की तरह जहां हर घटक समग्र सुरक्षा और दक्षता सुनिश्चित करता है।" if is_hindi else "Like assembling an aerospace system where every validated subsystem guarantees total mission success.",
                "key_points": [
                    "एकीकरण और बड़े पैमाने पर परिनियोजन" if is_hindi else "Enterprise architecture and horizontal scalability",
                    "विश्वसनीयता और दीर्घकालिक स्थिरता" if is_hindi else "Resilience patterns, telemetry, and fault isolation",
                    "व्यावसायिक प्रभाव और भविष्य का परिदृश्य" if is_hindi else "Production readiness, compliance, and architectural future-proofing"
                ],
                "visual_diagram_type": "flowchart",
                "visual_description": f"End-to-end architectural system topology for {topic}",
                "visual_code_or_math": f"Architecture: Subsystem A + Subsystem B -> Scalable Platform ({topic})",
                "question": {
                    "id": "q_4",
                    "question_text": f"उत्पादन परिवेश में {topic} को एकीकृत करते समय प्राथमिक विचार क्या होना चाहिए?" if is_hindi else f"What is the primary architectural consideration when scaling {topic} in production?",
                    "options": [
                        "स्थिरता, मॉड्यूलरिटी और त्रुटि सहनशीलता सुनिश्चित करना" if is_hindi else "Ensuring fault isolation, telemetry observability, and modularity",
                        "सुरक्षा नीतियों को हटा देना" if is_hindi else "Disabling telemetry to save compute cycles",
                        "केंद्रीकृत विफलता बिंदु बनाना" if is_hindi else "Introducing tight single points of failure",
                        "सभी सत्यापन परीक्षणों को छोड़ना" if is_hindi else "Skipping integration regression testing"
                    ],
                    "correct_answer": "स्थिरता, मॉड्यूलरिटी और त्रुटि सहनशीलता सुनिश्चित करना" if is_hindi else "Ensuring fault isolation, telemetry observability, and modularity",
                    "hint": "Consider enterprise reliability and fault tolerance.",
                    "explanation": "Modularity and fault isolation guarantee robust scalable operations."
                }
            })

        return base_segs[:count]

    def _handle_evaluation(self, prompt: str, is_hindi: bool, is_hinglish: bool = False) -> Dict[str, Any]:
        p_lower = prompt.lower()
        topic, _ = self._extract_clean_topic(prompt)

        ans_part = ""
        if 'student\'s submitted answer: "' in p_lower:
            ans_part = p_lower.split('student\'s submitted answer: "')[1].split('"')[0].strip()
        elif "student answer:" in p_lower:
            ans_part = p_lower.split("student answer:")[1].split("\n")[0].strip()

        expected_part = ""
        if "expected correct answer:" in p_lower:
            expected_part = p_lower.split("expected correct answer:")[1].split("\n")[0].strip()

        # Check for semantic agreement or correct indicators
        is_correct = False
        if expected_part and ans_part:
            exp_tokens = set(re.findall(r'\w+', expected_part.lower()))
            ans_tokens = set(re.findall(r'\w+', ans_part.lower()))
            overlap = exp_tokens.intersection(ans_tokens)
            if len(overlap) >= max(1, len(exp_tokens) * 0.4) or ans_part.lower() == expected_part.lower():
                is_correct = True

        # Check positive/negative indicators
        positive_cues = ["photolysis", "water", "splitting", "जल", "h2o", "rubisco", "रुबिस्को", "stack overflow", "lifo", "decreases", "घट", "hash", "super()", "superposition", "transpiration", "syn -> syn-ack -> ack", "1 / λ", "wavelength", "low latency", "planning", "tool"]
        negative_cues = ["friction", "बढ़", "increases", "dyed blue", "ocean reflects", "infinite", "fifo", "this()", "randomly", "halved", "deleting", "100 rows"]

        if any(w in ans_part.lower() for w in positive_cues):
            is_correct = True
        elif any(w in ans_part.lower() for w in negative_cues):
            is_correct = False

        if is_correct:
            tb_state = {
                "learner_level": "Beginner",
                "current_concept": topic,
                "understanding_state": "High",
                "detected_misconception": "None (Concept sound)",
                "teaching_strategy": "Advance to next learning objective",
                "difficulty": "Adapted Higher",
                "next_action": "Positive reinforcement & next segment unlock"
            }
            fb_text = "शानदार! आपका उत्तर वैचारिक रूप से बिल्कुल सटीक है।" if is_hindi else ("Bilkul sahi! Aapka conceptual understanding spot-on hai." if is_hinglish else "Excellent! That is conceptually spot-on and demonstrates clear understanding of the core principle.")
            return {
                "is_correct": True,
                "score": 1.0,
                "feedback": fb_text,
                "misconception_detected": False,
                "misconception_explanation": "",
                "concept": topic,
                "misconception": "",
                "reasoning": "",
                "severity": "low",
                "needs_remediation": False,
                "recommended_strategy": "advance_next",
                "missing_concept": "",
                "confidence": 0.98,
                "adaptation_needed": False,
                "teacher_brain_state": tb_state
            }
        else:
            # Diagnose specific misconception
            misc = f"Student's explanation diverged from the governing causal relationship in {topic}."
            missing = f"Core operational principle of {topic}"
            concept_name = topic
            strategy = "real_world_analogy"

            t_low = topic.lower()
            if "electric" in t_low or "ohm" in t_low:
                concept_name = "Ohm's Law"
                misc = "Student believes current increases when resistance increases, confusing inverse with direct proportionality."
                missing = "Inverse relationship in Ohm's Law (I = V / R)"
                strategy = "water_pipe_analogy"
            elif "photosynthesis" in t_low:
                concept_name = "Light Reactions & Photolysis"
                misc = "Student confused the source of oxygen with CO2 carbon fixation rather than water photolysis."
                missing = "Light-dependent photolysis of H2O"
                strategy = "step_by_step_visual"
            elif "recursion" in t_low:
                concept_name = "Recursion Base Case"
                misc = "Student overlooked that without a base case, recursive stack frames exhaust available memory."
                missing = "Base case termination condition"
                strategy = "stack_visualizer"
            elif "blockchain" in t_low:
                concept_name = "Cryptographic Immutability"
                misc = "Student assumed central databases can alter chained cryptographic hashes without detection."
                missing = "Cryptographic hash chaining"
                strategy = "first_principles"
            elif "sky" in t_low:
                concept_name = "Rayleigh Scattering Law"
                misc = "Student assumed atmospheric gases have blue pigmentation rather than wavelength-dependent Rayleigh scattering (1/λ⁴)."
                missing = "Rayleigh scattering 1/λ⁴"
                strategy = "particle_wave_filter"
            elif "tcp" in t_low or "udp" in t_low:
                concept_name = "Transport Protocol Trade-offs"
                misc = "Student confused connection-oriented reliability with low-latency streaming requirements."
                missing = "TCP 3-way handshake vs UDP connectionless throughput"
                strategy = "comparative_matrix"

            tb_state = {
                "learner_level": "Beginner",
                "current_concept": concept_name,
                "understanding_state": "Needs Remediation",
                "detected_misconception": misc,
                "teaching_strategy": strategy.replace("_", " ").title(),
                "difficulty": "Adapted Simpler Analogy",
                "next_action": f"Deploy {strategy.replace('_', ' ')} video & ask confirmation check"
            }

            fb_text = "अच्छा प्रयास! आपने चरों के संबंध को देखा, लेकिन मुख्य दिशा या सिद्धांत में थोड़ा अंतर रह गया। आइए इसे एक नए सादृश्य से समझें।" if is_hindi else ("Achha koshish! Lekin core principle me confusion hai. Chaliye ek fresh real-world example se isse clarify karte hain." if is_hinglish else "Good attempt! You recognized that the variables interact, but inverted the core operational relationship. Let's revisit this with a fresh intuitive perspective.")
            return {
                "is_correct": False,
                "score": 0.2,
                "feedback": fb_text,
                "misconception_detected": True,
                "misconception_explanation": misc,
                "concept": concept_name,
                "misconception": misc,
                "reasoning": f"Learner's response indicates mental model confusion regarding {missing} in {concept_name}.",
                "severity": "medium",
                "needs_remediation": True,
                "recommended_strategy": strategy,
                "missing_concept": missing,
                "confidence": 0.94,
                "adaptation_needed": True,
                "teacher_brain_state": tb_state
            }

    def _handle_remediation(self, prompt: str, is_hindi: bool, is_hinglish: bool = False) -> Dict[str, Any]:
        topic, _ = self._extract_clean_topic(prompt)
        t_lower = topic.lower()

        if "photosynthesis" in t_lower:
            return {
                "title": "प्रकाश संश्लेषण का नया नजरिया: पानी का विभाजन" if is_hindi else "Revisiting Photosynthesis: The Water Splitting Analogy",
                "explanation": "ऑक्सीजन वास्तव में कार्बन डाइऑक्साइड से नहीं, बल्कि जल (H2O) के अणुओं को सूर्य के प्रकाश द्वारा तोड़ने से निकलती है। पौधे हाइड्रोजन को अपने पास रखते हैं और शुद्ध ऑक्सीजन हवा में छोड़ देते हैं।" if is_hindi else "Remember: Oxygen gas does NOT come from carbon dioxide. When sunlight hits chlorophyll, it splits water (H2O) to grab hydrogen electrons, releasing pure oxygen (O2) into the air as a fresh by-product!",
                "example": "जैसे नारियल को फोड़कर पानी पीना और उसके छिलके को अलग करना: यहाँ पानी से हाइड्रोजन लेकर ऑक्सीजन छोड़ी जाती है।" if is_hindi else "Like cracking an egg to bake a cake: the plant keeps the hydrogen yolk to build sugars and releases the oxygen shell into the atmosphere.",
                "key_points": [
                    "जल (H2O) का विभाजन ऑक्सीजन (O2) बनाता है" if is_hindi else "Water photolysis (H2O splitting) produces all atmospheric O2",
                    "CO2 का उपयोग बाद में ग्लूकोज बनाने के लिए होता है" if is_hindi else "CO2 is used later during the Calvin cycle to build glucose",
                    "प्रकाश ऊर्जा इस रासायनिक अभिक्रिया को गति देती है" if is_hindi else "Solar photons provide the activation energy for photolysis"
                ],
                "visual_diagram_type": "equation",
                "question": {
                    "question_text": "प्रकाश संश्लेषण में ऑक्सीजन गैस किस अणु के टूटने से मुक्त होती है?" if is_hindi else "Which specific molecule is split to release oxygen during photosynthesis?",
                    "options": [
                        "जल (H2O)" if is_hindi else "Water (H2O)",
                        "कार्बन डाइऑक्साइड (CO2)" if is_hindi else "Carbon Dioxide (CO2)",
                        "ग्लूकोज (C6H12O6)" if is_hindi else "Glucose (C6H12O6)",
                        "नाइट्रोजन गैस" if is_hindi else "Nitrogen gas"
                    ],
                    "correct_answer": "जल (H2O)" if is_hindi else "Water (H2O)",
                    "hint": "Water molecules split into protons and oxygen.",
                    "explanation": "Light reactions split H2O into protons, electrons, and O2."
                }
            }
        elif "sky" in t_lower:
            return {
                "title": "रेले प्रकीर्णन का सादृश्य: रंगीन गेंदों का फिल्टर" if is_hindi else "Visualizing Sky Color: The Particle Wave Filter",
                "explanation": "हवा के कण किसी रंग के नहीं होते। नीले रंग की तरंगें इतनी छोटी होती हैं कि वे हवा के छोटे अणुओं से टकराकर चारों तरफ बिखर जाती हैं, जबकि लाल रंग की लंबी तरंगें बिना टकराए सीधी निकल जाती हैं।" if is_hindi else "Air molecules have no blue dye. Short blue waves are so small that they bounce off tiny gas particles in every direction, filling the entire atmosphere with scattered blue light, while long red waves pass straight through unscattered!",
                "example": "जैसे बारीक छलनी में से बड़े कंचे सीधे निकल जाते हैं लेकिन रेत के कण हर दिशा में उड़ जाते हैं।" if is_hindi else "Like a fine mesh filter that scatters fine sand particles everywhere while allowing rolling bowling balls to pass uninterrupted.",
                "key_points": [
                    "छोटी तरंग दैर्ध्य = विशाल प्रकीर्णन (1 / λ⁴)" if is_hindi else "Short blue wavelength = Maximum atmospheric scattering (1/λ⁴)",
                    "हवा के अणु नीले रंग को चारों दिशाओं में फैलाते हैं" if is_hindi else "Molecules scatter blue light into your line of sight from all angles",
                    "लाल रंग सीधे पार निकल जाता है" if is_hindi else "Long red wavelengths travel directly without significant scattering"
                ],
                "visual_diagram_type": "diagram",
                "question": {
                    "question_text": "आकाश नीला क्यों दिखता है?" if is_hindi else "Why does the daytime sky appear blue rather than red?",
                    "options": [
                        "क्योंकि छोटी नीली तरंगें वायुमंडल में सभी दिशाओं में बिखर जाती हैं" if is_hindi else "Because short blue wavelengths scatter intensely in all directions off air molecules",
                        "क्योंकि हवा का अपना रंग नीला है" if is_hindi else "Because nitrogen gas is naturally dyed blue",
                        "क्योंकि सूरज केवल नीला प्रकाश फेंकता है" if is_hindi else "Because sunlight only contains blue colors",
                        "क्योंकि समुद्र का रंग ऊपर चला जाता है" if is_hindi else "Because gravity pulls red light into the earth"
                    ],
                    "correct_answer": "क्योंकि छोटी नीली तरंगें वायुमंडल में सभी दिशाओं में बिखर जाती हैं" if is_hindi else "Because short blue wavelengths scatter intensely in all directions off air molecules",
                    "hint": "Short wavelengths scatter in all directions.",
                    "explanation": "Rayleigh scattering disperses short blue wavelengths across the sky dome."
                }
            }
        else:
            return {
                "title": f"नए दृष्टिकोण से समझें: {topic}" if is_hindi else f"Intuitive Remediation: Mastering {topic}",
                "explanation": f"आइए {topic} को एक नए और सरल सादृश्य से देखें। जब हम प्रणाली के मुख्य नियमों और कारणों को स्पष्ट रूप से जोड़ते हैं, तो पूरी कार्यप्रणाली एकदम स्पष्ट हो जाती है।" if is_hindi else f"Let's look at {topic} through a completely fresh, intuitive perspective. Tracing how inputs transform step-by-step through core governing constraints resolves the confusion immediately.",
                "example": "जैसे गियर वाली साइकिल में सही गियर चुनना ताकि कम मेहनत में सबसे तेज गति मिल सके।" if is_hindi else "Like shifting gears on a bicycle: matching input force to gear ratios produces smooth, efficient forward momentum.",
                "key_points": [
                    f"{topic} के मुख्य कारण और प्रभाव की स्पष्ट पहचान" if is_hindi else f"Clear causal relationships governing {topic}",
                    "चरों और बाधाओं के बीच सही संबंध" if is_hindi else "Resolving inverse vs direct relationships among variables",
                    "सत्यापित सिद्धांतों द्वारा सही समाधान" if is_hindi else "Applying verified operational rules to prevent misconceptions"
                ],
                "visual_diagram_type": "comparison",
                "question": {
                    "question_text": f"{topic} के इस नए दृष्टिकोण से मुख्य निष्कर्ष क्या है?" if is_hindi else f"What is the key takeaway from this re-explanation of {topic}?",
                    "options": [
                        f"{topic} के कारण और प्रभाव के सही संबंधों को समझना" if is_hindi else f"Correctly identifying the governing causal relationships in {topic}",
                        "सभी नियमों को अनदेखा करना" if is_hindi else "Assuming static random behavior",
                        "डेटा को बिना सोचे डिलीट करना" if is_hindi else "Bypassing constraint verification",
                        "सिस्टम की गति शून्य करना" if is_hindi else "Treating dynamic inputs as static zero"
                    ],
                    "correct_answer": f"{topic} के कारण और प्रभाव के सही संबंधों को समझना" if is_hindi else f"Correctly identifying the governing causal relationships in {topic}",
                    "hint": "Focus on the verified governing principles.",
                    "explanation": f"Understanding causal relationships ensures robust problem-solving in {topic}."
                }
            }

    def _handle_followup(self, prompt: str, is_hindi: bool, is_hinglish: bool = False) -> Dict[str, Any]:
        topic, _ = self._extract_clean_topic(prompt)
        p_lower = prompt.lower()

        if "hindi" in p_lower or "हिंदी" in p_lower:
            return {
                "response_text": f"निश्चय ही! {topic} की इस अवधारणा को हिंदी में समझते हैं। इसका मुख्य सिद्धांत यह है कि हर इनपुट व्यवस्थित नियमों के तहत काम करता है और जब हम कारणों को समझते हैं तो परिणाम स्पष्ट हो जाते हैं।",
                "example": "जैसे जब आप नल चालू करते हैं तो पानी का दबाव प्रवाह निर्धारित करता है, वैसे ही यहाँ प्रत्येक चरण पिछले चरण से जुड़ा है।"
            }
        elif "example" in p_lower or "analogy" in p_lower:
            return {
                "response_text": f"Here is another clear real-world analogy for {topic}: Think of an airport security checkpoint. If more security scanners open up, throughput increases and passenger congestion disappears instantly.",
                "example": "Opening additional checkout lanes at a busy supermarket directly reduces wait times for everyone in line."
            }
        elif "simpler" in p_lower or "easier" in p_lower or "don't understand" in p_lower:
            return {
                "response_text": f"Let's break down {topic} into three fundamental steps: First, identify your input variables. Second, observe the transformation rule. Third, verify the final outcome. That is all there is to it!",
                "example": "Like following a 3-step recipe: gather raw ingredients, apply heat, and enjoy the prepared meal."
            }
        else:
            return {
                "response_text": f"Great question regarding {topic}! The core takeaway is to trace how inputs transform through the system's operational constraints to produce predictable outcomes.",
                "example": "Think of it as a clear chain of dominoes where each action triggers the next state predictably."
            }

    def _handle_quiz(self, prompt: str, is_hindi: bool, is_hinglish: bool = False) -> Dict[str, Any]:
        topic, _ = self._extract_clean_topic(prompt)
        t_lower = topic.lower()

        if "photosynthesis" in t_lower:
            return {
                "title": "प्रकाश संश्लेषण मूल्यांकन" if is_hindi else "Photosynthesis Mastery Assessment",
                "questions": [
                    {
                        "id": "qz_1",
                        "question_text": "प्रकाश संश्लेषण में सौर ऊर्जा को अवशोषित करने वाला वर्णक कौन सा है?" if is_hindi else "Which photosynthetic pigment absorbs solar photon energy in chloroplast thylakoids?",
                        "options": [
                            "क्लोरोफिल (Chlorophyll)" if is_hindi else "Chlorophyll a and b",
                            "हीमोग्लोबिन" if is_hindi else "Hemoglobin",
                            "मेलानिन" if is_hindi else "Melanin",
                            "केरोटिन" if is_hindi else "Myoglobin"
                        ],
                        "correct_option_index": 0,
                        "concept_tested": "Chlorophyll Photon Capture",
                        "explanation": "Chlorophyll pigments absorb blue and red light to excite electrons."
                    },
                    {
                        "id": "qz_2",
                        "question_text": "केल्विन चक्र में CO2 का स्थिरीकरण कौन सा एंजाइम करता है?" if is_hindi else "Which primary enzyme fixes atmospheric carbon dioxide into organic sugars?",
                        "options": [
                            "रुबिस्को (RuBisCO)" if is_hindi else "RuBisCO enzyme",
                            "पेप्सिन" if is_hindi else "Pepsin",
                            "लाइगेज" if is_hindi else "DNA Ligase",
                            "ट्रिप्सिन" if is_hindi else "Trypsin"
                        ],
                        "correct_option_index": 0,
                        "concept_tested": "Calvin Cycle RuBisCO Fixation",
                        "explanation": "RuBisCO catalyzes the fixation of CO2 onto RuBP."
                    },
                    {
                        "id": "qz_3",
                        "question_text": "प्रकाश संश्लेषण का मुख्य शर्करा उत्पाद क्या है?" if is_hindi else "What is the primary chemical energy storage molecule produced by photosynthesis?",
                        "options": [
                            "ग्लूकोज (C6H12O6)" if is_hindi else "Glucose (C6H12O6)",
                            "सोडियम क्लोराइड" if is_hindi else "Sodium Chloride",
                            "सल्फ्यूरिक एसिड" if is_hindi else "Sulfuric Acid",
                            "मीथेन" if is_hindi else "Methane gas"
                        ],
                        "correct_option_index": 0,
                        "concept_tested": "Glucose Synthesis",
                        "explanation": "Photosynthesis synthesizes glucose as stored chemical energy."
                    }
                ]
            }

        return {
            "title": f"{topic} मूल्यांकन" if is_hindi else f"Mastery Assessment: {topic}",
            "questions": [
                {
                    "id": "qz_1",
                    "question_text": f"{topic} का केंद्रीय मूलभूत सिद्धांत क्या है?" if is_hindi else f"What is the foundational principle underlying {topic}?",
                    "options": [
                        f"{topic} के व्यवस्थित परिचालन नियमों और संबंधों को समझना" if is_hindi else f"Systematic understanding of governing operational rules in {topic}",
                        "अनियंत्रित यादृच्छिक प्रक्रियाएं" if is_hindi else "Random uncoordinated processes without verification",
                        "इनपुट बाधाओं को अनदेखा करना" if is_hindi else "Ignoring state transitions and system constraints",
                        "स्थिर अपरिवर्तनीय स्थिरांक" if is_hindi else "Treating dynamic inputs as static zero"
                    ],
                    "correct_option_index": 0,
                    "concept_tested": f"{topic} Foundations",
                    "explanation": f"The lesson highlighted systematic operational principles for {topic}."
                },
                {
                    "id": "qz_2",
                    "question_text": f"प्रणाली की बाधाएं {topic} के निष्पादन को कैसे प्रभावित करती हैं?" if is_hindi else f"How do system constraints impact the execution of {topic}?",
                    "options": [
                        "वे परिचालन सीमाओं और प्रदर्शन व्यापार-नापों को परिभाषित करती हैं" if is_hindi else "They define the operating boundaries and performance trade-offs",
                        "उनका सिस्टम पर कोई प्रभाव नहीं पड़ता" if is_hindi else "They have zero impact on system outcomes",
                        "वे सभी डेटा को तुरंत हटा देती हैं" if is_hindi else "They cause all data to be deleted immediately",
                        "वे सभी चरों को शून्य कर देती हैं" if is_hindi else "They turn all dynamic variables into static zeros"
                    ],
                    "correct_option_index": 0,
                    "concept_tested": f"{topic} Operational Dynamics",
                    "explanation": "System constraints dictate operational trade-offs and execution boundaries."
                },
                {
                    "id": "qz_3",
                    "question_text": f"{topic} में विश्वसनीय समस्या समाधान कौन सी रणनीति सुनिश्चित करती है?" if is_hindi else f"Which strategy ensures reliable problem solving in {topic}?",
                    "options": [
                        "बाधाओं का व्यवस्थित विश्लेषण और सत्यापित सिद्धांतों को लागू करना" if is_hindi else "Systematically analyzing requirements and applying verified principles",
                        "सत्यापन और जांच चरणों को छोड़ना" if is_hindi else "Skipping all validation and verification stages",
                        "बिना मापे परिणामों का अनुमान लगाना" if is_hindi else "Guessing outcomes without measuring performance metrics",
                        "सभी वातावरणों को एक जैसा मानना" if is_hindi else "Assuming all external environments are identical"
                    ],
                    "correct_option_index": 0,
                    "concept_tested": f"{topic} Best Practices",
                    "explanation": "Rigorous systematic analysis guarantees predictable outcomes."
                }
            ]
        }

    def _handle_report(self, prompt: str, is_hindi: bool, is_hinglish: bool = False) -> Dict[str, Any]:
        topic, _ = self._extract_clean_topic(prompt)
        t_low = topic.lower()

        # Derive logical next topic in same subject
        if "photosynthesis" in t_low or "cellular" in t_low or "bio" in t_low:
            next_topic = "पादप फिजियोलॉजी और सेलुलर मेटाबॉलिज्म" if is_hindi else "Cellular Respiration, ATP Synthase & Metabolic Pathways"
        elif "recursion" in t_low or "algorithm" in t_low or "programming" in t_low:
            next_topic = "डायनामिक प्रोग्रामिंग और ट्री ट्रैवर्सल" if is_hindi else "Dynamic Programming, Memoization & Tree Traversal Algorithms"
        elif "blockchain" in t_low or "crypto" in t_low:
            next_topic = "स्मार्ट कॉन्ट्रैक्ट्स और डीसेंट्रलाइज्ड ऐप्स (DApps)" if is_hindi else "Smart Contract Architecture, Zero-Knowledge Proofs & DApps"
        elif "tcp" in t_low or "udp" in t_low or "network" in t_low:
            next_topic = "HTTP/3, QUIC प्रोटोकॉल और सॉकेट प्रोग्रामिंग" if is_hindi else "HTTP/3, QUIC Protocol & Asynchronous Socket Architectures"
        elif "machine learning" in t_low or "ai" in t_low or "agent" in t_low:
            next_topic = "ट्रांसफॉर्मर आर्किटेक्चर और ऑटोनॉमस मल्टी-एजेंट सिस्टम" if is_hindi else "Transformer Architectures, RAG & Autonomous Multi-Agent Workflows"
        elif "newton" in t_low or "physics" in t_low or "motion" in t_low:
            next_topic = "कार्य, ऊर्जा, शक्ति और संवेग संरक्षण" if is_hindi else "Work, Energy, Power & Conservation of Linear Momentum"
        elif "electric" in t_low or "ohm" in t_low or "circuit" in t_low:
            next_topic = "किरचॉफ के नियम और एसी परिपथ विश्लेषण" if is_hindi else "Kirchhoff's Laws, AC Circuit Analysis & RC Time Constants"
        else:
            next_topic = f"{topic} के उन्नत अनुप्रयोग और रियल-वर्ल्ड प्रोजेक्ट्स" if is_hindi else f"Advanced Real-World Applications & Architecture of {topic}"

        return {
            "recommendations": [
                f"आपने {topic} के मुख्य सिद्धांतों पर मजबूत वैचारिक पकड़ बनाई है।" if is_hindi else f"You demonstrated strong conceptual grasp of the core principles of {topic}.",
                f"अब आप व्यावहारिक समस्याओं और उन्नत परिदृश्यों को हल करने के लिए तैयार हैं।" if is_hindi else f"You are ready to advance to real-world problem-solving and architectural design in {topic}."
            ],
            "next_recommended_topic": next_topic,
            "summary_feedback": f"अद्भुत प्रदर्शन! आपने {topic} में उत्कृष्ट समझ प्रदर्शित की है।" if is_hindi else f"Outstanding performance! You achieved mastery on {topic}, demonstrating a robust understanding of core concepts and mechanisms."
        }


def extract_json_from_text(text: str) -> Dict[str, Any]:
    if not text:
        return {}
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r'(\{[\s\S]*\})', text)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return {}


class ResilientLLMProvider(LLMProvider):
    """
    Multi-Provider Resilient LLM Wrapper.
    Orchestrates execution with:
    1. Primary provider retry (up to 2 attempts)
    2. Automatic failover to secondary configured provider (Gemini <-> Groq)
    3. Final fallback to zero-dependency OfflineProvider
    """
    def __init__(self, primary: Optional[LLMProvider] = None, secondary: Optional[LLMProvider] = None, fallback: Optional[LLMProvider] = None):
        self.primary = primary
        self.secondary = secondary
        self.fallback = fallback or OfflineProvider()
        self.active_provider_name = (
            "Gemini" if isinstance(self.primary, GeminiProvider)
            else "Groq" if isinstance(self.primary, GroqProvider)
            else "Offline"
        )
        self.fallback_occurred = False

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        # 1. Primary provider with retry
        if self.primary:
            for attempt in range(2):
                try:
                    res = self.primary.generate_text(prompt, system_prompt=system_prompt, temperature=temperature)
                    if res:
                        return res
                except Exception as e:
                    print(f"[ResilientLLM] Primary attempt {attempt+1} failed: {e}")

        # 2. Secondary provider failover
        if self.secondary:
            try:
                print("[ResilientLLM] Failing over to secondary provider...")
                self.fallback_occurred = True
                res = self.secondary.generate_text(prompt, system_prompt=system_prompt, temperature=temperature)
                if res:
                    return res
            except Exception as e:
                print(f"[ResilientLLM] Secondary provider failed: {e}")

        # 3. Offline fallback
        self.fallback_occurred = True
        return self.fallback.generate_text(prompt, system_prompt=system_prompt, temperature=temperature)

    def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Dict[str, Any]:
        # 1. Primary provider with retry
        if self.primary:
            for attempt in range(2):
                try:
                    res = self.primary.generate_json(prompt, system_prompt=system_prompt)
                    if res:
                        return res
                except Exception as e:
                    print(f"[ResilientLLM] Primary attempt {attempt+1} failed: {e}")

        # 2. Secondary provider failover
        if self.secondary:
            try:
                print("[ResilientLLM] Failing over to secondary provider...")
                self.fallback_occurred = True
                res = self.secondary.generate_json(prompt, system_prompt=system_prompt)
                if res:
                    return res
            except Exception as e:
                print(f"[ResilientLLM] Secondary provider failed: {e}")

        # 3. Offline fallback
        self.fallback_occurred = True
        return self.fallback.generate_json(prompt, system_prompt=system_prompt)

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_provider": self.active_provider_name,
            "has_primary": self.primary is not None,
            "has_secondary": self.secondary is not None,
            "fallback_occurred": self.fallback_occurred
        }


def create_llm_provider() -> LLMProvider:
    """
    Factory creating the ResilientLLMProvider instance based on environment variables.
    """
    chosen_provider = os.getenv("LLM_PROVIDER", "").lower().strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    groq_key = os.getenv("GROQ_API_KEY", "").strip()

    primary = None
    secondary = None

    if (chosen_provider == "gemini" or not chosen_provider) and gemini_key and _GEMINI_AVAILABLE:
        try:
            model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            primary = GeminiProvider(api_key=gemini_key, model_name=model)
        except Exception as e:
            print(f"[LLM] Gemini initialization error: {e}")

    if (chosen_provider == "groq" or not chosen_provider or primary is not None) and groq_key and _GROQ_AVAILABLE:
        try:
            model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
            if primary is None:
                primary = GroqProvider(api_key=groq_key, model_name=model)
            else:
                secondary = GroqProvider(api_key=groq_key, model_name=model)
        except Exception as e:
            print(f"[LLM] Groq initialization error: {e}")

    # If groq was chosen and gemini is available as secondary
    if chosen_provider == "groq" and gemini_key and _GEMINI_AVAILABLE and secondary is None and primary is not None:
        try:
            model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            secondary = GeminiProvider(api_key=gemini_key, model_name=model)
        except Exception:
            pass

    return ResilientLLMProvider(primary=primary, secondary=secondary, fallback=OfflineProvider())


# Global singleton provider instance
llm_service = create_llm_provider()

