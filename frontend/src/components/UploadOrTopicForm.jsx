import React, { useState, useRef } from 'react';
import { Upload, FileText, Sparkles, Clock, Layers, Globe, Check, AlertCircle, ArrowRight } from 'lucide-react';

const PRESET_TOPICS = [
  { title: "Cellular Respiration & ATP Synthase", category: "Biology" },
  { title: "Quantum Superposition & Qubits", category: "Physics" },
  { title: "Neural Networks & Backpropagation", category: "AI & ML" },
  { title: "Photosynthesis & Solar Energy Conversion", category: "Biochemistry" }
];

export default function UploadOrTopicForm({ onSubmit, isLoading }) {
  const [activeTab, setActiveTab] = useState('pdf'); // 'pdf' or 'topic'
  const [pdfFile, setPdfFile] = useState(null);
  const [topicText, setTopicText] = useState('');
  const [level, setLevel] = useState('beginner');
  const [timeMinutes, setTimeMinutes] = useState(5);
  const [language, setLanguage] = useState('en');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
        setPdfFile(file);
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setPdfFile(e.target.files[0]);
    }
  };

  const handleLoadSamplePdf = async () => {
    try {
      // Create a virtual file object representing the sample chapter
      const sampleBlob = new Blob(["Sample Cellular Respiration Chapter Content"], { type: "application/pdf" });
      const sampleFile = new File([sampleBlob], "cellular_respiration_chapter.pdf", { type: "application/pdf" });
      setPdfFile(sampleFile);
      setActiveTab('pdf');
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (activeTab === 'pdf' && !pdfFile) {
      alert("Please select or drop a PDF file, or choose the sample PDF.");
      return;
    }
    if (activeTab === 'topic' && !topicText.trim()) {
      alert("Please enter a topic to teach.");
      return;
    }

    onSubmit({
      pdfFile: activeTab === 'pdf' ? pdfFile : null,
      topic: activeTab === 'topic' ? topicText : (pdfFile ? pdfFile.name.replace('.pdf', '') : ''),
      level,
      timeMinutes,
      language
    });
  };

  return (
    <div className="onboarding-container">
      <div className="hero-badge">
        <Sparkles size={14} className="text-indigo" />
        <span>ROUND 2 • AI INNOVATION HACKATHON 2026</span>
      </div>

      <h1 className="hero-title">
        The Future of <span className="text-gradient">Personalized Education</span>
      </h1>
      <p className="hero-description">
        Upload any textbook chapter or choose a topic. Your AI Teacher will plan a tailored curriculum,
        narrate with dynamic visual slides and synchronized avatar, and adapt re-explanations to your exact misconceptions.
      </p>

      <form className="form-card glass-panel glass-panel-glow" onSubmit={handleSubmit}>
        {/* Source Mode Tabs */}
        <div className="tab-switcher">
          <button
            type="button"
            className={`tab-btn ${activeTab === 'pdf' ? 'active' : ''}`}
            onClick={() => setActiveTab('pdf')}
          >
            <Upload size={18} />
            <span>Upload PDF Chapter</span>
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'topic' ? 'active' : ''}`}
            onClick={() => setActiveTab('topic')}
          >
            <Sparkles size={18} />
            <span>Type Any Topic</span>
          </button>
        </div>

        {/* Tab Content: PDF Dropzone */}
        {activeTab === 'pdf' && (
          <div className="tab-section">
            <div
              className={`dropzone ${isDragging ? 'dragging' : ''} ${pdfFile ? 'has-file' : ''}`}
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleFileDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,application/pdf"
                className="hidden-file-input"
                onChange={handleFileChange}
              />
              
              {pdfFile ? (
                <div className="file-info-box">
                  <div className="file-icon-box">
                    <FileText size={32} className="text-indigo" />
                  </div>
                  <div className="file-details">
                    <p className="file-name">{pdfFile.name}</p>
                    <p className="file-size">{(pdfFile.size / 1024).toFixed(1)} KB • Ready for RAG Analysis</p>
                  </div>
                  <span className="file-badge">Selected</span>
                </div>
              ) : (
                <div className="dropzone-content">
                  <div className="upload-icon-circle">
                    <Upload size={28} />
                  </div>
                  <p className="drop-title">Drag & drop your PDF chapter here</p>
                  <p className="drop-sub">or click to browse your local documents</p>
                </div>
              )}
            </div>

            {/* Quick Demo Sample Action */}
            <div className="sample-quick-bar">
              <span className="sample-label">⚡ Hackathon Demo Fast-Track:</span>
              <button
                type="button"
                className="btn-sample-chip"
                onClick={handleLoadSamplePdf}
              >
                Load Sample Chapter: <strong>Cellular Respiration (PDF)</strong>
              </button>
            </div>
          </div>
        )}

        {/* Tab Content: Topic Input */}
        {activeTab === 'topic' && (
          <div className="tab-section">
            <div className="input-group">
              <label className="input-label">What concept or topic would you like to master?</label>
              <input
                type="text"
                className="text-input"
                placeholder="e.g., Quantum Entanglement, CRISPR Gene Editing, Photosynthesis..."
                value={topicText}
                onChange={(e) => setTopicText(e.target.value)}
              />
            </div>

            <div className="presets-wrapper">
              <span className="presets-label">Popular Suggestions:</span>
              <div className="preset-chips">
                {PRESET_TOPICS.map((p, i) => (
                  <button
                    key={i}
                    type="button"
                    className="chip-btn"
                    onClick={() => setTopicText(p.title)}
                  >
                    <span>{p.title}</span>
                    <span className="chip-cat">{p.category}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Preferences Grid */}
        <div className="pref-grid">
          {/* Target Level */}
          <div className="pref-box">
            <label className="pref-label">
              <Layers size={16} />
              <span>Target Level</span>
            </label>
            <div className="pill-group">
              {[
                { id: 'beginner', label: 'Beginner', desc: 'Intuitive & Concept-focused' },
                { id: 'intermediate', label: 'Intermediate', desc: 'Mechanisms & Processes' },
                { id: 'advanced', label: 'Advanced', desc: 'Deep-dive & Rigorous' }
              ].map((lvl) => (
                <button
                  key={lvl.id}
                  type="button"
                  className={`pill-btn ${level === lvl.id ? 'active' : ''}`}
                  onClick={() => setLevel(lvl.id)}
                >
                  <span className="pill-title">{lvl.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Time Budget */}
          <div className="pref-box">
            <label className="pref-label">
              <Clock size={16} />
              <span>Time Budget</span>
            </label>
            <div className="pill-group">
              {[
                { mins: 5, segs: '2 segments' },
                { mins: 10, segs: '3 segments' },
                { mins: 15, segs: '4 segments' },
                { mins: 20, segs: '5 segments' }
              ].map((t) => (
                <button
                  key={t.mins}
                  type="button"
                  className={`pill-btn ${timeMinutes === t.mins ? 'active' : ''}`}
                  onClick={() => setTimeMinutes(t.mins)}
                >
                  <span className="pill-title">{t.mins} Min</span>
                  <span className="pill-sub">{t.segs}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Language Preference */}
          <div className="pref-box">
            <label className="pref-label">
              <Globe size={16} />
              <span>Instruction Language</span>
            </label>
            <div className="pill-group">
              {[
                { code: 'en', label: 'English', flag: '🇬🇧' },
                { code: 'hi', label: 'Hindi (हिंदी)', flag: '🇮🇳' }
              ].map((lang) => (
                <button
                  key={lang.code}
                  type="button"
                  className={`pill-btn ${language === lang.code ? 'active' : ''}`}
                  onClick={() => setLanguage(lang.code)}
                >
                  <span className="pill-flag">{lang.flag}</span>
                  <span className="pill-title">{lang.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Submit CTA */}
        <button
          type="submit"
          className="btn-primary-cta"
          disabled={isLoading}
        >
          <span>{isLoading ? 'Synthesizing Lesson...' : 'Launch Interactive AI Teacher Lesson'}</span>
          <ArrowRight size={20} />
        </button>
      </form>
    </div>
  );
}
