import React, { useEffect } from 'react';
import { Award, CheckCircle, AlertCircle, Sparkles, ArrowRight, RotateCcw, BookOpen, Target, Compass } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function FeedbackReport({ report, sources, sourceRoute, onStartNextTopic, onResetLesson }) {
  const pct = report.percentage || 0;
  const isHighMastery = pct >= 75;

  useEffect(() => {
    if (isHighMastery) {
      try {
        confetti({
          particleCount: 100,
          spread: 80,
          origin: { y: 0.5 },
          colors: ['#6366f1', '#10b981', '#06b6d4', '#f59e0b', '#ec4899']
        });
      } catch (e) {}
    }
  }, [isHighMastery]);

  // Circle meter calculations
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (pct / 100) * circumference;

  return (
    <div className="report-container">
      {/* Top Banner */}
      <div className="report-header glass-panel glass-panel-glow">
        <div className="report-header-left">
          <div className="report-badge">
            <Award size={18} className="text-indigo" />
            <span>AI PEDAGOGICAL MASTERY REPORT</span>
          </div>
          <h1 className="report-lesson-title">{report.title}</h1>
          <p className="report-summary-text">{report.summary_feedback}</p>
        </div>

        {/* Circular Score Gauge */}
        <div className="score-gauge-box">
          <svg className="gauge-svg" width="140" height="140" viewBox="0 0 140 140">
            {/* Background Track */}
            <circle
              cx="70"
              cy="70"
              r={radius}
              className="gauge-track"
              strokeWidth="10"
            />
            {/* Progress Arc */}
            <circle
              cx="70"
              cy="70"
              r={radius}
              className={`gauge-progress ${isHighMastery ? 'gauge-green' : 'gauge-indigo'}`}
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
            />
          </svg>
          <div className="gauge-inner-text">
            <span className="gauge-score-val">{pct}%</span>
            <span className="gauge-score-sub">{report.total_score}/{report.max_score} Correct</span>
          </div>
        </div>
      </div>

      {/* Grid: Strengths vs Weaknesses */}
      <div className="report-grid">
        {/* Concepts Mastered */}
        <div className="report-card glass-panel">
          <div className="card-heading text-emerald">
            <CheckCircle size={20} />
            <h3>Concepts Mastered</h3>
          </div>
          {report.concepts_understood && report.concepts_understood.length > 0 ? (
            <div className="concept-tags-list">
              {report.concepts_understood.map((c, i) => (
                <div key={i} className="concept-pill pill-success">
                  <span className="pill-check">✓</span>
                  <span>{c}</span>
                </div>
              ))}
            </div>
          ) : (
            <p className="empty-concept-text">Review foundational topics to strengthen core models.</p>
          )}
        </div>

        {/* Concepts Needing Review */}
        <div className="report-card glass-panel">
          <div className="card-heading text-amber">
            <AlertCircle size={20} />
            <h3>Focus Areas for Review</h3>
          </div>
          {report.weak_concepts && report.weak_concepts.length > 0 ? (
            <div className="concept-tags-list">
              {report.weak_concepts.map((w, i) => (
                <div key={i} className="concept-pill pill-warning">
                  <span className="pill-dot-amber"></span>
                  <span>{w}</span>
                </div>
              ))}
            </div>
          ) : (
            <div className="concept-pill pill-success">
              <span className="pill-check">✓</span>
              <span>All tested concepts demonstrated high fidelity!</span>
            </div>
          )}
        </div>
      </div>

      {/* Misconceptions Diagnosed & Remediated */}
      {report.misconceptions && report.misconceptions.length > 0 && (
        <div className="report-recs-card glass-panel" style={{ borderLeft: '4px solid #f59e0b' }}>
          <div className="card-heading text-amber">
            <AlertCircle size={20} />
            <h3>Misconceptions Diagnosed & Remediated During Lesson</h3>
          </div>
          <ul className="recs-list">
            {report.misconceptions.map((misc, i) => (
              <li key={i} className="rec-item">
                <span className="rec-num" style={{ background: '#78350f', color: '#fef3c7' }}>{i + 1}</span>
                <span className="rec-text">{misc}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Actionable Recommendations */}
      {report.recommendations && report.recommendations.length > 0 && (
        <div className="report-recs-card glass-panel">
          <div className="card-heading text-cyan">
            <Target size={20} />
            <h3>Personalized Learning Recommendations</h3>
          </div>
          <ul className="recs-list">
            {report.recommendations.map((rec, i) => (
              <li key={i} className="rec-item">
                <span className="rec-num">{i + 1}</span>
                <span className="rec-text">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Verified Grounded Sources */}
      {sources && sources.length > 0 && (
        <div className="report-recs-card glass-panel" style={{ borderLeft: '4px solid #06b6d4' }}>
          <div className="card-heading text-cyan">
            <BookOpen size={20} />
            <h3>Grounded Knowledge Sources ({sourceRoute === 'external_web' ? 'Live Web Retrieval' : 'Document Ingestion'})</h3>
          </div>
          <ul className="recs-list">
            {sources.map((s, i) => (
              <li key={i} className="rec-item" style={{ alignItems: 'flex-start' }}>
                <span className="rec-num" style={{ background: '#0e7490', color: '#cffafe' }}>{i + 1}</span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  {s.url ? (
                    <a
                      href={s.url}
                      target="_blank"
                      rel="noreferrer"
                      style={{ color: '#38bdf8', fontWeight: '600', textDecoration: 'none' }}
                    >
                      🔗 {s.title} ({s.source})
                    </a>
                  ) : (
                    <strong style={{ color: '#cbd5e1' }}>📄 {s.title} ({s.source})</strong>
                  )}
                  {s.snippet && (
                    <p style={{ margin: 0, fontSize: '0.8rem', color: '#94a3b8' }}>
                      "{s.snippet.length > 160 ? s.snippet.slice(0, 160) + '...' : s.snippet}"
                    </p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* 7-Day Master Study Roadmap */}
      {report.study_roadmap_7_days && report.study_roadmap_7_days.length > 0 && (
        <div className="report-recs-card glass-panel" style={{ borderLeft: '4px solid #8b5cf6' }}>
          <div className="card-heading text-indigo">
            <Sparkles size={20} />
            <h3>7-Day Structured Mastery Curriculum</h3>
          </div>
          <div className="roadmap-grid">
            {report.study_roadmap_7_days.map((dayPlan) => (
              <div key={dayPlan.day} className="roadmap-day-card">
                <div className="day-card-badge">Day {dayPlan.day} • {dayPlan.duration_minutes}m</div>
                <h4 className="day-card-title">{dayPlan.title}</h4>
                <div className="day-card-meta">
                  <p><strong>Practice:</strong> {dayPlan.practice_goals}</p>
                  <p><strong>Revision:</strong> {dayPlan.revision_schedule}</p>
                  <span className="day-check-tag">{dayPlan.assessment_type}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Hierarchical Learning Path Progression */}
      {report.learning_path && report.learning_path.length > 0 && (
        <div className="report-recs-card glass-panel" style={{ borderLeft: '4px solid #10b981' }}>
          <div className="card-heading text-emerald">
            <Compass size={20} />
            <h3>Longitudinal Mastery Learning Path</h3>
          </div>
          <div className="learning-path-stepper">
            {report.learning_path.map((node) => (
              <div key={node.step} className={`stepper-node ${node.status}`}>
                <div className="stepper-dot">
                  {node.status === 'completed' ? '✓' : node.step}
                </div>
                <div className="stepper-content">
                  <div className="stepper-title">{node.topic}</div>
                  <span className={`stepper-badge ${node.status}`}>
                    {node.status === 'completed' ? 'Mastered' : (node.status === 'current' ? 'In Progress' : 'Upcoming')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Next Recommended Topic Banner */}
      {report.next_recommended_topic && (
        <div className="next-topic-banner glass-panel glass-panel-glow">
          <div className="next-topic-info">
            <div className="next-topic-tag">
              <Compass size={16} className="text-indigo" />
              <span>Recommended Next Horizon:</span>
            </div>
            <h2 className="next-topic-title">{report.next_recommended_topic}</h2>
            <p className="next-topic-desc">
              Building directly on what you mastered today to deepen your conceptual framework.
            </p>
          </div>

          <button
            type="button"
            className="btn-primary-cta btn-launch-next"
            onClick={() => onStartNextTopic(report.next_recommended_topic)}
          >
            <span>Launch This Lesson</span>
            <ArrowRight size={20} />
          </button>
        </div>
      )}

      {/* Bottom Actions */}
      <div className="report-actions-bar">
        <button type="button" className="btn-secondary" onClick={onResetLesson}>
          <RotateCcw size={18} />
          <span>Explore Another Topic or PDF</span>
        </button>
      </div>
    </div>
  );
}
