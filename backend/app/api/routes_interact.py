from fastapi import APIRouter, HTTPException

from app.lesson_planning.schemas import AnswerSubmission, EvaluationResult
from app.session_store import session_store
from app.interaction.evaluator import answer_evaluator
from app.interaction.adapter import lesson_adapter

router = APIRouter(prefix="/api/interact", tags=["Interaction"])


@router.post("/submit-answer", response_model=EvaluationResult)
async def submit_answer(sub: AnswerSubmission):
    """
    Evaluates student answer, detects misconceptions, and dynamically compiles
    a customized remediation video segment when conceptual gaps are found.
    """
    lesson = session_store.get_lesson(sub.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson session not found.")

    target_seg = None
    for s in lesson.segments:
        if s.id == sub.segment_id:
            target_seg = s
            break

    if not target_seg:
        # Check if it was already a remediation segment
        raise HTTPException(status_code=404, detail="Segment not found in active lesson.")

    lang = sub.language or lesson.target_language

    # 1. Formative Evaluation
    eval_result = answer_evaluator.evaluate_answer(
        segment=target_seg,
        user_answer=sub.user_answer,
        lesson_title=lesson.title,
        language=lang
    )
    print(f"[EVALUATION] Student answer assessed: is_correct={eval_result.is_correct}, score={eval_result.score:.2f}")

    # 2. Adaptive Remediation Trigger
    if eval_result.adaptation_needed:
        print(f"[ADAPTATION] Misconception detected: {eval_result.misconception_explanation}")
        adapted_seg = lesson_adapter.create_remediation_segment(
            original_segment=target_seg,
            user_answer=sub.user_answer,
            misconception=eval_result.misconception_explanation,
            lesson_title=lesson.title,
            language=lang
        )
        eval_result.adapted_segment = adapted_seg
        print(f"[ADAPTATION] Generated remediation segment '{adapted_seg.title}' with video at '{adapted_seg.video_url}'.")

    return eval_result
