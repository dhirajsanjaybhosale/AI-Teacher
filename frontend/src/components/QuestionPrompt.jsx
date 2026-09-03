import React, { useState } from 'react';
import { HelpCircle, Send, CheckCircle2, AlertTriangle, ArrowRight, RotateCcw, Lightbulb, MessageSquarePlus, Sparkles, Volume2 } from 'lucide-react';
import confetti from 'canvas-confetti';
import { askTeacher, getFullMediaUrl } from '../api/client';

export default function QuestionPrompt({
  question,
  onSubmitAnswer,
  isEvaluating,
  evaluationResult,
  onAdvanceNext,
  onPlayRemediation,
  isLastSegment,
  lessonId,
  segmentId,
  language
}) {
  const [typedAnswer, setTypedAnswer] = useState('');
  const [selectedOption, setSelectedOption] = useState(null);

  // Follow-up Teacher Interaction state
  const [isAskOpen, setIsAskOpen] = useState(false);
  const [followupQuery, setFollowupQuery] = useState('');
  const [isAskingTeacher, setIsAskingTeacher] = useState(false);
  const [teacherResponse, setTeacherResponse] = useState(null);

  const handleSelectOption = (opt) => {
    setSelectedOption(opt);
    setTypedAnswer(opt);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!typedAnswer.trim()) return;
    onSubmitAnswer(typedAnswer);
  };

  const handleAskTeacher = async (queryToUse) => {
    const q = queryToUse || followupQuery;
    if (!q || !q.trim() || !lessonId) return;

    setIsAskingTeacher(true);
    try {
      const resp = await askTeacher({
        lessonId,
        segmentId,
        userQuery: q,
        language
      });
      setTeacherResponse(resp);
    } catch (err) {
      console.error("Error asking teacher:", err);
      alert("Teacher assistant temporarily unavailable.");
    } finally {
      setIsAskingTeacher(false);
    }
  };

  // Trigger confetti if evaluation is successful
  React.useEffect(() => {
    if (evaluationResult?.is_correct) {
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#6366f1', '#10b981', '#06b6d4', '#f59e0b']
        });
      } catch (err) {}
    }
  }, [evaluationResult]);

  return (
    <div className="question-panel glass-panel glass-panel-glow">
      {/* Header */}
      <div className="q-header">
        <div className="q-badge">
          <span className="q-brain-icon">🧠</span>
          <span className="q-badge-text">Let's check your understanding</span>
        </div>
        {question.hint && (
          <div className="q-hint-box" title={question.hint}>
            <Lightbulb size={15} className="text-amber" />
            <span>Hint: {question.hint}</span>
          </div>
        )}
      </div>

      {/* Question Text */}
      <h3 className="q-title">{question.question_text}</h3>

      {/* Interactive Options Cards */}
      {question.options && question.options.length > 0 && (
        <div className="options-grid">
          {question.options.map((opt, i) => {
            const isSelected = selectedOption === opt || typedAnswer.trim() === opt.trim();
            return (
              <button
                key={i}
                type="button"
                className={`option-card ${isSelected ? 'selected' : ''}`}
                onClick={() => handleSelectOption(opt)}
                disabled={isEvaluating || !!evaluationResult}
              >
                <span className="opt-letter">{String.fromCharCode(65 + i)}</span>
                <span className="opt-text">{opt}</span>
              </button>
            );
          })}
        </div>
      )}

      {/* Form Submission or Result Display */}
      {!evaluationResult ? (
        <form onSubmit={handleSubmit} className="q-submit-form">
          <div className="input-group">
            <textarea
              className="text-input q-textarea"
              rows={2}
              placeholder="Select an option above or type your reasoning in your own words..."
              value={typedAnswer}
              onChange={(e) => {
                setTypedAnswer(e.target.value);
                setSelectedOption(null);
              }}
              disabled={isEvaluating}
            />
          </div>

          <button
            type="submit"
            className="btn-primary-cta btn-submit-answer"
            disabled={isEvaluating || !typedAnswer.trim()}
          >
            {isEvaluating ? (
              <span>Diagnosing & Evaluating Concept...</span>
            ) : (
              <>
                <span>Submit Answer</span>
                <Send size={18} />
              </>
            )}
          </button>
        </form>
      ) : (
        /* Evaluation Feedback Card */
        <div className={`eval-feedback-card ${evaluationResult.is_correct ? 'feedback-success' : 'feedback-remedy'}`}>
          <div className="feedback-top">
            <div className="feedback-icon-box">
              {evaluationResult.is_correct ? (
                <CheckCircle2 size={28} className="text-emerald" />
              ) : (
                <AlertTriangle size={28} className="text-amber" />
              )}
            </div>
            <div>
              <h4 className="feedback-title">
                {evaluationResult.is_correct
                  ? 'Concept Mastered! Outstanding Work'
                  : 'Let\'s Revisit This: You\'re Very Close!'}
              </h4>
              <p className="feedback-body">{evaluationResult.feedback}</p>
            </div>
          </div>

          {/* Conversational Teacher Dialogue on Misconception */}
          {!evaluationResult.is_correct && (
            <div className="teacher-dialogue-bubble" style={{ margin: '10px 0', padding: '10px 14px', borderRadius: '8px', background: 'rgba(30, 41, 59, 0.7)', borderLeft: '3px solid #f59e0b' }}>
              <span style={{ fontSize: '0.75rem', fontWeight: 'bold', color: '#fbbf24', display: 'block', marginBottom: '4px' }}>
                👩‍🏫 Dr. Nova (AI Teacher):
              </span>
              <p style={{ margin: 0, fontSize: '0.86rem', color: '#f8fafc', fontStyle: 'italic', lineHeight: 1.45 }}>
                “You're very close! Don't worry—this is a very common confusion. Let's look at this another way with a dedicated re-explanation video!”
              </p>
            </div>
          )}

          {/* Misconception details if incorrect */}
          {!evaluationResult.is_correct && (evaluationResult.misconception_explanation || evaluationResult.misconception) && (
            <div className="misconception-callout">
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '8px', marginBottom: '6px', flexWrap: 'wrap' }}>
                <span className="misconception-tag">💡 Key Concept to Clarify</span>
                <span style={{ fontSize: '0.74rem', padding: '2px 8px', borderRadius: '4px', background: 'rgba(99,102,241,0.15)', color: '#a5b4fc', fontWeight: '500' }}>
                  Pedagogical Guidance
                </span>
              </div>
              <p className="misconception-text">{evaluationResult.misconception_explanation || evaluationResult.misconception}</p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="feedback-actions">
            {evaluationResult.is_correct ? (
              <button
                type="button"
                className="btn-primary-cta"
                onClick={onAdvanceNext}
              >
                <span>{isLastSegment ? 'Proceed to Final Mastery Quiz' : 'Advance to Next Segment'}</span>
                <ArrowRight size={18} />
              </button>
            ) : (
              <div className="remedy-btn-group">
                {evaluationResult.adapted_segment && (
                  <button
                    type="button"
                    className="btn-remedy-cta"
                    onClick={() => onPlayRemediation(evaluationResult.adapted_segment)}
                  >
                    <RotateCcw size={18} />
                    <span>Watch Custom Re-Explanation Video</span>
                  </button>
                )}
                <button
                  type="button"
                  className="btn-secondary"
                  onClick={() => {
                    setTypedAnswer('');
                    setSelectedOption(null);
                  }}
                >
                  <span>Try Answering Again</span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* --- IN-LESSON ASK AI TEACHER INTERACTIVE PANEL --- */}
      <div className="ask-teacher-dock" style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <button
            type="button"
            className="btn-secondary"
            style={{ fontSize: '0.85rem', padding: '0.4rem 0.8rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}
            onClick={() => setIsAskOpen(!isAskOpen)}
          >
            <MessageSquarePlus size={16} className="text-indigo" />
            <span>{isAskOpen ? 'Hide Teacher Clarification' : '💬 Ask AI Teacher a Follow-Up'}</span>
          </button>
          <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>Live context-retained tutoring</span>
        </div>

        {isAskOpen && (
          <div className="ask-teacher-body" style={{ background: 'rgba(15,23,42,0.6)', padding: '1rem', borderRadius: '10px', marginTop: '0.5rem' }}>
            {/* Quick Chips */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '0.75rem' }}>
              {[
                "Explain that again in simpler terms",
                "Give me another real-world example",
                "Explain this concept in Hindi",
                "Why is this principle important?"
              ].map((chip, idx) => (
                <button
                  key={idx}
                  type="button"
                  className="btn-sample-chip"
                  style={{ fontSize: '0.75rem', padding: '0.3rem 0.6rem' }}
                  onClick={() => {
                    setFollowupQuery(chip);
                    handleAskTeacher(chip);
                  }}
                  disabled={isAskingTeacher}
                >
                  <Sparkles size={12} style={{ marginRight: '4px' }} />
                  {chip}
                </button>
              ))}
            </div>

            {/* Custom Input */}
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                className="text-input"
                style={{ fontSize: '0.85rem', padding: '0.5rem 0.75rem' }}
                placeholder="Ask Dr. Nova any follow-up question about this segment..."
                value={followupQuery}
                onChange={(e) => setFollowupQuery(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleAskTeacher(); }}
                disabled={isAskingTeacher}
              />
              <button
                type="button"
                className="btn-primary-cta"
                style={{ padding: '0.5rem 1rem', fontSize: '0.85rem' }}
                onClick={() => handleAskTeacher()}
                disabled={isAskingTeacher || !followupQuery.trim()}
              >
                {isAskingTeacher ? 'Thinking...' : 'Ask'}
              </button>
            </div>

            {/* Teacher's Live Answer */}
            {teacherResponse && (
              <div style={{ marginTop: '0.75rem', padding: '0.85rem', background: 'rgba(30,41,59,0.7)', borderRadius: '8px', borderLeft: '3px solid #6366f1' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
                  <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: '#818cf8' }}>Dr. Nova (AI Teacher):</span>
                  {teacherResponse.audio_url && (
                    <audio
                      src={getFullMediaUrl(teacherResponse.audio_url)}
                      controls
                      autoPlay
                      style={{ height: '24px', maxWidth: '180px' }}
                    />
                  )}
                </div>
                <p style={{ fontSize: '0.85rem', color: '#f1f5f9', margin: '0 0 0.35rem 0', lineHeight: 1.4 }}>
                  {teacherResponse.response_text}
                </p>
                {teacherResponse.example && (
                  <p style={{ fontSize: '0.8rem', color: '#cbd5e1', fontStyle: 'italic', margin: 0 }}>
                    💡 <strong>Example:</strong> {teacherResponse.example}
                  </p>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

