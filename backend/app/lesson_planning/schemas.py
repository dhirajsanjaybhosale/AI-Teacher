from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Question(BaseModel):
    id: str = Field(..., description="Unique ID for the question (e.g., q_1)")
    question_text: str = Field(..., description="The question text asking about the segment's core concept")
    options: Optional[List[str]] = Field(default=None, description="Multiple choice options if applicable")
    correct_answer: str = Field(..., description="Expected correct answer or key criteria")
    hint: Optional[str] = Field(default="", description="Helpful hint for the learner")
    explanation: Optional[str] = Field(default="", description="Detailed explanation of the correct answer")


class Segment(BaseModel):
    id: str = Field(..., description="Segment identifier, e.g. seg_1")
    title: str = Field(..., description="Title of the topic/subtopic")
    explanation: str = Field(..., description="Clear, engaging spoken narration explanation (in target language)")
    example: Optional[str] = Field(default="", description="Real-world intuitive analogy or example")
    key_points: List[str] = Field(default_factory=list, description="3-4 bullet points to show on the visual slide")
    visual_diagram_type: Optional[str] = Field(default="flowchart", description="code/equation/comparison/flowchart/process/timeline/diagram")
    visual_description: Optional[str] = Field(default="", description="Description of the supporting visual diagram or layout")
    visual_code_or_math: Optional[str] = Field(default="", description="Code snippet or mathematical formula for visual render")
    question: Question = Field(..., description="Interactive check question embedded in this segment")
    video_url: Optional[str] = Field(default=None, description="URL or relative path to the generated segment video")
    is_remediation: bool = Field(default=False, description="Flag indicating if this is an adaptive re-explanation segment")


class LessonPlan(BaseModel):
    lesson_id: str = Field(..., description="Unique ID for this generated lesson session")
    title: str = Field(..., description="Main title of the lesson")
    subject: Optional[str] = Field(default="General", description="Subject area: Physics, Computer Science, Biology, Mathematics, etc.")
    description: str = Field(..., description="Short overview of what the learner will master")
    learning_objectives: List[str] = Field(default_factory=list, description="Target outcomes of the lesson")
    target_level: str = Field(default="beginner", description="beginner, intermediate, or advanced")
    target_language: str = Field(default="en", description="Language code: en (English) or hi (Hindi)")
    estimated_minutes: int = Field(default=10, description="Total time budget in minutes")
    goal: Optional[str] = Field(default="understand", description="Learning goal: understand, exam, interview, practice")
    segments: List[Segment] = Field(..., description="Ordered list of instructional segments")
    source_type: str = Field(default="topic", description="'pdf' or 'topic'")
    source_name: Optional[str] = Field(default="", description="Filename or topic query")


class LearnerPreferences(BaseModel):
    topic: Optional[str] = Field(default="", description="Typed topic string or chapter name")
    level: str = Field(default="beginner", description="beginner, intermediate, or advanced")
    time_minutes: int = Field(default=10, description="Time budget in minutes (5, 10, 20, 30, 60)")
    language: str = Field(default="en", description="Target language: en (English) or hi (Hindi)")
    goal: Optional[str] = Field(default="understand", description="understand, exam, interview, practice")
    teaching_style: Optional[str] = Field(default="intuitive", description="intuitive, rigorous, visual, analogy")


class EvaluationResult(BaseModel):
    is_correct: bool = Field(..., description="Whether the learner's answer is correct")
    score: float = Field(..., description="Score between 0.0 and 1.0")
    feedback: str = Field(..., description="Encouraging feedback explaining what was right or missing")
    misconception_detected: bool = Field(default=False, description="True if a specific conceptual flaw was found")
    misconception_explanation: Optional[str] = Field(default="", description="Identified misconception details")
    missing_concept: Optional[str] = Field(default="", description="Key underlying concept missing from student answer")
    confidence: Optional[float] = Field(default=0.95, description="Confidence in evaluation score")
    adaptation_needed: bool = Field(default=False, description="Whether to trigger a remediation video")
    adapted_segment: Optional[Segment] = Field(default=None, description="New customized explanation segment if adapted")


class AnswerSubmission(BaseModel):
    lesson_id: str
    segment_id: str
    user_answer: str
    language: str = "en"


class FollowUpRequest(BaseModel):
    lesson_id: str
    segment_id: Optional[str] = None
    user_query: str
    language: Optional[str] = "en"


class FollowUpResponse(BaseModel):
    lesson_id: str
    segment_id: Optional[str] = None
    response_text: str
    example: Optional[str] = ""
    audio_url: Optional[str] = None


class QuizQuestion(BaseModel):
    id: str
    question_text: str
    options: List[str]
    correct_option_index: int
    concept_tested: str
    explanation: str


class Quiz(BaseModel):
    quiz_id: str
    lesson_id: str
    title: str
    questions: List[QuizQuestion]


class QuizAnswerItem(BaseModel):
    question_id: str
    selected_option_index: Optional[int] = None
    typed_answer: Optional[str] = None


class QuizSubmission(BaseModel):
    lesson_id: str
    quiz_id: str
    answers: List[QuizAnswerItem]


class FeedbackReport(BaseModel):
    lesson_id: str
    title: str
    total_score: int
    max_score: int
    percentage: float
    concepts_understood: List[str]
    weak_concepts: List[str]
    misconceptions: List[str] = Field(default_factory=list, description="Specific mental misconceptions identified and remediated")
    recommendations: List[str]
    next_recommended_topic: str
    summary_feedback: str

