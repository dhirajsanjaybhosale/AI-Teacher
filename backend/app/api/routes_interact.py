from fastapi import APIRouter, HTTPException

from app.lesson_planning.schemas import AnswerSubmission, EvaluationResult, FollowUpRequest, FollowUpResponse
from app.session_store import session_store, learner_profile_store, student_profile_store
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
    for seg in lesson.segments:
        if seg.id == sub.segment_id:
            target_seg = seg
            break

    if not target_seg:
        raise HTTPException(status_code=404, detail="Segment not found in this lesson.")

    lang = sub.language or lesson.target_language

    # Fetch prior answers from this lesson session for memory
    prior_answers = session_store.get_student_answers(sub.lesson_id)

    # 1. Formative Evaluation
    eval_result = answer_evaluator.evaluate_answer(
        segment=target_seg,
        user_answer=sub.user_answer,
        lesson_title=lesson.title,
        language=lang,
        prior_answers=prior_answers
    )
    print(f"[EVALUATION] Student answer assessed: is_correct={eval_result.is_correct}, score={eval_result.score:.2f}")

    # Record in active session memory so teacher remembers student's answers
    session_store.record_student_answer(
        lesson_id=sub.lesson_id,
        segment_id=target_seg.id,
        question_text=target_seg.question.question_text if target_seg.question else "",
        user_answer=sub.user_answer,
        is_correct=eval_result.is_correct,
        feedback=eval_result.feedback,
        misconception=eval_result.misconception if eval_result.misconception_detected else None
    )

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
        student_profile_store.record_misconception(
            concept=eval_result.concept or target_seg.title,
            misconception=eval_result.misconception_explanation
        )
        
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


@router.get("/session-history/{lesson_id}")
async def get_session_history(lesson_id: str):
    """
    Returns recorded student answer history and teacher memories for the active lesson session.
    """
    return {
        "lesson_id": lesson_id,
        "answers": session_store.get_student_answers(lesson_id),
        "misconceptions": session_store.get_misconceptions(lesson_id)
    }


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

