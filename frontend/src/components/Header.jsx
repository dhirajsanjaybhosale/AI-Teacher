import React from 'react';
import { Bot, Sparkles, Cpu, Globe, RotateCcw } from 'lucide-react';

export default function Header({ systemHealth, language, onResetLesson, hasActiveLesson, onSwitchLanguage }) {
  const isGPU = Boolean(systemHealth?.gpu_available);
  const currentLang = language?.toLowerCase() || 'en';

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
        {/* Avatar Execution Mode Badge */}
        <div className="status-pill avatar-mode-pill" title={isGPU ? 'GPU Accelerated Lip-Sync' : 'Lightweight CPU Synchronized 2D Vector Avatar'}>
          <span className="mode-status-dot">🟢</span>
          <Cpu size={14} className="text-cyan" />
          <span className="mode-name">{isGPU ? 'GPU Lip-Sync Mode' : 'CPU Avatar Mode'}</span>
        </div>

        {/* Live Mid-Lesson Language Switcher */}
        {hasActiveLesson && onSwitchLanguage ? (
          <div className="lang-switcher-pill">
            <Globe size={14} className="text-indigo" />
            <button
              className={`lang-btn ${currentLang === 'en' ? 'active' : ''}`}
              onClick={() => onSwitchLanguage('en')}
              title="Switch to English"
            >
              EN
            </button>
            <button
              className={`lang-btn ${currentLang === 'hi' ? 'active' : ''}`}
              onClick={() => onSwitchLanguage('hi')}
              title="Switch to Hindi"
            >
              हिंदी
            </button>
            <button
              className={`lang-btn ${currentLang === 'hinglish' ? 'active' : ''}`}
              onClick={() => onSwitchLanguage('hinglish')}
              title="Switch to Hinglish"
            >
              Hinglish
            </button>
          </div>
        ) : (
          <div className="status-pill">
            <Globe size={14} className="text-indigo" />
            <span>{currentLang === 'hi' ? 'हिंदी' : (currentLang === 'hinglish' ? 'Hinglish' : 'English')}</span>
          </div>
        )}

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
