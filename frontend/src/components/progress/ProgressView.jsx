import React from 'react';
import { TrendingUp, Award, Clock, Flame, BookOpen, CheckCircle, BarChart2 } from 'lucide-react';

export default function ProgressView({ studentProfile, onStartTopic }) {
  const overallMastery = studentProfile?.overall_mastery || 78;
  const quizAverage = studentProfile?.quiz_average || 86;
  const lessonsCompleted = studentProfile?.lessons_completed || 24;
  const hoursLearned = studentProfile?.hours_learned || 38;
  const streakDays = studentProfile?.learning_streak_days || 7;

  const subjects = studentProfile?.subjects_mastery || [];
  const recentQuizScores = studentProfile?.learning_history?.slice(0, 5) || [];

  return (
    <div className="progress-page-container">
      {/* Page Header */}
      <div className="page-title-banner">
        <h1 className="page-main-heading">My Learning Progress</h1>
        <p className="page-sub-heading">Track your cognitive mastery, streak consistency, and quiz performance over time.</p>
      </div>

      {/* Top Metrics Cards */}
      <div className="progress-quad-row">
        <div className="stat-glass-card">
          <span className="stat-card-title">Overall Mastery</span>
          <div className="circular-meter-wrap">
            <span className="huge-meter-val text-primary">{overallMastery}%</span>
          </div>
          <span className="stat-card-footer text-emerald">↑ +4% improvement this week</span>
        </div>

        <div className="stat-glass-card">
          <span className="stat-card-title">Quiz Average</span>
          <div className="circular-meter-wrap">
            <span className="huge-meter-val text-cyan">{quizAverage}%</span>
          </div>
          <span className="stat-card-footer text-cyan">Across {recentQuizScores.length} recent assessments</span>
        </div>

        <div className="stat-glass-card">
          <span className="stat-card-title">Lessons Completed</span>
          <div className="circular-meter-wrap">
            <span className="huge-meter-val text-indigo">{lessonsCompleted}</span>
          </div>
          <span className="stat-card-footer text-indigo">{hoursLearned} total hours learned</span>
        </div>

        <div className="stat-glass-card">
          <span className="stat-card-title">Learning Streak</span>
          <div className="circular-meter-wrap">
            <span className="huge-meter-val text-orange">🔥 {streakDays}d</span>
          </div>
          <span className="stat-card-footer text-amber">Active daily learner</span>
        </div>
      </div>

      {/* Subject-by-Subject Mastery Breakdown */}
      <div className="progress-section-card glass-panel">
        <div className="card-header-simple">
          <BarChart2 size={20} className="text-primary" />
          <h3>Subject Mastery Breakdown</h3>
        </div>

        <div className="subjects-progress-list">
          {subjects.map((sub, i) => (
            <div key={i} className="subject-progress-row">
              <div className="sub-row-header">
                <span className="sub-row-name">{sub.subject}</span>
                <span className="sub-row-pct">{sub.overall_percentage}%</span>
              </div>
              <div className="progress-bar-track">
                <div
                  className="progress-bar-fill fill-primary"
                  style={{ width: `${sub.overall_percentage}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quiz Performance History */}
      <div className="progress-section-card glass-panel">
        <div className="card-header-simple">
          <Award size={20} className="text-amber" />
          <h3>Recent Quiz Performance</h3>
        </div>

        <div className="quiz-history-grid">
          {recentQuizScores.map((q, idx) => (
            <div key={idx} className="quiz-stat-box" onClick={() => onStartTopic?.(q.topic)} style={{ cursor: 'pointer' }}>
              <div className="q-box-top">
                <span className="q-box-topic">{q.topic}</span>
                <span className="score-chip">{q.quiz_score_percentage}%</span>
              </div>
              <div className="q-box-bottom">
                <span>{q.date}</span>
                <span className="text-emerald font-semibold">{q.mastery_delta}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
