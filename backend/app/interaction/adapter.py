import uuid
from typing import Optional, Dict, Any
from app.lesson_planning.schemas import Segment, Question, EvaluationResult
from app.narration_avatar.video_assembler import video_assembler
from app.llm.llm_service import llm_service


class LessonAdapter:
    """
    Dynamically generates customized remediation re-explanations and videos
    targeting specific student misconceptions identified during formative assessment checks.
    """

    def __init__(self):
        self.llm = llm_service
        self.assembler = video_assembler

    def create_remediation_segment(
        self,
        original_segment: Segment,
        user_answer: str,
        misconception: str,
        lesson_title: str = "AI Teacher Lesson",
        language: str = "en"
    ) -> Segment:
        """
        Synthesizes a novel, customized remediation segment and generates its video clip.
        """
        is_hindi = (language.lower() in ["hi", "hindi"])
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"
        remed_id = f"remed_{uuid.uuid4().hex[:6]}"

        system_prompt = f"""You are an elite adaptive AI Teacher specializing in intuitive remediation and misconception unblocking.
A student gave an incorrect answer to a check question. Your goal is to re-explain the concept using a completely fresh, intuitive analogy or visual perspective.

LANGUAGE: {lang_name} ({'Respond entirely in natural, encouraging Hindi script' if is_hindi else 'Respond in clear, supportive English'})

PEDAGOGICAL STRATEGY:
1. 'title': Engaging title indicating a fresh perspective (e.g., 'Revisiting Energy Storage: Fuel vs. Battery' or 'नए नजरिए से समझें').
2. 'explanation': Conversational spoken script (approx 50-70 words) for the AI avatar. Empathize, clarify the exact misconception, and present the new angle.
3. 'example': A vivid, memorable analogy different from the original segment.
4. 'key_points': 3 crystal-clear bullet points summarizing why the new distinction matters.
5. 'question': A quick confirmation check question with 4 options and the correct answer.

JSON SPECIFICATION:
Respond ONLY with a JSON object matching:
{{
  "title": "Remediation Subtopic Title",
  "explanation": "Spoken avatar script...",
  "example": "Fresh analogy...",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "visual_diagram_type": "comparison",
  "question": {{
    "question_text": "Confirmation check question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "hint": "Hint...",
    "explanation": "Why correct..."
  }}
}}
"""

        prompt = f"""ORIGINAL SEGMENT TITLE: {original_segment.title}
ORIGINAL CONCEPT: {original_segment.explanation}
ORIGINAL QUESTION: {original_segment.question.question_text}
STUDENT ANSWER: "{user_answer}"
DIAGNOSED MISCONCEPTION: "{misconception}"

Create an adaptive remediation segment that bridges this conceptual gap."""

        res = self.llm.generate_json(prompt, system_prompt=system_prompt)

        # Parse question
        q_data = res.get("question") or {}
        remed_q = Question(
            id=f"q_{remed_id}",
            question_text=q_data.get("question_text", "What is the key takeaway from this re-explanation?"),
            options=q_data.get("options", ["Key Takeaway A", "Option B", "Option C", "Option D"]),
            correct_answer=str(q_data.get("correct_answer", "Key Takeaway A")),
            hint=q_data.get("hint", ""),
            explanation=q_data.get("explanation", "")
        )

        remed_segment = Segment(
            id=remed_id,
            title=res.get("title", f"Deep Dive: {original_segment.title}"),
            explanation=res.get("explanation", f"Let's look at {original_segment.title} from another angle."),
            example=res.get("example", "Think of this mechanism as a streamlined sequence of handoffs."),
            key_points=res.get("key_points", [
                f"Clarifying the misconception regarding {original_segment.title}",
                "Understanding the core operational principle",
                "Connecting key variables and causal relationships"
            ]),
            visual_diagram_type=res.get("visual_diagram_type", "comparison"),
            question=remed_q,
            is_remediation=True
        )

        # Assemble the remediation video immediately
        print(f"[LessonAdapter] Assembling remediation video for segment '{remed_segment.title}'...")
        video_info = self.assembler.assemble_segment_video(
            segment=remed_segment,
            lesson_title=f"{lesson_title} (Remediation)",
            segment_index=1,
            total_segments=1,
            language=language
        )
        remed_segment.video_url = video_info["relative_url"]

        return remed_segment


# Global singleton
lesson_adapter = LessonAdapter()
