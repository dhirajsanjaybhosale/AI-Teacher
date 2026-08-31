from typing import Dict, Optional, List
from app.lesson_planning.schemas import LessonPlan, Quiz, FeedbackReport


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


# Global singleton
session_store = SessionStore()

