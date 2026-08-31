import os
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.session_store import session_store
from app.narration_avatar.video_assembler import video_assembler

router = APIRouter(prefix="/api/segment", tags=["Segment"])


class RenderRequest(BaseModel):
    lesson_id: str
    segment_id: str


@router.post("/render")
async def render_segment(req: RenderRequest):
    """
    Renders or fetches the MP4 video for a specific lesson segment on demand.
    """
    lesson = session_store.get_lesson(req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson session not found.")

    # Find segment
    target_seg = None
    target_idx = 1
    for idx, s in enumerate(lesson.segments):
        if s.id == req.segment_id:
            target_seg = s
            target_idx = idx + 1
            break

    if not target_seg:
        raise HTTPException(status_code=404, detail=f"Segment '{req.segment_id}' not found in lesson.")

    # Check if video already exists on disk
    if target_seg.video_url:
        local_path = target_seg.video_url.lstrip("/")
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            return {
                "segment_id": target_seg.id,
                "video_url": target_seg.video_url,
                "cached": True
            }

    print(f"[routes_segment] Rendering video for segment {target_idx}: '{target_seg.title}'...")
    v_res = video_assembler.assemble_segment_video(
        segment=target_seg,
        lesson_title=lesson.title,
        segment_index=target_idx,
        total_segments=len(lesson.segments),
        language=lesson.target_language
    )

    target_seg.video_url = v_res["relative_url"]
    session_store.save_lesson(lesson)

    return {
        "segment_id": target_seg.id,
        "video_url": v_res["relative_url"],
        "duration": v_res["duration"],
        "cached": False
    }
