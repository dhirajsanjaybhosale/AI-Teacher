import React from 'react';
import {
  BookOpen,
  CheckCircle2,
  Clock,
  Globe,
  Layers,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  FileText,
  Zap,
  Play
} from 'lucide-react';

export default function LessonPlanReviewModal({
  lessonPlan,
  onStartLesson,
  onClose
}) {
  if (!lessonPlan) return null;

  const title = lessonPlan.title || "Personalized Masterclass";
  const level = (lessonPlan.target_level || "intermediate").toUpperCase();
  const language = (lessonPlan.target_language || "English").toUpperCase();
  const estimatedMins = lessonPlan.estimated_minutes || 10;
  const segments = lessonPlan.segments || [];
  const objectives = lessonPlan.learning_objectives || [
    `Master the foundational principles of ${title}`,
    "Analyze dynamic visual demonstration on the smartboard",
    "Verify conceptual intuition with live interactive checkpoints"
  ];
  const groundedNotice = lessonPlan.grounded_source_display || (
    lessonPlan.source_name && lessonPlan.source_type !== 'topic'
      ? `✓ Lesson grounded in ${lessonPlan.source_name}`
      : "✓ Personalized for your learning level"
  );

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(10, 15, 29, 0.85)',
        backdropFilter: 'blur(8px)',
        zIndex: 9999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '780px',
          maxHeight: '90vh',
          overflowY: 'auto',
          borderRadius: '18px',
          border: '1px solid rgba(99, 102, 241, 0.35)',
          boxShadow: '0 25px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(99, 102, 241, 0.15)',
          background: 'linear-gradient(135deg, rgba(17, 24, 39, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%)',
          color: '#f8fafc',
          padding: '32px'
        }}
      >
        {/* Top Header Badge */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '6px',
                padding: '4px 12px',
                borderRadius: '20px',
                background: 'rgba(99, 102, 241, 0.2)',
                border: '1px solid rgba(99, 102, 241, 0.4)',
                fontSize: '0.75rem',
                fontWeight: '600',
                color: '#a5b4fc',
                letterSpacing: '0.05em'
              }}
            >
              <Sparkles size={13} className="text-primary" />
              PERSONALIZED LESSON PLAN
            </span>
          </div>

          <button
            type="button"
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#94a3b8',
              cursor: 'pointer',
              fontSize: '1.2rem'
            }}
          >
            ✕
          </button>
        </div>

        {/* Lesson Title */}
        <h2 style={{ fontSize: '1.65rem', fontWeight: '700', marginBottom: '10px', color: '#f8fafc', lineHeight: 1.3 }}>
          {title}
        </h2>

        {/* Key Lesson Metadata Badges */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px', marginBottom: '20px' }}>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 10px', borderRadius: '6px', background: 'rgba(30, 41, 59, 0.8)', fontSize: '0.80rem', color: '#cbd5e1' }}>
            <Layers size={14} className="text-indigo" /> {level} LEVEL
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 10px', borderRadius: '6px', background: 'rgba(30, 41, 59, 0.8)', fontSize: '0.80rem', color: '#cbd5e1' }}>
            <Clock size={14} className="text-primary" /> {estimatedMins} MINUTES ALLOCATED
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 10px', borderRadius: '6px', background: 'rgba(30, 41, 59, 0.8)', fontSize: '0.80rem', color: '#cbd5e1' }}>
            <Globe size={14} className="text-emerald" /> {language}
          </span>
          <span style={{ display: 'flex', alignItems: 'center', gap: '5px', padding: '4px 10px', borderRadius: '6px', background: 'rgba(30, 41, 59, 0.8)', fontSize: '0.80rem', color: '#cbd5e1' }}>
            <Zap size={14} className="text-amber" /> {segments.length} INTERACTIVE MODULES
          </span>
        </div>

        {/* Grounding Notice Banner */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            padding: '12px 16px',
            borderRadius: '10px',
            background: 'rgba(16, 185, 129, 0.12)',
            border: '1px solid rgba(16, 185, 129, 0.3)',
            marginBottom: '24px'
          }}
        >
          <ShieldCheck size={18} className="text-emerald" style={{ flexShrink: 0 }} />
          <span style={{ fontSize: '0.88rem', fontWeight: '500', color: '#6ee7b7' }}>
            {groundedNotice}
          </span>
        </div>

        {/* Section 1: What You'll Learn */}
        <div style={{ marginBottom: '24px' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: '600', color: '#cbd5e1', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span>🎯</span> What you'll learn in this masterclass:
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {objectives.map((obj, i) => (
              <div
                key={i}
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '10px',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'rgba(30, 41, 59, 0.4)'
                }}
              >
                <CheckCircle2 size={16} className="text-emerald" style={{ marginTop: '2px', flexShrink: 0 }} />
                <span style={{ fontSize: '0.88rem', color: '#e2e8f0', lineHeight: 1.4 }}>{obj}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Section 2: Lesson Modules with Allocated Timing */}
        <div style={{ marginBottom: '28px' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: '600', color: '#cbd5e1', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span>📚</span> Structured Lesson Curriculum:
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {segments.map((seg, idx) => {
              const allocatedSec = seg.actual_seconds || seg.target_seconds || 120;
              const mins = Math.max(1, Math.round(allocatedSec / 60));
              const visualType = (seg.visual_diagram_type || "Smartboard").toUpperCase();
              return (
                <div
                  key={idx}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 16px',
                    borderRadius: '10px',
                    background: 'rgba(30, 41, 59, 0.6)',
                    border: '1px solid rgba(255, 255, 255, 0.07)'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div
                      style={{
                        width: '32px',
                        height: '32px',
                        borderRadius: '8px',
                        background: 'rgba(99, 102, 241, 0.25)',
                        color: '#a5b4fc',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontWeight: '700',
                        fontSize: '0.85rem'
                      }}
                    >
                      {idx + 1}
                    </div>
                    <div>
                      <div style={{ fontSize: '0.92rem', fontWeight: '600', color: '#f1f5f9' }}>
                        {seg.title}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: '#94a3b8', marginTop: '2px' }}>
                        Visual: {visualType} • Formative Interactive Check Included
                      </div>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span
                      style={{
                        padding: '4px 10px',
                        borderRadius: '6px',
                        background: 'rgba(99, 102, 241, 0.15)',
                        color: '#c7d2fe',
                        fontSize: '0.78rem',
                        fontWeight: '600'
                      }}
                    >
                      ~{mins} min
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Action CTA Button */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
          <button
            type="button"
            onClick={onClose}
            className="btn-secondary"
            style={{ padding: '12px 20px', borderRadius: '10px' }}
          >
            Back to Topics
          </button>
          <button
            type="button"
            onClick={onStartLesson}
            className="btn-primary-gradient"
            style={{
              padding: '12px 28px',
              borderRadius: '10px',
              fontWeight: '600',
              fontSize: '0.95rem',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '8px',
              cursor: 'pointer'
            }}
          >
            <Play size={18} fill="white" />
            <span>Start Lesson</span>
            <ArrowRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
}
