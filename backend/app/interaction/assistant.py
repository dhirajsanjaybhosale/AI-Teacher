import os
from typing import Optional, Dict, Any
from app.lesson_planning.schemas import LessonPlan, Segment, FollowUpRequest, FollowUpResponse
from app.llm.llm_service import llm_service
from app.narration_avatar.tts import tts_engine


class TeacherAssistant:
    """
    Handles in-lesson live student inquiries, clarifying concepts, providing fresh examples,
    simplifying explanations, or translating into other languages while maintaining strict lesson context.
    """

    def __init__(self):
        self.llm = llm_service

    def answer_followup(
        self,
        lesson: LessonPlan,
        request: FollowUpRequest,
        current_segment: Optional[Segment] = None
    ) -> FollowUpResponse:
        """
        Synthesizes a tailored, context-aware teacher response to a student question.
        """
        lang = request.language or lesson.target_language
        is_hindi = (lang.lower() in ["hi", "hindi"] or "hindi" in request.user_query.lower() or "हिंदी" in request.user_query)
        lang_name = "Hindi (हिंदी)" if is_hindi else "English"

        seg_context = ""
        if current_segment:
            seg_context = f"""
CURRENT SUBTOPIC: {current_segment.title}
CONCEPT TAUGHT: {current_segment.explanation}
EXAMPLE PROVIDED: {current_segment.example}
KEY POINTS: {', '.join(current_segment.key_points)}
"""

        system_prompt = f"""You are Dr. Nova, a supportive, highly knowledgeable AI Teacher currently teaching a live lesson on '{lesson.title}'.
A student in your class just asked a follow-up clarification question.

CRITICAL INSTRUCTIONS:
1. Stay strictly within the context of '{lesson.title}'.
2. Answer warmly, clearly, and concisely (approx 40-70 words).
3. If they asked for another example, provide a completely new real-world analogy.
4. If they asked to simplify, break it into 2-3 intuitive steps.
5. If they asked to explain in Hindi, write the response in natural, encouraging Hindi script.

LANGUAGE: {lang_name} ({'Respond entirely in natural, fluent Hindi script' if is_hindi else 'Respond in clear, encouraging English'})

JSON FORMAT SPECIFICATION:
Respond ONLY with a JSON object:
{{
  "response_text": "Direct, empathetic clarification spoken to the student...",
  "example": "A memorable real-world analogy..."
}}
"""

        prompt = f"""LESSON: {lesson.title} ({lesson.target_level} level)
{seg_context}
STUDENT INQUIRY: "{request.user_query}"

Provide your pedagogical response."""

        res = self.llm.generate_json(prompt, system_prompt=system_prompt)

        resp_text = res.get("response_text", f"Let's look at {lesson.title} step-by-step to make the core mechanism intuitive.")
        example = res.get("example", "")

        # Optionally synthesize audio narration for the response
        audio_url = None
        try:
            full_speech = resp_text
            if example:
                full_speech += f" For example: {example}"
            wav_path, _, _ = tts_engine.synthesize(
                full_speech,
                language="hi" if is_hindi else "en",
                output_filename=f"followup_{lesson.lesson_id[:8]}"
            )
            # Audio file generated
            audio_url = f"/media/videos/followup_{lesson.lesson_id[:8]}.wav"
        except Exception as e:
            print(f"[TeacherAssistant] TTS speech note: {e}")

        return FollowUpResponse(
            lesson_id=lesson.lesson_id,
            segment_id=request.segment_id,
            response_text=resp_text,
            example=example,
            audio_url=audio_url
        )


# Global singleton
teacher_assistant = TeacherAssistant()
