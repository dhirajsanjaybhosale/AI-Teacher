import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import UploadOrTopicForm from './components/UploadOrTopicForm';
import VideoPlayer from './components/VideoPlayer';
import QuestionPrompt from './components/QuestionPrompt';
import QuizView from './components/QuizView';
import FeedbackReport from './components/FeedbackReport';
import LoadingOverlay from './components/LoadingOverlay';

import {
  createLesson,
  renderSegmentVideo,
  submitAnswer,
  getQuiz,
  submitQuiz,
  checkHealth
} from './api/client';

import './App.css';

export default function App() {
  // Navigation / View State
  const [viewState, setViewState] = useState('onboarding'); // 'onboarding' | 'lesson' | 'quiz' | 'report'
  const [systemHealth, setSystemHealth] = useState(null);

  // Lesson State
  const [activeLesson, setActiveLesson] = useState(null);
  const [currentSegmentIndex, setCurrentSegmentIndex] = useState(0);
  const [isRemediationMode, setIsRemediationMode] = useState(false);
  const [remediationSegment, setRemediationSegment] = useState(null);

  // Interaction State
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  // Quiz & Report State
  const [quiz, setQuiz] = useState(null);
  const [isSubmittingQuiz, setIsSubmittingQuiz] = useState(false);
  const [report, setReport] = useState(null);

  // Loading States
  const [isLoadingLesson, setIsLoadingLesson] = useState(false);
  const [isLoadingVideo, setIsLoadingVideo] = useState(false);

  // Initial Health Check
  useEffect(() => {
    checkHealth().then((data) => setSystemHealth(data));
  }, []);

  // 1. Create Lesson
  const handleCreateLesson = async (params) => {
    setIsLoadingLesson(true);
    try {
      const lessonData = await createLesson(params);
      setActiveLesson(lessonData);
      setCurrentSegmentIndex(0);
      setIsRemediationMode(false);
      setRemediationSegment(null);
      setEvaluationResult(null);
      setViewState('lesson');
    } catch (err) {
      console.error("Error creating lesson:", err);
      alert("Failed to generate lesson. Please check backend connection.");
    } finally {
      setIsLoadingLesson(false);
    }
  };

  // 2. Submit Formative Check Answer
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
    } catch (err) {
      console.error("Error submitting answer:", err);
      alert("Failed to evaluate answer.");
    } finally {
      setIsEvaluating(false);
    }
  };

  // 3. Play Remediation Video
  const handlePlayRemediation = (adaptedSeg) => {
    setRemediationSegment(adaptedSeg);
    setIsRemediationMode(true);
    setEvaluationResult(null); // Reset feedback so student can re-attempt after watching
  };

  // 4. Advance to Next Segment or Launch Quiz
  const handleAdvanceNext = async () => {
    setEvaluationResult(null);
    setIsRemediationMode(false);
    setRemediationSegment(null);

    const nextIndex = currentSegmentIndex + 1;
    if (activeLesson && nextIndex < activeLesson.segments.length) {
      setCurrentSegmentIndex(nextIndex);
      const nextSeg = activeLesson.segments[nextIndex];

      // Ensure video is rendered for the next segment
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
      // Reached end of lesson segments -> Fetch and Launch Summative Quiz
      setIsLoadingLesson(true);
      try {
        const quizData = await getQuiz(activeLesson.lesson_id);
        setQuiz(quizData);
        setViewState('quiz');
      } catch (err) {
        console.error("Error fetching quiz:", err);
        alert("Failed to generate quiz.");
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
      setViewState('report');
    } catch (err) {
      console.error("Error submitting quiz:", err);
      alert("Failed to generate report.");
    } finally {
      setIsSubmittingQuiz(false);
    }
  };

  // 6. Reset or Start Recommended Topic
  const handleResetLesson = () => {
    setViewState('onboarding');
    setActiveLesson(null);
    setCurrentSegmentIndex(0);
    setIsRemediationMode(false);
    setRemediationSegment(null);
    setEvaluationResult(null);
    setQuiz(null);
    setReport(null);
  };

  const handleStartNextTopic = (topicName) => {
    handleResetLesson();
    handleCreateLesson({
      topic: topicName,
      level: activeLesson?.target_level || 'beginner',
      timeMinutes: 5,
      language: activeLesson?.target_language || 'en'
    });
  };

  // Active segment display object
  const activeSegment = isRemediationMode
    ? remediationSegment
    : activeLesson?.segments?.[currentSegmentIndex];

  return (
    <div className="app-layout">
      {/* Universal Header */}
      <Header
        systemHealth={systemHealth}
        language={activeLesson?.target_language || 'en'}
        onResetLesson={handleResetLesson}
        hasActiveLesson={viewState !== 'onboarding'}
      />

      {/* Main Studio Viewport */}
      <main className="main-content">
        {/* VIEW 1: Onboarding & Input Form */}
        {viewState === 'onboarding' && (
          <UploadOrTopicForm
            onSubmit={handleCreateLesson}
            isLoading={isLoadingLesson}
          />
        )}

        {/* VIEW 2: Interactive Teaching Studio */}
        {viewState === 'lesson' && activeSegment && (
          <div className="lesson-studio-grid">
            {/* Left/Main Column: Video Player */}
            <div className="studio-video-col">
              <VideoPlayer
                videoUrl={activeSegment.video_url}
                segmentTitle={activeSegment.title}
                segmentIndex={currentSegmentIndex + 1}
                totalSegments={activeLesson?.segments?.length || 1}
                isRemediation={isRemediationMode}
                isLoadingVideo={isLoadingVideo}
              />
            </div>

            {/* Right/Bottom Column: Formative Question Dock */}
            <div className="studio-interact-col">
              <QuestionPrompt
                question={activeSegment.question}
                onSubmitAnswer={handleSubmitAnswer}
                isEvaluating={isEvaluating}
                evaluationResult={evaluationResult}
                onAdvanceNext={handleAdvanceNext}
                onPlayRemediation={handlePlayRemediation}
                isLastSegment={currentSegmentIndex === (activeLesson?.segments?.length || 1) - 1}
              />
            </div>
          </div>
        )}

        {/* VIEW 3: Summative Quiz View */}
        {viewState === 'quiz' && quiz && (
          <QuizView
            quiz={quiz}
            onSubmitQuiz={handleSubmitQuiz}
            isSubmitting={isSubmittingQuiz}
          />
        )}

        {/* VIEW 4: Feedback & Mastery Report */}
        {viewState === 'report' && report && (
          <FeedbackReport
            report={report}
            onStartNextTopic={handleStartNextTopic}
            onResetLesson={handleResetLesson}
          />
        )}
      </main>

      {/* Loading Overlay Modal */}
      {isLoadingLesson && (
        <LoadingOverlay
          title={viewState === 'onboarding' ? "Synthesizing AI Lesson & Avatar Video" : "Generating Mastery Assessment"}
          subtitle="Processing RAG vectors, audio synthesis, and ffmpeg visual compositing..."
        />
      )}
    </div>
  );
}
