# ⚠️ Known Limitations & Future Roadmap
## AI Teacher — Human-Like Adaptive AI Educator

This document outlines the current architectural scope boundaries of **AI Teacher** (built for Round 2 of the AI Innovation Hackathon 2026) along with the planned evolution roadmap.

---

## Current Scope Boundaries

### 1. Language Support
- **Current**: Fully supports **English (`en`)**, **Hindi (`hi`)**, and **Hinglish (`hinglish`)** across curriculum planning, neural voice narration (Edge-TTS `en-US-JennyNeural`, `hi-IN-SwaraNeural`, `en-IN-NeerjaNeural`), smartboard typography, formative diagnostics, and live mid-lesson dynamic language switching without progress loss.
- **Future Roadmap**: Expansion to additional Indic languages (Tamil, Telugu, Bengali, Marathi) and European languages (Spanish, French, German) using multilingual Whisper and expanded Edge-TTS voice catalogs.

### 2. Interaction Input Modality
- **Current**: Formative check questions accept **typed natural language reasoning** and **interactive multiple-choice option selection**, accompanied by an in-lesson interactive "Ask AI Teacher" follow-up panel.
- **Future Roadmap**: Integration of real-time student microphone voice input powered by local Whisper STT for fully conversational voice-to-voice Q&A tutoring.

### 3. Session & Learner Profile Persistence
- **Current**: Active sessions and lessons are stored in an in-memory session registry with asynchronous persistence. Longitudinal learner mastery, quiz histories, topics studied, and accuracy trajectories are persisted locally to `backend/media/learner_progress.json` and served via `/api/lesson/progress`.
- **Future Roadmap**: PostgreSQL / Supabase cloud persistence with multi-tenant user authentication and spaced-repetition notification workflows.

### 4. Classroom Educator Animation
- **Current**:
  - **Articulated Vector Educator**: Full upper-body presentation with 6 pedagogical postures (`point_board`, `explain`, `question`, `praise`, `remediate`, `welcome`), breathing cycles, blinking state machines, pointer wand, and smartboard focus highlighting.
  - **GPU Mode**: Hook available for neural lip-sync avatar models (Wav2Lip / SadTalker).
- **Future Roadmap**: Real-time 3D WebGL / Three.js classroom teacher avatar rendered directly on the client to eliminate server-side video rendering latency.

### 5. Document Ingestion Types
- **Current**: Multi-format document parser handles **`.pdf`**, **`.docx`**, **`.pptx`**, **`.txt`**, and **`.md`** files with automatic page/slide splitting, table/heading detection, and scanned PDF detection that alerts the user with an OCR recommendation.
- **Future Roadmap**: Native optical character recognition (OCR) via Tesseract / PaddleOCR for handwritten notes and scanned paper textbooks.
