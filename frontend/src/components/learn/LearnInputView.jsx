import React, { useState, useRef } from 'react';
import {
  Sparkles,
  Upload,
  BookOpen,
  ArrowRight,
  Clock,
  Globe,
  CheckCircle2,
  X,
  Lightbulb
} from 'lucide-react';

export default function LearnInputView({
  onSubmitLesson,
  isLoading = false,
  studentProfile,
  initialQuery = ''
}) {
  const [topicInput, setTopicInput] = useState(initialQuery || '');
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showUploadZone, setShowUploadZone] = useState(false);
  const [fileProcessedStatus, setFileProcessedStatus] = useState(null);
  const fileInputRef = useRef(null);

  // Duration & Language selection
  const [selectedDuration, setSelectedDuration] = useState(10);
  const [selectedLanguage, setSelectedLanguage] = useState(
    studentProfile?.learning_profile?.preferred_language || 'en'
  );

  const durationOptions = [
    { label: '5 min', value: 5, desc: 'Quick Core (3 modules)' },
    { label: '10 min', value: 10, desc: 'Standard Masterclass (5 modules)' },
    { label: '20 min', value: 20, desc: 'Deep Dive (7 modules)' },
    { label: '30 min', value: 30, desc: 'Comprehensive (8 modules)' },
    { label: '60 min', value: 60, desc: 'Complete Bootcamp (10 modules)' }
  ];

  const languageOptions = [
    { label: 'English', value: 'en' },
    { label: 'Hinglish', value: 'hinglish' },
    { label: 'हिंदी (Hindi)', value: 'hi' },
    { label: 'मराठी (Marathi)', value: 'mr' }
  ];

  const promptSuggestions = [
    "Explain Binary Search",
    "Teach me Operating Systems",
    "Explain Newton's Laws",
    "Teach me React",
    "Explain Photosynthesis",
    "Explain Black Holes",
    "How does TCP work?",
    "Explain Quantum Computing",
    "Teach me Java Inheritance",
    "Explain Stock Market Basics"
  ];

  const handleFileSelect = (file) => {
    if (!file) return;
    setSelectedFile(file);
    setFileProcessedStatus({
      fileName: file.name,
      message: `Your lesson will be grounded in ${file.name}`
    });
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const query = topicInput.trim() || (selectedFile ? selectedFile.name.replace(/\.[^/.]+$/, "") : "");
    if (!query && !selectedFile) return;

    onSubmitLesson?.({
      topic: query,
      documentFile: selectedFile,
      time_minutes: selectedDuration,
      language: selectedLanguage,
      level: studentProfile?.learning_profile?.current_level || 'intermediate',
      goal: studentProfile?.learning_profile?.learning_goals?.[0] || 'understand',
      teachingStyle: studentProfile?.learning_profile?.learning_styles?.[0] || 'Visual'
    });
  };

  return (
    <div className="learn-page-container">
      {/* Hero Header */}
      <div className="learn-hero-header">
        <div className="learn-badge">
          <Sparkles size={16} className="text-primary" />
          <span>PERSONALIZED AI CLASSROOM</span>
        </div>
        <h1 className="learn-main-title">What do you want to learn?</h1>
        <p className="learn-subtitle">
          Ask me anything... from physics to coding, calculus to history — or upload your course notes.
        </p>
      </div>

      {/* Main Learning Input Card */}
      <div className="learn-input-card glass-panel">
        <form onSubmit={handleSubmit} className="learn-form">
          <div className="search-field-wrapper">
            <BookOpen size={20} className="field-icon" />
            <input
              type="text"
              className="learn-text-input"
              placeholder="Ask me anything... (e.g. Explain Binary Search, Teach me Operating Systems, Explain Photosynthesis)"
              value={topicInput}
              onChange={(e) => setTopicInput(e.target.value)}
              disabled={isLoading}
            />
          </div>

          {/* Duration & Language Selector Controls */}
          <div className="learn-controls-row" style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', margin: '14px 0', alignItems: 'center' }}>
            {/* Duration Selector */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.82rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: '500' }}>
                <Clock size={15} className="text-primary" /> Target Duration:
              </span>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {durationOptions.map((d) => (
                  <button
                    key={d.value}
                    type="button"
                    title={d.desc}
                    onClick={() => setSelectedDuration(d.value)}
                    style={{
                      padding: '5px 12px',
                      borderRadius: '6px',
                      fontSize: '0.80rem',
                      fontWeight: selectedDuration === d.value ? '600' : '400',
                      background: selectedDuration === d.value ? 'rgba(99, 102, 241, 0.25)' : 'rgba(30, 41, 59, 0.6)',
                      border: selectedDuration === d.value ? '1px solid #6366f1' : '1px solid rgba(255, 255, 255, 0.1)',
                      color: selectedDuration === d.value ? '#a5b4fc' : '#cbd5e1',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    {d.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Language Selector */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.82rem', color: '#94a3b8', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: '500' }}>
                <Globe size={15} className="text-emerald" /> Language:
              </span>
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {languageOptions.map((l) => (
                  <button
                    key={l.value}
                    type="button"
                    onClick={() => setSelectedLanguage(l.value)}
                    style={{
                      padding: '5px 12px',
                      borderRadius: '6px',
                      fontSize: '0.80rem',
                      fontWeight: selectedLanguage === l.value ? '600' : '400',
                      background: selectedLanguage === l.value ? 'rgba(16, 185, 129, 0.22)' : 'rgba(30, 41, 59, 0.6)',
                      border: selectedLanguage === l.value ? '1px solid #10b981' : '1px solid rgba(255, 255, 255, 0.1)',
                      color: selectedLanguage === l.value ? '#6ee7b7' : '#cbd5e1',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    {l.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Uploaded Material Pill if Present */}
          {selectedFile && (
            <div className="uploaded-file-banner">
              <div className="file-banner-left">
                <CheckCircle2 size={16} className="text-emerald" />
                <span className="file-banner-name">{selectedFile.name}</span>
                <span className="file-banner-tag">✓ Ready for lesson</span>
              </div>
              <button
                type="button"
                className="file-remove-btn"
                onClick={() => {
                  setSelectedFile(null);
                  setFileProcessedStatus(null);
                }}
                title="Remove file"
              >
                <X size={14} />
              </button>
            </div>
          )}

          {/* Action Buttons */}
          <div className="learn-form-actions">
            <button
              type="button"
              className={`btn-upload-toggle ${showUploadZone ? 'active' : ''}`}
              onClick={() => setShowUploadZone(!showUploadZone)}
            >
              <Upload size={16} />
              <span>{selectedFile ? 'Change Material' : 'Upload Material'}</span>
            </button>

            <button
              type="submit"
              className="btn-primary-gradient btn-start-learning"
              disabled={isLoading || (!topicInput.trim() && !selectedFile)}
            >
              {isLoading ? (
                <span>Generating Personalized Curriculum...</span>
              ) : (
                <>
                  <span>Start Learning</span>
                  <ArrowRight size={17} />
                </>
              )}
            </button>
          </div>
        </form>

        {/* Drag & Drop Upload Zone (Toggled) */}
        {showUploadZone && (
          <div
            className={`file-dropzone ${isDragOver ? 'drag-over' : ''}`}
            onDragOver={(e) => {
              e.preventDefault();
              setIsDragOver(true);
            }}
            onDragLeave={() => setIsDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              style={{ display: 'none' }}
              accept=".pdf,.docx,.doc,.pptx,.ppt,.txt,.md"
              onChange={(e) => handleFileSelect(e.target.files[0])}
            />
            <div className="dropzone-content">
              <div className="dropzone-icon-box">
                <Upload size={24} className="text-primary" />
              </div>
              <p className="dropzone-title">
                Drag & drop your course material, or <span className="text-primary">browse files</span>
              </p>
              <p className="dropzone-hint">
                Supports PDF, PPTX, Word Documents, TXT, Course Notes, and Research Papers
              </p>
            </div>
          </div>
        )}

        {/* Friendly Material Status Messages */}
        {fileProcessedStatus && (
          <div className="student-friendly-status-card">
            <div className="status-item">
              <CheckCircle2 size={16} className="text-emerald" />
              <span>Material processed successfully</span>
            </div>
            <div className="status-item">
              <CheckCircle2 size={16} className="text-emerald" />
              <span>Relevant curriculum concepts identified</span>
            </div>
            <div className="status-item">
              <Lightbulb size={16} className="text-amber" />
              <span>{fileProcessedStatus.message}</span>
            </div>
          </div>
        )}
      </div>

      {/* Quick Prompt Suggestions */}
      <div className="suggestions-section">
        <span className="suggestions-label">Popular topics to explore:</span>
        <div className="suggestions-pills-row">
          {promptSuggestions.map((sug, idx) => (
            <button
              key={idx}
              type="button"
              className="suggestion-pill"
              onClick={() => setTopicInput(sug)}
            >
              <span>{sug}</span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
