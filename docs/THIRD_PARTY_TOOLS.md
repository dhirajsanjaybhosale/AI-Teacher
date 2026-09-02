# 🛠️ Third-Party Tools, Models & Libraries
## AI Teacher — Human-Like Adaptive AI Educator

All technologies used in **AI Teacher** are 100% open-source or free-tier compatible with zero paid API requirements.

---

## 1. Large Language Models (LLM Layer)

| Tool / Model | Role | Free Tier / License | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **Google Gemini API** (`gemini-1.5-flash` / `gemini-2.0-flash`) | Core Reasoning & Curriculum Planning | Free Tier (Google AI Studio) | High-speed multi-lingual generation, structured JSON curriculum planning, formative misconception diagnosis, and analogy generation. |
| **Groq API** (`llama-3.3-70b-versatile`) | High-Speed LLM Fallback | Free Tier (Groq Cloud) | Ultra-low latency Llama-3 inference for instant real-time answer evaluation and remediation generation. |
| **Universal Offline Domain Engine** | Resilient Offline Fallback Engine | MIT / Open Source | Deterministic heuristics ensuring an unbreakable live demo regardless of network or API key status. Covers STEM, humanities, and programming. |

---

## 2. Ingestion, Embeddings & Vector Retrieval

| Library | Version | License | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **PyMuPDF (`pymupdf` / `fitz`)** | `1.28.2` | AGPL-3.0 / Open Source | High-performance extraction of text, table of contents, and structural metadata from PDF chapters. Scanned PDF detection with OCR alerts. |
| **python-docx (`docx`)** | `1.1.2` | MIT License | Native parsing of Word documents (.docx), paragraph extraction, and heading detection. |
| **python-pptx (`pptx`)** | `1.0.2` | MIT License | Native extraction of PowerPoint slides (.pptx), slide titles, bullet hierarchies, and notes. |
| **`sentence-transformers`** | `6.0.1` (`all-MiniLM-L6-v2`) | Apache 2.0 | Local dense 384-dimensional semantic embeddings running entirely on CPU without external API calls. |
| **FAISS (`faiss-cpu`)** | `1.15.0` | MIT License | In-memory indexing and fast cosine similarity vector retrieval with normalized confidence scoring. |
| **DuckDuckGo Search (`duckduckgo_search` / `ddgs`)** | Latest | MIT License | Live external search for temporal, breakthrough, and trending queries. |
| **ArXiv Search (`arxiv`)** | Latest | MIT License | Direct retrieval of verified scientific preprints and research papers for cutting-edge queries. |
| **Wikipedia (`wikipedia-api`)** | Latest | MIT License | Authoritative conceptual retrieval for foundational and encyclopedia topics. |

---

## 3. Text-to-Speech (TTS) & Narration

| Tool / Library | Version | License | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **Edge-TTS (`edge-tts`)** | `7.2.8` | GPL-3.0 / Open Source | High-fidelity neural voice synthesis supporting English (`en-US-JennyNeural`), Hindi (`hi-IN-SwaraNeural`), and Hinglish (`en-IN-NeerjaNeural` / `en-IN-PrabhatNeural`) with zero API key requirement. |
| **`pyttsx3`** | `2.98` | MPL-2.0 | Offline fallback speech synthesizer ensuring zero audio generation failures. |
| **`scipy` / `wave` / `numpy`** | Latest | BSD / Open Source | Audio amplitude analysis, RMS energy extraction, and frame-by-frame envelope calculation (25 fps). |

---

## 4. Classroom Educator Presentation & Video Compositing

| Tool / Library | License | Role & Rationale |
| :--- | :--- | :--- |
| **Articulated Classroom Avatar Engine** | Custom / MIT | Full upper-body educator presentation with articulated shoulders, blazer, spectacles, blinking state machine, sinusoidal breathing cycle, and 6 pedagogical postures (`point_board`, `explain`, `question`, `praise`, `remediate`, `welcome`). |
| **Smartboard Choreography Engine** | Custom / MIT | Coordinates teacher gestures with dynamic illuminated borders on smartboard equations, code snippets, and key takeaway cards. |
| **GPU Lip-Sync Hook (Wav2Lip / SadTalker)** | Academic / Research | Optional neural lip-sync avatar generation engaged when CUDA GPU is present. |
| **FFmpeg (`imageio-ffmpeg`)** | LGPL / GPL | High-speed video compositing (avatar + slides + text overlays + subtitles + narration audio) into standard H.264/AAC MP4 clips at 25 fps. |
| **Pillow (`PIL`)** | `12.3.0` (HPND License) | Procedural 1280x720 frame rendering, smartboard typography, vector pointers, and glassmorphism elements. |

---

## 5. Web Frameworks & Frontend

| Library | Version | License | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **FastAPI** | `0.141.1` | MIT | High-performance async Python backend framework. |
| **Uvicorn** | `0.52.4` | BSD-3-Clause | Lightning-fast ASGI web server. |
| **Pydantic** | `2.13.5` | MIT | Strict data validation and schema serialization. |
| **React** | `19.2.8` | MIT | Modern interactive user interface. |
| **Vite** | `8.2.2` | MIT | Next-generation frontend build tooling and HMR dev server. |
| **Lucide React** | `1.38.0` | ISC | Modern vector iconography. |
| **Canvas Confetti** | `1.9.4` | ISC | Formative mastery celebrations. |
