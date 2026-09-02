import React, { useState } from 'react';
import {
  Play,
  Sparkles,
  Flame,
  Clock,
  Target,
  Award,
  BookOpen,
  ArrowRight,
  TrendingUp,
  AlertCircle,
  HelpCircle,
  CheckCircle2
} from 'lucide-react';

export default function StudentDashboard({
  studentProfile,
  onStartTopic,
  onContinueLesson,
  onOpenTopicImprovement
}) {
  const [showReasonModal, setShowReasonModal] = useState(false);

  const studentName = studentProfile?.personal_info?.full_name?.split(' ')[0] || 'Dhiraj';
  const continueTopic = studentProfile?.continue_learning_topic || 'Binary Search';
  const continueProgress = studentProfile?.continue_learning_progress || 68;
  const continueTimeRemaining = studentProfile?.continue_learning_time_remaining || 12;

  const aiRec = studentProfile?.ai_recommendation || 'Revise Graph Representation before starting DFS.';
  const aiReason = studentProfile?.ai_recommendation_reason || 'You had difficulty with graph representation in your last lesson.';
  const aiRecTopic = studentProfile?.ai_recommendation_topic || 'Graph Representation';

  const todayGoalDone = studentProfile?.today_goal_completed || 3;
  const todayGoalTotal = studentProfile?.today_goal_total || 4;
  const todayGoalPct = Math.round((todayGoalDone / todayGoalTotal) * 100);
  const studyTimeMins = studentProfile?.today_study_time_minutes || 42;
  const targetTimeMins = studentProfile?.learning_profile?.daily_study_time_minutes || 60;
  const streakDays = studentProfile?.learning_streak_days || 7;

  // Strengths list
  const strengths = [
    { name: 'Arrays & Strings', score: 92, subject: 'Data Structures' },
    { name: 'SQL & Queries', score: 88, subject: 'DBMS' },
    { name: 'OOP Principles', score: 84, subject: 'Programming' },
    { name: 'React Hooks', score: 81, subject: 'Programming' },
  ];

  // Topics to improve list
  const improveTopics = [
    { name: 'Graph Traversal', score: 48, subject: 'Data Structures' },
    { name: 'Dynamic Programming', score: 52, subject: 'Data Structures' },
    { name: 'Memory Management', score: 61, subject: 'Operating Systems' },
  ];

  // Recent learning history
  const recentLessons = studentProfile?.learning_history?.slice(0, 3) || [
    { topic: 'Binary Search', date: 'Today', duration_minutes: 20, quiz_score_percentage: 90 },
    { topic: 'DBMS Normalization', date: 'Yesterday', duration_minutes: 30, quiz_score_percentage: 82 },
    { topic: 'React Hooks', date: '2 days ago', duration_minutes: 20, quiz_score_percentage: 94 },
  ];

  return (
    <div className="dashboard-page-container">
      {/* Welcome Greeting Banner */}
      <section className="dashboard-greeting-section">
        <div className="greeting-content">
          <h1 className="greeting-title">Good evening, {studentName} 👋</h1>
          <p className="greeting-subtitle">Let's continue your personalized learning journey.</p>
        </div>
      </section>

      {/* Top Prominent Row: Continue Learning & AI Recommendation */}
      <section className="dashboard-hero-grid">
        {/* Continue Learning Card */}
        <div className="dashboard-card continue-learning-card">
          <div className="card-top-tag">
            <span className="live-dot" />
            <span>CONTINUE LEARNING</span>
          </div>
          <h2 className="continue-topic-title">{continueTopic}</h2>
          <p className="continue-topic-sub">Continue where you left off in your classroom session.</p>

          <div className="continue-progress-row">
            <div className="progress-info-labels">
              <span>Progress: <strong>{continueProgress}%</strong></span>
              <span className="time-rem"><Clock size={13} /> {continueTimeRemaining} min left</span>
            </div>
            <div className="progress-bar-track">
              <div className="progress-bar-fill" style={{ width: `${continueProgress}%` }} />
            </div>
          </div>

          <button
            type="button"
            className="btn-primary-gradient"
            onClick={() => onContinueLesson?.(continueTopic)}
          >
            <Play size={16} fill="currentColor" />
            <span>Continue Lesson</span>
          </button>
        </div>

        {/* AI Teacher Recommendation Card */}
        <div className="dashboard-card ai-recommendation-card">
          <div className="rec-header">
            <div className="rec-badge">
              <Sparkles size={16} className="text-amber" />
              <span>AI TEACHER RECOMMENDATION</span>
            </div>
          </div>

          <h3 className="rec-headline">{aiRec}</h3>
          <p className="rec-reason">“{aiReason}”</p>

          <div className="rec-actions-row">
            <button
              type="button"
              className="btn-amber-action"
              onClick={() => onStartTopic?.(aiRecTopic)}
            >
              <span>Start Revision</span>
              <ArrowRight size={15} />
            </button>

            <button
              type="button"
              className="btn-text-ghost"
              onClick={() => setShowReasonModal(!showReasonModal)}
            >
              <HelpCircle size={14} />
              <span>Why this recommendation?</span>
            </button>
          </div>

          {showReasonModal && (
            <div className="rec-modal-popover">
              <p>
                <strong>AI Pedagogical Diagnosis:</strong> During your recent session, you answered
                a conceptual question about graph storage incorrectly. Reviewing adjacency lists
                before DFS will ensure maximum concept retention and quiz mastery.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Today's Goal & Quick Stats */}
      <section className="dashboard-stats-grid">
        {/* Today's Learning Goal */}
        <div className="dashboard-card goal-card">
          <div className="card-header-simple">
            <Target size={18} className="text-primary" />
            <h4>Today's Learning Goal</h4>
          </div>
          <div className="goal-metric-row">
            <span className="goal-main-num">{todayGoalDone} / {todayGoalTotal}</span>
            <span className="goal-sub-text">completed today</span>
          </div>

          <div className="goal-progress-wrap">
            <div className="progress-bar-track">
              <div className="progress-bar-fill" style={{ width: `${todayGoalPct}%` }} />
            </div>
            <div className="goal-meta-row">
              <span>Study Time: <strong>{studyTimeMins}m / {targetTimeMins}m</strong></span>
              <span className="streak-badge"><Flame size={14} className="text-orange" /> {streakDays} days streak</span>
            </div>
          </div>

          <button
            type="button"
            className="btn-secondary-light"
            onClick={() => onContinueLesson?.(continueTopic)}
          >
            <span>Continue Learning</span>
            <ArrowRight size={14} />
          </button>
        </div>

        {/* 4 Clean Quick Stats Cards */}
        <div className="stats-quad-grid">
          <div className="stat-card">
            <span className="stat-label">Overall Mastery</span>
            <span className="stat-value">{studentProfile?.overall_mastery || 78}%</span>
            <span className="stat-hint text-emerald">↑ +4% this week</span>
          </div>

          <div className="stat-card">
            <span className="stat-label">Quiz Average</span>
            <span className="stat-value">{studentProfile?.quiz_average || 86}%</span>
            <span className="stat-hint text-cyan">Across all sessions</span>
          </div>

          <div className="stat-card">
            <span className="stat-label">Lessons Completed</span>
            <span className="stat-value">{studentProfile?.lessons_completed || 24}</span>
            <span className="stat-hint text-indigo">38 hours learned</span>
          </div>

          <div className="stat-card">
            <span className="stat-label">Learning Streak</span>
            <span className="stat-value text-orange"><Flame size={20} className="inline-icon" /> {streakDays} Days</span>
            <span className="stat-hint text-amber">Active daily learner</span>
          </div>
        </div>
      </section>

      {/* Lower Section: Strengths, Topics to Improve, Recent Learning */}
      <section className="dashboard-tri-grid">
        {/* My Strengths */}
        <div className="dashboard-card strengths-card">
          <div className="card-header-simple">
            <Award size={18} className="text-emerald" />
            <h4>Your Strengths</h4>
          </div>
          <div className="strengths-list">
            {strengths.map((item, idx) => (
              <div key={idx} className="strength-item">
                <div className="strength-info">
                  <span className="strength-name">{item.name}</span>
                  <span className="strength-sub">{item.subject}</span>
                </div>
                <span className="strength-pct">{item.score}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Topics to Improve */}
        <div className="dashboard-card improve-card">
          <div className="card-header-simple">
            <AlertCircle size={18} className="text-amber" />
            <h4>Topics to Improve</h4>
          </div>
          <div className="improve-list">
            {improveTopics.map((item, idx) => (
              <div key={idx} className="improve-item">
                <div className="improve-info">
                  <span className="improve-name">{item.name}</span>
                  <span className="improve-score">{item.score}% mastery</span>
                </div>
                <div className="improve-actions">
                  <button
                    type="button"
                    className="btn-chip-action"
                    onClick={() => onStartTopic?.(item.name)}
                  >
                    Practice
                  </button>
                  <button
                    type="button"
                    className="btn-chip-action btn-chip-revise"
                    onClick={() => onStartTopic?.(item.name)}
                  >
                    Revise
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Learning */}
        <div className="dashboard-card recent-card">
          <div className="card-header-simple">
            <BookOpen size={18} className="text-indigo" />
            <h4>Recent Learning</h4>
          </div>
          <div className="recent-list">
            {recentLessons.map((item, idx) => (
              <div
                key={idx}
                className="recent-item"
                onClick={() => onStartTopic?.(item.topic)}
                title={`Review ${item.topic}`}
              >
                <div className="recent-left">
                  <span className="recent-topic">{item.topic}</span>
                  <span className="recent-meta">{item.date} • {item.duration_minutes} min</span>
                </div>
                <div className="recent-score-badge">
                  <span>Quiz {item.quiz_score_percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
