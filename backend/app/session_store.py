import os
import json
from typing import Dict, Optional, List, Any
from app.lesson_planning.schemas import LessonPlan, Quiz, FeedbackReport, LearnerProgress


class SessionStore:
    """
    In-memory session registry for active lessons, generated quizzes, session misconceptions, and student states.
    Guarantees strict session isolation with zero cross-session state leakage.
    """

    def __init__(self):
        self._lessons: Dict[str, LessonPlan] = {}
        self._quizzes: Dict[str, Quiz] = {}
        self._reports: Dict[str, FeedbackReport] = {}
        self._misconceptions: Dict[str, List[str]] = {}

    def save_lesson(self, lesson: LessonPlan) -> None:
        self._lessons[lesson.lesson_id] = lesson
        if lesson.lesson_id not in self._misconceptions:
            self._misconceptions[lesson.lesson_id] = []

    def get_lesson(self, lesson_id: str) -> Optional[LessonPlan]:
        return self._lessons.get(lesson_id)

    def record_misconception(self, lesson_id: str, misconception: str) -> None:
        if lesson_id not in self._misconceptions:
            self._misconceptions[lesson_id] = []
        if misconception and misconception not in self._misconceptions[lesson_id]:
            self._misconceptions[lesson_id].append(misconception)

    def get_misconceptions(self, lesson_id: str) -> List[str]:
        return self._misconceptions.get(lesson_id, [])

    def save_quiz(self, quiz: Quiz) -> None:
        self._quizzes[quiz.lesson_id] = quiz

    def get_quiz(self, lesson_id: str) -> Optional[Quiz]:
        return self._quizzes.get(lesson_id)

    def save_report(self, report: FeedbackReport) -> None:
        self._reports[report.lesson_id] = report

    def get_report(self, lesson_id: str) -> Optional[FeedbackReport]:
        return self._reports.get(lesson_id)

    def clear_session(self, lesson_id: str) -> None:
        self._lessons.pop(lesson_id, None)
        self._quizzes.pop(lesson_id, None)
        self._reports.pop(lesson_id, None)
        self._misconceptions.pop(lesson_id, None)


class LearnerProfileStore:
    """
    Persistent student learning profile and longitudinal progress store.
    Persists progress to disk at 'media/learner_progress.json'.
    """
    def __init__(self, filepath: str = "media/learner_progress.json"):
        self.filepath = filepath
        self.progress = self._load()

    def _load(self) -> LearnerProgress:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return LearnerProgress(**data)
            except Exception as e:
                print(f"[LearnerProfileStore] Load error: {e}")
        return LearnerProgress()

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.progress.model_dump(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[LearnerProfileStore] Save error: {e}")

    def record_lesson_started(self, topic: str) -> None:
        if topic and topic not in self.progress.topics_studied:
            self.progress.topics_studied.append(topic)
        self.progress.total_lessons_studied = len(self.progress.topics_studied)
        self._save()

    def record_question_attempt(self, is_correct: bool, concept: str, misconception: Optional[str] = None) -> None:
        self.progress.questions_attempted += 1
        if is_correct:
            self.progress.questions_correct += 1
            if concept and concept not in self.progress.mastered_concepts:
                self.progress.mastered_concepts.append(concept)
        else:
            if concept and concept not in self.progress.weak_concepts:
                self.progress.weak_concepts.append(concept)
            if misconception and misconception not in self.progress.all_misconceptions_encountered:
                self.progress.all_misconceptions_encountered.append(misconception)

        if self.progress.questions_attempted > 0:
            self.progress.accuracy_percentage = round((self.progress.questions_correct / self.progress.questions_attempted) * 100, 1)
        self._save()

    def record_quiz_completed(self, report: FeedbackReport) -> None:
        self.progress.recent_quiz_scores.append({
            "lesson_title": report.title,
            "percentage": report.percentage,
            "total_score": report.total_score,
            "max_score": report.max_score
        })
        if report.next_recommended_topic and report.next_recommended_topic not in self.progress.recommended_topics_history:
            self.progress.recommended_topics_history.append(report.next_recommended_topic)
        self._save()

    def get_progress(self) -> LearnerProgress:
        return self.progress


# Global singletons
session_store = SessionStore()
learner_profile_store = LearnerProfileStore()


