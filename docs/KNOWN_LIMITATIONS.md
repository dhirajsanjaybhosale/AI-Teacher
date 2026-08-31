# ⚠️ Known Limitations & Future Roadmap

This document outlines the current architectural scope boundaries of **AI Teacher** (built for Round 2 of the AI Innovation Hackathon 2026) along with the planned evolution roadmap.

---

## Current Scope Limitations

### 1. Language Support
- **Current**: Fully supports **English (`en`)** and **Hindi (`hi`)** across text planning, neural voice narration (Edge-TTS), slide typography (Unicode / Devanagari), and formative diagnostics.
- **Future Roadmap**: Expansion to additional Indic languages (Tamil, Telugu, Bengali, Marathi) and European languages (Spanish, French, German) using multilingual Whisper and expanded Edge-TTS voice catalogs.

### 2. Interaction Input Modality
- **Current**: Formative check questions accept **typed text responses** and **interactive multiple-choice option selection**.
- **Future Roadmap**: Integration of real-time student microphone voice input powered by local Whisper STT for fully conversational voice-to-voice Q&A tutoring.

### 3. Session & Learner Profile Persistence
- **Current**: Active sessions, lesson plans, remediation trees, and quiz submissions are maintained in an in-memory session registry for fast hackathon demo performance.
- **Future Roadmap**: SQLite / PostgreSQL relational database integration with user authentication, long-term spaced repetition scheduling, and longitudinal learner mastery trajectory tracking.

### 4. Hardware Avatar Rendering Performance
- **Current**:
  - On **CUDA GPUs**: Full neural lip-sync pipeline hook (Wav2Lip / SadTalker).
  - On **CPUs**: Synchronized 2D vector animated avatar with 4 discrete phonetic mouth shapes, blinking state machines, and audio visualizers rendering at ~15-20 seconds per segment.
- **Future Roadmap**: Pre-compiling WebAssembly / WebGL client-side real-time avatar animation shaders to eliminate server-side video rendering latencies entirely.

### 5. Document Ingestion Types
- **Current**: Ingestion supports standard text and structured layout PDFs via PyMuPDF. Scanned image-only PDFs without an OCR layer require optical character recognition.
- **Future Roadmap**: Integration of Tesseract / PaddleOCR for handwritten notes and scanned textbook page transcription.
