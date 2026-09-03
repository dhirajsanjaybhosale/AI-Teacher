import React, { useState } from 'react';
import VideoPlayer from '../VideoPlayer';
import ClassroomBoard from '../ClassroomBoard';
import TeacherReactionBadge from '../TeacherReactionBadge';
import QuestionPrompt from '../QuestionPrompt';
import QuizView from '../QuizView';
import FeedbackReport from '../FeedbackReport';
import { BookOpen, Sparkles, CheckCircle2, ArrowRight, RotateCcw, Layers } from 'lucide-react';

export default function ClassroomView({
  activeLesson,
  activeSegment,
  currentSegmentIndex,
  isRemediationMode,
  isLoadingVideo,
  isEvaluating,
  evaluationResult,
  quiz,
  report,
  viewState, // 'lesson' | 'quiz' | 'report'
  onSubmitAnswer,
  onAdvanceNext,
  onPlayRemediation,
  onSubmitQuiz,
  isSubmittingQuiz,
  onRestartLesson,
  studentProfile
}) {
  const [boardMode, setBoardMode] = useState('split'); // 'split' | 'video' | 'board'

  if (!activeLesson && viewState === 'lesson') {
    return (
      <div className="classroom-empty-state glass-panel">
        <BookOpen size={36} className="text-primary" />
        <h3>No Active Classroom Session</h3>
        <p>Select a topic from your dashboard or search to start a personalized lesson with Dr. Nova.</p>
        <button
          type="button"
          className="btn-primary-gradient"
          onClick={() => onRestartLesson?.()}
        >
          <span>Choose a Topic</span>
          <ArrowRight size={16} />
        </button>
      </div>
    );
  }

  // Quiz View
  if (viewState === 'quiz' && quiz) {
    return (
      <div className="classroom-quiz-container">
        <QuizView
          quiz={quiz}
          onSubmitQuiz={onSubmitQuiz}
          isSubmitting={isSubmittingQuiz}
        />
      </div>
    );
  }

  // Final Report View
  if (viewState === 'report' && report) {
    return (
      <div className="classroom-report-container">
        <FeedbackReport
          report={report}
          onRestartLesson={onRestartLesson}
        />
      </div>
    );
  }

  // Active Lesson View
  const totalSegments = activeLesson?.segments?.length || 1;
  const currentPartNum = currentSegmentIndex + 1;
  const progressPct = Math.round((currentPartNum / totalSegments) * 100);

  // Lesson duration and progress calculations
  const [currentSegVideoSec, setCurrentSegVideoSec] = useState(0);
  const totalTargetSeconds = activeLesson?.target_duration_seconds || ((activeLesson?.estimated_minutes || 10) * 60);

  const prevCompletedSecs = (activeLesson?.segments || [])
    .slice(0, currentSegmentIndex)
    .reduce((acc, seg) => acc + (seg.actual_seconds || seg.target_seconds || 120), 0);
  const lessonProgressSeconds = Math.min(totalTargetSeconds, Math.floor(prevCompletedSecs + currentSegVideoSec));

  const formatSecs = (sec) => {
    if (!sec || isNaN(sec)) return '00:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
  };

  const getTeachingState = () => {
    if (isEvaluating) return 'evaluating';
    if (evaluationResult?.is_correct) return 'correct';
    if (isRemediationMode || (evaluationResult && !evaluationResult.is_correct)) return 'remediating';
    return 'teaching';
  };

  return (
    <div className="classroom-view-container">
      {/* Clean Classroom Header Bar */}
      <div className="classroom-top-header glass-panel">
        <div className="classroom-header-left">
          <span className="classroom-eyebrow">AI CLASSROOM SESSION</span>
          <h2 className="classroom-topic-title">{activeLesson.title}</h2>
          <div className="classroom-sub-badges">
            <span className="classroom-part-badge">Part {currentPartNum} of {totalSegments}</span>
            <span className="classroom-subject-badge">{activeLesson.subject || 'Educational Concept'}</span>
            {activeLesson.source_name && (
              <span className="classroom-source-tag">
                ✓ Grounded in {activeLesson.source_name}
              </span>
            )}
          </div>

          {/* Real-time Lesson Duration & Module Progress Ticker */}
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '8px',
            marginTop: '10px',
            padding: '6px 14px',
            borderRadius: '8px',
            background: 'rgba(15, 23, 42, 0.85)',
            border: '1px solid rgba(99, 102, 241, 0.35)',
            fontSize: '0.84rem',
            fontFamily: 'monospace',
            color: '#cbd5e1'
          }}>
            <span style={{ color: '#a5b4fc', fontWeight: '600' }}>Lesson Duration:</span> {formatSecs(totalTargetSeconds)}
            <span style={{ color: '#475569' }}>|</span>
            <span style={{ color: '#38bdf8', fontWeight: '600' }}>Progress:</span> {formatSecs(lessonProgressSeconds)} / {formatSecs(totalTargetSeconds)}
            <span style={{ color: '#475569' }}>|</span>
            <span style={{ color: '#34d399', fontWeight: '600' }}>Module:</span> {currentPartNum.toString().padStart(2, '0')} / {totalSegments.toString().padStart(2, '0')}
          </div>
        </div>

        {/* Layout Switcher */}
        <div className="classroom-layout-toggles">
          <div className="toggle-pill-group">
            <button
              type="button"
              className={`toggle-btn ${boardMode === 'split' ? 'active' : ''}`}
              onClick={() => setBoardMode('split')}
            >
              Classroom (Split)
            </button>
            <button
              type="button"
              className={`toggle-btn ${boardMode === 'video' ? 'active' : ''}`}
              onClick={() => setBoardMode('video')}
            >
              Teacher Focus
            </button>
            <button
              type="button"
              className={`toggle-btn ${boardMode === 'board' ? 'active' : ''}`}
              onClick={() => setBoardMode('board')}
            >
              Smartboard Focus
            </button>
          </div>
        </div>
      </div>

      {/* Real-Time Teacher Presence Badge */}
      <TeacherReactionBadge
        teachingState={getTeachingState()}
        teacherName="Dr. Nova"
        conceptName={activeSegment?.title}
        speechSnippet={evaluationResult?.feedback}
      />

      {/* Main Classroom Layout Grid */}
      <div className="classroom-main-grid">
        {/* Visual Presentation Area (Teacher Video and/or Smartboard) */}
        <div className="classroom-visual-col">
          {(boardMode === 'split' || boardMode === 'video') && (
            <VideoPlayer
              videoUrl={activeSegment?.video_url}
              segmentTitle={activeSegment?.title}
              segmentIndex={currentPartNum}
              totalSegments={totalSegments}
              isRemediation={isRemediationMode}
              isLoadingVideo={isLoadingVideo}
              onTimeUpdate={(sec) => setCurrentSegVideoSec(sec)}
            />
          )}

          {(boardMode === 'split' || boardMode === 'board') && (
            <ClassroomBoard
              segment={activeSegment}
              lessonTitle={activeLesson.title}
              subject={activeLesson.subject || 'General'}
              isRemediation={isRemediationMode}
              highlightFocus={isRemediationMode}
            />
          )}
        </div>

        {/* Interactive Pedagogical Question Dock */}
        <div className="classroom-dock-col">
          <QuestionPrompt
            question={activeSegment?.question}
            onSubmitAnswer={onSubmitAnswer}
            isEvaluating={isEvaluating}
            evaluationResult={evaluationResult}
            onAdvanceNext={onAdvanceNext}
            onPlayRemediation={onPlayRemediation}
            isLastSegment={currentSegmentIndex === totalSegments - 1}
            lessonId={activeLesson?.lesson_id}
            segmentId={activeSegment?.id}
            language={activeLesson?.target_language}
          />
        </div>
      </div>
    </div>
  );
}
