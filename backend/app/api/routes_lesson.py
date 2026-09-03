import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.ingestion.knowledge_router import knowledge_router
from app.lesson_planning.planner import lesson_planner
from app.lesson_planning.schemas import LessonPlan, LearnerPreferences, LanguageSwitchRequest, LearnerProgress
from app.narration_avatar.video_assembler import video_assembler
from app.session_store import session_store, learner_profile_store, student_profile_store

router = APIRouter(prefix="/api/lesson", tags=["Lesson"])


@router.post("/create", response_model=LessonPlan)
async def create_lesson(
    document_file: Optional[UploadFile] = File(None),
    pdf_file: Optional[UploadFile] = File(None),
    topic: Optional[str] = Form(None),
    level: str = Form("beginner"),
    time_minutes: int = Form(10),
    language: str = Form("en"),
    teaching_style: str = Form("Simple"),
    existing_knowledge: str = Form(""),
    force_web_search: bool = Form(False)
):
    """
    Unified Lesson Creation Endpoint.
    Dynamically routes between Document RAG, External Live Web Search, and Universal LLM Knowledge.
    Personalizes curriculum using the student profile memory.
    """
    doc_upload = document_file or pdf_file
    doc_bytes = None
    doc_filename = None

    if doc_upload and doc_upload.filename:
        doc_filename = doc_upload.filename
        doc_bytes = await doc_upload.read()

    # Retrieve student profile for memory & personalization
    stud_prof = student_profile_store.get_profile()

    # 1. Dynamic Knowledge Routing
    routing_result = await knowledge_router.route_knowledge(
        document_bytes=doc_bytes,
        document_filename=doc_filename,
        topic=topic,
        level=level,
        time_minutes=time_minutes,
        language=language,
        force_web_search=force_web_search
    )

    effective_level = routing_result.detected_level or (level if level != "beginner" else stud_prof.learning_profile.current_level)
    effective_lang = routing_result.detected_language or (language if language != "en" else stud_prof.learning_profile.preferred_language)
    effective_goal = routing_result.detected_goal or (stud_prof.learning_profile.learning_goals[0] if stud_prof.learning_profile.learning_goals else "understand")
    effective_style = routing_result.detected_style or (teaching_style if teaching_style != "Simple" else (stud_prof.learning_profile.learning_styles[0] if stud_prof.learning_profile.learning_styles else "Visual"))

    # Prioritize explicit duration passed by user if not inferred from textual query
    effective_minutes = time_minutes
    if routing_result.detected_minutes and ("minute" in (topic or "").lower() or "min" in (topic or "").lower() or "hour" in (topic or "").lower()):
        effective_minutes = routing_result.detected_minutes

    # 2. Setup Learner Preferences
    preferences = LearnerPreferences(
        topic=routing_result.clean_topic or topic or doc_filename or "Core Concepts",
        level=effective_level,
        time_minutes=effective_minutes,
        language=effective_lang,
        goal=effective_goal,
        teaching_style=effective_style,
        existing_knowledge=existing_knowledge or f"Student: {stud_prof.personal_info.full_name}, {stud_prof.personal_info.course}",
        force_web_search=force_web_search
    )

    # 3. Plan Curriculum
    lesson_plan = lesson_planner.plan_lesson(
        preferences=preferences,
        retrieved_context=routing_result.grounded_context,
        source_name=routing_result.source_name,
        source_route=routing_result.route_type,
        sources=routing_result.sources,
        retrieval_confidence=routing_result.retrieval_confidence,
        retrieval_warning=routing_result.retrieval_warning,
        is_scanned=routing_result.is_scanned
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

    # 5. Save to session store & record in longitudinal profile
    session_store.save_lesson(lesson_plan)
    learner_profile_store.record_lesson_started(lesson_plan.title)

    return lesson_plan


@router.post("/{lesson_id}/switch-language", response_model=LessonPlan)
async def switch_language(lesson_id: str, req: LanguageSwitchRequest):
    """
    Switches lesson instruction language mid-lesson without losing progress.
    Re-narrates the current segment in the requested language.
    """
    lesson = session_store.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    lesson.target_language = req.new_language
    seg_idx = req.current_segment_index or 0

    if 0 <= seg_idx < len(lesson.segments):
        target_seg = lesson.segments[seg_idx]
        print(f"[LANGUAGE] Switching language to {req.new_language} for segment {seg_idx + 1} ('{target_seg.title}')...")
        v_res = video_assembler.assemble_segment_video(
            segment=target_seg,
            lesson_title=lesson.title,
            segment_index=seg_idx + 1,
            total_segments=len(lesson.segments),
            language=req.new_language
        )
        target_seg.video_url = v_res["relative_url"]

    session_store.save_lesson(lesson)
    return lesson


@router.get("/progress", response_model=LearnerProgress)
async def get_learner_progress():
    """
    Fetches the learner's longitudinal learning trajectory, accuracy, and topic history.
    """
    return learner_profile_store.get_progress()


@router.get("/{lesson_id}", response_model=LessonPlan)
async def get_lesson(lesson_id: str):
    """
    Fetches the active lesson plan by ID.
    """
    lesson = session_store.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")
    return lesson


@router.post("/{lesson_id}/assemble-full-video", response_model=LessonPlan)
async def assemble_full_video(lesson_id: str):
    """
    Assembles all segments of the lesson into a continuous full-length MP4 video.
    """
    lesson = session_store.get_lesson(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    print(f"[VIDEO] Assembling full video for lesson '{lesson.title}' ({len(lesson.segments)} segments)...")
    res = video_assembler.assemble_full_lesson_video(lesson)
    session_store.save_lesson(lesson)
    return lesson
