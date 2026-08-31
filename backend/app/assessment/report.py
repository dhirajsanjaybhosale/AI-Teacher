from typing import Dict, Any, List
from app.lesson_planning.schemas import LessonPlan, Quiz, QuizSubmission, FeedbackReport
from .scorer import quiz_scorer
from app.llm.llm_service import llm_service


class ReportGenerator:
    """
    Synthesizes rich analytical feedback reports with strength/weakness diagnostics
    and actionable next-topic learning pathways.
    """

    def __init__(self):
        self.llm = llm_service
        self.scorer = quiz_scorer

    def generate_report(
        self,
        lesson_plan: LessonPlan,
        quiz: Quiz,
        submission: QuizSubmission
    ) -> FeedbackReport:
        """
        Creates a comprehensive mastery feedback report.
        """
        score_data = self.scorer.score_quiz(quiz, submission)
        is_hindi = (lesson_plan.target_language.lower() in ["hi", "hindi"])
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"

        score = score_data["total_score"]
        max_score = score_data["max_score"]
        pct = score_data["percentage"]
        understood = score_data["concepts_understood"]
        weak = score_data["weak_concepts"]

        system_prompt = f"""You are an encouraging educational mentor and AI Teacher.
Generate a comprehensive final feedback report and tailored next-topic recommendation for a student.

LANGUAGE: {lang_name} ({'Respond entirely in natural, inspiring Hindi script' if is_hindi else 'Respond in clear, inspiring English'})

JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object:
{{
  "recommendations": [
    "Concrete actionable recommendation 1",
    "Concrete actionable recommendation 2"
  ],
  "next_recommended_topic": "Next Logical Topic Title",
  "summary_feedback": "A warm, motivating 2-3 sentence summary evaluating their progress and key takeaways."
}}
"""

        prompt = f"""LESSON: {lesson_plan.title}
TARGET LEVEL: {lesson_plan.target_level}
STUDENT SCORE: {score} out of {max_score} ({pct}%)
CONCEPTS UNDERSTOOD: {', '.join(understood) if understood else 'Basic introductory terms'}
WEAK / MISSED CONCEPTS: {', '.join(weak) if weak else 'None! Flawless execution'}

Generate the feedback report analysis."""

        res = self.llm.generate_json(prompt, system_prompt=system_prompt)

        recommendations = res.get("recommendations", [])
        if not recommendations:
            if pct >= 80:
                recommendations = [
                    "You demonstrated outstanding conceptual grasp of biological energetic pathways.",
                    "Ready to advance to higher-level biochemical regulation and kinetics."
                ] if not is_hindi else [
                    "आपने ऊर्जा उत्पादन के सिद्धांतों को बहुत अच्छे से समझा है।",
                    "आप अगले उन्नत स्तर के विषयों को सीखने के लिए पूरी तरह तैयार हैं।"
                ]
            else:
                recommendations = [
                    "Spend a few minutes reviewing the electron transport chain and proton gradient.",
                    "Focus on how ATP synthase uses rotational mechanical energy."
                ] if not is_hindi else [
                    "इलेक्ट्रॉन ट्रांसपोर्ट चेन और प्रोटॉन ग्रेडिएंट की अवधारणा का पुनरावलोकन करें।",
                    "ATP सिंथेस की कार्यप्रणाली पर विशेष ध्यान दें।"
                ]

        next_topic = res.get("next_recommended_topic", "Photosynthesis & Solar Energy Conversion" if "cellular" in lesson_plan.title.lower() else "Advanced Conceptual Principles")
        summary_feedback = res.get("summary_feedback", "")
        if not summary_feedback:
            if pct >= 80:
                summary_feedback = f"अद्भुत प्रदर्शन! आपने {lesson_plan.title} में {pct}% अंक प्राप्त कर विषय पर गहरी पकड़ बनाई है।" if is_hindi else f"Outstanding performance! You achieved {pct}% mastery on {lesson_plan.title}, demonstrating a robust understanding of core concepts."
            else:
                summary_feedback = f"अच्छा प्रयास! आपने {pct}% अंक प्राप्त किए हैं। थोड़े और अभ्यास से आप इसमें पूर्ण निपुणता हासिल कर लेंगे।" if is_hindi else f"Good effort! You achieved {pct}% mastery. With a quick review of the highlighted concepts, you will achieve complete fluency."

        return FeedbackReport(
            lesson_id=lesson_plan.lesson_id,
            title=lesson_plan.title,
            total_score=score,
            max_score=max_score,
            percentage=pct,
            concepts_understood=understood,
            weak_concepts=weak,
            recommendations=recommendations,
            next_recommended_topic=next_topic,
            summary_feedback=summary_feedback
        )


# Global singleton
report_generator = ReportGenerator()
