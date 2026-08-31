import React, { useState } from 'react';
import { HelpCircle, Send, CheckCircle2, AlertTriangle, ArrowRight, RotateCcw, Lightbulb } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function QuestionPrompt({
  question,
  onSubmitAnswer,
  isEvaluating,
  evaluationResult,
  onAdvanceNext,
  onPlayRemediation,
  isLastSegment
}) {
  const [typedAnswer, setTypedAnswer] = useState('');
  const [selectedOption, setSelectedOption] = useState(null);

  const handleSelectOption = (opt) => {
    setSelectedOption(opt);
    setTypedAnswer(opt);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!typedAnswer.trim()) return;

    onSubmitAnswer(typedAnswer);

    // If answer is evaluated as correct later, confetti triggers
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
      } catch (err) {
        // Safe catch
      }
    }
  }, [evaluationResult]);

  return (
    <div className="question-panel glass-panel glass-panel-glow">
      {/* Header */}
      <div className="q-header">
        <div className="q-badge">
          <HelpCircle size={18} className="text-cyan" />
          <span>Formative Check • Concept Verification</span>
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
                  : 'Misconception Detected: Let\'s Revisit This'}
              </h4>
              <p className="feedback-body">{evaluationResult.feedback}</p>
            </div>
          </div>

          {/* Misconception details if incorrect */}
          {!evaluationResult.is_correct && evaluationResult.misconception_explanation && (
            <div className="misconception-callout">
              <span className="misconception-tag">Diagnosed Mental Gap:</span>
              <p className="misconception-text">{evaluationResult.misconception_explanation}</p>
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
                    // Reset to try typing again
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
    </div>
  );
}
