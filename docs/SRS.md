# 📋 Software Requirements Specification (SRS)
## AI Teacher — Round 2 AI Innovation Hackathon 2026
### Human-Like Adaptive AI Educator

---

## 1. System Overview & Core Philosophy
**AI Teacher** is a full-stack, autonomous, adaptive educational system designed to replicate the complete pedagogical lifecycle of a master classroom educator.

Rather than acting as a static chatbot or talking avatar, the experience feels like:
> **A REAL HUMAN TEACHER TEACHING A STUDENT IN A MODERN DIGITAL CLASSROOM.**

The system follows the 14-step human teaching loop:
$$\text{Understand} \longrightarrow \text{Plan} \longrightarrow \text{Explain} \longrightarrow \text{Visualize} \longrightarrow \text{Demonstrate} \longrightarrow \text{Question} \longrightarrow \text{Evaluate} \longrightarrow \text{Diagnose} \longrightarrow \text{Adapt} \longrightarrow \text{Re-explain} \longrightarrow \text{Re-test} \longrightarrow \text{Continue} \longrightarrow \text{Assess} \longrightarrow \text{Recommend}$$

---

## 2. Functional Requirements (FR)

### FR-1: Universal Ingestion & Dynamic Knowledge Routing
- **FR-1.1**: The system shall accept multi-format document uploads: PDF, DOCX, PPTX, TXT, and Markdown.
- **FR-1.2**: Extracted text shall be segmented into semantic sliding windows with structural heading and slide metadata retention.
- **FR-1.3**: Chunks shall be embedded using local dense vectors (`all-MiniLM-L6-v2`, 384-dim) and indexed via FAISS with normalized retrieval confidence scoring.
- **FR-1.4**: Scanned or image-only documents shall be automatically detected and flagged with OCR advisory notices without system crash.
- **FR-1.5**: If no document is provided, the **Dynamic Knowledge Router** shall automatically parse natural language intent (subject, level, duration, language, goal, teaching style) and route between:
  - **Route 1: Document RAG** (uploaded documents)
  - **Route 2: External Live Web Retrieval** (temporal / recent / breakthrough queries via ArXiv, DuckDuckGo, and Wikipedia)
  - **Route 3: Universal General LLM Knowledge** (stable concepts across STEM, Humanities, and Programming)

### FR-2: Pedagogical Curriculum & Time-Budgeted Planning
- **FR-2.1**: The curriculum planner shall scale segment count and cognitive load proportionally to time budget:
  - 5 minutes: 2 concise high-yield segments
  - 10 minutes: 3 progressive segments
  - 20 minutes: 4–5 deep conceptual segments
  - Multi-day / 7-Day: 7 structured daily modules with spaced repetition revision schedules and practice goals.
- **FR-2.2**: The planner shall adapt vocabulary and depth to learner levels (*Beginner*, *Intermediate*, *Advanced*).
- **FR-2.3**: Multi-lingual support for English (`en`), Hindi (`hi`), and conversational Hinglish (`hinglish`), generating scripts, subtitles, slide text, and questions natively.
- **FR-2.4**: Every segment shall define a distinct visual diagram type: `equation`, `code`, `process`, `comparison`, `flowchart`, or `diagram`.

### FR-3: Classroom Educator Presentation & Video Compositing
- **FR-3.1**: The avatar engine shall present an articulated upper-body classroom educator featuring:
  - Natural sinusoidal breathing cycle and blinking state machine
  - Articulated shoulders, blazer, collar, neck, spectacles, and styled hair
  - Multi-directional gaze (looking forward at student vs. looking right towards the smartboard)
  - 6 distinct pedagogical postures:
    1. `point_board`: Torso and gaze turned right, arm extended with golden-tipped pointer wand
    2. `question`: Thoughtful contemplative pose, hand resting at chin, inquisitive expression
    3. `praise`: Celebratory double thumbs-up, bright smile, sparkling eyes
    4. `remediate`: Empathetic reassuring posture, hand placed gently over the chest
    5. `explain`: Conversational gestures with dynamic hand/finger cadence moving with speech amplitude
    6. `welcome`: Calm resting hands, welcoming smile
- **FR-3.2**: When in `point_board` pose, the smartboard formulas and key points shall dynamically highlight with an illuminated focus border and teacher indicator.
- **FR-3.3**: Neural speech synthesized via Edge-TTS (`en-US-JennyNeural`, `hi-IN-SwaraNeural`, `en-IN-NeerjaNeural`) with offline `pyttsx3` fallback.
- **FR-3.4**: 720p H.264/AAC MP4 video compositing executed via FFmpeg at 25 fps with synchronized subtitles ticker and progress slider.

### FR-4: Formative Assessment & Misconception Remediation Loop
- **FR-4.1**: After key concepts, the teacher pauses instruction and presents:
  `🧠 Let's check your understanding`
- **FR-4.2**: The system supports multiple question formats: MCQ, short-answer reasoning, conceptual, application, and problem solving.
- **FR-4.3**: When an answer is incorrect, the AI diagnostician does NOT simply output "Wrong". It isolates the root cause (e.g. confusing direct vs. inverse proportionality in Ohm's Law), and the teacher provides empathetic conversational guidance:
  *“You're very close! The confusion is between voltage and current. Let's look at this using a water-pipe example.”*
- **FR-4.4**: An adaptive remediation segment is synthesized with a completely fresh intuitive analogy, alternative visual, and a newly rendered on-the-fly remediation video clip.

### FR-5: Digital Classroom Frontend & Cognitive Telemetry
- **FR-5.1**: Split-screen Digital Classroom interface featuring:
  - Teacher presentation video player
  - Interactive Smartboard (`ClassroomBoard`) with formulas ($V = I \times R$), code syntax blocks, step-by-step workflow capsules, and comparison tables
  - Layout switcher: Split-Screen Classroom, Teacher Video Focus, Smartboard Focus
- **FR-5.2**: Real-time `TeacherReactionBadge` reflecting teacher state (Teaching, Waiting, Evaluating, Praising, Remediating).
- **FR-5.3**: Live cognitive telemetry panel (`TeacherBrainPanel`) displaying learner level, understanding state, diagnosed mental gaps, and current teaching strategy.

### FR-6: Summative Assessment & Analytics Feedback Report
- **FR-6.1**: Multi-question summative quiz assessing cross-segment mastery.
- **FR-6.2**: Comprehensive analytics report with circular mastery gauge, concepts mastered vs. focus areas, personalized study guidance, and a 1-click launch button for the next learning horizon.

---

## 3. Non-Functional Requirements (NFR)

- **NFR-1 (100% Free & Open-Source)**: Zero paid API requirements. Operates with Gemini / Groq free tiers or entirely offline.
- **NFR-2 (CPU Usability)**: Full video generation, avatar articulation, and vector retrieval execute cleanly on standard CPUs without GPU dependencies.
- **NFR-3 (Resilience)**: Resilient multi-tier fallbacks for LLM, TTS, embeddings, and video ensuring zero crashes during live demonstrations.
- **NFR-4 (Pedagogical Excellence)**: Teaching experience prioritizes conceptual depth, intuitive analogies, and adaptive remediation over simple chatbot responses.
