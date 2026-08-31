# 🤖 AI Teacher — Adaptive Pedagogical Video Platform
### Round 2 Submission — AI Innovation Hackathon 2026

**AI Teacher** is a full-stack, autonomous, adaptive educational studio that transforms textbook chapters (PDFs) or topic prompts into interactive, structured, multi-segment narrated lessons featuring a talking AI avatar, synchronized visual slide decks, formative misconception-diagnosing check questions, on-the-fly remediation video generation, and summative mastery quizzes with comprehensive analytical feedback reports.

---

## 🌟 Key Highlights & Architectural Features

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

```
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
│   │   └── session_store.py      # Active lesson and quiz session manager
│   ├── main.py                   # FastAPI application server entrypoint
│   ├── requirements.txt          # Python dependencies
│   └── .env.example              # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── api/client.js         # API integration client
│   │   ├── components/           # UI components (Header, UploadOrTopicForm, VideoPlayer, QuestionPrompt, QuizView, FeedbackReport, LoadingOverlay)
│   │   ├── App.jsx               # Main application controller
│   │   ├── App.css               # Component styles
│   │   └── index.css             # Design tokens & glassmorphic system
│   └── package.json
├── sample_data/
│   └── cellular_respiration_chapter.pdf   # Pre-packaged PDF chapter for instant live testing
├── docs/
│   ├── README.md
│   ├── THIRD_PARTY_TOOLS.md
│   ├── SRS.md
│   └── KNOWN_LIMITATIONS.md
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
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Configure environment variables
copy .env.example .env

# Start FastAPI backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
The backend API is accessible at `http://127.0.0.1:8000` (Swagger docs: `http://127.0.0.1:8000/docs`).

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

## 🎬 How to Run the Demo

1. Open `http://127.0.0.1:5173`.
2. Click **"⚡ Load Sample Chapter: Cellular Respiration (PDF)"** (or upload your own PDF or type any topic).
3. Select your preferred **Target Level** (*Beginner*), **Time Budget** (*5 Min*), and **Language** (*English* or *Hindi*).
4. Click **"Launch Interactive AI Teacher Lesson"**.
5. Watch the animated avatar teach **Segment 1** with synchronized slides and subtitles.
6. When the video ends, the **Formative Check Question** appears:
   - **To test the Adaptive Remediation Loop**: Type or select an incorrect answer (e.g. *"The cell directly burns glucose without making ATP"*).
   - Observe how the AI diagnoses the exact misconception (*"Conflated storage fuel with currency"*), synthesizes a new remediation script, and renders a new video segment on-the-fly!
   - Click **"Watch Custom Re-Explanation Video"** to watch the remediation clip.
7. Submit a correct answer to advance.
8. Complete the **Summative Quiz** to view the **Pedagogical Mastery Report** with your score gauge, understood concepts, review areas, and recommended next topic.
