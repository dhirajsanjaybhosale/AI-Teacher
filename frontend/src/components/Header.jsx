import React from 'react';
import { Bot, Sparkles, Cpu, Globe, RotateCcw } from 'lucide-react';

export default function Header({ systemHealth, language, onResetLesson, hasActiveLesson }) {
  return (
    <header className="header-container">
      <div className="header-brand" onClick={onResetLesson}>
        <div className="brand-logo-box">
          <Bot className="brand-icon" size={26} />
        </div>
        <div className="brand-text">
          <div className="brand-title">
            <span>AI</span> Teacher
            <span className="brand-badge">STUDIO</span>
          </div>
          <p className="brand-subtitle">Adaptive Pedagogical Video Intelligence</p>
        </div>
      </div>

      <div className="header-actions">
        {/* Hardware Mode Pill */}
        <div className="status-pill">
          <Cpu size={15} className="text-cyan" />
          <span>{systemHealth?.gpu_available ? 'GPU Engine (CUDA)' : 'CPU Neural Engine'}</span>
          <span className="status-dot"></span>
        </div>

        {/* Language Badge */}
        <div className="status-pill">
          <Globe size={15} className="text-indigo" />
          <span>{language === 'hi' ? 'Hindi (हिंदी)' : 'English'}</span>
        </div>

        {/* Reset / New Lesson Button */}
        {hasActiveLesson && (
          <button className="btn-secondary btn-sm" onClick={onResetLesson} title="Start New Lesson">
            <RotateCcw size={15} />
            <span>New Lesson</span>
          </button>
        )}
      </div>
    </header>
  );
}
