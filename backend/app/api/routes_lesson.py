import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.ingestion.parser import PDFParser
from app.ingestion.chunker import TextChunker
from app.ingestion.retriever import FAISSRetriever
from app.lesson_planning.planner import LessonPlanner
from app.lesson_planning.schemas import LessonPlan, LearnerPreferences
from app.narration_avatar.video_assembler import video_assembler
from app.session_store import session_store

router = APIRouter(prefix="/api/lesson", tags=["Lesson"])

parser = PDFParser()
chunker = TextChunker()
planner = LessonPlanner()


@router.post("/create", response_model=LessonPlan)
async def create_lesson(
    pdf_file: Optional[UploadFile] = File(None),
    topic: Optional[str] = Form(None),
    level: str = Form("beginner"),
    time_minutes: int = Form(10),
    language: str = Form("en")
):
    """
    Creates a new structured lesson from an uploaded PDF or typed topic.
    Immediately generates the video for segment 1 for instant playback.
    """
    if not pdf_file and not topic:
        raise HTTPException(status_code=400, detail="Please provide either a PDF document or a topic name.")

    retrieved_context = ""
    source_name = topic or "Uploaded Document"

    # Handle PDF Ingestion if uploaded
    if pdf_file and pdf_file.filename:
        source_name = pdf_file.filename
        try:
            pdf_bytes = await pdf_file.read()
            doc_data = parser.extract_text_from_bytes(pdf_bytes, filename=pdf_file.filename)
            chunks = chunker.chunk_document(doc_data)
            
            retriever = FAISSRetriever()
            retriever.add_chunks(chunks)
            
            # Query top context
            search_query = topic if topic else doc_data.get("title", "Core concepts and mechanisms")
            retrieved_context = retriever.get_combined_context(search_query, top_k=5, max_words=2000)
            if not retrieved_context and doc_data.get("full_text"):
                retrieved_context = doc_data["full_text"][:3000]
            print(f"[INGESTION] Extracted {doc_data.get('total_words', 0)} words across {doc_data.get('total_pages', 1)} pages from '{pdf_file.filename}'.")
            print(f"[INGESTION] Created {len(chunks)} overlapping semantic chunks.")
            print(f"[RETRIEVAL] Indexed chunks in FAISS. Retrieved relevant context ({len(retrieved_context)} chars).")
        except Exception as e:
            print(f"[INGESTION] PDF processing error: {e}")
            retrieved_context = f"Topic extracted from PDF: {pdf_file.filename}"

    # Plan curriculum
    preferences = LearnerPreferences(
        topic=topic or source_name,
        level=level,
        time_minutes=time_minutes,
        language=language
    )

    lesson_plan = planner.plan_lesson(
        preferences=preferences,
        retrieved_context=retrieved_context,
        source_name=source_name
    )
    print(f"[LESSON] Generated lesson '{lesson_plan.title}' with {len(lesson_plan.segments)} segments for time budget {time_minutes}m ({level}).")

    # Immediately render video for Segment 1 so the user can start playing immediately
    if lesson_plan.segments:
        first_seg = lesson_plan.segments[0]
        print(f"[VIDEO] Pre-rendering video for segment 1: '{first_seg.title}'...")
        v_res = video_assembler.assemble_segment_video(
            segment=first_seg,
            lesson_title=lesson_plan.title,
            segment_index=1,
            total_segments=len(lesson_plan.segments),
            language=language
        )
        first_seg.video_url = v_res["relative_url"]
        print(f"[VIDEO] Segment 1 video ready at '{first_seg.video_url}'.")

    # Save to session store
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
