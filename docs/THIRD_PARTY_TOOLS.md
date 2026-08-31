# 🛠️ Third-Party Tools, Models & Libraries

All technologies used in **AI Teacher** are 100% open-source or free-tier compatible with zero paid API requirements.

---

## 1. Large Language Models (LLM)

| Tool / Model | Role | Free Tier / License | Description & Rationale |
| :--- | :--- | :--- | :--- |
| **Google Gemini API** (`gemini-1.5-flash` / `gemini-2.0-flash`) | Core Reasoning & Planning | Free Tier (Google AI Studio) | High-speed multi-lingual generation, structured JSON curriculum planning, formative misconception diagnosis. |
| **Groq API** (`llama-3.3-70b-versatile`) | Alternate LLM Provider | Free Tier (Groq Cloud) | Ultra-low latency Llama-3 inference for instant real-time answer evaluation and remediation generation. |
| **Built-in Intelligent Domain Engine** | Offline Fallback Engine | MIT / Open Source | Deterministic heuristics ensuring an unbreakable live demo regardless of network or API key status. |

---

## 2. Ingestion, Embeddings & Vector Search

| Library | Version | License | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **PyMuPDF (`pymupdf` / `fitz`)** | `1.28.2` | AGPL-3.0 / Open Source | High-performance extraction of text, table of contents, and structural metadata from PDF chapters. |
| **`sentence-transformers`** | `6.0.1` (`all-MiniLM-L6-v2`) | Apache 2.0 | Local dense 384-dimensional semantic embeddings running entirely on CPU/GPU without external API calls. |
| **FAISS (`faiss-cpu`)** | `1.15.0` | MIT License | In-memory indexing and fast cosine similarity vector retrieval for RAG-grounded lesson synthesis. |

---

## 3. Text-to-Speech (TTS) & Narration

| Tool / Library | Version | License | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **Edge-TTS (`edge-tts`)** | `7.2.8` | GPL-3.0 / Open Source | High-fidelity neural voice synthesis supporting English (`en-US-JennyNeural`) and Hindi (`hi-IN-SwaraNeural`) with zero API key requirement. |
| **`pyttsx3`** | `2.98` | MPL-2.0 | Offline fallback speech synthesizer ensuring zero audio generation failures. |
| **`scipy` / `wave` / `numpy`** | Latest | BSD / Open Source | Audio amplitude analysis, RMS energy extraction, and frame-by-frame envelope calculation (25 fps). |

---

## 4. Video & Avatar Synthesis

| Tool / Library | License | Role & Rationale |
| :--- | :--- | :--- |
| **GPU Lip-Sync Hook (Wav2Lip / SadTalker)** | Open Source (Academic/Research) | Neural lip-synced avatar generation engaged automatically when CUDA GPU is present. |
| **2D Vector Synced Avatar Engine** | Custom / MIT | Synchronized 4-phoneme audio-driven mouth shape state machine with natural blinking and reactive audio visualizers for instant CPU rendering. |
| **FFmpeg (`imageio-ffmpeg`)** | LGPL / GPL | High-speed video compositing (avatar + slides + text overlays + subtitles + narration audio) into standard H.264/AAC MP4 clips. |
| **Pillow (`PIL`)** | `12.3.0` (HPND License) | Procedural 1280x720 frame rendering, slide typography, glassmorphism containers, and vector cards. |

---

## 5. Web Frameworks & Frontend

| Library | Version | License | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **FastAPI** | `0.141.1` | MIT | High-performance async Python backend framework. |
| **Uvicorn** | `0.52.4` | BSD-3-Clause | Lightning-fast ASGI web server. |
| **Pydantic** | `2.13.5` | MIT | Strict data validation and schema serialization. |
| **React** | `19.2.8` | MIT | Frontend interactive user interface. |
| **Vite** | `8.2.2` | MIT | Next-generation frontend build tooling and HMR dev server. |
| **Lucide React** | `1.38.0` | ISC | Modern, clean vector iconography. |
| **Canvas Confetti** | `1.9.4` | ISC | Formative success celebrations. |
