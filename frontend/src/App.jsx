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
          <div className="lesson-studio-container">
            {/* Knowledge Route Grounding Bar */}
            <div className="grounding-bar glass-panel" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '10px 16px', marginBottom: '16px', borderRadius: '10px', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
                <span style={{ fontWeight: '600', color: '#94a3b8' }}>Grounded Knowledge Source:</span>
                <span className="route-badge" style={{ padding: '3px 10px', borderRadius: '6px', background: activeLesson?.source_route === 'external_web' ? 'rgba(6, 182, 212, 0.15)' : activeLesson?.source_route === 'pdf_rag' ? 'rgba(99, 102, 241, 0.15)' : 'rgba(16, 185, 129, 0.15)', color: activeLesson?.source_route === 'external_web' ? '#22d3ee' : activeLesson?.source_route === 'pdf_rag' ? '#a5b4fc' : '#34d399', border: '1px solid currentColor' }}>
                  {activeLesson?.source_route === 'external_web' ? '🌐 Live Web Retrieval' : activeLesson?.source_route === 'pdf_rag' ? '📄 PDF Document RAG' : '🧠 AI Knowledge Base'}
                </span>
                {activeLesson?.subject && (
                  <span style={{ color: '#64748b' }}>• Subject: <strong style={{ color: '#cbd5e1' }}>{activeLesson.subject}</strong></span>
                )}
              </div>

              {activeLesson?.sources && activeLesson.sources.length > 0 && (
                <div className="sources-inline-list" style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>Verified Sources:</span>
                  {activeLesson.sources.map((s, idx) => (
                    s.url ? (
                      <a
                        key={idx}
                        href={s.url}
                        target="_blank"
                        rel="noreferrer"
                        className="source-link-chip"
                        style={{ padding: '2px 8px', borderRadius: '4px', background: '#1e293b', color: '#38bdf8', textDecoration: 'none', fontSize: '0.75rem', border: '1px solid #334155' }}
                        title={`${s.title} (${s.source})`}
                      >
                        🔗 {s.source}
                      </a>
                    ) : (
                      <span
                        key={idx}
                        className="source-link-chip"
                        style={{ padding: '2px 8px', borderRadius: '4px', background: '#1e293b', color: '#94a3b8', fontSize: '0.75rem', border: '1px solid #334155' }}
                      >
                        📄 {s.source}
                      </span>
                    )
                  ))}
                </div>
              )}
            </div>

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
                  lessonId={activeLesson?.lesson_id}
                  segmentId={activeSegment?.id}
                  language={activeLesson?.target_language}
                />
              </div>
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
            sources={activeLesson?.sources}
            sourceRoute={activeLesson?.source_route}
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
