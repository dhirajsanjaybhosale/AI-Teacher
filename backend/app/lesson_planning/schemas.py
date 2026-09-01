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


class SourceMetadata(BaseModel):
    title: str = Field(..., description="Title of the retrieved source")
    url: Optional[str] = Field(default="", description="Verified URL of the source")
    source: str = Field(..., description="Source name, domain, or provider (e.g. Wikipedia, DuckDuckGo, PDF Document)")
    retrieved_at: Optional[str] = Field(default="", description="ISO timestamp of when the source was retrieved")
    snippet: Optional[str] = Field(default="", description="Relevant excerpt extracted from the source")


class LessonPlan(BaseModel):
    lesson_id: str = Field(..., description="Unique ID for this generated lesson session")
    title: str = Field(..., description="Main title of the lesson")
    subject: Optional[str] = Field(default="General", description="Subject area: Physics, Computer Science, Biology, Mathematics, etc.")
    description: str = Field(..., description="Short overview of what the learner will master")
    learning_objectives: List[str] = Field(default_factory=list, description="Target outcomes of the lesson")
    target_level: str = Field(default="beginner", description="beginner, intermediate, or advanced")
    target_language: str = Field(default="en", description="Language code: en (English), hi (Hindi), or hinglish")
    estimated_minutes: int = Field(default=10, description="Total time budget in minutes")
    goal: Optional[str] = Field(default="understand", description="Learning goal: understand, exam, interview, practice")
    segments: List[Segment] = Field(..., description="Ordered list of instructional segments")
    source_type: str = Field(default="topic", description="'pdf', 'docx', 'pptx', 'txt', 'topic', or 'external_web'")
    source_name: Optional[str] = Field(default="", description="Filename or topic query")
    source_route: Optional[str] = Field(default="llm_knowledge", description="'pdf_rag', 'external_web', 'llm_knowledge', or 'hybrid'")
    sources: List[SourceMetadata] = Field(default_factory=list, description="List of verified grounded sources")
    retrieval_confidence: Optional[float] = Field(default=1.0, description="RAG Retrieval confidence score (0.0 - 1.0)")
    retrieval_warning: Optional[str] = Field(default="", description="Notice if retrieval confidence is low or scanned document detected")
    is_scanned_doc: Optional[bool] = Field(default=False, description="Whether uploaded document was detected as image-only/scanned")
    study_roadmap_7_days: Optional[List[Dict[str, Any]]] = Field(default=None, description="Structured 7-day curriculum when 7-day budget selected")
    learning_path: Optional[List[Dict[str, Any]]] = Field(default=None, description="Hierarchical sequential mastery path nodes")


class LearnerPreferences(BaseModel):
    topic: Optional[str] = Field(default="", description="Typed topic string or chapter name")
    level: str = Field(default="beginner", description="beginner, intermediate, or advanced")
    time_minutes: int = Field(default=10, description="Time budget in minutes (5, 10, 20, 30, 60, 10080)")
    language: str = Field(default="en", description="Target language: en, hi, or hinglish")
    goal: Optional[str] = Field(default="understand", description="understand, exam, interview, practice")
    teaching_style: Optional[str] = Field(default="intuitive", description="Simple, Detailed, Visual, Practical, Socratic, Exam-focused")
    existing_knowledge: Optional[str] = Field(default="", description="Student's self-reported background or prior knowledge")
    force_web_search: Optional[bool] = Field(default=False, description="Whether to explicitly force external web retrieval")


class EvaluationResult(BaseModel):
    is_correct: bool = Field(..., description="Whether the learner's answer is correct")
    score: float = Field(..., description="Score between 0.0 and 1.0")
    feedback: str = Field(..., description="Encouraging feedback explaining what was right or missing")
    misconception_detected: bool = Field(default=False, description="True if a specific conceptual flaw was found")
    misconception_explanation: Optional[str] = Field(default="", description="Identified misconception details")
    concept: Optional[str] = Field(default="", description="Concept being tested, e.g., Ohm's Law")
    misconception: Optional[str] = Field(default="", description="Concise mental model diagnosis")
    reasoning: Optional[str] = Field(default="", description="Why the misconception occurred")
    severity: Optional[str] = Field(default="medium", description="Severity: low, medium, high")
    needs_remediation: Optional[bool] = Field(default=False, description="Whether adaptive remediation video is required")
    recommended_strategy: Optional[str] = Field(default="real_world_analogy", description="Pedagogical strategy: water_pipe_analogy, step_by_step_visual, real_world_analogy, first_principles, counter_example")
    missing_concept: Optional[str] = Field(default="", description="Key underlying concept missing from student answer")
    confidence: Optional[float] = Field(default=0.95, description="Confidence in evaluation score")
    adaptation_needed: bool = Field(default=False, description="Whether to trigger a remediation video")
    adapted_segment: Optional[Segment] = Field(default=None, description="New customized explanation segment if adapted")
    teacher_brain_state: Optional[Dict[str, Any]] = Field(default=None, description="Live telemetry snapshot for Teacher Brain panel")


class AnswerSubmission(BaseModel):
    lesson_id: str
    segment_id: str
    user_answer: str
    language: str = "en"


class LanguageSwitchRequest(BaseModel):
    lesson_id: str
    new_language: str = Field(..., description="en, hi, or hinglish")
    current_segment_index: Optional[int] = 0


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
    question_type: Optional[str] = Field(default="mcq", description="'mcq', 'conceptual', 'application', or 'short_answer'")


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
    learning_path: Optional[List[Dict[str, Any]]] = None
    study_roadmap_7_days: Optional[List[Dict[str, Any]]] = None
    retrieval_confidence: Optional[float] = 1.0


class LearnerProgress(BaseModel):
    total_lessons_studied: int = 0
    topics_studied: List[str] = Field(default_factory=list)
    segments_completed: int = 0
    questions_attempted: int = 0
    questions_correct: int = 0
    accuracy_percentage: float = 0.0
    all_misconceptions_encountered: List[str] = Field(default_factory=list)
    mastered_concepts: List[str] = Field(default_factory=list)
    weak_concepts: List[str] = Field(default_factory=list)
    recommended_topics_history: List[str] = Field(default_factory=list)
    recent_quiz_scores: List[Dict[str, Any]] = Field(default_factory=list)


