import React, { useState, useEffect } from 'react';
import Sidebar from './components/layout/Sidebar';
import TopHeader from './components/layout/TopHeader';
import StudentDashboard from './components/dashboard/StudentDashboard';
import LearnInputView from './components/learn/LearnInputView';
import ClassroomView from './components/classroom/ClassroomView';
import ProgressView from './components/progress/ProgressView';
import LearningPathView from './components/roadmap/LearningPathView';
import StudyPlanView from './components/study_plan/StudyPlanView';
import StudentProfileView from './components/profile/StudentProfileView';
import SettingsView from './components/settings/SettingsView';
import DeveloperModeModal from './components/settings/DeveloperModeModal';
import LessonPlanReviewModal from './components/classroom/LessonPlanReviewModal';
import LoadingOverlay from './components/LoadingOverlay';

import {
  createLesson,
  renderSegmentVideo,
  submitAnswer,
  getQuiz,
  submitQuiz,
  checkHealth,
  switchLanguage,
  getStudentProfile,
  updateStudentProfile,
  updateStudyPlan
} from './api/client';

import './App.css';

export default function App() {
  // Navigation: 'dashboard' | 'learn' | 'classroom' | 'progress' | 'path' | 'study_plan' | 'profile' | 'settings'
  const [activeNav, setActiveNav] = useState('dashboard');
  const [developerMode, setDeveloperMode] = useState(false);
  const [isDevConsoleOpen, setIsDevConsoleOpen] = useState(false);
  const [systemHealth, setSystemHealth] = useState(null);

  // Student Profile Persistent State
  const [studentProfile, setStudentProfile] = useState(null);

  // Classroom Session State
  const [activeLesson, setActiveLesson] = useState(null);
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0);
  const [isRemediationMode, setIsRemediationMode] = useState(false);
  const [remediationSegment, setRemediationSegment] = useState(null);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  // Classroom View State ('lesson' | 'quiz' | 'report')
  const [classroomViewState, setClassroomViewState] = useState('lesson');
  const [quiz, setQuiz] = useState(null);
  const [isSubmittingQuiz, setIsSubmittingQuiz] = useState(false);
  const [report, setReport] = useState(null);

  // Loading States
  const [isLoadingLesson, setIsLoadingLesson] = useState(false);
  const [isLoadingVideo, setIsLoadingVideo] = useState(false);
  const [showLessonPlanReview, setShowLessonPlanReview] = useState(false);

  // Search buffer from TopHeader
  const [pendingSearchQuery, setPendingSearchQuery] = useState('');

  // Initial Load: Health check & Student Profile
  useEffect(() => {
    checkHealth().then((data) => setSystemHealth(data));
    getStudentProfile()
      .then((data) => setStudentProfile(data))
      .catch((err) => console.error("Could not fetch student profile:", err));
  }, []);

  // Update Profile Handler
  const handleUpdateProfile = async (updateData) => {
    try {
      const updated = await updateStudentProfile(updateData);
      setStudentProfile(updated);
    } catch (err) {
      console.error("Failed to update student profile:", err);
    }
  };

  // Update Study Plan Handler
  const handleUpdateStudyPlan = async (plan) => {
    try {
      await updateStudyPlan(plan);
      if (studentProfile) {
        setStudentProfile({ ...studentProfile, study_plan: plan });
      }
    } catch (err) {
      console.error("Failed to update study plan:", err);
    }
  };

  // 1. Create or Launch Lesson
  const handleCreateLesson = async (params) => {
    setIsLoadingLesson(true);
    try {
      const lessonData = await createLesson({
        ...params,
        level: params.level || studentProfile?.learning_profile?.current_level || 'intermediate',
        language: params.language || studentProfile?.learning_profile?.preferred_language || 'hinglish',
        goal: params.goal || studentProfile?.learning_profile?.learning_goals?.[0] || 'understand',
        teachingStyle: params.teachingStyle || studentProfile?.learning_profile?.learning_styles?.[0] || 'Visual'
      });

      setActiveLesson(lessonData);
      setCurrentSegmentIndex(0);
      setIsRemediationMode(false);
      setRemediationSegment(null);
      setEvaluationResult(null);
      setQuiz(null);
      setReport(null);
      setClassroomViewState('lesson');
      setShowLessonPlanReview(true); // Display the Personalized Lesson Plan review screen first!

      // Refresh profile to reflect active lesson
      getStudentProfile().then((data) => setStudentProfile(data));
    } catch (err) {
      console.error("Error creating lesson:", err);
      alert("Unable to generate classroom lesson. Please check your server connection.");
    } finally {
      setIsLoadingLesson(false);
    }
  };

  const handleStartClassroomSession = () => {
    setShowLessonPlanReview(false);
    setActiveNav('classroom');
  };

  // Start Topic from Pill, Recommendation, or Streak Card
  const handleStartTopic = (topicName) => {
    handleCreateLesson({ topic: topicName });
  };

  // Continue Active or Recent Lesson
  const handleContinueLesson = (topicName) => {
    if (activeLesson && activeLesson.title.toLowerCase().includes((topicName || '').toLowerCase())) {
      setActiveNav('classroom');
      setClassroomViewState('lesson');
    } else {
      handleCreateLesson({ topic: topicName || 'Binary Search' });
    }
  };

  // Global Search from TopHeader
  const handleGlobalSearch = (query) => {
    setPendingSearchQuery(query);
    setActiveNav('learn');
  };

  // Switch Language
  const handleSwitchLanguage = async (newLang) => {
    if (studentProfile) {
      handleUpdateProfile({
        learning_profile: {
          ...studentProfile.learning_profile,
          preferred_language: newLang
        }
      });
    }

    if (activeLesson) {
      setIsLoadingVideo(true);
      try {
        const updatedLesson = await switchLanguage({
          lessonId: activeLesson.lesson_id,
          newLanguage: newLang,
          currentSegmentIndex
        });
        setActiveLesson(updatedLesson);
      } catch (err) {
        console.error("Language switch delay:", err);
      } finally {
        setIsLoadingVideo(false);
      }
    }
  };

  // 2. Formative Answer Submission
  const handleSubmitAnswer = async (userAnswer) => {
    if (!activeLesson) return;
    setIsEvaluating(true);
    try {
      const currentSeg = isRemediationMode
        ? remediationSegment
        : activeLesson.segments[currentSegmentIndex];

      const evalData = await submitAnswer({
        lessonId: activeLesson.lesson_id,
        segmentId: currentSeg.id,
        userAnswer,
        language: activeLesson.target_language
      });

      setEvaluationResult(evalData);
      // Refresh student profile after evaluation
      getStudentProfile().then((data) => setStudentProfile(data));
    } catch (err) {
      console.error("Error submitting answer:", err);
      alert("Failed to evaluate your answer.");
    } finally {
      setIsEvaluating(false);
    }
  };

  // 3. Play Remediation Video
  const handlePlayRemediation = (adaptedSeg) => {
    setRemediationSegment(adaptedSeg);
    setIsRemediationMode(true);
    setEvaluationResult(null);
  };

  // 4. Advance Next Segment or Launch Quiz
  const handleAdvanceNext = async () => {
    setEvaluationResult(null);
    setIsRemediationMode(false);
    setRemediationSegment(null);

    const nextIndex = currentSegmentIndex + 1;
    if (activeLesson && nextIndex < activeLesson.segments.length) {
      setCurrentSegmentIndex(nextIndex);
      const nextSeg = activeLesson.segments[nextIndex];

      if (!nextSeg.video_url) {
        setIsLoadingVideo(true);
        try {
          const vData = await renderSegmentVideo({
            lessonId: activeLesson.lesson_id,
            segmentId: nextSeg.id
          });
          nextSeg.video_url = vData.video_url;
        } catch (err) {
          console.error("Error rendering segment video:", err);
        } finally {
          setIsLoadingVideo(false);
        }
      }
    } else {
      // End of segments -> launch quiz
      setIsLoadingLesson(true);
      try {
        const quizData = await getQuiz(activeLesson.lesson_id);
        setQuiz(quizData);
        setClassroomViewState('quiz');
      } catch (err) {
        console.error("Error fetching quiz:", err);
        alert("Failed to generate quiz assessment.");
      } finally {
        setIsLoadingLesson(false);
      }
    }
  };

  // 5. Submit Summative Quiz
  const handleSubmitQuiz = async (answers) => {
    if (!activeLesson || !quiz) return;
    setIsSubmittingQuiz(true);
    try {
      const reportData = await submitQuiz({
        lessonId: activeLesson.lesson_id,
        quizId: quiz.quiz_id,
        answers
      });
      setReport(reportData);
      setClassroomViewState('report');
      // Refresh profile to reflect completed quiz
      getStudentProfile().then((data) => setStudentProfile(data));
    } catch (err) {
      console.error("Error submitting quiz:", err);
      alert("Failed to compile feedback report.");
    } finally {
      setIsSubmittingQuiz(false);
    }
  };

  // Active segment
  const activeSegment = isRemediationMode
    ? remediationSegment
    : activeLesson?.segments?.[currentSegmentIndex];

  return (
    <div className="app-shell-layout">
      {/* 1. Main Navigation Sidebar */}
      <Sidebar
        activeNav={activeNav}
        onSelectNav={setActiveNav}
        studentProfile={studentProfile}
      />

      {/* 2. Primary Content Stage */}
      <div className="app-stage-wrapper">
        <TopHeader
          studentProfile={studentProfile}
          language={studentProfile?.learning_profile?.preferred_language || 'hinglish'}
          onSwitchLanguage={handleSwitchLanguage}
          onGlobalSearch={handleGlobalSearch}
          onOpenProfile={() => setActiveNav('profile')}
        />

        <main className="app-main-viewport">
          {/* VIEW: DASHBOARD */}
          {activeNav === 'dashboard' && (
            <StudentDashboard
              studentProfile={studentProfile}
              onStartTopic={handleStartTopic}
              onContinueLesson={handleContinueLesson}
            />
          )}

          {/* VIEW: LEARN */}
          {activeNav === 'learn' && (
            <LearnInputView
              onSubmitLesson={handleCreateLesson}
              isLoading={isLoadingLesson}
              studentProfile={studentProfile}
              initialQuery={pendingSearchQuery}
            />
          )}

          {/* VIEW: CLASSROOM */}
          {activeNav === 'classroom' && (
            <ClassroomView
              activeLesson={activeLesson}
              activeSegment={activeSegment}
              currentSegmentIndex={currentSegmentIndex}
              isRemediationMode={isRemediationMode}
              isLoadingVideo={isLoadingVideo}
              isEvaluating={isEvaluating}
              evaluationResult={evaluationResult}
              quiz={quiz}
              report={report}
              viewState={classroomViewState}
              onSubmitAnswer={handleSubmitAnswer}
              onAdvanceNext={handleAdvanceNext}
              onPlayRemediation={handlePlayRemediation}
              onSubmitQuiz={handleSubmitQuiz}
              isSubmittingQuiz={isSubmittingQuiz}
              onRestartLesson={() => setActiveNav('learn')}
              studentProfile={studentProfile}
            />
          )}

          {/* VIEW: PROGRESS */}
          {activeNav === 'progress' && (
            <ProgressView
              studentProfile={studentProfile}
              onStartTopic={handleStartTopic}
            />
          )}

          {/* VIEW: LEARNING PATH */}
          {activeNav === 'path' && (
            <LearningPathView
              studentProfile={studentProfile}
              onStartTopic={handleStartTopic}
            />
          )}

          {/* VIEW: STUDY PLAN */}
          {activeNav === 'study_plan' && (
            <StudyPlanView
              studentProfile={studentProfile}
              onUpdateStudyPlan={handleUpdateStudyPlan}
              onStartTopic={handleStartTopic}
            />
          )}

          {/* VIEW: MY PROFILE */}
          {activeNav === 'profile' && (
            <StudentProfileView
              studentProfile={studentProfile}
              onUpdateProfile={handleUpdateProfile}
              onStartTopic={handleStartTopic}
            />
          )}

          {/* VIEW: SETTINGS */}
          {activeNav === 'settings' && (
            <SettingsView
              developerMode={developerMode}
              onToggleDeveloperMode={setDeveloperMode}
              onOpenDevConsole={() => setIsDevConsoleOpen(true)}
              systemHealth={systemHealth}
            />
          )}
        </main>
      </div>

      {/* Developer Inspection Console Modal (Developer Mode Only) */}
      <DeveloperModeModal
        isOpen={isDevConsoleOpen && developerMode}
        onClose={() => setIsDevConsoleOpen(false)}
        systemHealth={systemHealth}
        activeLesson={activeLesson}
        activeSegment={activeSegment}
      />

      {/* Personalized Lesson Plan Review Modal (Shown before classroom starts) */}
      {showLessonPlanReview && activeLesson && (
        <LessonPlanReviewModal
          lessonPlan={activeLesson}
          onStartLesson={handleStartClassroomSession}
          onClose={() => setShowLessonPlanReview(false)}
        />
      )}

      {/* Loading Overlay */}
      {isLoadingLesson && (
        <LoadingOverlay
          title="Preparing Your Personalized Lesson"
          subtitle="Grounded in your student profile, learning goals, and course curriculum..."
        />
      )}
    </div>
  );
}
