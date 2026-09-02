from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from app.session_store import student_profile_store
from app.lesson_planning.schemas import CompleteStudentProfile

router = APIRouter(prefix="/api/profile", tags=["Student Profile & Progress"])


@router.get("", response_model=CompleteStudentProfile)
async def get_student_profile():
    """
    Returns the complete persistent student profile including:
    personal info, learning preferences, subject/topic mastery,
    strong & weak areas, misconception history, learning history,
    study plan, and personalized AI recommendations.
    """
    return student_profile_store.get_profile()


@router.post("", response_model=CompleteStudentProfile)
async def update_student_profile(payload: Dict[str, Any] = Body(...)):
    """
    Updates student personal info or learning preferences and persists to disk.
    """
    try:
        updated = student_profile_store.update_profile(payload)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update profile: {str(e)}")


@router.post("/record-lesson")
async def record_lesson_completion(payload: Dict[str, Any] = Body(...)):
    """
    Records a completed lesson in student learning history and updates mastery.
    """
    topic = payload.get("topic", "General Lesson")
    duration = int(payload.get("duration_minutes", 20))
    score = int(payload.get("quiz_score_percentage", 85))
    language = payload.get("language", "English")

    student_profile_store.record_lesson_completion(topic, duration, score, language)
    return {"status": "success", "profile": student_profile_store.get_profile()}


@router.post("/study-plan")
async def update_study_plan(payload: Dict[str, Any] = Body(...)):
    """
    Updates the student's study plan schedule.
    """
    study_plan = payload.get("study_plan", [])
    updated = student_profile_store.update_profile({"study_plan": study_plan})
    return {"status": "success", "study_plan": updated.study_plan}
