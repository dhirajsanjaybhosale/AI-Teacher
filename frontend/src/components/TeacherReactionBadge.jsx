import React from 'react';
import { Sparkles, Brain, CheckCircle, AlertCircle, Volume2, HelpCircle } from 'lucide-react';

export default function TeacherReactionBadge({
  teachingState, // 'teaching' | 'waiting' | 'evaluating' | 'correct' | 'remediating'
  teacherName = "Dr. Nova",
  conceptName = "",
  speechSnippet = ""
}) {
  const getBadgeContent = () => {
    switch (teachingState) {
      case 'correct':
        return {
          icon: <CheckCircle size={18} className="text-emerald animate-bounce" />,
          title: `${teacherName} • Celebrating Mastery!`,
          message: "“Brilliant! You grasped the underlying principle completely. Let's build upon this!”",
          styleClass: "badge-state-correct"
        };
      case 'remediating':
        return {
          icon: <AlertCircle size={18} className="text-amber animate-pulse" />,
          title: `${teacherName} • Reassuring & Adapting`,
          message: speechSnippet || "“You're very close! Let's approach this differently using an intuitive real-world analogy.”",
          styleClass: "badge-state-remedy"
        };
      case 'evaluating':
        return {
          icon: <Brain size={18} className="text-cyan animate-spin" />,
          title: `${teacherName} • Diagnosing Mental Model...`,
          message: "Analyzing your pedagogical reasoning and verifying core conceptual relationships...",
          styleClass: "badge-state-evaluating"
        };
      case 'waiting':
        return {
          icon: <HelpCircle size={18} className="text-indigo animate-pulse" />,
          title: `${teacherName} • Attentively Listening`,
          message: "“Take your time to think it through. Formulate your reasoning in your own words!”",
          styleClass: "badge-state-waiting"
        };
      default:
        return {
          icon: <Sparkles size={18} className="text-indigo" />,
          title: `${teacherName} • Actively Teaching & Gesturing`,
          message: `Presenting step-by-step mechanisms for ${conceptName || 'this concept'} on the smartboard.`,
          styleClass: "badge-state-teaching"
        };
    }
  };

  const badge = getBadgeContent();

  return (
    <div className={`teacher-reaction-dock glass-panel ${badge.styleClass}`}>
      <div className="reaction-header">
        <div className="reaction-icon-wrapper">
          {badge.icon}
        </div>
        <div className="reaction-meta">
          <span className="reaction-teacher-title">{badge.title}</span>
          <p className="reaction-speech-bubble">{badge.message}</p>
        </div>
      </div>
    </div>
  );
}
