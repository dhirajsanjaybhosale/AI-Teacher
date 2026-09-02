import React, { useState } from 'react';
import { CalendarDays, Clock, CheckCircle2, Circle, Sparkles, ArrowRight, Save } from 'lucide-react';

export default function StudyPlanView({ studentProfile, onUpdateStudyPlan, onStartTopic }) {
  const [studyPlan, setStudyPlan] = useState(
    studentProfile?.study_plan || [
      { day_name: 'Monday', topic: 'Graphs Revision & Representation', duration_minutes: 30, is_completed: true },
      { day_name: 'Tuesday', topic: 'Breadth-First Search (BFS) Traversal', duration_minutes: 40, is_completed: true },
      { day_name: 'Wednesday', topic: 'Depth-First Search (DFS) & Call Stack', duration_minutes: 40, is_completed: true },
      { day_name: 'Thursday', topic: 'Binary Search Boundary Conditions', duration_minutes: 30, is_completed: false },
      { day_name: 'Friday', topic: 'DBMS B-Tree Indexing Deep Dive', duration_minutes: 45, is_completed: false },
      { day_name: 'Saturday', topic: 'Operating Systems Paging & Virtual Memory', duration_minutes: 45, is_completed: false },
      { day_name: 'Sunday', topic: 'Full Conceptual Revision & Mastery Assessment', duration_minutes: 60, is_completed: false },
    ]
  );

  const [examDate, setExamDate] = useState('2026-11-15');
  const [dailyTargetMins, setDailyTargetMins] = useState(60);

  const toggleDayCompletion = (idx) => {
    const next = [...studyPlan];
    next[idx].is_completed = !next[idx].is_completed;
    setStudyPlan(next);
    onUpdateStudyPlan?.(next);
  };

  const completedCount = studyPlan.filter((d) => d.is_completed).length;

  return (
    <div className="study-plan-page-container">
      {/* Page Header */}
      <div className="page-title-banner">
        <h1 className="page-main-heading">My Adaptive Study Plan</h1>
        <p className="page-sub-heading">
          Structured 7-day learning schedule dynamically tuned to your available time and semester exams.
        </p>
      </div>

      {/* Plan Parameters Card */}
      <div className="study-plan-config-card glass-panel">
        <div className="config-grid">
          <div className="config-item">
            <label>Target Exam Date</label>
            <input
              type="date"
              value={examDate}
              onChange={(e) => setExamDate(e.target.value)}
              className="config-input"
            />
          </div>
          <div className="config-item">
            <label>Daily Study Target</label>
            <select
              value={dailyTargetMins}
              onChange={(e) => setDailyTargetMins(Number(e.target.value))}
              className="config-select"
            >
              <option value={30}>30 minutes / day</option>
              <option value={45}>45 minutes / day</option>
              <option value={60}>60 minutes / day</option>
              <option value={90}>90 minutes / day</option>
            </select>
          </div>
          <div className="config-item-summary">
            <span className="summary-label">Week Completion</span>
            <span className="summary-val">{completedCount} / {studyPlan.length} Days Done</span>
          </div>
        </div>
      </div>

      {/* Weekly Schedule Days List */}
      <div className="study-plan-days-list">
        {studyPlan.map((day, idx) => (
          <div
            key={idx}
            className={`plan-day-card glass-panel ${day.is_completed ? 'completed' : ''}`}
          >
            <button
              type="button"
              className="day-check-btn"
              onClick={() => toggleDayCompletion(idx)}
              title={day.is_completed ? 'Mark pending' : 'Mark completed'}
            >
              {day.is_completed ? (
                <CheckCircle2 size={22} className="text-emerald" />
              ) : (
                <Circle size={22} className="text-muted" />
              )}
            </button>

            <div className="day-meta-col">
              <span className="day-name">{day.day_name}</span>
              <span className="day-duration"><Clock size={13} /> {day.duration_minutes} min</span>
            </div>

            <div className="day-topic-col">
              <h4 className="day-topic-title">{day.topic}</h4>
            </div>

            <div className="day-action-col">
              <button
                type="button"
                className={day.is_completed ? 'btn-secondary-light' : 'btn-primary-gradient'}
                onClick={() => onStartTopic?.(day.topic)}
              >
                <span>{day.is_completed ? 'Revise' : 'Start Day'}</span>
                <ArrowRight size={14} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
