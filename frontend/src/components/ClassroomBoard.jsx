import React from 'react';
import {
  BookOpen,
  Sparkles,
  Layers,
  Code,
  Cpu,
  Activity,
  Lightbulb,
  ArrowRight,
  Check,
  Terminal,
  Calculator,
  Compass,
  MapPin,
  Calendar,
  CheckCircle2
} from 'lucide-react';

export default function ClassroomBoard({
  segment,
  lessonTitle = "AI Classroom",
  subject = "General",
  isRemediation = false,
  highlightFocus = false
}) {
  if (!segment) return null;

  const visualType = (segment.visual_diagram_type || "process").toLowerCase();
  const mathOrCode = segment.visual_code_or_math || segment.visual_description || "";
  const whiteboard = segment.whiteboard_data || {};
  const domain = (whiteboard.domain || (
    subject.toLowerCase().includes("prog") || subject.toLowerCase().includes("code") || subject.toLowerCase().includes("python") || subject.toLowerCase().includes("react") ? "programming" :
    subject.toLowerCase().includes("math") || subject.toLowerCase().includes("calc") ? "mathematics" :
    subject.toLowerCase().includes("physic") || subject.toLowerCase().includes("electr") ? "physics" :
    subject.toLowerCase().includes("bio") ? "biology" :
    subject.toLowerCase().includes("history") ? "history" : "general"
  )).toLowerCase();

  const keyPoints = segment.key_points && segment.key_points.length > 0
    ? segment.key_points
    : ["Master core mechanism", "Identify governing laws & relationships", "Apply intuitive practical analogy"];

  // Subject icon helper
  const getSubjectIcon = () => {
    if (domain === "programming") return "💻";
    if (domain === "mathematics") return "📐";
    if (domain === "physics") return "⚡";
    if (domain === "biology") return "🧬";
    if (domain === "history") return "🏛️";
    return "🎓";
  };

  return (
    <div className={`classroom-board-card glass-panel ${isRemediation ? 'board-remediation-glow' : 'board-classroom-glow'} ${highlightFocus ? 'board-pointer-active' : ''}`}>
      {/* Board Top Header Frame */}
      <div className="board-top-frame">
        <div className="board-subject-tag">
          <span className="subject-icon">{getSubjectIcon()}</span>
          <span className="subject-name">{domain.toUpperCase()} SMART WHITEBOARD</span>
          {isRemediation && (
            <span className="remediation-pill">🔄 ADAPTIVE RE-EXPLANATION</span>
          )}
        </div>
        <div className="board-meta">
          <span className="board-lesson-name">{lessonTitle}</span>
        </div>
      </div>

      {/* Main Concept Title */}
      <div className="board-title-section">
        <h3 className="board-concept-title">{segment.title}</h3>
        <div className="board-type-chip">
          <Layers size={13} />
          <span>{domain.toUpperCase()} ARCHITECTURE</span>
        </div>
      </div>

      {/* Dynamic Domain-Tailored Smartboard Canvas */}
      <div className="board-visual-container">
        {/* DOMAIN 1: PROGRAMMING (Code -> Execution Flow -> Output) */}
        {domain === "programming" && (
          <div className="board-programming-suite" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {/* 1. Code Editor View */}
            <div className="board-code-card" style={{ background: '#0b0f19', border: '1px solid #334155', borderRadius: '10px', padding: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px', borderBottom: '1px solid #1e293b', paddingBottom: '6px' }}>
                <span style={{ fontSize: '0.78rem', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '600' }}>
                  <Code size={14} /> SOURCE IMPLEMENTATION
                </span>
                <span style={{ fontSize: '0.70rem', color: '#64748b' }}>UTF-8 • Strict Mode</span>
              </div>
              <pre style={{ margin: 0, fontSize: '0.84rem', color: '#e2e8f0', fontFamily: 'monospace', lineHeight: 1.45, overflowX: 'auto' }}>
                <code>{whiteboard.code || mathOrCode || "// Core Algorithm Execution\nfunction process() {\n  return executeDeterministicStep();\n}"}</code>
              </pre>
            </div>

            {/* 2. Step-by-Step Execution Sequence */}
            {whiteboard.execution && whiteboard.execution.length > 0 && (
              <div style={{ background: 'rgba(30, 41, 59, 0.7)', borderRadius: '8px', padding: '10px 14px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#a5b4fc', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                  <Activity size={13} /> STEP-BY-STEP EXECUTION TRACE:
                </span>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  {whiteboard.execution.map((step, sIdx) => (
                    <div key={sIdx} style={{ fontSize: '0.80rem', color: '#cbd5e1', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ color: '#6366f1', fontWeight: 'bold' }}>{sIdx + 1}.</span>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 3. Terminal / Console Output */}
            {whiteboard.output && (
              <div style={{ background: '#020617', borderRadius: '8px', padding: '8px 12px', border: '1px solid #1e293b' }}>
                <span style={{ fontSize: '0.72rem', color: '#10b981', display: 'flex', alignItems: 'center', gap: '6px', fontWeight: '600', marginBottom: '4px' }}>
                  <Terminal size={12} /> CONSOLE OUTPUT
                </span>
                <div style={{ fontFamily: 'monospace', fontSize: '0.80rem', color: '#4ade80' }}>
                  $ {whiteboard.output}
                </div>
              </div>
            )}
          </div>
        )}

        {/* DOMAIN 2: MATHEMATICS (Equation -> Steps -> Graph -> Answer) */}
        {domain === "mathematics" && (
          <div className="board-math-suite" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="board-equation-card" style={{ background: '#0f172a', border: '1px solid #6366f1', borderRadius: '10px', padding: '14px' }}>
              <div style={{ fontSize: '0.75rem', color: '#a5b4fc', fontWeight: '700', marginBottom: '6px', letterSpacing: '0.05em' }}>
                MATHEMATICAL FORMULATION
              </div>
              <div style={{ fontSize: '1.2rem', fontFamily: 'serif', color: '#f8fafc', padding: '8px 0' }}>
                <code>{whiteboard.equation || mathOrCode || "f(x) = ∑ [ a_n * x^n ]"}</code>
              </div>
            </div>

            {whiteboard.steps && (
              <div style={{ background: 'rgba(30, 41, 59, 0.6)', borderRadius: '8px', padding: '10px 14px' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: '700', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                  <Calculator size={13} /> STEP-BY-STEP DERIVATION:
                </span>
                {whiteboard.steps.map((st, i) => (
                  <div key={i} style={{ fontSize: '0.82rem', color: '#cbd5e1', padding: '3px 0' }}>
                    <strong>Step {i + 1}:</strong> {st}
                  </div>
                ))}
              </div>
            )}

            {whiteboard.graph && (
              <div style={{ background: 'rgba(15, 23, 42, 0.8)', border: '1px dashed #475569', borderRadius: '8px', padding: '8px 12px', fontSize: '0.80rem', color: '#94a3b8' }}>
                📈 <strong>Graph & Convergence:</strong> {whiteboard.graph}
              </div>
            )}

            {whiteboard.answer && (
              <div style={{ background: 'rgba(16, 185, 129, 0.15)', border: '1px solid #10b981', borderRadius: '8px', padding: '8px 12px', color: '#6ee7b7', fontSize: '0.85rem', fontWeight: '600' }}>
                ✓ Verified Solution: {whiteboard.answer}
              </div>
            )}
          </div>
        )}

        {/* DOMAIN 3: PHYSICS (Diagram -> Formula -> Calculation) */}
        {domain === "physics" && (
          <div className="board-physics-suite" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ background: '#0b1329', border: '1px solid #3b82f6', borderRadius: '10px', padding: '12px' }}>
              <span style={{ fontSize: '0.75rem', color: '#93c5fd', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Compass size={14} /> VECTOR SCHEMATIC & PHENOMENON
              </span>
              <p style={{ margin: '8px 0 0 0', fontSize: '0.86rem', color: '#f1f5f9', lineHeight: 1.4 }}>
                {whiteboard.diagram || segment.visual_description || "Dynamic force and energy conservation vector diagram."}
              </p>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div style={{ background: 'rgba(30, 41, 59, 0.7)', borderRadius: '8px', padding: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <span style={{ fontSize: '0.72rem', color: '#a5b4fc', fontWeight: '700' }}>GOVERNING FORMULA</span>
                <div style={{ marginTop: '4px', fontSize: '0.90rem', color: '#f8fafc', fontFamily: 'monospace' }}>
                  {whiteboard.formula || mathOrCode || "F = m * a"}
                </div>
              </div>
              <div style={{ background: 'rgba(30, 41, 59, 0.7)', borderRadius: '8px', padding: '10px', border: '1px solid rgba(255,255,255,0.06)' }}>
                <span style={{ fontSize: '0.72rem', color: '#34d399', fontWeight: '700' }}>CALCULATION RESULT</span>
                <div style={{ marginTop: '4px', fontSize: '0.82rem', color: '#cbd5e1' }}>
                  {whiteboard.calculation || "Equilibrium state verified under constraints"}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* DOMAIN 4: BIOLOGY (Diagram -> Labels -> Process) */}
        {domain === "biology" && (
          <div className="board-biology-suite" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div style={{ background: '#06201a', border: '1px solid #10b981', borderRadius: '10px', padding: '12px' }}>
              <span style={{ fontSize: '0.75rem', color: '#6ee7b7', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px' }}>
                🧬 ANATOMICAL & CELLULAR STRUCTURE
              </span>
              <p style={{ margin: '8px 0 0 0', fontSize: '0.86rem', color: '#f1f5f9', lineHeight: 1.4 }}>
                {whiteboard.diagram || segment.visual_description || "Membrane transport and metabolic process."}
              </p>
            </div>

            {whiteboard.labels && whiteboard.labels.length > 0 && (
              <div style={{ background: 'rgba(30, 41, 59, 0.6)', borderRadius: '8px', padding: '10px 14px' }}>
                <span style={{ fontSize: '0.74rem', color: '#38bdf8', fontWeight: '700', marginBottom: '6px', display: 'block' }}>
                  ANATOMICAL IDENTIFIERS & LABELS:
                </span>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {whiteboard.labels.map((lbl, idx) => (
                    <span key={idx} style={{ padding: '3px 8px', borderRadius: '4px', background: 'rgba(16, 185, 129, 0.2)', color: '#a7f3d0', fontSize: '0.76rem' }}>
                      • {lbl}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {whiteboard.process && (
              <div style={{ background: 'rgba(15, 23, 42, 0.8)', borderRadius: '8px', padding: '10px', borderLeft: '3px solid #10b981', fontSize: '0.82rem', color: '#e2e8f0' }}>
                <strong>Metabolic Cycle:</strong> {whiteboard.process}
              </div>
            )}
          </div>
        )}

        {/* DOMAIN 5: HISTORY (Timeline -> Map -> Events) */}
        {domain === "history" && (
          <div className="board-history-suite" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {whiteboard.timeline && (
              <div style={{ background: '#1c1917', border: '1px solid #d97706', borderRadius: '10px', padding: '12px' }}>
                <span style={{ fontSize: '0.75rem', color: '#fbbf24', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Calendar size={14} /> CHRONOLOGICAL TIMELINE PHASES
                </span>
                <div style={{ marginTop: '8px', display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {whiteboard.timeline.map((t, idx) => (
                    <div key={idx} style={{ fontSize: '0.82rem', color: '#fed7aa' }}>
                      ⏱️ {t}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {whiteboard.map_context && (
              <div style={{ background: 'rgba(30, 41, 59, 0.6)', borderRadius: '8px', padding: '10px 14px', fontSize: '0.82rem', color: '#cbd5e1', display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                <MapPin size={16} className="text-amber" style={{ flexShrink: 0, marginTop: '2px' }} />
                <span><strong>Geographic Context:</strong> {whiteboard.map_context}</span>
              </div>
            )}

            {whiteboard.events && (
              <div style={{ background: 'rgba(15, 23, 42, 0.8)', borderRadius: '8px', padding: '10px 14px', borderLeft: '3px solid #f59e0b' }}>
                <span style={{ fontSize: '0.74rem', color: '#fde68a', fontWeight: '700', marginBottom: '4px', display: 'block' }}>
                  WATERSHED EVENTS:
                </span>
                {whiteboard.events.map((ev, idx) => (
                  <div key={idx} style={{ fontSize: '0.80rem', color: '#f8fafc', padding: '2px 0' }}>
                    • {ev}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* DOMAIN 6: GENERAL / FALLBACK */}
        {domain === "general" && (
          <div className="board-general-suite" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div className="board-diagram-card" style={{ background: '#0f172a', border: '1px solid #475569', borderRadius: '10px', padding: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <Activity size={16} className="text-primary" />
                <span style={{ fontSize: '0.80rem', color: '#a5b4fc', fontWeight: '700' }}>
                  CONCEPT MODEL SPECIFICATION
                </span>
              </div>
              <p style={{ margin: 0, fontSize: '0.88rem', color: '#f1f5f9', lineHeight: 1.45 }}>
                {whiteboard.specification || segment.visual_description || mathOrCode || "Structural relationships, boundary invariants, and system behavior."}
              </p>
            </div>

            {whiteboard.key_principles && (
              <div style={{ background: 'rgba(30, 41, 59, 0.6)', borderRadius: '8px', padding: '10px 14px' }}>
                <span style={{ fontSize: '0.74rem', color: '#38bdf8', fontWeight: '700', marginBottom: '6px', display: 'block' }}>
                  OPERATIONAL INVARIANTS:
                </span>
                {whiteboard.key_principles.map((pr, idx) => (
                  <div key={idx} style={{ fontSize: '0.80rem', color: '#cbd5e1', padding: '2px 0' }}>
                    ✓ {pr}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Key Takeaways Section */}
      <div className="board-points-section">
        <span className="points-header-label">📌 Core Principles Verified on Smartboard:</span>
        <div className="board-points-list">
          {keyPoints.slice(0, 3).map((pt, idx) => (
            <div key={idx} className="board-point-item">
              <div className="point-badge">
                <Check size={12} />
              </div>
              <span className="point-text">{pt}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Intuitive Analogy / Real-World Model */}
      {segment.example && (
        <div className={`board-analogy-box ${isRemediation ? 'analogy-remedy' : 'analogy-standard'}`}>
          <div className="analogy-title">
            <Lightbulb size={15} className={isRemediation ? 'text-amber' : 'text-indigo'} />
            <span>{isRemediation ? '💡 INTUITIVE REMEDIATION ANALOGY' : '💡 REAL-WORLD INTUITIVE ANALOGY'}</span>
          </div>
          <p className="analogy-content">{segment.example}</p>
        </div>
      )}
    </div>
  );
}
