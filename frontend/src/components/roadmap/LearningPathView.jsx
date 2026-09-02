import React from 'react';
import { Milestone, CheckCircle2, Play, Lock, ArrowRight, Sparkles } from 'lucide-react';

export default function LearningPathView({ studentProfile, onStartTopic }) {
  const learningPath = studentProfile?.learning_path || [
    { id: 1, name: 'Programming Fundamentals', status: 'completed', topics_count: 8 },
    { id: 2, name: 'OOP Principles', status: 'completed', topics_count: 6 },
    { id: 3, name: 'Arrays & Strings', status: 'completed', topics_count: 10 },
    { id: 4, name: 'Linked Lists & Stacks', status: 'completed', topics_count: 7 },
    { id: 5, name: 'Binary Trees & BST', status: 'current', topics_count: 9 },
    { id: 6, name: 'Graphs & Traversals', status: 'locked', topics_count: 8 },
    { id: 7, name: 'Dynamic Programming & Advanced Algorithms', status: 'locked', topics_count: 12 }
  ];

  const currentTopic = learningPath.find((t) => t.status === 'current') || learningPath[4];

  return (
    <div className="learning-path-page-container">
      {/* Page Header */}
      <div className="page-title-banner">
        <h1 className="page-main-heading">Structured Learning Path</h1>
        <p className="page-sub-heading">
          A pedagogical sequence tailored to your B.Tech curriculum and goal of <strong>Exam Preparation</strong>.
        </p>
      </div>

      {/* AI Next Topic Banner */}
      <div className="path-ai-banner glass-panel">
        <div className="banner-left">
          <div className="banner-tag">
            <Sparkles size={14} className="text-amber" />
            <span>NEXT RECOMMENDED MILESTONE</span>
          </div>
          <h3>{currentTopic.name}</h3>
          <p>You have mastered foundational data structures. Dive into hierarchical trees and search trees.</p>
        </div>
        <button
          type="button"
          className="btn-primary-gradient"
          onClick={() => onStartTopic?.(currentTopic.name)}
        >
          <span>Start Milestone</span>
          <ArrowRight size={16} />
        </button>
      </div>

      {/* Visual Step Roadmap */}
      <div className="path-roadmap-list">
        {learningPath.map((step, idx) => {
          const isCompleted = step.status === 'completed';
          const isCurrent = step.status === 'current';
          const isLocked = step.status === 'locked';

          return (
            <div key={step.id} className={`roadmap-step-card ${step.status} glass-panel`}>
              <div className="step-num-col">
                <div className={`step-badge-circle ${step.status}`}>
                  {isCompleted && <CheckCircle2 size={18} />}
                  {isCurrent && <Play size={16} fill="currentColor" />}
                  {isLocked && <Lock size={16} />}
                </div>
                {idx < learningPath.length - 1 && <div className="step-connector-line" />}
              </div>

              <div className="step-info-col">
                <div className="step-meta-row">
                  <span className="step-number-tag">Stage 0{step.id}</span>
                  <span className={`step-status-chip chip-${step.status}`}>
                    {isCompleted ? '✓ Completed' : isCurrent ? '▶ Active Milestone' : '🔒 Prerequisite Required'}
                  </span>
                </div>
                <h4 className="step-title">{step.name}</h4>
                <p className="step-sub">{step.topics_count} core pedagogical modules</p>
              </div>

              <div className="step-action-col">
                {isCurrent && (
                  <button
                    type="button"
                    className="btn-primary-gradient"
                    onClick={() => onStartTopic?.(step.name)}
                  >
                    <span>Continue Stage</span>
                    <ArrowRight size={15} />
                  </button>
                )}
                {isCompleted && (
                  <button
                    type="button"
                    className="btn-secondary-light"
                    onClick={() => onStartTopic?.(step.name)}
                  >
                    <span>Revise Stage</span>
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
