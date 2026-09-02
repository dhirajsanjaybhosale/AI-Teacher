import React, { useState, useRef } from 'react';
import { Upload, FileText, Sparkles, Clock, Layers, Globe, Search, ArrowRight, BookOpen, Cpu, ShieldCheck } from 'lucide-react';

const PRESET_TOPICS = [
  { title: "What is photosynthesis?", category: "Biology", query: "What is photosynthesis?" },
  { title: "Explain recursion with an example", category: "Programming", query: "Explain recursion with an example." },
  { title: "What is blockchain?", category: "Cryptography", query: "What is blockchain?" },
  { title: "What are the latest developments in AI agents?", category: "Current Tech / Web", query: "What are the latest developments in AI agents?" },
  { title: "Explain Newton's Second Law", category: "Physics", query: "Explain Newton's Second Law." },
  { title: "Explain TCP vs UDP", category: "Networking", query: "Explain TCP vs UDP." },
  { title: "Why is the sky blue?", category: "Optics / Physics", query: "Why is the sky blue?" },
  { title: "Explain photosynthesis in Hindi", category: "Hindi (हिंदी)", query: "Explain photosynthesis in Hindi." },
  { title: "Explain Ohm's Law in Hinglish", category: "Hinglish (हिंदी + Eng)", query: "Explain Ohm's Law in Hinglish." },
  { title: "7-Day Mastery Curriculum for Photosynthesis", category: "7-Day Roadmap", query: "7-Day Mastery Curriculum for Photosynthesis." },
  { title: "Teach me Python from beginner level", category: "Programming", query: "Teach me Python from beginner level." }
];

export default function UploadOrTopicForm({ onSubmit, isLoading }) {
  const [activeTab, setActiveTab] = useState('topic'); // 'topic' or 'pdf'
  const [docFile, setDocFile] = useState(null);
  const [topicText, setTopicText] = useState('');
  const [level, setLevel] = useState('beginner');
  const [timeMinutes, setTimeMinutes] = useState(10);
  const [goal, setGoal] = useState('understand');
  const [language, setLanguage] = useState('en');
  const [teachingStyle, setTeachingStyle] = useState('Simple');
  const [existingKnowledge, setExistingKnowledge] = useState('');
  const [forceWebSearch, setForceWebSearch] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setDocFile(file);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setDocFile(e.target.files[0]);
    }
  };

  const handleLoadSamplePdf = async (sampleName = "sample_chapter.pdf", title = "Introduction to Electricity & Ohm's Law") => {
    try {
      const res = await fetch(`/${sampleName}`);
      if (res.ok) {
        const blob = await res.blob();
        const file = new File([blob], sampleName, { type: "application/pdf" });
        setDocFile(file);
      } else {
        const sampleBlob = new Blob([`Sample Chapter Content for ${title}`], { type: "application/pdf" });
        const sampleFile = new File([sampleBlob], sampleName, { type: "application/pdf" });
        setDocFile(sampleFile);
      }
      setActiveTab('pdf');
    } catch (err) {
      console.error("Error loading sample PDF:", err);
      const sampleBlob = new Blob([`Sample Chapter Content for ${title}`], { type: "application/pdf" });
      const sampleFile = new File([sampleBlob], sampleName, { type: "application/pdf" });
      setDocFile(sampleFile);
      setActiveTab('pdf');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (activeTab === 'pdf' && !docFile) {
      alert("Please select or drop a PDF, DOCX, PPTX, or TXT file, or choose a benchmark chapter.");
      return;
    }
    if (activeTab === 'topic' && !topicText.trim()) {
      alert("Please enter any topic, question, or concept to teach.");
      return;
    }

    onSubmit({
      documentFile: activeTab === 'pdf' ? docFile : null,
      pdfFile: activeTab === 'pdf' ? docFile : null,
      topic: activeTab === 'topic' ? topicText : (docFile ? docFile.name.replace(/\.[^/.]+$/, '') : ''),
      level,
      timeMinutes,
      goal,
      language,
      teachingStyle,
      existingKnowledge,
      forceWebSearch
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
        Enter <strong>ANY topic, concept, question, or learning request</strong>. Your AI Teacher dynamically routes knowledge,
        creates tailored curricula, speaks with synchronized visual slides & avatar, and adapts re-explanations to your exact misconceptions.
      </p>

      {/* Dynamic Knowledge Router Status Strip */}
      <div className="router-status-strip">
        <div className="router-tag">
          <ShieldCheck size={14} className="text-cyan" />
          <span>Knowledge Router:</span>
        </div>
        <div className="router-item">📄 PDF RAG Vector Ingestion</div>
        <div className="router-dot">•</div>
        <div className="router-item">🌐 Live Free Web Retrieval (DuckDuckGo/Wikipedia)</div>
        <div className="router-dot">•</div>
        <div className="router-item">🧠 Multi-Domain LLM Engine</div>
      </div>

      <form className="form-card glass-panel glass-panel-glow" onSubmit={handleSubmit}>
        {/* Source Mode Tabs */}
        <div className="tab-switcher">
          <button
            type="button"
            className={`tab-btn ${activeTab === 'topic' ? 'active' : ''}`}
            onClick={() => setActiveTab('topic')}
          >
            <Sparkles size={18} />
            <span>Type Any Educational Topic / Question</span>
          </button>
          <button
            type="button"
            className={`tab-btn ${activeTab === 'pdf' ? 'active' : ''}`}
            onClick={() => setActiveTab('pdf')}
          >
            <Upload size={18} />
            <span>Upload PDF Chapter (RAG)</span>
          </button>
        </div>

        {/* Tab Content: Topic Input */}
        {activeTab === 'topic' && (
          <div className="tab-section">
            <div className="input-group">
              <label className="input-label">What concept or educational question would you like to master?</label>
              <input
                type="text"
                className="text-input"
                placeholder="e.g., What is photosynthesis? Explain TCP vs UDP, What are the latest developments in AI agents?, Teach me Python from beginner level..."
                value={topicText}
                onChange={(e) => setTopicText(e.target.value)}
              />
            </div>

            {/* Optional Web Search Toggle */}
            <div className="web-search-toggle-bar">
              <label className="toggle-label" style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '0.85rem', color: '#94a3b8' }}>
                <input
                  type="checkbox"
                  checked={forceWebSearch}
                  onChange={(e) => setForceWebSearch(e.target.checked)}
                  style={{ cursor: 'pointer', accentColor: '#6366f1' }}
                />
                <Search size={14} className="text-indigo" />
                <span>Force Live Web Grounding (DuckDuckGo / Wikipedia / ArXiv)</span>
              </label>
              <span className="toggle-hint" style={{ fontSize: '0.75rem', color: '#64748b' }}>
                (Automatically enabled for temporal queries containing 'latest', 'recent', '2026', etc.)
              </span>
            </div>

            <div className="presets-wrapper">
              <span className="presets-label">⚡ Multi-Domain Topic & Question Examples:</span>
              <div className="preset-chips">
                {PRESET_TOPICS.map((p, i) => (
                  <button
                    key={i}
                    type="button"
                    className="chip-btn"
                    onClick={() => {
                      setTopicText(p.query);
                      if (p.category.includes("Web")) {
                        setForceWebSearch(true);
                      }
                      if (p.category.includes("Hindi")) {
                        setLanguage("hi");
                      }
                    }}
                  >
                    <span>{p.title}</span>
                    <span className="chip-cat">{p.category}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Tab Content: Document Dropzone */}
        {activeTab === 'pdf' && (
          <div className="tab-section">
            <div
              className={`dropzone ${isDragging ? 'dragging' : ''} ${docFile ? 'has-file' : ''}`}
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleFileDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.pptx,.txt,.md"
                className="hidden-file-input"
                onChange={handleFileChange}
              />
              
              {docFile ? (
                <div className="file-info-box">
                  <div className="file-icon-box">
                    <FileText size={32} className="text-indigo" />
                  </div>
                  <div className="file-details">
                    <p className="file-name">{docFile.name}</p>
                    <p className="file-size">{(docFile.size / 1024).toFixed(1)} KB • Universal Document RAG Ingestion Active</p>
                  </div>
                  <span className="file-badge">Selected</span>
                </div>
              ) : (
                <div className="dropzone-content">
                  <div className="upload-icon-circle">
                    <Upload size={28} />
                  </div>
                  <p className="drop-title">Drag & drop your Document here (PDF, Word, PPT, TXT)</p>
                  <p className="drop-sub">Supported: .pdf, .docx, .pptx, .txt, .md for vector grounding</p>
                </div>
              )}
            </div>

            {/* Quick Demo Sample Action */}
            <div className="sample-quick-bar">
              <span className="sample-label">⚡ Benchmark Chapters:</span>
              <div className="sample-buttons-group">
                <button
                  type="button"
                  className="btn-sample-chip"
                  onClick={() => handleLoadSamplePdf("sample_chapter.pdf", "Electricity & Ohm's Law")}
                >
                  ⚡ Chapter 1: <strong>Electricity & Circuits (PDF)</strong>
                </button>
                <button
                  type="button"
                  className="btn-sample-chip"
                  onClick={() => handleLoadSamplePdf("cellular_respiration_chapter.pdf", "Cellular Respiration")}
                >
                  🧬 Chapter 2: <strong>Cellular Respiration (PDF)</strong>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Existing Knowledge Input */}
        <div className="existing-knowledge-section">
          <label className="pref-label">
            <BookOpen size={16} />
            <span>What do you already know? (Optional Prior Knowledge)</span>
          </label>
          <input
            type="text"
            className="input-field"
            placeholder="e.g. 'I know basic arithmetic, but struggle with circuit diagrams' or 'None'"
            value={existingKnowledge}
            onChange={(e) => setExistingKnowledge(e.target.value)}
          />
        </div>

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
                { id: 'beginner', label: 'Beginner', desc: 'Intuitive & Analogies' },
                { id: 'intermediate', label: 'Intermediate', desc: 'Mechanisms & Equations' },
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
                { mins: 5, label: '5m', segs: '2 segs' },
                { mins: 10, label: '10m', segs: '3 segs' },
                { mins: 20, label: '20m', segs: '4 segs' },
                { mins: 30, label: '30m', segs: '5 segs' },
                { mins: 60, label: '60m', segs: '6 segs' },
                { mins: 10080, label: '7-Day Plan', segs: 'Roadmap' }
              ].map((t) => (
                <button
                  key={t.mins}
                  type="button"
                  className={`pill-btn ${timeMinutes === t.mins ? 'active' : ''}`}
                  onClick={() => setTimeMinutes(t.mins)}
                >
                  <span className="pill-title">{t.label}</span>
                  <span className="pill-sub">{t.segs}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Teaching Style */}
          <div className="pref-box">
            <label className="pref-label">
              <Sparkles size={16} />
              <span>Teaching Style</span>
            </label>
            <div className="pill-group">
              {['Simple', 'Detailed', 'Visual', 'Practical', 'Socratic', 'Exam-focused'].map((style) => (
                <button
                  key={style}
                  type="button"
                  className={`pill-btn ${teachingStyle === style ? 'active' : ''}`}
                  onClick={() => setTeachingStyle(style)}
                >
                  <span className="pill-title">{style}</span>
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
                { code: 'hi', label: 'Hindi (हिंदी)', flag: '🇮🇳' },
                { code: 'hinglish', label: 'Hinglish', flag: '🇮🇳' }
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
          <span>{isLoading ? 'Synthesizing Lesson & Grounding...' : 'Launch Interactive AI Teacher Lesson'}</span>
          <ArrowRight size={20} />
        </button>
      </form>
    </div>
  );
}
