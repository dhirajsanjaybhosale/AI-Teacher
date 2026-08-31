# 🤖 AI Teacher — Human-Like Adaptive AI Educator
### AI Innovation Hackathon 2026 — Round 2

**AI Teacher** is a full-stack, autonomous, adaptive educational platform that transforms textbook chapters (PDFs) or topic prompts into interactive, structured, multi-segment narrated lessons featuring a talking AI avatar, synchronized visual slide decks, formative misconception-diagnosing check questions, on-the-fly remediation video generation, and summative mastery quizzes with comprehensive analytical feedback reports.

---

## 💡 The Problem & The Solution

- **The Problem**: Traditional digital learning platforms (videos, static quizzes, generic chatbots) fail to behave like real human teachers. When a student misunderstands a concept, standard platforms either just say "Incorrect" or provide the same canned explanation repeatedly.
- **The Solution**: An AI Educator that follows the true human teaching lifecycle:
  $$\text{Understand} \longrightarrow \text{Plan} \longrightarrow \text{Explain} \longrightarrow \text{Demonstrate} \longrightarrow \text{Question} \longrightarrow \text{Evaluate} \longrightarrow \text{Adapt} \longrightarrow \text{Continue} \longrightarrow \text{Assess} \longrightarrow \text{Recommend}$$

The **adaptive teaching loop is the core innovation**: when a student submits an incorrect answer, the system semantically diagnoses their specific mental model misconception, formulates an alternative explanation with a fresh intuitive analogy, dynamically synthesizes a targeted remediation video clip on the fly, and re-evaluates their comprehension.

---

## 🏛️ System Architecture

```text
                                 USER INTERFACE (React 19 + Vite)
      ┌──────────────────────────────────────────────────────────────────────────────────┐
      │  • PDF Dropzone / Topic Prompt Selector                                           │
      │  • Personalization Matrix: Level (Beginner/Inter/Adv), Time (5-60m), Lang (EN/HI)│
      │  • Interactive Studio: Video Player + Formative Q&A Dock + Confetti Feedback     │
      │  • Summative Mastery Quiz + Circular Mastery Gauge + Learning Horizon Pathway    │
      └────────────────────────────────────────┬─────────────────────────────────────────┘
                                               │ HTTP / REST APIs
                                               ▼
                              BACKEND SERVICE (FastAPI + Uvicorn)
      ┌──────────────────────────────────────────────────────────────────────────────────┐
      │                                                                                  │
      │  ┌────────────────────────────────────────────────────────────────────────────┐  │
      │  │ 1. RAG Ingestion Pipeline                                                  │  │
      │  │    PDF ──> PyMuPDF ──> Semantic Chunker ──> sentence-transformers          │  │
      │  │                         (all-MiniLM-L6-v2) ──> FAISS Vector Index          │  │
      │  └─────────────────────────────────────┬──────────────────────────────────────┘  │
      │                                        │ Top-k Context                           │
      │  ┌─────────────────────────────────────▼──────────────────────────────────────┐  │
      │  │ 2. Curriculum & Lesson Planner (LLM Abstraction Layer)                    │  │
      │  │    GeminiProvider / GroqProvider / OfflineDomainEngine                     │  │
      │  │    Outputs Structured JSON: Segments, Narrations, Analogies, Questions     │  │
      │  └─────────────────────────────────────┬──────────────────────────────────────┘  │
      │                                        │ Segment Script & Keypoints              │
      │  ┌─────────────────────────────────────▼──────────────────────────────────────┐  │
      │  │ 3. Narration & Video Compositor                                            │  │
      │  │    • TTS: Edge-TTS (en-US-Jenny / hi-IN-Swara) / pyttsx3 fallback          │  │
      │  │    • RMS Audio Envelope Analysis (25 fps energy extraction)                │  │
      │  │    • Avatar Engine: GPU (Wav2Lip/SadTalker) OR CPU (2D Vector Mouth States)│  │
      │  │    • Slide Deck: Cosmic Tech Frame + Badges + Bullets + Subtitle Ticker    │  │
      │  │    • FFmpeg Pipeline ──> Playable H.264/AAC MP4                            │  │
      │  └─────────────────────────────────────┬──────────────────────────────────────┘  │
      │                                        │ Playable MP4 Video Stream               │
      │  ┌─────────────────────────────────────▼──────────────────────────────────────┐  │
      │  │ 4. Formative Interaction & Adaptive Remediation Loop                       │  │
      │  │    • Student Answer ──> Semantic Evaluator (LLM)                           │  │
      │  │    • If Incorrect: Diagnose Specific Mental Model Misconception            │  │
      │  │    • Synthesize Novel Re-explanation + Fresh Analogy                       │  │
      │  │    • Dynamically Render New Video Clip ──> Re-present to Learner           │  │
      │  └─────────────────────────────────────┬──────────────────────────────────────┘  │
      │                                        │ Quiz Generation & Final Assessment      │
      │  ┌─────────────────────────────────────▼──────────────────────────────────────┐  │
      │  │ 5. Summative Assessment & Analytical Report Generator                     │  │
      │  │    • Multi-Question Quiz (MCQ / Application / Conceptual)                  │  │
      │  │    • Mastery Scoring + Concepts Mastered vs Weak Areas                     │  │
      │  │    • Actionable Guidance + Next Topic Recommendation (1-Click Launch)      │  │
      │  └────────────────────────────────────────────────────────────────────────────┘  │
      └──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌟 Key Highlights & Features

1. **RAG-Grounded Ingestion Pipeline**:
   - Parses complex PDF chapters with **PyMuPDF**, chunks content into overlapping semantic windows, and generates high-dimensional embeddings locally with **`sentence-transformers` (`all-MiniLM-L6-v2`)**.
   - Vector indexing and top-$k$ context retrieval powered by **FAISS**.

2. **Unified Free-Tier LLM Abstraction**:
   - First-class support for **Google Gemini** (`GEMINI_API_KEY`) and **Groq** (`GROQ_API_KEY`).
   - Includes an intelligent offline domain engine ensuring an unbreakable, reliable live judging demonstration even with zero API keys configured.

3. **Neural Voice Narration & Audio Envelope Analysis**:
   - Natural spoken speech generation for both **English** (`en-US-JennyNeural` / `en-US-GuyNeural`) and **Hindi** (`hi-IN-SwaraNeural` / `hi-IN-MadhurNeural`) using **`edge-tts`** with offline **`pyttsx3`** fallback.
   - Calculates 25fps normalized audio amplitude and RMS energy envelopes for synchronized lip animation and visualizer waveforms.

4. **GPU-Aware Avatar & Video Compositing Engine**:
   - Automatically detects CUDA GPU availability at startup.
   - **GPU Mode**: Enables neural lip-synced avatar generation (Wav2Lip / SadTalker).
   - **CPU Mode (Fallback)**: Seamlessly engages a synchronized 2D vector animated avatar with 4 phonetic mouth shapes, natural blinking state machines, and reactive audio visualizers.
   - **FFmpeg Compositor**: Assembles teacher portrait, cosmic tech slide cards, lesson badges, key takeaway bullets, analogy banners, subtitles, and progress bars into crisp 720p H.264/AAC MP4 files.

5. **Formative Assessment & Misconception Remediation Loop**:
   - The core differentiator: when a student answers incorrectly, the AI diagnostician isolates the **specific mental model misconception** (not just marking it wrong), generates a custom re-explanation from a novel intuitive angle or concrete analogy, dynamically renders a new remediation video clip on the fly, and re-presents it to the learner.

6. **Summative Assessment & Analytics Feedback Report**:
   - Concludes with a 3–5 question multiple-choice mastery quiz.
   - Generates a visual mastery gauge, identifies strengths (concepts mastered), isolates focus areas (weak concepts), provides targeted study tips, and recommends the next learning horizon with a 1-click launch button.

---

## 📂 Repository Structure

```text
AI-Teacher/
├── backend/
│   ├── app/
│   │   ├── api/                  # FastAPI REST routes (lesson, segment, interact, assessment)
│   │   ├── assessment/           # Quiz generator, quiz scorer, feedback report builder
│   │   ├── ingestion/            # PDF parser, chunker, sentence embedder, FAISS retriever
│   │   ├── interaction/          # Answer evaluator & adaptive misconception remediation engine
│   │   ├── lesson_planning/      # Pydantic schemas & multi-segment curriculum planner
│   │   ├── llm/                  # Unified LLM provider (Gemini + Groq + Offline Engine)
│   │   ├── narration_avatar/     # Neural TTS, GPU/CPU avatar engine, FFmpeg video assembler
│   │   ├── services/             # GPU detection, storage manager, LLM factory
│   │   └── session_store.py      # Active lesson and quiz session manager
│   ├── main.py                   # FastAPI application server entrypoint
│   ├── requirements.txt          # Python dependencies
│   ├── test_demo_flow.py         # Automated QA & end-to-end verification script
│   └── .env.example              # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── api/client.js         # API integration client
│   │   ├── components/           # UI components (Header, UploadOrTopicForm, VideoPlayer, QuestionPrompt, QuizView, FeedbackReport, LoadingOverlay)
│   │   ├── App.jsx               # Main application controller
│   │   ├── App.css               # Component styles & design system
│   │   └── index.css             # Base tokens & dark-mode styling
│   ├── public/
│   │   ├── sample_chapter.pdf    # Sample 1: Electricity & Ohm's Law
│   │   └── cellular_respiration_chapter.pdf # Sample 2: Cellular Respiration
│   └── package.json
├── sample_data/
│   ├── sample_chapter.pdf        # Electricity & Ohm's Law chapter
│   ├── cellular_respiration_chapter.pdf # Biology chapter
│   ├── generate_electricity_pdf.py
│   └── generate_sample_pdf.py
├── docs/
│   ├── THIRD_PARTY_TOOLS.md      # Comprehensive tool, license, and model documentation
│   ├── KNOWN_LIMITATIONS.md      # Transparent scope limitations & future roadmap
│   └── SRS.md                    # System requirements specification
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm
- (Optional) `GEMINI_API_KEY` or `GROQ_API_KEY`

### 1. Backend Setup
```bash
cd backend

# Create virtual environment (optional)
python -m venv venv
# Windows activation:
.\venv\Scripts\activate
# Linux/macOS activation:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure environment variables
copy .env.example .env

# Start FastAPI backend
python main.py
# Or with uvicorn directly:
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API is accessible at `http://127.0.0.1:8000` (Swagger interactive docs: `http://127.0.0.1:8000/docs`).

### 2. Frontend Setup
```bash
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```
Open `http://127.0.0.1:5173` in your browser.

---

## 🧪 Automated Verification Suite

To verify the complete 7-stage end-to-end pipeline automatically:
```bash
cd backend
python test_demo_flow.py
```
This automatically verifies:
1. System Health & Hardware Mode Detection
2. PDF Ingestion, Chunking, Embedding, FAISS Indexing & RAG Retrieval
3. Adaptive Lesson Planning & Curriculum Generation
4. Neural TTS Synthesis & RMS Audio Amplitude Analysis
5. Talking Avatar Frame Generation & FFmpeg Video Assembly
6. Formative Assessment: Misconception Diagnosis & Adaptive Reteaching Video Loop
7. Summative Assessment: Quiz Generation, Scoring, and Feedback Reporting

---

## 🎬 Hackathon Live Demo Walkthrough

### Scenario: The Electricity & Ohm's Law Masterclass
1. Open `http://127.0.0.1:5173`.
2. In the setup screen, click **"⚡ Sample 1: Electricity & Ohm's Law (PDF)"** (or upload any PDF / type any topic).
3. Set **Target Level** to *Beginner*, **Time Budget** to *5 Min (or custom)*, and **Language** to *English (or Hindi)*.
4. Click **"Launch Interactive AI Teacher Lesson"**.
5. **Watch Segment 1**: Dr. Nova explains Voltage, Current, and Resistance with synchronized slide deck, key takeaway cards, audio visualizers, and subtitle ticker.
6. **Formative Check**:
   - Enter an incorrect answer (e.g., *"Current increases when resistance increases because more resistance creates more friction"*).
   - **Observe Adaptation**: The AI diagnoses the exact misconception (*"Student believes current increases with resistance, confusing inverse with direct proportionality"*), generates a fresh water-pipe analogy, and synthesizes a **custom remediation video clip on the spot**!
   - Click **"Watch Custom Re-Explanation Video"** to view the remedial video.
7. Submit the correct answer to advance.
8. Complete the **Summative Mastery Quiz**.
9. Review the **Pedagogical Mastery Report** with your score gauge, mastered concepts, areas for review, and 1-click button to launch the recommended next topic (*"Advanced Conceptual Principles"*).

