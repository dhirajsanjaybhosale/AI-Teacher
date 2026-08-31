from typing import Dict, Optional
from app.lesson_planning.schemas import LessonPlan, Quiz, FeedbackReport


class SessionStore:
    """
    In-memory session registry for active lessons, generated quizzes, and student states.
    """

    def __init__(self):
        self._lessons: Dict[str, LessonPlan] = {}
        self._quizzes: Dict[str, Quiz] = {}
        self._reports: Dict[str, FeedbackReport] = {}

    def save_lesson(self, lesson: LessonPlan) -> None:
        self._lessons[lesson.lesson_id] = lesson

    def get_lesson(self, lesson_id: str) -> Optional[LessonPlan]:
        return self._lessons.get(lesson_id)

    def save_quiz(self, quiz: Quiz) -> None:
        self._quizzes[quiz.lesson_id] = quiz

    def get_quiz(self, lesson_id: str) -> Optional[Quiz]:
        return self._quizzes.get(lesson_id)

    def save_report(self, report: FeedbackReport) -> None:
        self._reports[report.lesson_id] = report

    def get_report(self, lesson_id: str) -> Optional[FeedbackReport]:
        return self._reports.get(lesson_id)


# Global singleton
session_store = SessionStore()
