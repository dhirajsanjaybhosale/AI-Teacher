import uuid
from typing import List, Dict, Any, Optional
from app.lesson_planning.schemas import LessonPlan, Quiz, QuizQuestion
from app.llm.llm_service import llm_service


class QuizGenerator:
    """
    Generates comprehensive summative quizzes grounded in the taught lesson curriculum.
    """

    def __init__(self):
        self.llm = llm_service

    def generate_quiz(self, lesson_plan: LessonPlan) -> Quiz:
        """
        Synthesizes 3-5 multiple-choice questions testing core concepts of the lesson.
        """
        is_hindi = (lesson_plan.target_language.lower() in ["hi", "hindi"])
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"
        quiz_id = f"quiz_{uuid.uuid4().hex[:8]}"

        # Extract summary of segments
        segment_summaries = []
        for s in lesson_plan.segments:
            segment_summaries.append(f"- Subtopic '{s.title}': {s.explanation[:120]} (Key points: {', '.join(s.key_points)})")

        curriculum_text = "\n".join(segment_summaries)

        system_prompt = f"""You are an assessment specialist. Create a 3-question multiple-choice summative quiz for a student who just finished this lesson.

LANGUAGE: {lang_name} ({'All questions, options, and explanations must be in natural Hindi script' if is_hindi else 'All questions, options, and explanations must be in clear English'})

REQUIREMENTS:
1. Exactly 3 conceptual multiple-choice questions.
2. Each question has 4 options.
3. Indicate 'correct_option_index' (0, 1, 2, or 3).
4. State 'concept_tested' (a concise 2-4 word concept name).
5. Provide a clear pedagogical 'explanation'.

JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object:
{{
  "title": "Mastery Quiz: Lesson Title",
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

        prompt = f"""LESSON TITLE: {lesson_plan.title}
TARGET LEVEL: {lesson_plan.target_level}
CURRICULUM COVERED:
{curriculum_text}

Generate the 3-question mastery quiz."""

        res = self.llm.generate_json(prompt, system_prompt=system_prompt)

        raw_questions = res.get("questions", [])
        quiz_questions: List[QuizQuestion] = []

        for i, q in enumerate(raw_questions):
            q_id = q.get("id") or f"qz_{i+1}"
            options = q.get("options") or ["Option A", "Option B", "Option C", "Option D"]
            correct_idx = q.get("correct_option_index", 0)
            if not isinstance(correct_idx, int) or correct_idx < 0 or correct_idx >= len(options):
                correct_idx = 0

            quiz_questions.append(QuizQuestion(
                id=q_id,
                question_text=q.get("question_text", f"Assessment Question {i+1}"),
                options=options,
                correct_option_index=correct_idx,
                concept_tested=q.get("concept_tested", f"Core Concept {i+1}"),
                explanation=q.get("explanation", "Review the lesson material for more details.")
            ))

        if not quiz_questions:
            # Fallback 3 questions
            quiz_questions = [
                QuizQuestion(
                    id="qz_1",
                    question_text=f"What is the main biological function emphasized in {lesson_plan.title}?",
                    options=["Energy production & regulation", "Structural bone support", "Photosynthetic light capture", "Passive diffusion"],
                    correct_option_index=0,
                    concept_tested="Primary Biological Function",
                    explanation="The lesson highlighted energetic synthesis and cellular metabolism."
                ),
                QuizQuestion(
                    id="qz_2",
                    question_text="How does the system maintain biochemical efficiency?",
                    options=["Through regulated multi-stage enzymatic coupling", "By skipping electron transfer", "By relying strictly on heat", "Without consuming any reactants"],
                    correct_option_index=0,
                    concept_tested="Metabolic Regulation",
                    explanation="Multi-stage pathways minimize heat loss and maximize ATP generation."
                ),
                QuizQuestion(
                    id="qz_3",
                    question_text="What happens if the terminal acceptor is absent?",
                    options=["The respiratory chain halts and ATP synthesis declines", "Respiration rate doubles", "ATP synthase spins faster", "Nothing changes"],
                    correct_option_index=0,
                    concept_tested="Electrochemical Gradient Maintenance",
                    explanation="Without a final acceptor to relieve electrons, the gradient collapses."
                )
            ]

        return Quiz(
            quiz_id=quiz_id,
            lesson_id=lesson_plan.lesson_id,
            title=res.get("title", f"Mastery Assessment: {lesson_plan.title}"),
            questions=quiz_questions
        )


# Global singleton
quiz_generator = QuizGenerator()
