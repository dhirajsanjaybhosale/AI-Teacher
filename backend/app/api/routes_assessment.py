from fastapi import APIRouter, HTTPException

from app.lesson_planning.schemas import Quiz, QuizSubmission, FeedbackReport
from app.session_store import session_store
from app.assessment.quiz_generator import quiz_generator
from app.assessment.report import report_generator

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])


@router.get("/quiz/{lesson_id}", response_model=Quiz)
async def get_or_create_quiz(lesson_id: str):
    """
    Retrieves or generates the summative mastery quiz for a completed lesson.
    """
    lesson = session_store.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson session not found.")

    cached_quiz = session_store.get_quiz(lesson_id)
    if cached_quiz:
        return cached_quiz

    print(f"[ASSESSMENT] Generating summative quiz for lesson '{lesson.title}'...")
    quiz = quiz_generator.generate_quiz(lesson)
    session_store.save_quiz(quiz)
    print(f"[ASSESSMENT] Summative quiz '{quiz.title}' generated with {len(quiz.questions)} questions.")
    return quiz


@router.post("/submit-quiz", response_model=FeedbackReport)
async def submit_quiz(sub: QuizSubmission):
    """
    Scores the completed quiz and generates a comprehensive analytical feedback report.
    """
    lesson = session_store.get_lesson(sub.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson session not found.")

    quiz = session_store.get_quiz(sub.lesson_id)
    if not quiz:
        # Generate on the fly if needed
        quiz = quiz_generator.generate_quiz(lesson)
        session_store.save_quiz(quiz)

    print(f"[ASSESSMENT] Scoring quiz submission and compiling feedback report for '{lesson.title}'...")
    session_misconceptions = session_store.get_misconceptions(sub.lesson_id)
    report = report_generator.generate_report(lesson, quiz, sub, misconceptions=session_misconceptions)
    session_store.save_report(report)
    print(f"[ASSESSMENT] Final feedback report created: Score={report.total_score}/{report.max_score} ({report.percentage}%), Misconceptions remediated={len(report.misconceptions)}, Next topic='{report.next_recommended_topic}'.")
    return report


@router.get("/report/{lesson_id}", response_model=FeedbackReport)
async def get_report(lesson_id: str):
    """
    Fetches the generated feedback report for a lesson.
    """
    report = session_store.get_report(lesson_id)
    if not report:
        raise HTTPException(status_code=404, detail="Feedback report not found for this lesson.")
    return report
