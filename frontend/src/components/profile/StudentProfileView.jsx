import React, { useState } from 'react';
import {
  User,
  GraduationCap,
  Sparkles,
  BookOpen,
  Award,
  AlertCircle,
  HelpCircle,
  CheckCircle2,
  Clock,
  Flame,
  Globe,
  Brain,
  Edit3,
  Save,
  Check,
  ArrowRight,
  TrendingUp
} from 'lucide-react';

export default function StudentProfileView({
  studentProfile,
  onUpdateProfile,
  onStartTopic
}) {
  const [isEditingPersonal, setIsEditingPersonal] = useState(false);
  const [activeSubjectTab, setActiveSubjectTab] = useState(0);

  // Form State
  const [fullName, setFullName] = useState(studentProfile?.personal_info?.full_name || 'Dhiraj Bhosale');
  const [institution, setInstitution] = useState(studentProfile?.personal_info?.institution || 'MMCOE');
  const [course, setCourse] = useState(studentProfile?.personal_info?.course || 'B.Tech');
  const [branch, setBranch] = useState(studentProfile?.personal_info?.branch || 'Information Technology');
  const [year, setYear] = useState(studentProfile?.personal_info?.year || '3rd Year');
  const [semester, setSemester] = useState(studentProfile?.personal_info?.semester || 6);

  // Learning Profile State
  const [selectedLanguage, setSelectedLanguage] = useState(studentProfile?.learning_profile?.preferred_language || 'hinglish');
  const [selectedGoals, setSelectedGoals] = useState(studentProfile?.learning_profile?.learning_goals || ['Exam Preparation', 'Concept Understanding']);
  const [selectedStyles, setSelectedStyles] = useState(studentProfile?.learning_profile?.learning_styles || ['Visual', 'Practical', 'Step-by-step', 'Analogy based']);
  const [dailyStudyTime, setDailyStudyTime] = useState(studentProfile?.learning_profile?.daily_study_time_minutes || 60);
  const [currentLevel, setCurrentLevel] = useState(studentProfile?.learning_profile?.current_level || 'intermediate');

  const allAvailableGoals = [
    { id: 'University Exam', label: '🎓 University Exam' },
    { id: 'Coding Skills', label: '💻 Coding Skills' },
    { id: 'Concept Understanding', label: '🧠 Concept Understanding' },
    { id: 'Interview Preparation', label: '💼 Interview Preparation' },
    { id: 'Project Development', label: '🚀 Project Development' },
    { id: 'Competitive Exams', label: '🏆 Competitive Exams' },
    { id: 'Certification', label: '📜 Certification' },
    { id: 'Quick Revision', label: '⚡ Quick Revision' },
  ];

  const allAvailableStyles = [
    'Visual', 'Practical', 'Step-by-step', 'Problem solving',
    'Examples first', 'Theory first', 'Analogy based',
    'Interactive', 'Fast revision', 'Deep learning'
  ];

  const languagesList = [
    { code: 'hinglish', label: '🇮🇳 Hinglish', desc: 'Conversational Hindi-English mix' },
    { code: 'en', label: '🇬🇧 English', desc: 'Standard formal English' },
    { code: 'hi', label: '🇮🇳 हिंदी (Hindi)', desc: 'Pure Devanagari Hindi' },
    { code: 'mr', label: '🇮🇳 मराठी (Marathi)', desc: 'Devanagari Marathi' },
  ];

  const toggleGoal = (goalId) => {
    if (selectedGoals.includes(goalId)) {
      setSelectedGoals(selectedGoals.filter((g) => g !== goalId));
    } else {
      setSelectedGoals([...selectedGoals, goalId]);
    }
  };

  const toggleStyle = (styleName) => {
    if (selectedStyles.includes(styleName)) {
      setSelectedStyles(selectedStyles.filter((s) => s !== styleName));
    } else {
      setSelectedStyles([...selectedStyles, styleName]);
    }
  };

  const handleSaveAll = () => {
    const updated = {
      personal_info: {
        ...studentProfile?.personal_info,
        full_name: fullName,
        institution,
        course,
        branch,
        year,
        semester: Number(semester)
      },
      learning_profile: {
        preferred_language: selectedLanguage,
        learning_goals: selectedGoals,
        learning_styles: selectedStyles,
        daily_study_time_minutes: Number(dailyStudyTime),
        current_level: currentLevel,
        preferred_difficulty: 'adaptive'
      }
    };
    onUpdateProfile?.(updated);
    setIsEditingPersonal(false);
  };

  const subjects = studentProfile?.subjects_mastery || [];
  const currentSubjectObj = subjects[activeSubjectTab] || subjects[0];
  const misconceptions = studentProfile?.misconceptions || [];
  const learningHistory = studentProfile?.learning_history || [];

  return (
    <div className="profile-page-container">
      {/* 1. LARGE PROFILE HEADER */}
      <section className="profile-header-card glass-panel">
        <div className="profile-header-left">
          <div className="profile-large-avatar">
            <span>{studentProfile?.personal_info?.avatar_initials || 'DB'}</span>
          </div>
          <div className="profile-header-meta">
            <div className="profile-name-row">
              <h1 className="profile-full-name">{fullName}</h1>
              <span className="profile-status-pill">
                <span className="status-live-dot" /> Active learner
              </span>
            </div>
            <p className="profile-degree-line">
              🎓 {course} in {branch} • {institution} ({year})
            </p>
            <div className="profile-tags-row">
              <span className="profile-sub-tag">Level: <strong>{currentLevel.toUpperCase()}</strong></span>
              <span className="profile-sub-tag">Semester: <strong>{semester}</strong></span>
              <span className="profile-sub-tag">Language: <strong>{selectedLanguage.toUpperCase()}</strong></span>
            </div>
          </div>
        </div>

        <button
          type="button"
          className="btn-secondary-light edit-profile-btn"
          onClick={() => setIsEditingPersonal(!isEditingPersonal)}
        >
          <Edit3 size={15} />
          <span>{isEditingPersonal ? 'Cancel Editing' : 'Edit Profile'}</span>
        </button>
      </section>

      {/* 2. PROFILE STATISTICS ROW */}
      <section className="profile-stats-bar glass-panel">
        <div className="p-stat-box">
          <span className="p-stat-val">{studentProfile?.lessons_completed || 24}</span>
          <span className="p-stat-lbl">Lessons</span>
        </div>
        <div className="p-stat-box">
          <span className="p-stat-val">{studentProfile?.hours_learned || 38}h</span>
          <span className="p-stat-lbl">Hours Learned</span>
        </div>
        <div className="p-stat-box">
          <span className="p-stat-val text-cyan">{studentProfile?.quiz_average || 86}%</span>
          <span className="p-stat-lbl">Quiz Average</span>
        </div>
        <div className="p-stat-box">
          <span className="p-stat-val text-orange">🔥 {studentProfile?.learning_streak_days || 7}d</span>
          <span className="p-stat-lbl">Current Streak</span>
        </div>
        <div className="p-stat-box">
          <span className="p-stat-val text-emerald">{studentProfile?.overall_mastery || 78}%</span>
          <span className="p-stat-lbl">Overall Mastery</span>
        </div>
      </section>

      {/* 3. PERSONAL INFORMATION FORM (Collapsible / Editable) */}
      {isEditingPersonal && (
        <section className="profile-form-section glass-panel">
          <div className="form-header-bar">
            <h3>👤 Edit Personal Information</h3>
            <span className="form-sub-hint">Update your student information used to personalize lessons.</span>
          </div>

          <div className="personal-form-grid">
            <div className="input-field">
              <label>Full Name</label>
              <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} />
            </div>

            <div className="input-field">
              <label>Institution / College</label>
              <input type="text" value={institution} onChange={(e) => setInstitution(e.target.value)} />
            </div>

            <div className="input-field">
              <label>Course</label>
              <input type="text" value={course} onChange={(e) => setCourse(e.target.value)} />
            </div>

            <div className="input-field">
              <label>Branch</label>
              <input type="text" value={branch} onChange={(e) => setBranch(e.target.value)} />
            </div>

            <div className="input-field">
              <label>Year</label>
              <input type="text" value={year} onChange={(e) => setYear(e.target.value)} />
            </div>

            <div className="input-field">
              <label>Semester</label>
              <input type="number" min="1" max="8" value={semester} onChange={(e) => setSemester(e.target.value)} />
            </div>
          </div>

          <div className="form-save-actions">
            <button type="button" className="btn-primary-gradient" onClick={handleSaveAll}>
              <Save size={16} />
              <span>Save Changes</span>
            </button>
          </div>
        </section>
      )}

      {/* 4. MY LEARNING PROFILE */}
      <section className="learning-profile-card glass-panel">
        <div className="card-header-with-badge">
          <div className="header-title-box">
            <Brain size={20} className="text-primary" />
            <h3>My Learning Profile</h3>
          </div>
          <span className="badge-pill">Influences AI Teacher Behavior</span>
        </div>

        {/* 6 Key Preferences Row */}
        <div className="pref-metrics-grid">
          <div className="pref-box">
            <span className="pref-lbl">Preferred Language</span>
            <span className="pref-val">{selectedLanguage === 'hinglish' ? '🇮🇳 Hinglish' : selectedLanguage === 'hi' ? '🇮🇳 हिंदी' : selectedLanguage === 'mr' ? '🇮🇳 मराठी' : '🇬🇧 English'}</span>
          </div>
          <div className="pref-box">
            <span className="pref-lbl">Learning Goal</span>
            <span className="pref-val">{selectedGoals[0] || 'Exam Preparation'}</span>
          </div>
          <div className="pref-box">
            <span className="pref-lbl">Learning Style</span>
            <span className="pref-val">{selectedStyles.slice(0, 2).join(' + ')}</span>
          </div>
          <div className="pref-box">
            <span className="pref-lbl">Current Level</span>
            <span className="pref-val">{currentLevel.toUpperCase()}</span>
          </div>
          <div className="pref-box">
            <span className="pref-lbl">Daily Study Time</span>
            <span className="pref-val">⏱ {dailyStudyTime} min</span>
          </div>
          <div className="pref-box">
            <span className="pref-lbl">Difficulty Mode</span>
            <span className="pref-val">⚡ Adaptive</span>
          </div>
        </div>

        {/* Language Selector */}
        <div className="pref-choice-block">
          <label className="pref-block-label">Primary Teaching Language:</label>
          <div className="lang-options-grid">
            {languagesList.map((lang) => (
              <button
                key={lang.code}
                type="button"
                className={`lang-card-btn ${selectedLanguage === lang.code ? 'active' : ''}`}
                onClick={() => setSelectedLanguage(lang.code)}
              >
                <span className="lang-title">{lang.label}</span>
                <span className="lang-desc">{lang.desc}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Learning Goals Multi-select Chips */}
        <div className="pref-choice-block">
          <label className="pref-block-label">Select Learning Goals:</label>
          <div className="chips-wrap">
            {allAvailableGoals.map((g) => {
              const isSel = selectedGoals.includes(g.id);
              return (
                <button
                  key={g.id}
                  type="button"
                  className={`choice-chip ${isSel ? 'selected' : ''}`}
                  onClick={() => toggleGoal(g.id)}
                >
                  <span>{g.label}</span>
                  {isSel && <Check size={13} />}
                </button>
              );
            })}
          </div>
        </div>

        {/* Learning Styles Multi-select Chips */}
        <div className="pref-choice-block">
          <label className="pref-block-label">Select Learning Styles:</label>
          <div className="chips-wrap">
            {allAvailableStyles.map((s) => {
              const isSel = selectedStyles.includes(s);
              return (
                <button
                  key={s}
                  type="button"
                  className={`choice-chip ${isSel ? 'selected' : ''}`}
                  onClick={() => toggleStyle(s)}
                >
                  <span>{s}</span>
                  {isSel && <Check size={13} />}
                </button>
              );
            })}
          </div>
        </div>

        <div className="pref-save-footer">
          <button type="button" className="btn-secondary-light" onClick={handleSaveAll}>
            <Save size={15} />
            <span>Update Learning Preferences</span>
          </button>
        </div>
      </section>

      {/* 5. SUBJECT & TOPIC MASTERY */}
      <section className="subject-mastery-card glass-panel">
        <div className="card-header-simple">
          <BookOpen size={20} className="text-primary" />
          <h3>My Subjects & Topic Mastery</h3>
        </div>

        {/* Subject Tab Bar */}
        <div className="subject-tab-bar">
          {subjects.map((sub, i) => (
            <button
              key={i}
              type="button"
              className={`subject-tab-btn ${activeSubjectTab === i ? 'active' : ''}`}
              onClick={() => setActiveSubjectTab(i)}
            >
              <span>{sub.subject}</span>
              <span className="sub-tab-score">{sub.overall_percentage}%</span>
            </button>
          ))}
        </div>

        {/* Topics Inside Selected Subject */}
        {currentSubjectObj && (
          <div className="topics-mastery-grid">
            {currentSubjectObj.topics.map((t, idx) => (
              <div key={idx} className="topic-mastery-item">
                <div className="topic-header-row">
                  <span className="topic-title">{t.name}</span>
                  <span className={`topic-status-tag tag-${t.status}`}>
                    {t.status === 'mastered' ? '✓ Mastered' : t.status === 'in_progress' ? 'In Progress' : 'Needs Practice'}
                  </span>
                </div>
                <div className="topic-bar-wrap">
                  <div className="progress-bar-track">
                    <div
                      className={`progress-bar-fill fill-${t.status}`}
                      style={{ width: `${t.mastery_percentage}%` }}
                    />
                  </div>
                  <span className="topic-pct-label">{t.mastery_percentage}%</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* 6. CONCEPTS I STRUGGLE WITH (Misconception Profile) */}
      <section className="misconception-profile-card glass-panel">
        <div className="card-header-simple">
          <AlertCircle size={20} className="text-amber" />
          <h3>Concepts I Struggle With (Misconception Profile)</h3>
        </div>
        <p className="card-subtitle-text">
          The AI Teacher tracks persistent conceptual confusions and adapts explanations in future lessons.
        </p>

        <div className="misconception-cards-list">
          {misconceptions.map((m, idx) => (
            <div key={idx} className="misconception-item-card">
              <div className="m-left">
                <h4 className="m-concept-title">{m.concept}</h4>
                <p className="m-text"><strong>Diagnosed Mental Model:</strong> “{m.misconception}”</p>
                <div className="m-meta">
                  <span>Attempts: <strong>{m.attempts}</strong></span>
                  <span>Mastery: <strong>{m.mastery_percentage}%</strong></span>
                  <span>Last Attempted: <strong>{m.last_attempted}</strong></span>
                </div>
              </div>
              <button
                type="button"
                className="btn-amber-action"
                onClick={() => onStartTopic?.(m.concept)}
              >
                <span>Review Concept</span>
                <ArrowRight size={14} />
              </button>
            </div>
          ))}
        </div>
      </section>

      {/* 7. LEARNING HISTORY */}
      <section className="learning-history-card glass-panel">
        <div className="card-header-simple">
          <TrendingUp size={20} className="text-indigo" />
          <h3>Learning History</h3>
        </div>

        <div className="history-table-container">
          <table className="history-table">
            <thead>
              <tr>
                <th>Topic</th>
                <th>Date</th>
                <th>Duration</th>
                <th>Quiz Score</th>
                <th>Mastery Gain</th>
                <th>Language</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {learningHistory.map((h, i) => (
                <tr key={i} onClick={() => onStartTopic?.(h.topic)} style={{ cursor: 'pointer' }}>
                  <td className="font-semibold text-primary">{h.topic}</td>
                  <td>{h.date}</td>
                  <td>{h.duration_minutes} min</td>
                  <td><span className="score-pill">{h.quiz_score_percentage}%</span></td>
                  <td className="text-emerald font-semibold">{h.mastery_delta}</td>
                  <td>{h.language}</td>
                  <td><span className="status-badge-done">✓ {h.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
