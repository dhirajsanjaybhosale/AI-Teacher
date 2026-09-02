import React, { useState } from 'react';
import { Search, Globe, Bell, Sparkles, ChevronDown } from 'lucide-react';

export default function TopHeader({
  studentProfile,
  language = 'hinglish',
  onSwitchLanguage,
  onGlobalSearch,
  onOpenProfile
}) {
  const [searchValue, setSearchValue] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showLangMenu, setShowLangMenu] = useState(false);

  const studentName = studentProfile?.personal_info?.full_name || 'Dhiraj Bhosale';
  const avatarInitials = studentProfile?.personal_info?.avatar_initials || 'DB';

  const languages = [
    { code: 'en', label: 'English', flag: '🇬🇧' },
    { code: 'hinglish', label: 'Hinglish', flag: '🇮🇳' },
    { code: 'hi', label: 'हिंदी (Hindi)', flag: '🇮🇳' },
    { code: 'mr', label: 'मराठी (Marathi)', flag: '🇮🇳' },
  ];

  const currentLangObj = languages.find(
    (l) => l.code === (language || 'hinglish').toLowerCase()
  ) || languages[1];

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchValue.trim()) {
      onGlobalSearch?.(searchValue.trim());
      setSearchValue('');
    }
  };

  return (
    <header className="top-header">
      {/* Search Input Bar */}
      <form onSubmit={handleSearchSubmit} className="header-search-box">
        <Search size={17} className="search-icon" />
        <input
          type="text"
          placeholder="What do you want to learn today? (e.g. Binary Search, React Hooks)..."
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          className="search-input"
        />
        <kbd className="search-kbd">↵ Enter</kbd>
      </form>

      {/* Right Actions */}
      <div className="header-right-actions">
        {/* Language Selector Dropdown */}
        <div className="header-dropdown-wrap">
          <button
            type="button"
            className="header-pill-btn lang-pill"
            onClick={() => setShowLangMenu(!showLangMenu)}
          >
            <Globe size={15} className="text-primary" />
            <span className="lang-code-text">{currentLangObj.label}</span>
            <ChevronDown size={13} className="chevron-icon" />
          </button>

          {showLangMenu && (
            <div className="header-dropdown-menu">
              <div className="dropdown-label">Select Teaching Language</div>
              {languages.map((l) => (
                <button
                  key={l.code}
                  type="button"
                  className={`dropdown-menu-item ${l.code === currentLangObj.code ? 'active' : ''}`}
                  onClick={() => {
                    onSwitchLanguage?.(l.code);
                    setShowLangMenu(false);
                  }}
                >
                  <span className="menu-item-flag">{l.flag}</span>
                  <span className="menu-item-text">{l.label}</span>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Notification Bell */}
        <div className="header-dropdown-wrap">
          <button
            type="button"
            className="header-icon-btn"
            onClick={() => setShowNotifications(!showNotifications)}
            title="Notifications"
          >
            <Bell size={18} />
            <span className="notification-badge" />
          </button>

          {showNotifications && (
            <div className="header-dropdown-menu notification-menu">
              <div className="dropdown-header">
                <span>Notifications</span>
                <span className="badge-chip">1 New</span>
              </div>
              <div className="notification-list">
                <div className="notification-item">
                  <div className="notif-dot" />
                  <div className="notif-content">
                    <p className="notif-title">AI Teacher Recommendation</p>
                    <p className="notif-desc">Revise Graph Representation before starting DFS for optimal retention.</p>
                    <span className="notif-time">10m ago</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* User Mini Chip */}
        <button
          type="button"
          className="header-user-chip"
          onClick={onOpenProfile}
          title="Open Profile"
        >
          <div className="header-avatar-circle">
            <span>{avatarInitials}</span>
          </div>
          <span className="header-user-name">{studentName.split(' ')[0]}</span>
        </button>
      </div>
    </header>
  );
}
