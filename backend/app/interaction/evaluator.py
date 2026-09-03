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
        language: str = "en",
        prior_answers: Optional[list] = None
    ) -> EvaluationResult:
        """
        Evaluates the student's answer against the segment question and explanation,
        incorporating past answer memory from the active lesson session.
        """
        clean_user_answer = user_answer.strip()
        q = segment.question
        lang_lower = language.lower()
        is_marathi = ("mr" in lang_lower or "marathi" in lang_lower)
        is_hinglish = ("hinglish" in lang_lower)
        is_hindi = (not is_hinglish and not is_marathi and ("hi" in lang_lower or "hindi" in lang_lower))
        lang_name = "Marathi (मराठी)" if is_marathi else ("Hindi (हिंदी)" if is_hindi else ("Hinglish" if is_hinglish else "English"))

        # Direct exact match check for quick optimization if options used
        exact_match = False
        if clean_user_answer.lower() == q.correct_answer.strip().lower():
            exact_match = True

        prior_context = ""
        if prior_answers:
            prev_summaries = [f"- Question: {pa.get('question_text', '')} | Student said: '{pa.get('user_answer', '')}' (Correct: {pa.get('is_correct', False)})" for pa in prior_answers[-3:]]
            prior_context = f"\nPRIOR STUDENT ANSWERS IN THIS LESSON:\n" + "\n".join(prev_summaries)

        system_prompt = f"""You are a master pedagogical diagnostician and empathetic AI Teacher.
Evaluate a student's answer to a formative check question.
{prior_context}

LANGUAGE OF FEEDBACK: {lang_name}

EVALUATION CRITERIA:
1. 'is_correct': boolean (true if conceptually sound, false if fundamentally incorrect or exhibiting misunderstanding).
2. 'score': float (1.0 for completely correct, 0.5-0.7 for partially correct, 0.0-0.3 for incorrect).
3. 'feedback': If correct, acknowledge enthusiastically: "Exactly! That's the key idea. Let's make it a little more challenging." If incorrect, be empathetic: "Almost. I can see where the confusion happened. Let's look at it another way."
4. 'misconception_detected': boolean (true if the student demonstrates a specific conceptual flaw or confusion).
5. 'misconception_explanation': Specific diagnosis of WHY the student made this error.
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

        memory_note = ""
        if prior_answers and len(prior_answers) > 0:
            last_ans = prior_answers[-1]
            if last_ans.get("is_correct"):
                memory_note = " Continuing from your strong grasp on the previous concept: "

        feedback = result_dict.get("feedback")
        if not feedback or "Exactly" not in feedback and "Almost" not in feedback:
            if is_correct:
                if is_marathi:
                    feedback = f"अगदी बरोबर! हाच मुख्य मुद्दा आहे. आता आपण याला थोडं आणखी आव्हानात्मक बनवूया. {memory_note}"
                elif is_hindi:
                    feedback = f"बिल्कुल सही! यही मुख्य विचार है। आइए अब इसे थोड़ा और चुनौतीपूर्ण बनाते हैं। {memory_note}"
                elif is_hinglish:
                    feedback = f"Exactly! Yahi key idea hai. Let's make it a little more challenging! {memory_note}"
                else:
                    feedback = f"Exactly! That's the key idea. Let's make it a little more challenging. {memory_note}"
            else:
                if is_marathi:
                    feedback = f"जवळपास बरोबर! गोंधळ कुठे झाला हे माझ्या लक्षात आले. चला, याकडे दुसऱ्या दृष्टीकोनातून पाहूया. योग्य उत्तर '{q.correct_answer}' आहे."
                elif is_hindi:
                    feedback = f"लगभग सही! मैं समझ सकता हूँ कि भ्रम कहाँ हुआ। आइए इसे दूसरे तरीके से देखते हैं। सही उत्तर '{q.correct_answer}' है।"
                elif is_hinglish:
                    feedback = f"Almost! I can see where the confusion happened. Let's look at it another way. Correct concept: '{q.correct_answer}'."
                else:
                    feedback = f"Almost. I can see where the confusion happened. Let's look at it another way. The key answer is '{q.correct_answer}'."

        misconception_explanation = result_dict.get("misconception_explanation", "")
        if not is_correct and not misconception_explanation:
            misconception_explanation = f"Student's explanation diverged from the expected core relationship for '{segment.title}'."

        concept = result_dict.get("concept", segment.title)
        misconception = result_dict.get("misconception", misconception_explanation)
        reasoning = result_dict.get("reasoning", f"Misunderstanding in {concept}")
        severity = result_dict.get("severity", "low" if is_correct else "medium")
        recommended_strategy = result_dict.get("recommended_strategy", "advance_next" if is_correct else "real_world_analogy")
        missing_concept = result_dict.get("missing_concept", "")

        tb_state = result_dict.get("teacher_brain_state") or {
            "learner_level": "Beginner",
            "current_concept": concept,
            "understanding_state": "High" if is_correct else "Needs Remediation",
            "detected_misconception": "None (Concept sound)" if is_correct else misconception,
            "teaching_strategy": "Advance to next objective" if is_correct else recommended_strategy.replace("_", " ").title(),
            "difficulty": "Standard / Progressive" if is_correct else "Adapted Simpler Analogy",
            "next_action": "Unlock next segment" if is_correct else f"Deploy {recommended_strategy.replace('_', ' ')} re-explanation"
        }

        return EvaluationResult(
            is_correct=is_correct,
            score=score,
            feedback=feedback,
            misconception_detected=misconception_detected,
            misconception_explanation=misconception_explanation,
            concept=concept,
            misconception=misconception,
            reasoning=reasoning,
            severity=severity,
            needs_remediation=not is_correct,
            recommended_strategy=recommended_strategy,
            missing_concept=missing_concept,
            confidence=float(result_dict.get("confidence", 0.95)),
            adaptation_needed=adaptation_needed,
            teacher_brain_state=tb_state
        )


# Global singleton
answer_evaluator = AnswerEvaluator()
