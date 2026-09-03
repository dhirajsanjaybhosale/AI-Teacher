import React, { useRef, useEffect, useState } from 'react';
import { Play, Pause, RotateCcw, Volume2, VolumeX, Maximize, Sparkles, AlertTriangle, FastForward } from 'lucide-react';
import { getFullMediaUrl } from '../api/client';

export default function VideoPlayer({
  videoUrl,
  segmentTitle,
  segmentIndex,
  totalSegments,
  isRemediation,
  onVideoEnded,
  isLoadingVideo,
  onTimeUpdate
}) {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [playbackRate, setPlaybackRate] = useState(1);

  const fullUrl = getFullMediaUrl(videoUrl);

  useEffect(() => {
    if (videoRef.current && fullUrl) {
      videoRef.current.load();
      videoRef.current.playbackRate = playbackRate;
      const playPromise = videoRef.current.play();
      if (playPromise !== undefined) {
        playPromise
          .then(() => setIsPlaying(true))
          .catch((err) => {
            console.log("Autoplay policy prevented audio play, waiting for user click:", err);
            setIsPlaying(false);
          });
      }
    }
  }, [fullUrl]);

  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play();
      setIsPlaying(true);
    }
  };

  const toggleMute = () => {
    if (!videoRef.current) return;
    videoRef.current.muted = !isMuted;
    setIsMuted(!isMuted);
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      const cur = videoRef.current.currentTime;
      setCurrentTime(cur);
      setDuration(videoRef.current.duration || 0);
      onTimeUpdate?.(cur);
    }
  };

  const handleSeek = (e) => {
    const time = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      setCurrentTime(time);
    }
  };

  const handleSpeedChange = () => {
    const nextRate = playbackRate === 1 ? 1.25 : playbackRate === 1.25 ? 1.5 : 1;
    setPlaybackRate(nextRate);
    if (videoRef.current) {
      videoRef.current.playbackRate = nextRate;
    }
  };

  const handleFullscreen = () => {
    if (videoRef.current) {
      if (videoRef.current.requestFullscreen) {
        videoRef.current.requestFullscreen();
      }
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
    if (onVideoEnded) {
      onVideoEnded();
    }
  };

  const formatTime = (sec) => {
    if (!sec || isNaN(sec)) return '00:00';
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
  };

  return (
    <div className={`video-player-card glass-panel ${isRemediation ? 'glass-panel-remedy' : 'glass-panel-glow'}`}>
      {/* Top Banner Status */}
      <div className="player-header-bar">
        <div className="player-status-badge">
          {isRemediation ? (
            <>
              <AlertTriangle size={16} className="text-amber" />
              <span className="badge-text-amber">Adaptive Re-Explanation • Clarifying Misconception</span>
            </>
          ) : (
            <>
              <Sparkles size={16} className="text-indigo" />
              <span className="badge-text-indigo">Interactive Segment {segmentIndex} of {totalSegments}</span>
            </>
          )}
        </div>
        <h2 className="player-title">{segmentTitle}</h2>
      </div>

      {/* Video Container */}
      <div className="video-viewport">
        {isLoadingVideo ? (
          <div className="video-skeleton">
            <div className="skeleton-pulse"></div>
            <p className="skeleton-text">Synthesizing audio & assembling visual segment video...</p>
          </div>
        ) : fullUrl ? (
          <>
            <video
              ref={videoRef}
              src={fullUrl}
              className="main-video-element"
              onTimeUpdate={handleTimeUpdate}
              onEnded={handleEnded}
              onPlay={() => setIsPlaying(true)}
              onPause={() => setIsPlaying(false)}
              playsInline
              onClick={togglePlay}
            />

            {/* Custom Bottom Controls */}
            <div className="video-controls-overlay">
              <input
                type="range"
                min="0"
                max={duration || 100}
                value={currentTime}
                onChange={handleSeek}
                className="video-progress-slider"
              />

              <div className="controls-row">
                <div className="controls-left">
                  <button type="button" className="ctrl-btn" onClick={togglePlay} title={isPlaying ? "Pause" : "Play"}>
                    {isPlaying ? <Pause size={20} /> : <Play size={20} />}
                  </button>

                  <button type="button" className="ctrl-btn" onClick={toggleMute} title={isMuted ? "Unmute" : "Mute"}>
                    {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
                  </button>

                  <span className="ctrl-time">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </span>
                </div>

                <div className="controls-right">
                  <button type="button" className="ctrl-speed-btn" onClick={handleSpeedChange} title="Playback Speed">
                    <FastForward size={14} />
                    <span>{playbackRate}x</span>
                  </button>

                  <button type="button" className="ctrl-btn" onClick={handleFullscreen} title="Fullscreen">
                    <Maximize size={18} />
                  </button>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div className="video-empty-state">
            <p>No video segment loaded.</p>
          </div>
        )}
      </div>
    </div>
  );
}
