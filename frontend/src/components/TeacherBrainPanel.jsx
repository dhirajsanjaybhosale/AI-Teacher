import React, { useState } from 'react';
import { Brain, ChevronDown, ChevronUp, AlertTriangle, CheckCircle, Lightbulb, Compass, Zap, ShieldAlert } from 'lucide-react';

export default function TeacherBrainPanel({ telemetry, retrievalConfidence, retrievalWarning }) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!telemetry && !retrievalWarning) {
    return null;
  }

  const isHealthy = telemetry?.understanding_state === 'High';

  return (
    <div className={`teacher-brain-container ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="teacher-brain-header" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="brain-header-left">
          <div className={`brain-pulse-icon ${isHealthy ? 'healthy' : 'adapting'}`}>
            <Brain size={18} />
          </div>
          <div className="brain-header-title">
            <span className="brain-title-text">Teacher Brain Telemetry</span>
            <span className={`status-badge-mini ${isHealthy ? 'badge-success' : 'badge-warning'}`}>
              {telemetry?.teaching_strategy || 'Analyzing Cognitive State'}
            </span>
          </div>
        </div>

        <div className="brain-header-right">
          <span className="brain-toggle-label">{isExpanded ? 'Hide Diagnostics' : 'Inspect Brain'}</span>
          {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </div>
      </div>

      {isExpanded && (
        <div className="teacher-brain-body">
          <div className="telemetry-grid">
            <div className="telemetry-card">
              <div className="telemetry-card-title">
                <Compass size={14} className="text-cyan" />
                <span>Learner Level</span>
              </div>
              <div className="telemetry-card-val">{telemetry?.learner_level || 'Beginner'}</div>
            </div>

            <div className="telemetry-card">
              <div className="telemetry-card-title">
                <Zap size={14} className="text-amber" />
                <span>Current Concept</span>
              </div>
              <div className="telemetry-card-val">{telemetry?.current_concept || 'Foundations'}</div>
            </div>

            <div className="telemetry-card">
              <div className="telemetry-card-title">
                {isHealthy ? <CheckCircle size={14} className="text-emerald" /> : <AlertTriangle size={14} className="text-amber" />}
                <span>Understanding State</span>
              </div>
              <div className={`telemetry-card-val ${isHealthy ? 'text-emerald' : 'text-amber'}`}>
                {telemetry?.understanding_state || 'Nominal'}
              </div>
            </div>

            <div className="telemetry-card">
              <div className="telemetry-card-title">
                <Lightbulb size={14} className="text-indigo" />
                <span>Adapted Strategy</span>
              </div>
              <div className="telemetry-card-val highlight-cyan">
                {telemetry?.teaching_strategy || 'Standard Presentation'}
              </div>
            </div>
          </div>

          {telemetry?.detected_misconception && telemetry.detected_misconception !== 'None (Concept sound)' && (
            <div className="misconception-callout">
              <div className="callout-header">
                <ShieldAlert size={16} className="text-amber" />
                <span className="callout-title">Diagnosed Mental Model Divergence</span>
              </div>
              <p className="callout-body">{telemetry.detected_misconception}</p>
            </div>
          )}

          {retrievalWarning && (
            <div className="retrieval-warning-callout">
              <AlertTriangle size={15} className="text-amber" />
              <span>{retrievalWarning}</span>
            </div>
          )}

          <div className="next-action-strip">
            <span className="action-tag">Next Teacher Action</span>
            <span className="action-desc">{telemetry?.next_action || 'Present core concept video and offer interactive follow-up.'}</span>
          </div>
        </div>
      )}
    </div>
  );
}
