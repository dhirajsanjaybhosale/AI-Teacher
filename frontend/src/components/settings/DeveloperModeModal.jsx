import React, { useState } from 'react';
import { Terminal, Cpu, Database, Network, X, RefreshCw, CheckCircle2 } from 'lucide-react';

export default function DeveloperModeModal({
  isOpen,
  onClose,
  systemHealth,
  activeLesson,
  activeSegment
}) {
  const [activeTab, setActiveTab] = useState('brain');

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop">
      <div className="dev-modal-panel glass-panel">
        <div className="dev-modal-header">
          <div className="dev-header-left">
            <Terminal size={18} className="text-amber" />
            <span className="dev-title">Developer Inspection Console (Technical Diagnostics)</span>
            <span className="dev-badge">DEBUG MODE</span>
          </div>
          <button type="button" className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="dev-tab-bar">
          <button
            type="button"
            className={`dev-tab ${activeTab === 'brain' ? 'active' : ''}`}
            onClick={() => setActiveTab('brain')}
          >
            🧠 Teacher Brain Telemetry
          </button>
          <button
            type="button"
            className={`dev-tab ${activeTab === 'rag' ? 'active' : ''}`}
            onClick={() => setActiveTab('rag')}
          >
            📚 RAG & Vector Chunks
          </button>
          <button
            type="button"
            className={`dev-tab ${activeTab === 'model' ? 'active' : ''}`}
            onClick={() => setActiveTab('model')}
          >
            ⚙ Provider & System
          </button>
        </div>

        {/* Tab 1: Teacher Brain Telemetry */}
        {activeTab === 'brain' && (
          <div className="dev-tab-content">
            <div className="dev-metric-grid">
              <div className="dev-card">
                <span className="dev-card-lbl">Learner Level</span>
                <span className="dev-card-val">{activeLesson?.preferences?.level || 'intermediate'}</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Adapted Strategy</span>
                <span className="dev-card-val text-primary">{activeSegment?.visual_type || 'step_by_step_visual'}</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Understanding State</span>
                <span className="dev-card-val text-emerald">Tracking Active</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Current Segment ID</span>
                <span className="dev-card-val font-mono">{activeSegment?.id || 'seg_01'}</span>
              </div>
            </div>

            <div className="dev-code-block">
              <span className="block-title">Visual Code / Math Formula Buffer:</span>
              <pre>{activeSegment?.visual_code_or_math || 'V = I * R (Ohm\'s Law Formula)'}</pre>
            </div>
          </div>
        )}

        {/* Tab 2: RAG & Vector Chunks */}
        {activeTab === 'rag' && (
          <div className="dev-tab-content">
            <div className="dev-metric-grid">
              <div className="dev-card">
                <span className="dev-card-lbl">Knowledge Route</span>
                <span className="dev-card-val text-primary">{activeLesson?.source_route || 'llm_knowledge'}</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Vector Dimension</span>
                <span className="dev-card-val">384 (all-MiniLM-L6-v2)</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Retrieval Confidence</span>
                <span className="dev-card-val text-cyan">{(activeLesson?.retrieval_confidence || 0.85) * 100}%</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Total Sources</span>
                <span className="dev-card-val">{activeLesson?.sources?.length || 0} Grounded</span>
              </div>
            </div>

            <div className="dev-code-block">
              <span className="block-title">Source Context Chunks:</span>
              <pre>
                {activeLesson?.sources && activeLesson.sources.length > 0
                  ? JSON.stringify(activeLesson.sources, null, 2)
                  : '[Document RAG / Live Web / Universal LLM Knowledge Context Engine active. Zero data leakage.]'}
              </pre>
            </div>
          </div>
        )}

        {/* Tab 3: Model & System Health */}
        {activeTab === 'model' && (
          <div className="dev-tab-content">
            <div className="dev-metric-grid">
              <div className="dev-card">
                <span className="dev-card-lbl">API Server Status</span>
                <span className="dev-card-val text-emerald">
                  <CheckCircle2 size={14} className="inline-icon" /> {systemHealth?.status || 'Online'}
                </span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">Compute Hardware</span>
                <span className="dev-card-val">
                  <Cpu size={14} className="inline-icon" /> {systemHealth?.device?.toUpperCase() || 'CPU'}
                </span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">CUDA GPU Acceleration</span>
                <span className="dev-card-val">{systemHealth?.gpu_available ? 'Enabled (Wav2Lip)' : 'Disabled (Vector Fallback)'}</span>
              </div>
              <div className="dev-card">
                <span className="dev-card-lbl">LLM Provider</span>
                <span className="dev-card-val">Gemini / Groq / Offline Fallback</span>
              </div>
            </div>

            <div className="dev-code-block">
              <span className="block-title">Diagnostics Payload:</span>
              <pre>{JSON.stringify(systemHealth, null, 2)}</pre>
            </div>
          </div>
        )}

        <div className="dev-modal-footer">
          <span className="footer-tip">Developer mode is hidden from students to keep the learning experience clean and focused.</span>
          <button type="button" className="btn-secondary-light" onClick={onClose}>
            Close Console
          </button>
        </div>
      </div>
    </div>
  );
}
