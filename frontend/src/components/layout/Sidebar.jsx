import React from 'react';
import {
  LayoutDashboard,
  BookOpen,
  GraduationCap,
  TrendingUp,
  Milestone,
  CalendarDays,
  User,
  Settings,
  Sparkles
} from 'lucide-react';

export default function Sidebar({ activeNav, onSelectNav, studentProfile }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'learn', label: 'Learn', icon: BookOpen },
    { id: 'classroom', label: 'AI Teacher', icon: GraduationCap },
    { id: 'progress', label: 'My Progress', icon: TrendingUp },
    { id: 'path', label: 'Learning Path', icon: Milestone },
    { id: 'study_plan', label: 'Study Plan', icon: CalendarDays },
    { id: 'profile', label: 'My Profile', icon: User },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const studentName = studentProfile?.personal_info?.full_name || 'Dhiraj Bhosale';
  const studentCourse = studentProfile?.personal_info?.branch
    ? `${studentProfile.personal_info.course || 'B.Tech'} ${studentProfile.personal_info.branch}`
    : 'B.Tech IT';
  const avatarInitials = studentProfile?.personal_info?.avatar_initials || 'DB';

  return (
    <aside className="app-sidebar">
      {/* Brand Header */}
      <div className="sidebar-brand" onClick={() => onSelectNav('dashboard')}>
        <div className="sidebar-logo-icon">
          <GraduationCap size={24} className="text-primary-gradient" />
        </div>
        <div className="sidebar-brand-text">
          <span className="sidebar-brand-title">AI Teacher</span>
          <span className="sidebar-brand-tag">PERSONAL CLASSROOM</span>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeNav === item.id;
          return (
            <button
              key={item.id}
              type="button"
              className={`sidebar-nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onSelectNav(item.id)}
            >
              <Icon size={19} className="nav-item-icon" />
              <span className="nav-item-label">{item.label}</span>
              {item.id === 'classroom' && (
                <span className="nav-live-dot" title="Active Classroom" />
              )}
            </button>
          );
        })}
      </nav>

      {/* Bottom Mini Student Profile */}
      <div
        className="sidebar-user-card"
        onClick={() => onSelectNav('profile')}
        title="View Student Profile"
      >
        <div className="user-avatar-circle">
          <span>{avatarInitials}</span>
          <span className="user-online-status" />
        </div>
        <div className="user-card-meta">
          <span className="user-card-name">{studentName}</span>
          <span className="user-card-sub">{studentCourse}</span>
        </div>
      </div>
    </aside>
  );
}
