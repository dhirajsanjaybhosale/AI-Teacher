import React from 'react';
import { Settings, Volume2, Bell, Terminal, Shield, CheckCircle2, Sliders } from 'lucide-react';

export default function SettingsView({
  developerMode,
  onToggleDeveloperMode,
  onOpenDevConsole,
  systemHealth
}) {
  return (
    <div className="settings-page-container">
      {/* Page Header */}
      <div className="page-title-banner">
        <h1 className="page-main-heading">Platform Settings</h1>
        <p className="page-sub-heading">Customize your learning environment, audio narration, and platform behavior.</p>
      </div>

      {/* Audio & Narration Preferences */}
      <div className="settings-card glass-panel">
        <div className="card-header-simple">
          <Volume2 size={20} className="text-primary" />
          <h3>Audio & Neural Narration</h3>
        </div>

        <div className="settings-options-list">
          <div className="setting-row">
            <div className="setting-meta">
              <span className="setting-title">Auto-play Teacher Speech</span>
              <span className="setting-desc">Automatically play teacher audio when a new segment loads.</span>
            </div>
            <label className="switch-toggle">
              <input type="checkbox" defaultChecked />
              <span className="slider-round" />
            </label>
          </div>

          <div className="setting-row">
            <div className="setting-meta">
              <span className="setting-title">Subtitles & Closed Captions</span>
              <span className="setting-desc">Display synchronized speech subtitles on the digital board.</span>
            </div>
            <label className="switch-toggle">
              <input type="checkbox" defaultChecked />
              <span className="slider-round" />
            </label>
          </div>
        </div>
      </div>

      {/* Developer Mode Section */}
      <div className="settings-card glass-panel developer-settings-card">
        <div className="card-header-simple">
          <Terminal size={20} className="text-amber" />
          <div className="dev-header-text">
            <h3>Developer Mode</h3>
            <span className="setting-desc">
              Expose internal AI telemetry, RAG vector retrieval confidence, model diagnostics, and debug logs.
            </span>
          </div>
        </div>

        <div className="setting-row dev-toggle-row">
          <div className="setting-meta">
            <span className="setting-title">Enable Technical Diagnostics</span>
            <span className="setting-desc">Default is OFF for students. Turn ON to inspect RAG embeddings, tokens, and pipelines.</span>
          </div>
          <label className="switch-toggle">
            <input
              type="checkbox"
              checked={developerMode}
              onChange={(e) => onToggleDeveloperMode(e.target.checked)}
            />
            <span className="slider-round" />
          </label>
        </div>

        {developerMode && (
          <div className="dev-enabled-box">
            <div className="dev-alert-banner">
              <Shield size={16} className="text-emerald" />
              <span>Developer mode is active. Technical diagnostics are now accessible.</span>
            </div>

            <button
              type="button"
              className="btn-amber-action"
              onClick={onOpenDevConsole}
            >
              <Terminal size={15} />
              <span>Open Developer Inspection Console</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
