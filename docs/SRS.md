# 📋 Software Requirements Specification (SRS)
## AI Teacher — Round 2 AI Innovation Hackathon 2026

---

## 1. System Overview & Purpose
**AI Teacher** is an interactive, multi-modal educational application designed to replace static textbooks and passive video lectures with an autonomous, adaptive teaching loop. The system ingests structured content (PDFs or user topics), generates a time-budgeted multi-segment curriculum, narrates it with a talking avatar and synchronized slide deck, checks comprehension with formative embedded questions, diagnoses mental misconceptions, generates on-the-fly remediation videos, and outputs a summative assessment feedback report.

---

## 2. Functional Requirements (FR)

### FR-1: Multi-Modal Ingestion & Retrieval
- **FR-1.1**: The system shall accept PDF document uploads up to 50MB.
- **FR-1.2**: Extracted text shall be segmented into semantic sliding windows with metadata retention.
- **FR-1.3**: Chunks shall be embedded using local dense vectors (`all-MiniLM-L6-v2`) and indexed via FAISS.
- **FR-1.4**: If free-text topic is provided, the system shall bypass PDF parsing and generate structured curriculum from LLM domain knowledge.

### FR-2: Lesson Planning & Pedagogical Structuring
- **FR-2.1**: The system shall dynamically scale the number of instructional segments to the time budget (e.g. 5 min = 2 segments; 10 min = 3 segments; 20 min = 5 segments).
- **FR-2.2**: The curriculum shall adapt vocabulary and depth to the learner level (*Beginner*, *Intermediate*, *Advanced*).
- **FR-2.3**: The planner shall support English (`en`) and Hindi (`hi`), outputting all titles, explanations, bullet points, and check questions directly in the target language.

### FR-3: Voice Narration, Avatar Animation & Video Compositing
- **FR-3.1**: The system shall synthesize neural speech in English and Hindi using `edge-tts` (with `pyttsx3` fallback).
- **FR-3.2**: Audio amplitude envelopes shall be calculated at 25 fps to drive phonetic mouth movements (4 states: closed, slight open, medium open, wide open).
- **FR-3.3**: The system shall detect GPU on startup and choose between neural lip-sync (GPU) and 2D synced animated avatar (CPU).
- **FR-3.4**: Visual slide overlays (header, bullet cards, analogy banner, subtitles, progress bar) and audio shall be compiled into H.264/AAC MP4 videos using FFmpeg.

### FR-4: Formative Assessment & Misconception Remediation Loop
- **FR-4.1**: Following each segment video, a formative check question shall appear with multiple options and free-form text input.
- **FR-4.2**: The LLM evaluator shall assess semantic correctness and diagnose the exact underlying misconception when incorrect.
- **FR-4.3**: Upon misconception detection, the system shall synthesize an adaptive remediation segment using a novel analogy and dynamically render a new video segment on-the-fly.

### FR-5: Summative Assessment & Analytics Reporting
- **FR-5.1**: Upon completing all segments, the system shall generate a 3–5 question multiple-choice quiz covering all lesson concepts.
- **FR-5.2**: The scorer shall calculate total score, percentage, mastered concepts, and weak concepts.
- **FR-5.3**: A feedback report shall be generated displaying a score gauge, strength/weakness cards, actionable study recommendations, and a 1-click launch button for the next recommended topic.

---

## 3. Non-Functional Requirements (NFR)

- **NFR-1 (Zero Paid APIs)**: The entire stack must operate with zero paid API dependencies.
- **NFR-2 (Performance)**: Video rendering for any segment must complete within ~15–30 seconds on standard CPU hardware to maintain live demo usability.
- **NFR-3 (Reliability & Fault-Tolerance)**: If external LLM or TTS services experience network timeouts, built-in offline fallbacks must ensure continuous uninterrupted operation.
- **NFR-4 (Accessibility & Multi-Lingual)**: Seamless multi-lingual support for English and Hindi across UI, voice narration, slide typography, and evaluations.
