import re
from typing import Dict, Any, List, Optional
from app.lesson_planning.schemas import LessonPlan, Quiz, QuizSubmission, FeedbackReport
from .scorer import quiz_scorer
from app.llm.llm_service import llm_service


class ReportGenerator:
    """
    Synthesizes rich analytical feedback reports with strength/weakness diagnostics
    and actionable next-topic learning pathways, strictly grounded in the active lesson.
    """

    def __init__(self):
        self.llm = llm_service
        self.scorer = quiz_scorer

    def generate_report(
        self,
        lesson_plan: LessonPlan,
        quiz: Quiz,
        submission: QuizSubmission,
        misconceptions: Optional[List[str]] = None
    ) -> FeedbackReport:
        """
        Creates a comprehensive mastery feedback report strictly isolated to the active lesson.
        """
        score_data = self.scorer.score_quiz(quiz, submission)
        is_hindi = (lesson_plan.target_language.lower() in ["hi", "hindi"])
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"

        score = score_data["total_score"]
        max_score = score_data["max_score"]
        pct = score_data["percentage"]
        understood = score_data["concepts_understood"]
        weak = score_data["weak_concepts"]
        session_misc = misconceptions or []

        system_prompt = f"""You are an encouraging educational mentor and AI Teacher generating a final feedback report for a lesson on '{lesson_plan.title}'.
CRITICAL: Every recommendation and feedback statement must be strictly about '{lesson_plan.title}' and the specific concepts tested: {', '.join(understood + weak)}.
Do NOT invent or refer to unrelated academic subjects.

LANGUAGE: {lang_name} ({'Respond entirely in natural, inspiring Hindi script' if is_hindi else 'Respond in clear, inspiring English'})

JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object:
{{
  "recommendations": [
    "Concrete actionable recommendation about {lesson_plan.title} 1",
    "Concrete actionable recommendation about {lesson_plan.title} 2"
  ],
  "next_recommended_topic": "Next Logical Topic directly following {lesson_plan.title}",
  "summary_feedback": "A warm, motivating 2-3 sentence summary evaluating their progress on {lesson_plan.title}."
}}
"""

        prompt = f"""REPORT REQUEST FOR LESSON: {lesson_plan.title}
TARGET LEVEL: {lesson_plan.target_level}
STUDENT SCORE: {score} out of {max_score} ({pct}%)
CONCEPTS MASTERED: {', '.join(understood) if understood else 'None'}
CONCEPTS NEEDING PRACTICE: {', '.join(weak) if weak else 'None'}
MISCONCEPTIONS REMEDIATED DURING LESSON: {', '.join(session_misc) if session_misc else 'None'}

Generate the tailored pedagogical report."""

        res = self.llm.generate_json(prompt, system_prompt=system_prompt)

        recommendations = res.get("recommendations", [])
        if not recommendations:
            recommendations = self._build_dynamic_recommendations(lesson_plan, pct, understood, weak, is_hindi)

        next_topic = res.get("next_recommended_topic")
        # Pedagogical rule: If student scored below 60% and has weak concepts, recommend targeted remediation drill
        if pct < 60 and weak:
            next_topic = f"Foundational Remediation Drill: {weak[0]}"
        elif not next_topic or next_topic.strip() == "":
            next_topic = self._infer_next_topic(lesson_plan, is_hindi)

        summary_feedback = res.get("summary_feedback", "")
        if not summary_feedback or summary_feedback.strip() == "":
            summary_feedback = self._build_summary_feedback(lesson_plan, pct, is_hindi)

        return FeedbackReport(
            lesson_id=lesson_plan.lesson_id,
            title=lesson_plan.title,
            total_score=score,
            max_score=max_score,
            percentage=pct,
            concepts_understood=understood,
            weak_concepts=weak,
            misconceptions=session_misc,
            recommendations=recommendations,
            next_recommended_topic=next_topic,
            summary_feedback=summary_feedback,
            learning_path=lesson_plan.learning_path,
            study_roadmap_7_days=lesson_plan.study_roadmap_7_days,
            retrieval_confidence=lesson_plan.retrieval_confidence
        )

    def _infer_next_topic(self, lesson_plan: LessonPlan, is_hindi: bool) -> str:
        """
        Infers a relevant subsequent learning topic strictly based on the current lesson title.
        """
        title_lower = lesson_plan.title.lower()
        if "electric" in title_lower or "ohm" in title_lower or "circuit" in title_lower:
            return "श्रेणी और समानांतर परिपथ (Series & Parallel Circuits)" if is_hindi else "Series and Parallel Circuits & Kirchhoff's Laws"
        elif "cellular" in title_lower or "respiration" in title_lower or "atp" in title_lower:
            return "प्रकाश संश्लेषण और सौर ऊर्जा रूपांतरण" if is_hindi else "Photosynthesis & Solar Energy Conversion"
        elif "quantum" in title_lower or "qubit" in title_lower:
            return "क्वांटम लॉजिक गेट्स और एल्गोरिदम" if is_hindi else "Quantum Logic Gates & Circuit Algorithms"
        elif "newton" in title_lower or "motion" in title_lower:
            return "कार्य, ऊर्जा और शक्ति (Work, Energy & Power)" if is_hindi else "Work, Energy and Power Dynamics"
        elif "neural" in title_lower or "network" in title_lower:
            return "कन्वोल्यूशनल न्यूरल नेटवर्क (CNNs) और विज़न" if is_hindi else "Convolutional Neural Networks & Computer Vision"
        else:
            return f"{lesson_plan.title} के उन्नत अनुप्रयोग" if is_hindi else f"Advanced Applications of {lesson_plan.title}"

    def _build_dynamic_recommendations(
        self,
        lesson_plan: LessonPlan,
        pct: float,
        understood: List[str],
        weak: List[str],
        is_hindi: bool
    ) -> List[str]:
        recs = []
        if understood:
            sample_u = ", ".join(understood[:2])
            if is_hindi:
                recs.append(f"आपने {sample_u} की अवधारणाओं पर उत्कृष्ट पकड़ प्रदर्शित की है।")
            else:
                recs.append(f"You demonstrated strong conceptual mastery of {sample_u}.")

        if weak:
            for w in weak[:2]:
                if is_hindi:
                    recs.append(f"'{w}' के मुख्य सिद्धांतों और सूत्रों का एक बार पुनः अभ्यास करें।")
                else:
                    recs.append(f"Review and practice real-world problem scenarios on '{w}'.")
        else:
            if is_hindi:
                recs.append(f"आप {lesson_plan.title} के अगले उन्नत स्तर के पाठ पर आगे बढ़ने के लिए तैयार हैं।")
            else:
                recs.append(f"You are ready to advance to higher-level concepts and complex applications of {lesson_plan.title}.")

        if not recs:
            recs = [
                f"Continue exploring core foundational concepts in {lesson_plan.title}.",
                "Practice solving quantitative and conceptual reasoning questions."
            ]

        return recs

    def _build_summary_feedback(self, lesson_plan: LessonPlan, pct: float, is_hindi: bool) -> str:
        if is_hindi:
            if pct >= 80:
                return f"अद्भुत प्रदर्शन! आपने {lesson_plan.title} में {pct}% अंक प्राप्त कर विषय पर गहरी पकड़ बनाई है।"
            else:
                return f"अच्छा प्रयास! आपने {pct}% अंक प्राप्त किए हैं। थोड़े और अभ्यास से आप {lesson_plan.title} में पूर्ण निपुणता हासिल कर लेंगे।"
        else:
            if pct >= 80:
                return f"Outstanding performance! You achieved {pct}% mastery on {lesson_plan.title}, demonstrating a robust understanding of core concepts."
            else:
                return f"Good effort! You achieved {pct}% mastery on {lesson_plan.title}. With a quick review of the highlighted concepts, you will achieve complete fluency."


# Global singleton
report_generator = ReportGenerator()
