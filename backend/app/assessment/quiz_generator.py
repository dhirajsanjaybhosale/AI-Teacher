import uuid
from typing import List, Dict, Any, Optional
from app.lesson_planning.schemas import LessonPlan, Quiz, QuizQuestion
from app.llm.llm_service import llm_service


class QuizGenerator:
    """
    Generates comprehensive summative quizzes strictly grounded in the taught lesson curriculum.
    Ensures zero cross-topic contamination by dynamically deriving questions from the active lesson plan.
    """

    def __init__(self):
        self.llm = llm_service

    def generate_quiz(self, lesson_plan: LessonPlan) -> Quiz:
        """
        Synthesizes 3-5 multiple-choice questions testing core concepts taught in the lesson.
        """
        is_hindi = (lesson_plan.target_language.lower() in ["hi", "hindi"])
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"
        quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"

        # Extract summary of segments
        segment_summaries = []
        for idx, s in enumerate(lesson_plan.segments):
            kp_str = ", ".join(s.key_points) if s.key_points else s.title
            segment_summaries.append(
                f"- Concept {idx+1} '{s.title}': {s.explanation[:150]} (Key takeaways: {kp_str})"
            )

        curriculum_text = "\n".join(segment_summaries)

        system_prompt = f"""You are an assessment specialist creating a summative quiz for a student who just finished a lesson on '{lesson_plan.title}'.
CRITICAL: Every question MUST be strictly and solely about '{lesson_plan.title}' and the specific concepts taught in this lesson. Do NOT ask about unrelated subjects.

LANGUAGE: {lang_name} ({'All questions, options, and explanations must be in natural Hindi script' if is_hindi else 'All questions, options, and explanations must be in clear English'})

REQUIREMENTS:
1. Exactly 3 conceptual multiple-choice questions testing the provided concepts.
2. Each question has 4 options.
3. Indicate 'correct_option_index' (0, 1, 2, or 3).
4. State 'concept_tested' (a concise 2-4 word concept name strictly from this lesson).
5. Provide a clear pedagogical 'explanation'.

JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object:
{{
  "title": "Mastery Quiz: {lesson_plan.title}",
  "questions": [
    {{
      "id": "qz_1",
      "question_text": "Clear question testing concept...",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_option_index": 0,
      "concept_tested": "Concept Name",
      "explanation": "Why option A is correct..."
    }}
  ]
}}
"""

        prompt = f"""QUIZ REQUEST FOR LESSON: {lesson_plan.title}
TARGET LEVEL: {lesson_plan.target_level}
CONCEPTS TAUGHT IN THIS LESSON:
{curriculum_text}

Generate the 3-question mastery quiz strictly grounded in these concepts."""

        res = self.llm.generate_json(prompt, system_prompt=system_prompt)

        raw_questions = res.get("questions", [])
        quiz_questions: List[QuizQuestion] = []

        for i, q in enumerate(raw_questions):
            q_id = q.get("id") or f"qz_{i+1}"
            options = q.get("options") or ["Option A", "Option B", "Option C", "Option D"]
            if len(options) < 2:
                options = ["Option A", "Option B", "Option C", "Option D"]
            correct_idx = q.get("correct_option_index", 0)
            if not isinstance(correct_idx, int) or correct_idx < 0 or correct_idx >= len(options):
                correct_idx = 0

            quiz_questions.append(QuizQuestion(
                id=q_id,
                question_text=q.get("question_text", f"Key conceptual question on {lesson_plan.title}"),
                options=options,
                correct_option_index=correct_idx,
                concept_tested=q.get("concept_tested", f"{lesson_plan.title} - Concept {i+1}"),
                explanation=q.get("explanation", "Review the lesson material for more details.")
            ))

        # Dynamic topic-grounded fallback if LLM returned insufficient questions
        if len(quiz_questions) < 3:
            quiz_questions = self._build_dynamic_grounded_quiz(lesson_plan, is_hindi)

        return Quiz(
            quiz_id=quiz_id,
            lesson_id=lesson_plan.lesson_id,
            title=res.get("title", f"Mastery Assessment: {lesson_plan.title}"),
            questions=quiz_questions[:5]
        )

    def _build_dynamic_grounded_quiz(self, lesson_plan: LessonPlan, is_hindi: bool) -> List[QuizQuestion]:
        """
        Dynamically constructs quiz questions directly from the segments of the active lesson plan.
        Guarantees 100% domain relevance for any arbitrary uploaded document or topic with zero contamination.
        """
        questions: List[QuizQuestion] = []

        for idx, segment in enumerate(lesson_plan.segments):
            q_src = segment.question
            options = list(q_src.options) if q_src.options and len(q_src.options) >= 2 else [
                q_src.correct_answer,
                f"Alternative perspective on {segment.title}",
                f"Contradictory factor to {segment.title}",
                "None of the above"
            ]

            # Find correct option index
            correct_idx = 0
            for opt_idx, opt in enumerate(options):
                if opt.strip().lower() == q_src.correct_answer.strip().lower():
                    correct_idx = opt_idx
                    break

            concept_name = segment.title if segment.title else f"Core Principle {idx+1}"

            questions.append(QuizQuestion(
                id=f"qz_{idx+1}",
                question_text=q_src.question_text if q_src.question_text else f"What is the key takeaway regarding {segment.title}?",
                options=options,
                correct_option_index=correct_idx,
                concept_tested=concept_name,
                explanation=q_src.explanation if q_src.explanation else segment.explanation[:120]
            ))

        # If still fewer than 3 questions, create supplementary questions from segment key points
        q_counter = len(questions) + 1
        for segment in lesson_plan.segments:
            if len(questions) >= 3:
                break
            if segment.key_points:
                primary_point = segment.key_points[0]
                q_text = (
                    f"'{primary_point}' के संदर्भ में {segment.title} का मुख्य सिद्धांत क्या है?"
                    if is_hindi else
                    f"Which principle accurately describes '{segment.title}' based on the lesson?"
                )
                questions.append(QuizQuestion(
                    id=f"qz_{q_counter}",
                    question_text=q_text,
                    options=[
                        primary_point,
                        f"The opposite of {primary_point}",
                        "An unrelated secondary factor",
                        "No direct relation exists"
                    ],
                    correct_option_index=0,
                    concept_tested=f"{segment.title} Mechanism",
                    explanation=f"The lesson emphasized that: {primary_point}."
                ))
                q_counter += 1

        return questions


# Global singleton
quiz_generator = QuizGenerator()
