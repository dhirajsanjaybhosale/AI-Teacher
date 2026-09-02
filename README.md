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

1. **Articulated Classroom Educator (Dr. Nova)**:
   - Not a static talking head or flat avatar: Dr. Nova features full upper-body educator presentation with articulated shoulders, blazer, spectacles, blinking state machine, and natural sinusoidal breathing cycles.
   - 6 pedagogical postures:
     - `point_board`: Turns torso and eyes right, using a golden-tipped pointer wand to direct student focus to smartboard equations and diagrams.
     - `explain`: Conversational arm and finger cadence moving in sync with speech amplitude.
     - `question`: Inquisitive expression, raised eyebrow, hand resting thoughtfully at chin.
     - `praise`: Celebratory double thumbs-up with bright beaming smile on concept mastery.
     - `remediate`: Empathetic reassuring posture, placing hand gently over the heart.
     - `welcome`: Welcoming posture introducing the lesson objectives.
   - Synchronized smartboard highlights: formula and key concept cards illuminate with a glowing focus border when the teacher points to them.

2. **Digital Classroom Smartboard (`ClassroomBoard`)**:
   - Modern interactive teaching board rendered alongside or split-screen with the teacher video.
   - Subject-aware visual presentations:
     - **Mathematics & Physics**: Large formatted formulas (e.g. $V = I \times R$) with component breakdowns.
     - **Computer Science & Programming**: Syntax-highlighted code blocks with execution flow.
     - **Sciences & Processes**: Step-by-step numbered visual workflow capsules.
     - **Trade-offs & Differences**: Side-by-side comparative analysis cards.
     - **Biology & Structures**: Labeled structural interaction overviews.
   - Core principle takeaways and memorable real-world analogy blocks (e.g. water-pipe model for Ohm's Law).

3. **Dynamic Knowledge Router (3 Unified Routes)**:
   - **Route 1: Document RAG**: Multi-format document parser (PDF, DOCX, PPTX, TXT, MD) with PyMuPDF, sentence-transformers (`all-MiniLM-L6-v2`), FAISS vector index, and scanned document OCR advisory.
   - **Route 2: External Live Web Retrieval**: Automatically triggered on temporal, breakthrough, or recent queries (e.g., "latest developments in AI agents", "who won 2026") using DuckDuckGo, ArXiv, and Wikipedia.
   - **Route 3: Universal General LLM Knowledge**: Deep foundational curricula across STEM, humanities, and programming.
   - **Natural Language Intent Parsing**: Auto-extracts level (*Beginner/Inter/Adv*), duration (*5m to 60m*), language (*English/Hindi/Hinglish*), learning goal (*Understand/Exam/Interview/Practice*), and teaching style (*Simple/Visual/Detailed/Socratic/Exam-focused*).

4. **Formative Assessment & Empathetic Misconception Remediation**:
   - Instruction pauses after key concepts with: `🧠 Let's check your understanding`.
   - Supports MCQ, short-answer reasoning, conceptual, application, and problem solving.
   - When an answer is incorrect, the AI diagnostician isolates the root cause (e.g., confusing direct and inverse proportionality), and the teacher warmly guides the student:
     *“You're very close! The confusion is between voltage and current. Let's look at this using a water-pipe example.”*
   - On-the-fly customized remediation video generation with a fresh analogy and alternative visual perspective.

5. **Real-Time Teacher Presence & Cognitive Telemetry**:
   - `TeacherReactionBadge`: Displays real-time teacher presence, speech bubbles, and pedagogical posture (Teaching, Waiting, Evaluating, Praising, Remediating).
   - `TeacherBrainPanel`: Live telemetry displaying learner level, understanding state, diagnosed mental gaps, and current teaching strategy.

6. **Summative Assessment & Analytics Feedback Report**:
   - 3–5 question mastery quiz scoring overall comprehension.
   - Visual circular mastery gauge, concepts mastered vs. focus areas, personalized study guidance, and a 1-click launch button for the next learning horizon.

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

AI Teacher includes two automated testing suites: the 16-point Master Verification Suite and the 7-stage QA regression script.

### 1. 16-Point Master Test Suite
```bash
cd backend
python test_master_suite.py
```
This suite verifies:
1. **Health Endpoint & Diagnostics**: Verifies CPU/GPU execution mode detection.
2. **Topic Lesson Generation**: Autonomous planning and video synthesis on any user prompt.
3. **Multi-Format Ingestion**: Ingests `.pdf`, `.docx`, `.pptx`, `.txt`, `.md`, and detects scanned image-only PDFs with OCR guidance.
4. **RAG Retrieval & Confidence Scoring**: Vector indexing with normalized confidence scores and low-relevance disclaimers.
5. **Adaptive Time Planning**: Synthesizes 5m, 20m, and 7-day structured mastery curriculums.
6. **Video & Avatar Synthesis**: Synchronized audio-driven lip animation, slide rendering, and FFmpeg assembly.
7. **Formative Evaluation**: Accurate conceptual grading and cognitive telemetry reporting.
8. **Misconception Diagnosis**: Isolates root-cause mental flaws, severity, and pedagogical strategies.
9. **Dynamic Remediation**: Custom re-explanation video generation and interactive in-lesson Q&A.
10. **Summative Quiz Generation**: Multi-question assessment tailored to the lesson domain.
11. **Automated Quiz Scoring**: Objective percentage grading and answer checking.
12. **Mastery Analytics & Learning Path**: Longitudinal multi-step pathway recommendations.
13. **Pure Hindi Script & Neural Voice**: Devanagari text generation and `hi-IN-SwaraNeural` voice synthesis.
14. **English Script & Neural Voice**: Fluent narration and `en-US-JennyNeural` voice synthesis.
15. **Hinglish Mode & Live Language Switch**: Conversational Hinglish (`en-IN`) and mid-lesson translation without progress loss.
16. **LLM Resiliency & Offline Fallback**: Zero-dependency intelligent domain engine fallback ensuring unbreakable execution.

### 2. End-to-End Demo QA Flow
```bash
cd backend
python test_demo_flow.py
```

---

## 🎬 Hackathon Live Demo Walkthrough

### Scenario: Universal Topic or Multi-Format Document Masterclass
1. Open `http://127.0.0.1:5173`.
2. **Choose Your Input**:
   - **Document Mode**: Upload any `.pdf`, `.docx`, `.pptx`, `.txt`, or choose a benchmark chapter.
   - **Topic Prompt Mode**: Type any topic (e.g., *"What is photosynthesis?"*, *"Explain recursion"*, *"What is blockchain?"*).
3. **Personalize Your Experience**:
   - **Target Level**: Beginner, Intermediate, or Advanced.
   - **Time Budget**: 5m, 10m, 20m, 30m, 60m, or **7-Day Plan**.
   - **Teaching Style**: Simple, Detailed, Visual, Practical, Socratic, or Exam-focused.
   - **Prior Knowledge**: (Optional) Note what you already know.
   - **Language**: English, Hindi (हिंदी), or Hinglish.
4. Click **"Launch Interactive AI Teacher Lesson"**.
5. **Watch the Lesson**:
   - Dr. Nova presents the concepts with synchronized audio visualizers, keyword badges, and takeaway slides.
   - Expand the **🧠 Teacher Brain** panel to inspect live cognitive telemetry: Learner Level, Understanding State, Misconception Diagnosis, Teaching Strategy, and Next Pedagogical Action.
   - Use the **Language Switcher** in the header to switch languages mid-lesson on the fly!
6. **Formative Check & Adaptation**:
   - Submit an intentionally flawed answer to trigger the adaptive loop.
   - The AI Teacher identifies your mental model gap, explains the root cause, and generates a **custom remediation video with a fresh analogy**.
   - Click **"Watch Custom Re-Explanation Video"** to review the concept.
7. Complete the **Summative Mastery Quiz**.
8. View the **Mastery Analytics Report** with your score gauge, 7-day study curriculum, longitudinal learning progression, and 1-click launch button for the recommended follow-up topic!

