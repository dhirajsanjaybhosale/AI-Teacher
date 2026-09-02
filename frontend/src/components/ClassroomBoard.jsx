import React from 'react';
import { BookOpen, Sparkles, Layers, Code, Cpu, Activity, Lightbulb, ArrowRight, Check } from 'lucide-react';

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
  const keyPoints = segment.key_points && segment.key_points.length > 0
    ? segment.key_points
    : ["Master core mechanism", "Identify governing laws & relationships", "Apply intuitive practical analogy"];

  // Helper to format subject icons
  const getSubjectIcon = () => {
    const sub = (subject || "").toLowerCase();
    if (sub.includes("physic") || sub.includes("electr")) return "⚡";
    if (sub.includes("bio") || sub.includes("cell")) return "🧬";
    if (sub.includes("math") || sub.includes("calc")) return "📐";
    if (sub.includes("prog") || sub.includes("code") || sub.includes("python") || sub.includes("react")) return "💻";
    if (sub.includes("network") || sub.includes("tcp")) return "🌐";
    return "🎓";
  };

  return (
    <div className={`classroom-board-card glass-panel ${isRemediation ? 'board-remediation-glow' : 'board-classroom-glow'} ${highlightFocus ? 'board-pointer-active' : ''}`}>
      {/* Board Top Header Frame */}
      <div className="board-top-frame">
        <div className="board-subject-tag">
          <span className="subject-icon">{getSubjectIcon()}</span>
          <span className="subject-name">{subject.toUpperCase()} SMARTBOARD</span>
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
          <span>{visualType.toUpperCase()} REPRESENTATION</span>
        </div>
      </div>

      {/* Subject-Aware Interactive Board Visual Content */}
      <div className="board-visual-container">
        {/* CASE 1: Equation / Mathematics / Physics */}
        {(visualType === "equation" || visualType === "math" || (subject.toLowerCase().includes("physic") && mathOrCode)) && (
          <div className="board-equation-card">
            <div className="equation-badge">FORMULA SPECIFICATION</div>
            <div className="equation-display">
              <code>{mathOrCode || "V = I × R"}</code>
            </div>
            <div className="equation-legend">
              <span className="legend-item">• <strong>V</strong> = Voltage / Potential (Volts)</span>
              <span className="legend-item">• <strong>I</strong> = Current / Flow Rate (Amperes)</span>
              <span className="legend-item">• <strong>R</strong> = Resistance / Opposition (Ohms)</span>
            </div>
          </div>
        )}

        {/* CASE 2: Code / Programming */}
        {(visualType === "code" || subject.toLowerCase().includes("prog") || subject.toLowerCase().includes("python")) && (
          <div className="board-code-card">
            <div className="code-header">
              <Code size={14} className="text-cyan" />
              <span>SYNTAX & EXECUTION FLOW</span>
            </div>
            <pre className="code-snippet">
              <code>{mathOrCode || "// Key structural implementation\nfunction executeConcept() {\n  return applyReasoning();\n}"}</code>
            </pre>
          </div>
        )}

        {/* CASE 3: Flowchart / Process / Sequence */}
        {(visualType === "flowchart" || visualType === "process" || visualType === "timeline") && (
          <div className="board-process-card">
            <div className="process-header">
              <Activity size={14} className="text-indigo" />
              <span>STEP-BY-STEP CAUSAL MECHANISM</span>
            </div>
            <div className="process-steps-row">
              <div className="step-capsule">
                <span className="step-num">1</span>
                <span className="step-label">Input / Initial State</span>
              </div>
              <ArrowRight size={16} className="text-indigo" />
              <div className="step-capsule active-step">
                <span className="step-num">2</span>
                <span className="step-label">Transformation Mechanism</span>
              </div>
              <ArrowRight size={16} className="text-indigo" />
              <div className="step-capsule">
                <span className="step-num">3</span>
                <span className="step-label">Result / Observable</span>
              </div>
            </div>
          </div>
        )}

        {/* CASE 4: Comparison / Two-Concept Trade-off */}
        {visualType === "comparison" && (
          <div className="board-comparison-card">
            <div className="comp-col">
              <div className="comp-title">Original / Common Assumption</div>
              <p className="comp-desc">Direct 1:1 proportionality without constraints.</p>
            </div>
            <div className="comp-divider">VS</div>
            <div className="comp-col highlight-col">
              <div className="comp-title">Physical Reality / Law</div>
              <p className="comp-desc">Inverse relationship: Higher opposition reduces throughput.</p>
            </div>
          </div>
        )}

        {/* CASE 5: General Diagram / Biological Structure */}
        {visualType === "diagram" && (
          <div className="board-diagram-card">
            <div className="diagram-header">
              <Cpu size={14} className="text-emerald" />
              <span>LABELED STRUCTURAL OVERVIEW</span>
            </div>
            <p className="diagram-desc">{segment.visual_description || mathOrCode || "Structural relationships and interaction boundaries."}</p>
          </div>
        )}
      </div>

      {/* Key Takeaways Section (Pointer wand targets this) */}
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
