from typing import Dict, Any, List, Tuple
from app.lesson_planning.schemas import Quiz, QuizSubmission, QuizAnswerItem


class QuizScorer:
    """
    Evaluates submitted quiz answers, calculating raw scores, percentages,
    and categorizing mastered vs. weak conceptual domains.
    """

    def score_quiz(self, quiz: Quiz, submission: QuizSubmission) -> Dict[str, Any]:
        """
        Scores the submission against the quiz questions.
        Returns: {
            "total_score": int,
            "max_score": int,
            "percentage": float,
            "concepts_understood": List[str],
            "weak_concepts": List[str],
            "question_results": List[Dict[str, Any]]
        }
        """
        submission_map = {a.question_id: a for a in submission.answers}
        total_score = 0
        max_score = len(quiz.questions)
        concepts_understood = []
        weak_concepts = []
        question_results = []

        for q in quiz.questions:
            user_answer = submission_map.get(q.id)
            is_correct = False
            user_selected_idx = None
            
            if user_answer:
                user_selected_idx = user_answer.selected_option_index
                if user_selected_idx is not None and user_selected_idx == q.correct_option_index:
                    is_correct = True
                elif user_answer.typed_answer:
                    expected_text = q.options[q.correct_option_index].strip().lower()
                    if user_answer.typed_answer.strip().lower() == expected_text:
                        is_correct = True

            if is_correct:
                total_score += 1
                concepts_understood.append(q.concept_tested)
            else:
                weak_concepts.append(q.concept_tested)

            question_results.append({
                "question_id": q.id,
                "question_text": q.question_text,
                "user_selected_index": user_selected_idx,
                "correct_option_index": q.correct_option_index,
                "is_correct": is_correct,
                "concept_tested": q.concept_tested,
                "explanation": q.explanation
            })

        percentage = round((total_score / float(max_score)) * 100.0, 1) if max_score > 0 else 0.0

        return {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "concepts_understood": concepts_understood,
            "weak_concepts": weak_concepts,
            "question_results": question_results
        }


# Global singleton
quiz_scorer = QuizScorer()
