import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.ingestion.knowledge_router import knowledge_router
from app.lesson_planning.planner import lesson_planner
from app.lesson_planning.schemas import LessonPlan, LearnerPreferences
from app.narration_avatar.video_assembler import video_assembler
from app.session_store import session_store

router = APIRouter(prefix="/api/lesson", tags=["Lesson"])


@router.post("/create", response_model=LessonPlan)
async def create_lesson(
    pdf_file: Optional[UploadFile] = File(None),
    topic: Optional[str] = Form(None),
    level: str = Form("beginner"),
    time_minutes: int = Form(10),
    language: str = Form("en"),
    force_web_search: bool = Form(False)
):
    """
    Creates a new structured lesson from an uploaded PDF, live web search, or general typed topic.
    Immediately routes knowledge via KnowledgeRouter and generates the video for segment 1 for instant playback.
    """
    if not pdf_file and not topic:
        raise HTTPException(status_code=400, detail="Please provide either a PDF document or a topic name.")

    pdf_bytes = None
    pdf_filename = None
    if pdf_file and pdf_file.filename:
        pdf_filename = pdf_file.filename
        pdf_bytes = await pdf_file.read()

    # 1. Execute Knowledge Routing (PDF RAG vs External Web vs LLM Knowledge)
    routing_result = await knowledge_router.route_knowledge(
        pdf_bytes=pdf_bytes,
        pdf_filename=pdf_filename,
        topic=topic,
        level=level,
        time_minutes=time_minutes,
        language=language,
        force_web_search=force_web_search
    )

    # 2. Setup Learner Preferences
    preferences = LearnerPreferences(
        topic=routing_result.clean_topic or topic or pdf_filename or "Core Concepts",
        level=routing_result.detected_level or level,
        time_minutes=routing_result.detected_minutes or time_minutes,
        language=routing_result.detected_language or language,
        force_web_search=force_web_search
    )

    # 3. Plan Curriculum
    lesson_plan = lesson_planner.plan_lesson(
        preferences=preferences,
        retrieved_context=routing_result.grounded_context,
        source_name=routing_result.source_name,
        source_route=routing_result.route_type,
        sources=routing_result.sources
    )

    print(f"[LESSON] Generated lesson '{lesson_plan.title}' with {len(lesson_plan.segments)} segments via route '{lesson_plan.source_route}' ({len(lesson_plan.sources)} sources).")

    # 4. Immediately render video for Segment 1 so the user can start playing immediately
    if lesson_plan.segments:
        first_seg = lesson_plan.segments[0]
        print(f"[VIDEO] Pre-rendering video for segment 1: '{first_seg.title}'...")
        v_res = video_assembler.assemble_segment_video(
            segment=first_seg,
            lesson_title=lesson_plan.title,
            segment_index=1,
            total_segments=len(lesson_plan.segments),
            language=lesson_plan.target_language
        )
        first_seg.video_url = v_res["relative_url"]
        print(f"[VIDEO] Segment 1 video ready at '{first_seg.video_url}'.")

    # 5. Save to session store
    session_store.save_lesson(lesson_plan)

    return lesson_plan


@router.get("/{lesson_id}", response_model=LessonPlan)
async def get_lesson(lesson_id: str):
    """
    Fetches the active lesson plan by ID.
    """
    lesson = session_store.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")
    return lesson
