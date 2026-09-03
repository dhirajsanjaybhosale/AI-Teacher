import os
import json
from typing import Dict, Optional, List, Any
from app.lesson_planning.schemas import LessonPlan, Quiz, FeedbackReport, LearnerProgress, CompleteStudentProfile


class SessionStore:
    """
    In-memory session registry for active lessons, generated quizzes, session misconceptions, and student states.
    Guarantees strict session isolation with zero cross-session state leakage.
    """

    def __init__(self):
        self._lessons: Dict[str, LessonPlan] = {}
        self._quizzes: Dict[str, Quiz] = {}
        self._reports: Dict[str, FeedbackReport] = {}
        self._misconceptions: Dict[str, List[str]] = {}
        self._answer_history: Dict[str, List[Dict[str, Any]]] = {}

    def save_lesson(self, lesson: LessonPlan) -> None:
        self._lessons[lesson.lesson_id] = lesson
        if lesson.lesson_id not in self._misconceptions:
            self._misconceptions[lesson.lesson_id] = []
        if lesson.lesson_id not in self._answer_history:
            self._answer_history[lesson.lesson_id] = []

    def get_lesson(self, lesson_id: str) -> Optional[LessonPlan]:
        return self._lessons.get(lesson_id)

    def record_misconception(self, lesson_id: str, misconception: str) -> None:
        if lesson_id not in self._misconceptions:
            self._misconceptions[lesson_id] = []
        if misconception and misconception not in self._misconceptions[lesson_id]:
            self._misconceptions[lesson_id].append(misconception)

    def get_misconceptions(self, lesson_id: str) -> List[str]:
        return self._misconceptions.get(lesson_id, [])

    def record_student_answer(
        self,
        lesson_id: str,
        segment_id: str,
        question_text: str,
        user_answer: str,
        is_correct: bool,
        feedback: str,
        misconception: Optional[str] = None
    ) -> None:
        if lesson_id not in self._answer_history:
            self._answer_history[lesson_id] = []
        self._answer_history[lesson_id].append({
            "segment_id": segment_id,
            "question_text": question_text,
            "user_answer": user_answer,
            "is_correct": is_correct,
            "feedback": feedback,
            "misconception": misconception
        })

    def get_student_answers(self, lesson_id: str) -> List[Dict[str, Any]]:
        return self._answer_history.get(lesson_id, [])

    def save_quiz(self, quiz: Quiz) -> None:
        self._quizzes[quiz.lesson_id] = quiz

    def get_quiz(self, lesson_id: str) -> Optional[Quiz]:
        return self._quizzes.get(lesson_id)

    def save_report(self, report: FeedbackReport) -> None:
        self._reports[report.lesson_id] = report

    def get_report(self, lesson_id: str) -> Optional[FeedbackReport]:
        return self._reports.get(lesson_id)

    def clear_session(self, lesson_id: str) -> None:
        self._lessons.pop(lesson_id, None)
        self._quizzes.pop(lesson_id, None)
        self._reports.pop(lesson_id, None)
        self._misconceptions.pop(lesson_id, None)
        self._answer_history.pop(lesson_id, None)


class LearnerProfileStore:
    """
    Persistent student learning profile and longitudinal progress store.
    Persists progress to disk at 'media/learner_progress.json'.
    """
    def __init__(self, filepath: str = "media/learner_progress.json"):
        self.filepath = filepath
        self.progress = self._load()

    def _load(self) -> LearnerProgress:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return LearnerProgress(**data)
            except Exception as e:
                print(f"[LearnerProfileStore] Load error: {e}")
        return LearnerProgress()

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.progress.model_dump(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[LearnerProfileStore] Save error: {e}")

    def record_lesson_started(self, topic: str) -> None:
        if topic and topic not in self.progress.topics_studied:
            self.progress.topics_studied.append(topic)
        self.progress.total_lessons_studied = len(self.progress.topics_studied)
        self._save()

    def record_question_attempt(self, is_correct: bool, concept: str, misconception: Optional[str] = None) -> None:
        self.progress.questions_attempted += 1
        if is_correct:
            self.progress.questions_correct += 1
            if concept and concept not in self.progress.mastered_concepts:
                self.progress.mastered_concepts.append(concept)
        else:
            if concept and concept not in self.progress.weak_concepts:
                self.progress.weak_concepts.append(concept)
            if misconception and misconception not in self.progress.all_misconceptions_encountered:
                self.progress.all_misconceptions_encountered.append(misconception)

        if self.progress.questions_attempted > 0:
            self.progress.accuracy_percentage = round((self.progress.questions_correct / self.progress.questions_attempted) * 100, 1)
        self._save()

    def record_quiz_completed(self, report: FeedbackReport) -> None:
        self.progress.recent_quiz_scores.append({
            "lesson_title": report.title,
            "percentage": report.percentage,
            "total_score": report.total_score,
            "max_score": report.max_score
        })
        if report.next_recommended_topic and report.next_recommended_topic not in self.progress.recommended_topics_history:
            self.progress.recommended_topics_history.append(report.next_recommended_topic)
        self._save()

    def get_progress(self) -> LearnerProgress:
        return self.progress


class StudentProfileStore:
    """
    Dedicated persistence store for the complete student profile,
    learning goals, styles, subject/topic mastery, misconceptions,
    learning history, study plans, and dynamic AI recommendations.
    Persists data to 'media/student_profile.json'.
    """

    def __init__(self, filepath: str = "media/student_profile.json"):
        self.filepath = filepath
        self.profile = self._load()

    def _default_profile(self) -> CompleteStudentProfile:
        from app.lesson_planning.schemas import (
            StudentPersonalInfo, StudentLearningProfile, SubjectMastery,
            TopicMastery, MisconceptionRecord, LearningHistoryEntry, StudyPlanItem
        )
        return CompleteStudentProfile(
            personal_info=StudentPersonalInfo(
                full_name="Dhiraj Bhosale",
                education_level="Undergraduate",
                institution="MMCOE",
                course="B.Tech",
                branch="Information Technology",
                year="3rd Year",
                semester=6,
                subjects=["Data Structures", "DBMS", "Operating Systems", "Computer Networks", "Programming"],
                status="Active learner",
                avatar_initials="DB"
            ),
            learning_profile=StudentLearningProfile(
                preferred_language="hinglish",
                learning_goals=["Exam Preparation", "Concept Understanding"],
                learning_styles=["Visual", "Practical", "Step-by-step", "Analogy based"],
                current_level="intermediate",
                daily_study_time_minutes=60,
                preferred_difficulty="adaptive"
            ),
            overall_mastery=78,
            quiz_average=86,
            lessons_completed=24,
            hours_learned=38,
            learning_streak_days=7,
            today_goal_completed=3,
            today_goal_total=4,
            today_study_time_minutes=42,
            continue_learning_topic="Binary Search",
            continue_learning_progress=68,
            continue_learning_time_remaining=12,
            ai_recommendation="Revise Graph Representation before starting DFS.",
            ai_recommendation_reason="You had difficulty with graph representation in your last lesson.",
            ai_recommendation_topic="Graph Representation",
            subjects_mastery=[
                SubjectMastery(
                    subject="Data Structures",
                    overall_percentage=82,
                    topics=[
                        TopicMastery(name="Arrays", mastery_percentage=92, is_completed=True, status="mastered", last_attempted="3 days ago"),
                        TopicMastery(name="Stacks & Queues", mastery_percentage=88, is_completed=True, status="mastered", last_attempted="5 days ago"),
                        TopicMastery(name="Linked Lists", mastery_percentage=81, is_completed=True, status="mastered", last_attempted="1 week ago"),
                        TopicMastery(name="Binary Trees", mastery_percentage=67, is_completed=False, status="in_progress", last_attempted="2 days ago"),
                        TopicMastery(name="Dynamic Programming", mastery_percentage=52, is_completed=False, status="needs_improvement", last_attempted="Yesterday"),
                        TopicMastery(name="Graph Traversal", mastery_percentage=48, is_completed=False, status="needs_improvement", last_attempted="Yesterday")
                    ]
                ),
                SubjectMastery(
                    subject="DBMS",
                    overall_percentage=76,
                    topics=[
                        TopicMastery(name="SQL Queries", mastery_percentage=88, is_completed=True, status="mastered", last_attempted="4 days ago"),
                        TopicMastery(name="Normalization", mastery_percentage=82, is_completed=True, status="mastered", last_attempted="Yesterday"),
                        TopicMastery(name="B-Tree Indexing", mastery_percentage=70, is_completed=False, status="in_progress", last_attempted="2 weeks ago"),
                        TopicMastery(name="ACID Transactions", mastery_percentage=64, is_completed=False, status="needs_improvement", last_attempted="3 days ago")
                    ]
                ),
                SubjectMastery(
                    subject="Operating Systems",
                    overall_percentage=68,
                    topics=[
                        TopicMastery(name="Process Scheduling", mastery_percentage=75, is_completed=True, status="in_progress", last_attempted="4 days ago"),
                        TopicMastery(name="Deadlocks", mastery_percentage=68, is_completed=False, status="in_progress", last_attempted="1 week ago"),
                        TopicMastery(name="Memory Management & Paging", mastery_percentage=61, is_completed=False, status="needs_improvement", last_attempted="5 days ago")
                    ]
                ),
                SubjectMastery(
                    subject="Computer Networks",
                    overall_percentage=74,
                    topics=[
                        TopicMastery(name="OSI & TCP/IP Model", mastery_percentage=85, is_completed=True, status="mastered", last_attempted="1 week ago"),
                        TopicMastery(name="TCP vs UDP", mastery_percentage=80, is_completed=True, status="mastered", last_attempted="3 days ago"),
                        TopicMastery(name="Routing Protocols", mastery_percentage=58, is_completed=False, status="needs_improvement", last_attempted="2 days ago")
                    ]
                ),
                SubjectMastery(
                    subject="Programming",
                    overall_percentage=91,
                    topics=[
                        TopicMastery(name="OOP Principles", mastery_percentage=84, is_completed=True, status="mastered", last_attempted="5 days ago"),
                        TopicMastery(name="React Hooks", mastery_percentage=81, is_completed=True, status="mastered", last_attempted="2 days ago"),
                        TopicMastery(name="Recursion & Backtracking", mastery_percentage=88, is_completed=True, status="mastered", last_attempted="4 days ago")
                    ]
                )
            ],
            misconceptions=[
                MisconceptionRecord(
                    concept="Graph Traversal",
                    misconception="Confused adjacency list space complexity with adjacency matrix",
                    attempts=2,
                    mastery_percentage=48,
                    last_attempted="Yesterday",
                    ai_recommendation="Revise Graph Representation before starting DFS."
                ),
                MisconceptionRecord(
                    concept="Ohm's Law",
                    misconception="Student believes current increases when resistance increases, confusing inverse with direct proportionality.",
                    attempts=2,
                    mastery_percentage=68,
                    last_attempted="2 days ago",
                    ai_recommendation="Review water-pipe pressure analogy for electrical resistance."
                ),
                MisconceptionRecord(
                    concept="Cellular Respiration",
                    misconception="Student confused the source of oxygen with CO2 carbon fixation rather than water photolysis.",
                    attempts=1,
                    mastery_percentage=72,
                    last_attempted="4 days ago",
                    ai_recommendation="Focus on light-dependent reaction photolysis step."
                )
            ],
            learning_history=[
                LearningHistoryEntry(topic="Binary Search", date="Today", duration_minutes=20, quiz_score_percentage=90, mastery_delta="+8%", language="Hinglish", status="Completed"),
                LearningHistoryEntry(topic="DBMS Normalization", date="Yesterday", duration_minutes=30, quiz_score_percentage=82, mastery_delta="+5%", language="English", status="Completed"),
                LearningHistoryEntry(topic="React Hooks", date="2 days ago", duration_minutes=20, quiz_score_percentage=94, mastery_delta="+10%", language="Hinglish", status="Completed"),
                LearningHistoryEntry(topic="TCP vs UDP", date="3 days ago", duration_minutes=25, quiz_score_percentage=88, mastery_delta="+6%", language="English", status="Completed"),
                LearningHistoryEntry(topic="Photosynthesis & Solar Conversion", date="4 days ago", duration_minutes=22, quiz_score_percentage=85, mastery_delta="+7%", language="Hindi", status="Completed"),
                LearningHistoryEntry(topic="Introduction to Electricity & Ohm's Law", date="5 days ago", duration_minutes=32, quiz_score_percentage=100, mastery_delta="+12%", language="English", status="Completed")
            ],
            study_plan=[
                StudyPlanItem(day_name="Monday", topic="Graphs Revision & Representation", duration_minutes=30, is_completed=True),
                StudyPlanItem(day_name="Tuesday", topic="Breadth-First Search (BFS) Traversal", duration_minutes=40, is_completed=True),
                StudyPlanItem(day_name="Wednesday", topic="Depth-First Search (DFS) & Call Stack", duration_minutes=40, is_completed=True),
                StudyPlanItem(day_name="Thursday", topic="Binary Search Boundary Conditions", duration_minutes=30, is_completed=False),
                StudyPlanItem(day_name="Friday", topic="DBMS B-Tree Indexing Deep Dive", duration_minutes=45, is_completed=False),
                StudyPlanItem(day_name="Saturday", topic="Operating Systems Paging & Virtual Memory", duration_minutes=45, is_completed=False),
                StudyPlanItem(day_name="Sunday", topic="Full Conceptual Revision & Mastery Assessment", duration_minutes=60, is_completed=False)
            ],
            learning_path=[
                {"id": 1, "name": "Programming Fundamentals", "status": "completed", "topics_count": 8},
                {"id": 2, "name": "OOP Principles", "status": "completed", "topics_count": 6},
                {"id": 3, "name": "Arrays & Strings", "status": "completed", "topics_count": 10},
                {"id": 4, "name": "Linked Lists & Stacks", "status": "completed", "topics_count": 7},
                {"id": 5, "name": "Binary Trees & BST", "status": "current", "topics_count": 9},
                {"id": 6, "name": "Graphs & Traversals", "status": "locked", "topics_count": 8},
                {"id": 7, "name": "Dynamic Programming & Advanced Algorithms", "status": "locked", "topics_count": 12}
            ]
        )

    def _load(self) -> CompleteStudentProfile:
        from app.lesson_planning.schemas import CompleteStudentProfile
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return CompleteStudentProfile(**data)
            except Exception as e:
                print(f"[StudentProfileStore] Load error: {e}. Generating default profile.")
        
        default_prof = self._default_profile()
        self._save(default_prof)
        return default_prof

    def _save(self, profile: Optional[CompleteStudentProfile] = None) -> None:
        try:
            prof_to_save = profile or self.profile
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(prof_to_save.model_dump(), f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[StudentProfileStore] Save error: {e}")

    def get_profile(self) -> CompleteStudentProfile:
        return self.profile

    def update_profile(self, data: Dict[str, Any]) -> CompleteStudentProfile:
        from app.lesson_planning.schemas import CompleteStudentProfile
        # Deep merge updates
        current_dict = self.profile.model_dump()
        for k, v in data.items():
            if isinstance(v, dict) and k in current_dict and isinstance(current_dict[k], dict):
                current_dict[k].update(v)
            else:
                current_dict[k] = v
        self.profile = CompleteStudentProfile(**current_dict)
        self._save()
        return self.profile

    def record_lesson_completion(self, topic: str, duration_min: int, score_pct: int, language: str) -> None:
        from app.lesson_planning.schemas import LearningHistoryEntry
        entry = LearningHistoryEntry(
            topic=topic,
            date="Today",
            duration_minutes=duration_min or 15,
            quiz_score_percentage=score_pct or 85,
            mastery_delta=f"+{max(3, round(score_pct * 0.1))}%",
            language=language or "English",
            status="Completed"
        )
        self.profile.learning_history.insert(0, entry)
        self.profile.lessons_completed += 1
        self.profile.hours_learned += round(duration_min / 60.0, 1)
        # Update streak
        self.profile.learning_streak_days = max(self.profile.learning_streak_days, 7)
        self.profile.continue_learning_topic = topic
        self.profile.continue_learning_progress = min(100, self.profile.continue_learning_progress + 15)
        self._save()

    def record_misconception(self, concept: str, misconception: str) -> None:
        from app.lesson_planning.schemas import MisconceptionRecord
        for m in self.profile.misconceptions:
            if m.concept.lower() == concept.lower():
                m.attempts += 1
                m.misconception = misconception
                m.last_attempted = "Today"
                self._save()
                return

        new_m = MisconceptionRecord(
            concept=concept,
            misconception=misconception,
            attempts=1,
            mastery_percentage=55,
            last_attempted="Today",
            ai_recommendation=f"Review foundational principles of {concept} with intuitive analogies."
        )
        self.profile.misconceptions.insert(0, new_m)
        self.profile.ai_recommendation = f"Revise {concept} before proceeding."
        self.profile.ai_recommendation_reason = f"You had difficulty with {concept} in your last lesson."
        self.profile.ai_recommendation_topic = concept
        self._save()


# Global singletons
session_store = SessionStore()
learner_profile_store = LearnerProfileStore()
student_profile_store = StudentProfileStore()



