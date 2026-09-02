import React, { useState, useRef } from 'react';
import {
  Sparkles,
  Upload,
  BookOpen,
  ArrowRight,
  FileText,
  CheckCircle2,
  X,
  HelpCircle,
  Layers,
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

  const promptSuggestions = [
    "Explain Binary Search",
    "Teach me Operating Systems",
    "Explain Newton's Laws",
    "Help me understand DBMS normalization",
    "Teach me React Hooks",
    "How does TCP vs UDP work?",
    "Photosynthesis & Light Reactions"
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
      level: studentProfile?.learning_profile?.current_level || 'intermediate',
      language: studentProfile?.learning_profile?.preferred_language || 'hinglish',
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
        <h1 className="learn-main-title">What would you like to learn today?</h1>
        <p className="learn-subtitle">
          Ask any concept across Computer Science, Engineering, Physics, or Mathematics — or upload your course notes.
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
              placeholder="Ask me anything... (e.g. Explain Binary Search, Teach me DBMS Normalization)"
              value={topicInput}
              onChange={(e) => setTopicInput(e.target.value)}
              disabled={isLoading}
            />
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
                <span>Preparing Your Lesson...</span>
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
