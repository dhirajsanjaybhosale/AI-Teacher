from fastapi import APIRouter, HTTPException

from app.lesson_planning.schemas import AnswerSubmission, EvaluationResult, FollowUpRequest, FollowUpResponse
from app.session_store import session_store, learner_profile_store
from app.interaction.evaluator import answer_evaluator
from app.interaction.adapter import lesson_adapter
from app.interaction.assistant import teacher_assistant

router = APIRouter(prefix="/api/interact", tags=["Interaction"])


@router.post("/submit-answer", response_model=EvaluationResult)
async def submit_answer(sub: AnswerSubmission):
    """
    Evaluates student answer, detects misconceptions, logs them in session store,
    and dynamically compiles a customized remediation video segment when conceptual gaps are found.
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

    # Track in persistent learner store
    learner_profile_store.record_question_attempt(
        is_correct=eval_result.is_correct,
        concept=eval_result.concept or target_seg.title,
        misconception=eval_result.misconception if eval_result.misconception_detected else None
    )

    # 2. Adaptive Remediation Trigger
    if eval_result.adaptation_needed:
        print(f"[ADAPTATION] Misconception detected: {eval_result.misconception_explanation}")
        session_store.record_misconception(lesson.lesson_id, eval_result.misconception_explanation)
        
        adapted_seg = lesson_adapter.create_remediation_segment(
            original_segment=target_seg,
            user_answer=sub.user_answer,
            misconception=eval_result.misconception_explanation,
            lesson_title=lesson.title,
            language=lang,
            strategy=eval_result.recommended_strategy
        )
        eval_result.adapted_segment = adapted_seg
        print(f"[ADAPTATION] Generated remediation segment '{adapted_seg.title}' with video at '{adapted_seg.video_url}'.")

    return eval_result


@router.post("/ask-teacher", response_model=FollowUpResponse)
async def ask_teacher(req: FollowUpRequest):
    """
    Handles in-lesson live student inquiries, clarifying concepts or providing fresh examples
    while strictly preserving the active lesson session context.
    """
    lesson = session_store.get_lesson(req.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson session not found.")

    target_seg = None
    if req.segment_id:
        for s in lesson.segments:
            if s.id == req.segment_id:
                target_seg = s
                break

    print(f"[INTERACTION] Student asked teacher: '{req.user_query}' for lesson '{lesson.title}'...")
    response = teacher_assistant.answer_followup(
        lesson=lesson,
        request=req,
        current_segment=target_seg
    )
    return response

