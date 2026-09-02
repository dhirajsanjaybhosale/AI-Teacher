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


class DailyRoadmapItem(BaseModel):
    day: int = Field(..., description="Day number: 1 to 7")
    title: str = Field(..., description="Focus module title for this day")
    duration_minutes: int = Field(default=30, description="Recommended study time")
    revision_schedule: str = Field(..., description="Spaced repetition recall schedule")
    practice_goals: str = Field(..., description="Key exercises and target practice goals")
    assessment_type: Optional[str] = Field(default="Formative Mastery Check", description="Diagnostic check format")


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
    study_roadmap_7_days: Optional[List[DailyRoadmapItem]] = Field(default=None, description="Structured 7-day curriculum when 7-day budget selected")
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


class StudentPersonalInfo(BaseModel):
    full_name: str = "Dhiraj Bhosale"
    education_level: str = "Undergraduate"
    institution: str = "MMCOE"
    course: str = "B.Tech"
    branch: str = "Information Technology"
    year: str = "3rd Year"
    semester: int = 6
    subjects: List[str] = Field(default_factory=lambda: [
        "Data Structures", "DBMS", "Operating Systems", "Computer Networks", "Programming"
    ])
    status: str = "Active learner"
    avatar_initials: str = "DB"


class StudentLearningProfile(BaseModel):
    preferred_language: str = "hinglish"
    learning_goals: List[str] = Field(default_factory=lambda: ["Exam Preparation", "Concept Understanding"])
    learning_styles: List[str] = Field(default_factory=lambda: ["Visual", "Practical", "Step-by-step", "Analogy based"])
    current_level: str = "intermediate"
    daily_study_time_minutes: int = 60
    preferred_difficulty: str = "adaptive"


class TopicMastery(BaseModel):
    name: str
    mastery_percentage: int
    is_completed: bool = False
    status: str = "mastered"  # "mastered", "in_progress", "needs_improvement"
    last_attempted: Optional[str] = None


class SubjectMastery(BaseModel):
    subject: str
    overall_percentage: int
    topics: List[TopicMastery] = Field(default_factory=list)


class MisconceptionRecord(BaseModel):
    concept: str
    misconception: str
    attempts: int = 1
    mastery_percentage: int = 60
    last_attempted: str = "Yesterday"
    ai_recommendation: str = ""


class LearningHistoryEntry(BaseModel):
    topic: str
    date: str
    duration_minutes: int
    quiz_score_percentage: int
    mastery_delta: str
    language: str
    status: str = "Completed"


class StudyPlanItem(BaseModel):
    day_name: str
    topic: str
    duration_minutes: int
    is_completed: bool = False


class CompleteStudentProfile(BaseModel):
    personal_info: StudentPersonalInfo = Field(default_factory=StudentPersonalInfo)
    learning_profile: StudentLearningProfile = Field(default_factory=StudentLearningProfile)
    overall_mastery: int = 78
    quiz_average: int = 86
    lessons_completed: int = 24
    hours_learned: float = 38.0
    learning_streak_days: int = 7
    today_goal_completed: int = 3
    today_goal_total: int = 4
    today_study_time_minutes: int = 42
    continue_learning_topic: str = "Binary Search"
    continue_learning_progress: int = 68
    continue_learning_time_remaining: int = 12
    ai_recommendation: str = "Revise Graph Representation before starting DFS."
    ai_recommendation_reason: str = "You had difficulty with graph representation in your last lesson."
    ai_recommendation_topic: str = "Graph Representation"
    subjects_mastery: List[SubjectMastery] = Field(default_factory=list)
    misconceptions: List[MisconceptionRecord] = Field(default_factory=list)
    learning_history: List[LearningHistoryEntry] = Field(default_factory=list)
    study_plan: List[StudyPlanItem] = Field(default_factory=list)
    learning_path: List[Dict[str, Any]] = Field(default_factory=list)



