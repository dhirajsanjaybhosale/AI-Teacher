import uuid
from typing import Optional, Dict, Any
from .schemas import LessonPlan, Segment, Question, LearnerPreferences
from app.llm.llm_service import llm_service


class LessonPlanner:
    """
    Synthesizes structured, time-budgeted pedagogical curricula from RAG context or topics.
    Outputs rich schemas compatible with voice narration, visual slide generation, and formative checks.
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
        Creates a full structured lesson plan.
        """
        # Determine number of segments based on time budget
        time_mins = preferences.time_minutes
        if time_mins <= 5:
            num_segments = 2
        elif time_mins <= 10:
            num_segments = 3
        elif time_mins <= 15:
            num_segments = 4
        else:
            num_segments = 5

        lang_code = preferences.language.lower()
        is_hindi = (lang_code == "hi")
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"
        level = preferences.level.lower()

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
            context_section = f"TOPIC TO TEACH: {preferences.topic}"

        system_prompt = f"""You are an elite, world-class interactive AI Teacher.
Your mission is to craft a structured, highly engaging educational lesson for a student.

STUDENT PROFILE:
- Target Level: {level.upper()} (adapt vocabulary, depth, and pacing accordingly)
- Time Budget: {time_mins} minutes (create exactly {num_segments} structured instructional segments)
- Instruction Language: {lang_name} ({'ALL titles, spoken explanations, examples, key points, and questions MUST be written in natural, fluent Hindi script' if is_hindi else 'All content must be in clear, engaging, conversational English'})

PEDAGOGICAL REQUIREMENTS FOR EACH SEGMENT:
1. 'explanation': Natural, spoken narration script (approx 60-90 words). The AI avatar will speak this directly to the student. Sound warm, enthusiastic, and pedagogical.
2. 'example': A vivid, intuitive real-world analogy.
3. 'key_points': 3-4 concise bullet points summarizing the core takeaways (these will be rendered on the on-screen visual slide).
4. 'visual_diagram_type': Choose one from: 'flowchart', 'cycle', 'comparison', 'structure', 'process'.
5. 'question': An embedded formative assessment check question testing understanding of that specific segment, with 4 options, the correct answer, a helpful hint, and an explanation.

CRITICAL JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object matching this exact structure:
{{
  "lesson_id": "lesson_{uuid.uuid4().hex[:8]}",
  "title": "Main Lesson Title",
  "description": "Short 1-2 sentence overview of what the learner will master",
  "target_level": "{level}",
  "target_language": "{preferences.language}",
  "estimated_minutes": {time_mins},
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

Ensure high conceptual accuracy, pedagogical clarity, and strict adherence to the requested JSON format in {lang_name}."""

        response_dict = self.llm.generate_json(prompt, system_prompt=system_prompt)

        # Enforce lesson_id and sanitize
        if not response_dict.get("lesson_id"):
            response_dict["lesson_id"] = f"lesson_{uuid.uuid4().hex[:8]}"

        response_dict["target_level"] = level
        response_dict["target_language"] = preferences.language
        response_dict["estimated_minutes"] = time_mins
        response_dict["source_type"] = "pdf" if retrieved_context else "topic"
        response_dict["source_name"] = source_name or preferences.topic

        # Sanitize segments
        segments_raw = response_dict.get("segments", [])
        sanitized_segments = []
        for i, s_data in enumerate(segments_raw):
            seg_id = s_data.get("id") or f"seg_{i+1}"
            q_data = s_data.get("question") or {}
            q_id = q_data.get("id") or f"q_{i+1}"
            
            question_obj = Question(
                id=q_id,
                question_text=q_data.get("question_text", "What is the key takeaway from this segment?"),
                options=q_data.get("options", ["Option A", "Option B", "Option C", "Option D"]),
                correct_answer=str(q_data.get("correct_answer", "Option A")),
                hint=q_data.get("hint", ""),
                explanation=q_data.get("explanation", "")
            )
            
            seg_obj = Segment(
                id=seg_id,
                title=s_data.get("title", f"Concept {i+1}"),
                explanation=s_data.get("explanation", ""),
                example=s_data.get("example", ""),
                key_points=s_data.get("key_points", []),
                visual_diagram_type=s_data.get("visual_diagram_type", "flowchart"),
                question=question_obj,
                is_remediation=s_data.get("is_remediation", False)
            )
            sanitized_segments.append(seg_obj)

        if not sanitized_segments:
            # Create a minimum fallback segment if empty
            default_q = Question(
                id="q_1",
                question_text="What is the core principle taught in this lesson?",
                options=["Key Principle A", "Alternative B", "Alternative C", "Alternative D"],
                correct_answer="Key Principle A",
                hint="Review the primary key point.",
                explanation="This principle forms the foundation of the topic."
            )
            sanitized_segments.append(Segment(
                id="seg_1",
                title=preferences.topic or "Introduction",
                explanation=f"Welcome to this lesson on {preferences.topic or 'the subject'}. Let's master the core concepts together.",
                example="Consider how interconnected elements work in harmony.",
                key_points=["Foundation concept", "Operational mechanism", "Practical application"],
                visual_diagram_type="flowchart",
                question=default_q
            ))

        return LessonPlan(
            lesson_id=response_dict["lesson_id"],
            title=response_dict.get("title", f"Mastering {preferences.topic or source_name}"),
            description=response_dict.get("description", "A structured interactive lesson session."),
            target_level=level,
            target_language=preferences.language,
            estimated_minutes=time_mins,
            segments=sanitized_segments,
            source_type=response_dict["source_type"],
            source_name=response_dict["source_name"]
        )
