import React, { useState, useEffect } from 'react';
import { Loader2, Sparkles, BookOpen, Film, BrainCircuit } from 'lucide-react';

const STEPS = [
  { label: 'Reading & extracting content structure...', icon: BookOpen },
  { label: 'Formulating adaptive lesson plan & visual diagrams...', icon: BrainCircuit },
  { label: 'Synthesizing neural voice & audio envelopes...', icon: Sparkles },
  { label: 'Compositing talking avatar & interactive video stream...', icon: Film },
];

export default function LoadingOverlay({ title = "Generating AI Lesson", subtitle = "Please wait a moment..." }) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 2800);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-overlay-backdrop">
      <div className="loading-modal glass-panel glass-panel-glow">
        <div className="loading-spinner-wrapper">
          <div className="loading-pulse-ring"></div>
          <Loader2 className="spinner-icon" size={44} />
        </div>

        <h3 className="loading-title">{title}</h3>
        <p className="loading-subtitle">{subtitle}</p>

        <div className="loading-steps-list">
          {STEPS.map((step, idx) => {
            const Icon = step.icon;
            const isDone = idx < currentStep;
            const isCurrent = idx === currentStep;

            return (
              <div
                key={idx}
                className={`loading-step-item ${isDone ? 'step-done' : ''} ${isCurrent ? 'step-current' : ''}`}
              >
                <div className="step-icon-box">
                  <Icon size={16} />
                </div>
                <span className="step-label">{step.label}</span>
                {isCurrent && <span className="step-pulsing-dot"></span>}
                {isDone && <span className="step-check">✓</span>}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
