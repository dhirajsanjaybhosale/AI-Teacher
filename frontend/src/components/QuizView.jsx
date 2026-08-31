import React, { useState } from 'react';
import { Award, CheckCircle, ChevronLeft, ChevronRight, Send, HelpCircle } from 'lucide-react';

export default function QuizView({ quiz, onSubmitQuiz, isSubmitting }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({}); // { [question_id]: option_index }

  const currentQ = quiz.questions[currentIndex];
  const totalQ = quiz.questions.length;
  const answeredCount = Object.keys(selectedAnswers).length;

  const handleSelect = (optionIdx) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [currentQ.id]: optionIdx,
    });
  };

  const handleNext = () => {
    if (currentIndex < totalQ - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const formattedAnswers = quiz.questions.map((q) => ({
      question_id: q.id,
      selected_option_index: selectedAnswers[q.id] !== undefined ? selectedAnswers[q.id] : 0,
      typed_answer: selectedAnswers[q.id] !== undefined ? q.options[selectedAnswers[q.id]] : q.options[0],
    }));

    onSubmitQuiz(formattedAnswers);
  };

  return (
    <div className="quiz-container glass-panel glass-panel-glow">
      {/* Header */}
      <div className="quiz-header-bar">
        <div className="quiz-title-box">
          <Award size={24} className="text-indigo" />
          <div>
            <h2 className="quiz-main-title">{quiz.title}</h2>
            <p className="quiz-sub">Summative Mastery Check • Answer all questions to generate your report</p>
          </div>
        </div>

        {/* Progress Pill */}
        <div className="quiz-progress-pill">
          <span>Question {currentIndex + 1} of {totalQ}</span>
          <span className="pill-dot"></span>
          <span>{answeredCount} / {totalQ} Answered</span>
        </div>
      </div>

      {/* Question Card */}
      <div className="quiz-question-box">
        <div className="concept-tag">
          <HelpCircle size={14} />
          <span>Testing: {currentQ.concept_tested}</span>
        </div>

        <h3 className="quiz-q-text">{currentQ.question_text}</h3>

        {/* Options */}
        <div className="quiz-options-list">
          {currentQ.options.map((opt, idx) => {
            const isSelected = selectedAnswers[currentQ.id] === idx;
            return (
              <button
                key={idx}
                type="button"
                className={`quiz-opt-btn ${isSelected ? 'selected' : ''}`}
                onClick={() => handleSelect(idx)}
              >
                <span className="quiz-opt-num">{String.fromCharCode(65 + idx)}</span>
                <span className="quiz-opt-label">{opt}</span>
                {isSelected && <CheckCircle size={18} className="text-indigo" />}
              </button>
            );
          })}
        </div>
      </div>

      {/* Bottom Navigation */}
      <div className="quiz-nav-row">
        <button
          type="button"
          className="btn-secondary"
          onClick={handlePrev}
          disabled={currentIndex === 0}
        >
          <ChevronLeft size={18} />
          <span>Previous</span>
        </button>

        {currentIndex < totalQ - 1 ? (
          <button
            type="button"
            className="btn-primary-cta btn-quiz-next"
            onClick={handleNext}
          >
            <span>Next Question</span>
            <ChevronRight size={18} />
          </button>
        ) : (
          <button
            type="button"
            className="btn-primary-cta btn-quiz-submit"
            onClick={handleSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? (
              <span>Evaluating Mastery & Building Report...</span>
            ) : (
              <>
                <span>Complete & View Feedback Report</span>
                <Send size={18} />
              </>
            )}
          </button>
        )}
      </div>
    </div>
  );
}
