import uuid
from typing import Optional, Dict, Any, List
from .schemas import LessonPlan, Segment, Question, LearnerPreferences
from app.llm.llm_service import llm_service


class LessonPlanner:
    """
    Synthesizes structured, time-budgeted pedagogical curricula from RAG context or arbitrary user topics.
    Outputs rich schemas compatible with voice narration, subject-aware visual slide generation, and formative checks.
    """

    def __init__(self):
        self.llm = llm_service

    def plan_lesson(
        self,
        preferences: LearnerPreferences,
        retrieved_context: Optional[str] = None,
        source_name: Optional[str] = None
    ) -> LessonPlan:
        """
        Creates a full structured lesson plan tailored to any educational subject.
        """
        # Determine number of segments based on time budget
        time_mins = preferences.time_minutes
        if time_mins <= 5:
            num_segments = 2
        elif time_mins <= 10:
            num_segments = 3
        elif time_mins <= 20:
            num_segments = 4
        elif time_mins <= 30:
            num_segments = 5
        else:
            num_segments = 6

        lang_code = preferences.language.lower()
        is_hindi = (lang_code == "hi" or "hindi" in lang_code)
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"
        level = preferences.level.lower()
        goal = preferences.goal or "understand"
        style = preferences.teaching_style or "intuitive"

        # Build prompt
        context_section = ""
        if retrieved_context and retrieved_context.strip():
            context_section = f"""
SOURCE MATERIAL / DOCUMENT EXCERPTS (Grounded Content):
\"\"\"
{retrieved_context[:4000]}
\"\"\"
"""
        else:
            context_section = f"USER TOPIC REQUEST: \"{preferences.topic}\""

        system_prompt = f"""You are a world-class educational curriculum architect and empathetic AI Teacher.
Your mission is to synthesize an intuitive, structured educational lesson for a student on any topic.

STUDENT PROFILE:
- Target Level: {level.upper()} (adapt vocabulary, depth, and pacing accordingly)
- Time Budget: {time_mins} minutes (create exactly {num_segments} structured instructional segments)
- Learning Goal: {goal.upper()} (e.g., focus on interview depth, exam definitions, or intuitive understanding)
- Teaching Style: {style.upper()}
- Instruction Language: {lang_name} ({'ALL titles, spoken explanations, examples, key points, and questions MUST be written in natural, fluent Hindi script' if is_hindi else 'All content must be in clear, engaging, conversational English'})

PEDAGOGICAL REQUIREMENTS FOR EACH SEGMENT:
1. 'title': Clear, distinct subtopic title.
2. 'explanation': Natural, spoken narration script (approx 60-90 words). The AI avatar will speak this directly to the student. Sound warm, enthusiastic, and pedagogical.
3. 'example': A vivid, intuitive real-world analogy or practical application.
4. 'key_points': 3-4 concise bullet points summarizing the core takeaways (these will be rendered on the on-screen visual slide).
5. 'visual_diagram_type': Choose the most appropriate representation: 'code' (for programming/CS), 'equation' (for math/physics), 'comparison' (for vs/trade-offs), 'flowchart' or 'process' (for mechanisms/algorithms), 'timeline' (for history/sequences), 'diagram' (for conceptual/biological structures).
6. 'visual_description': A short 1-sentence description of what visual card to display.
7. 'visual_code_or_math': A short representative snippet (code, formula, or steps) if applicable.
8. 'question': An embedded formative assessment check question testing understanding of that specific segment, with 4 options, the correct answer, a helpful hint, and an explanation.

CRITICAL JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object matching this exact structure:
{{
  "lesson_id": "lesson_{uuid.uuid4().hex[:8]}",
  "title": "Main Lesson Title",
  "subject": "Physics | Computer Science | Biology | Mathematics | General",
  "description": "Short 1-2 sentence overview of what the learner will master",
  "learning_objectives": ["Objective 1", "Objective 2", "Objective 3"],
  "target_level": "{level}",
  "target_language": "{preferences.language}",
  "estimated_minutes": {time_mins},
  "goal": "{goal}",
  "source_type": "{"pdf" if retrieved_context else "topic"}",
  "source_name": "{source_name or preferences.topic}",
  "segments": [
    {{
      "id": "seg_1",
      "title": "Segment 1 Subtopic Title",
      "explanation": "Spoken avatar narration text here...",
      "example": "Real-world analogy here...",
      "key_points": ["Point 1", "Point 2", "Point 3"],
      "visual_diagram_type": "flowchart",
      "visual_description": "Step-by-step concept flow",
      "visual_code_or_math": "",
      "question": {{
        "id": "q_1",
        "question_text": "Clear question testing the segment concept?",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "correct_answer": "Option A",
        "hint": "Gentle nudge hint...",
        "explanation": "Why this answer is right..."
      }}
    }}
  ]
}}
"""

        prompt = f"""Create a {num_segments}-segment lesson plan for: '{preferences.topic or source_name}'.
{context_section}

Ensure high conceptual accuracy, pedagogical clarity, subject-appropriate visuals, and strict adherence to the requested JSON format in {lang_name}."""

        response_dict = self.llm.generate_json(prompt, system_prompt=system_prompt)

        # Enforce unique lesson_id and sanitize
        lesson_id = f"lesson_{uuid.uuid4().hex[:8]}"
        if response_dict.get("lesson_id") and response_dict["lesson_id"].startswith("lesson_"):
            # Ensure uniqueness
            lesson_id = f"{response_dict['lesson_id']}_{uuid.uuid4().hex[:4]}"
        
        response_dict["lesson_id"] = lesson_id
        response_dict["target_level"] = level
        response_dict["target_language"] = preferences.language
        response_dict["estimated_minutes"] = time_mins
        response_dict["goal"] = goal
        response_dict["source_type"] = "pdf" if retrieved_context else "topic"
        response_dict["source_name"] = source_name or preferences.topic

        # Sanitize segments
        segments_raw = response_dict.get("segments", [])
        sanitized_segments: List[Segment] = []
        for i, s_data in enumerate(segments_raw):
            seg_id = s_data.get("id") or f"seg_{i+1}"
            q_data = s_data.get("question") or {}
            q_id = q_data.get("id") or f"q_{i+1}"
            
            question_obj = Question(
                id=q_id,
                question_text=q_data.get("question_text", f"What is the key takeaway regarding {s_data.get('title', f'Concept {i+1}')}?"),
                options=q_data.get("options", ["Option A", "Option B", "Option C", "Option D"]),
                correct_answer=str(q_data.get("correct_answer", "Option A")),
                hint=q_data.get("hint", ""),
                explanation=q_data.get("explanation", "")
            )
            
            seg_obj = Segment(
                id=seg_id,
                title=s_data.get("title", f"Concept {i+1}"),
                explanation=s_data.get("explanation", f"Let's explore {s_data.get('title', 'this key principle')}."),
                example=s_data.get("example", ""),
                key_points=s_data.get("key_points", [f"Key principle of {s_data.get('title', 'this topic')}"]),
                visual_diagram_type=s_data.get("visual_diagram_type", "flowchart"),
                visual_description=s_data.get("visual_description", ""),
                visual_code_or_math=s_data.get("visual_code_or_math", ""),
                question=question_obj,
                is_remediation=s_data.get("is_remediation", False)
            )
            sanitized_segments.append(seg_obj)

        if not sanitized_segments:
            # Fallback dynamic segments for arbitrary topic
            default_title = preferences.topic or source_name or "Foundations"
            sanitized_segments = [
                Segment(
                    id="seg_1",
                    title=f"Core Foundations of {default_title}",
                    explanation=f"Welcome! Today we are exploring {default_title}. Understanding the underlying core mechanics allows you to reason about practical applications effectively.",
                    example="Think of this system as interconnected components operating in harmony.",
                    key_points=[
                        f"Fundamental definition of {default_title}",
                        "Primary operational rules and relationships",
                        "Practical real-world implications"
                    ],
                    visual_diagram_type="flowchart",
                    visual_description="Foundation structure diagram",
                    question=Question(
                        id="q_1",
                        question_text=f"What is the central foundational premise of {default_title}?",
                        options=[
                            f"Understanding the core operational rules of {default_title}",
                            "Ignoring intermediate state transitions",
                            "Treating all variables as static constants",
                            "Relying solely on external random inputs"
                        ],
                        correct_answer=f"Understanding the core operational rules of {default_title}",
                        hint="Focus on the primary definition.",
                        explanation=f"The lesson emphasizes foundational mechanics for {default_title}."
                    )
                ),
                Segment(
                    id="seg_2",
                    title=f"Operational Mechanics & Practical Applications",
                    explanation=f"Now let's examine how {default_title} behaves under varying constraints and real-world conditions.",
                    example="Like tuning parameters in an optimized system to achieve peak performance.",
                    key_points=[
                        "Step-by-step causal mechanism",
                        "Handling edge cases and constraints",
                        "Industry and academic best practices"
                    ],
                    visual_diagram_type="process",
                    visual_description="Process workflow diagram",
                    question=Question(
                        id="q_2",
                        question_text=f"How do we apply the mechanics of {default_title} to solve real-world problems?",
                        options=[
                            "By systematically analyzing constraints and applying principles",
                            "By bypassing verification stages",
                            "By assuming all inputs are identical",
                            "Without tracking state progression"
                        ],
                        correct_answer="By systematically analyzing constraints and applying principles",
                        hint="Think about structured problem solving.",
                        explanation="Systematic application ensures predictable, robust outcomes."
                    )
                )
            ]

        return LessonPlan(
            lesson_id=lesson_id,
            title=response_dict.get("title", f"Mastering {preferences.topic or source_name}"),
            subject=response_dict.get("subject", "General"),
            description=response_dict.get("description", f"A personalized {time_mins}-minute interactive masterclass on {preferences.topic or source_name}."),
            learning_objectives=response_dict.get("learning_objectives", [f"Understand {preferences.topic or source_name}", "Apply core principles", "Verify understanding"]),
            target_level=level,
            target_language=preferences.language,
            estimated_minutes=time_mins,
            goal=goal,
            segments=sanitized_segments,
            source_type=response_dict["source_type"],
            source_name=response_dict["source_name"]
        )


# Global singleton
lesson_planner = LessonPlanner()
