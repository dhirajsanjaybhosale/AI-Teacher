import uuid
from typing import Dict, Any, Optional
from app.lesson_planning.schemas import Segment, EvaluationResult
from app.llm.llm_service import llm_service


class AnswerEvaluator:
    """
    Evaluates learner responses, semantically assessing conceptual mastery
    and pinpointing underlying mental model misconceptions.
    """

    def __init__(self):
        self.llm = llm_service

    def evaluate_answer(
        self,
        segment: Segment,
        user_answer: str,
        lesson_title: str = "AI Teacher Lesson",
        language: str = "en"
    ) -> EvaluationResult:
        """
        Evaluates the student's answer against the segment question and explanation.
        """
        clean_user_answer = user_answer.strip()
        q = segment.question
        is_hindi = (language.lower() in ["hi", "hindi"])
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"

        # Direct exact match check for quick optimization if options used
        exact_match = False
        if clean_user_answer.lower() == q.correct_answer.strip().lower():
            exact_match = True

        system_prompt = f"""You are a master pedagogical diagnostician and empathetic AI Teacher.
Evaluate a student's answer to a formative check question.

LANGUAGE OF FEEDBACK: {lang_name} ({'Respond entirely in natural, encouraging Hindi script' if is_hindi else 'Respond in clear, supportive English'})

EVALUATION CRITERIA:
1. 'is_correct': boolean (true if conceptually sound, false if fundamentally incorrect or exhibiting misunderstanding).
2. 'score': float (1.0 for completely correct, 0.5-0.7 for partially correct, 0.0-0.3 for incorrect).
3. 'feedback': Constructive, encouraging explanation of what was accurate or what core point was missed.
4. 'misconception_detected': boolean (true if the student demonstrates a specific conceptual flaw or confusion).
5. 'misconception_explanation': Specific diagnosis of WHY the student made this error (e.g., 'Confused anaerobic glycolysis with aerobic respiration', 'Mixed up the raw reactant with the catalytic enzyme').
6. 'adaptation_needed': boolean (true if is_correct is false, meaning the student needs an adaptive re-explanation).

CRITICAL JSON SPECIFICATION:
Respond ONLY with a JSON object:
{{
  "is_correct": true | false,
  "score": 1.0 | 0.0,
  "feedback": "Encouraging explanation...",
  "misconception_detected": true | false,
  "misconception_explanation": "Detailed diagnosis...",
  "adaptation_needed": true | false
}}
"""

        prompt = f"""LESSON: {lesson_title}
SEGMENT TITLE: {segment.title}
EXPLANATION TAUGHT: {segment.explanation}
KEY POINTS: {', '.join(segment.key_points)}

QUESTION ASKED: {q.question_text}
EXPECTED CORRECT ANSWER: {q.correct_answer}
STUDENT'S SUBMITTED ANSWER: "{clean_user_answer}"

Evaluate the student's answer accurately."""

        result_dict = self.llm.generate_json(prompt, system_prompt=system_prompt)

        # Ensure schema safety
        is_correct = bool(result_dict.get("is_correct", exact_match))
        if exact_match:
            is_correct = True
            result_dict["score"] = 1.0
            result_dict["adaptation_needed"] = False
            result_dict["misconception_detected"] = False

        score = float(result_dict.get("score", 1.0 if is_correct else 0.2))
        adaptation_needed = bool(result_dict.get("adaptation_needed", not is_correct))
        misconception_detected = bool(result_dict.get("misconception_detected", not is_correct))

        feedback = result_dict.get("feedback")
        if not feedback:
            if is_correct:
                feedback = "शानदार! आपका उत्तर बिल्कुल सही है।" if is_hindi else "Excellent! That is conceptually spot-on."
            else:
                feedback = f"अच्छा प्रयास! सही उत्तर '{q.correct_answer}' है। आइए इसे नए तरीके से समझें।" if is_hindi else f"Good attempt! The correct answer is '{q.correct_answer}'. Let's revisit this with an intuitive analogy."

        misconception_explanation = result_dict.get("misconception_explanation", "")
        if not is_correct and not misconception_explanation:
            misconception_explanation = f"Student's explanation diverged from the expected core relationship for '{segment.title}'."

        return EvaluationResult(
            is_correct=is_correct,
            score=score,
            feedback=feedback,
            misconception_detected=misconception_detected,
            misconception_explanation=misconception_explanation,
            adaptation_needed=adaptation_needed
        )


# Global singleton
answer_evaluator = AnswerEvaluator()
