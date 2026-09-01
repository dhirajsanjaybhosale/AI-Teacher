import os
import re
import datetime
from typing import Optional, Dict, Any, List, Tuple
from pydantic import BaseModel, Field

from app.lesson_planning.schemas import SourceMetadata, LearnerPreferences
from .parser import PDFParser
from .chunker import TextChunker
from .retriever import FAISSRetriever
from .search_retriever import search_retriever


class KnowledgeRoutingResult(BaseModel):
    route_type: str = Field(..., description="'pdf_rag', 'external_web', 'llm_knowledge', or 'hybrid'")
    grounded_context: str = Field(default="", description="Extracted context for LLM grounding")
    sources: List[SourceMetadata] = Field(default_factory=list, description="Verified sources with URLs and titles")
    source_name: str = Field(default="", description="Clean source identifier or topic title")
    clean_topic: str = Field(default="", description="Normalized topic/question title")
    detected_language: str = Field(default="en", description="en, hi, or hinglish")
    detected_level: str = Field(default="beginner", description="beginner, intermediate, or advanced")
    detected_minutes: int = Field(default=10, description="Inferred or requested duration in minutes")
    search_provider: Optional[str] = None
    retrieval_confidence: float = Field(default=1.0, description="Confidence score of RAG retrieval (0.0 - 1.0)")
    retrieval_warning: Optional[str] = Field(default="", description="Warning message if retrieval confidence is low or scanned document detected")
    is_scanned: bool = Field(default=False, description="True if document appears to be scanned image requiring OCR")


class KnowledgeRouter:
    """
    Intelligent Knowledge Routing Engine.
    Dynamically determines whether a request requires:
    1. Uploaded Document Grounding (PDF, DOCX, PPTX, TXT RAG via FAISS)
    2. Live External Web Search (DuckDuckGo / Wikipedia / ArXiv)
    3. Universal General LLM Knowledge Base
    """

    TEMPORAL_KEYWORDS = [
        "latest", "today", "recent", "current", "2026", "2025", "new developments",
        "recent research", "recent news", "news", "breakthrough", "breakthroughs",
        "state of the art", "sota", "trends", "trending", "who won", "updates"
    ]

    def __init__(self):
        self.parser = PDFParser()
        self.chunker = TextChunker()
        self.searcher = search_retriever

    def parse_natural_language_intent(self, query: str, default_level: str = "beginner", default_lang: str = "en", default_mins: int = 10) -> Tuple[str, str, str, int]:
        """
        Extracts language, level, time duration, and clean topic from natural language input.
        """
        q_clean = query.strip()
        q_lower = q_clean.lower()

        # 1. Language Detection (English, Hindi, Hinglish)
        detected_lang = default_lang
        if any(hg in q_lower for hg in ["in hinglish", "hinglish me", "hinglish mein", "hinglish script"]):
            detected_lang = "hinglish"
        elif any(h in q_lower for h in ["in hindi", "hindi me", "हिंदी", "hindi mein", "hindi script", "explain in hindi"]):
            detected_lang = "hi"

        # 2. Level Detection
        detected_level = default_level
        if any(b in q_lower for b in ["beginner", "basics", "from scratch", "for beginners", "fundamentals", "introductory", "for kids", "simple"]):
            detected_level = "beginner"
        elif any(adv in q_lower for adv in ["advanced", "deep dive", "expert", "rigorous", "internals", "architecture"]):
            detected_level = "advanced"
        elif any(mid in q_lower for mid in ["intermediate", "practical"]):
            detected_level = "intermediate"

        # 3. Time Duration Detection
        detected_mins = default_mins
        time_match = re.search(r'for (\d+)\s*(?:minutes|mins|m)\b', q_lower)
        if time_match:
            try:
                mins = int(time_match.group(1))
                if mins in [5, 10, 20, 30, 60]:
                    detected_mins = mins
                elif mins <= 7:
                    detected_mins = 5
                elif mins <= 15:
                    detected_mins = 10
                elif mins <= 25:
                    detected_mins = 20
                elif mins <= 45:
                    detected_mins = 30
                else:
                    detected_mins = 60
            except ValueError:
                pass
        elif any(q in q_lower for q in ["what is", "why is", "how does", "what are", "difference between", "vs"]):
            # For direct single concept questions, default to 5-10m
            detected_mins = min(default_mins, 10)

        # 4. Clean Topic Extraction (strip prefixes like "Teach me", "Explain", "What is", "in Hindi")
        clean_topic = q_clean
        # Remove trailing qualifiers
        clean_topic = re.sub(r'\s*(in hindi|hindi mein|हिंदी में|from beginner level|for beginners|for \d+\s*(?:minutes|mins|m))\s*$', '', clean_topic, flags=re.IGNORECASE).strip()
        
        # If user asked "What is X?" or "Explain X", clean title
        prefix_patterns = [
            r'^what is (?:the )?',
            r'^what are (?:the )?',
            r'^why is (?:the )?',
            r'^how does (?:the )?',
            r'^explain (?:about )?',
            r'^teach me (?:about )?',
            r'^tell me about '
        ]
        topic_candidate = clean_topic
        for pat in prefix_patterns:
            topic_candidate = re.sub(pat, '', topic_candidate, flags=re.IGNORECASE).strip()

        if topic_candidate and len(topic_candidate) > 2:
            if topic_candidate.islower():
                topic_candidate = topic_candidate.title()
            clean_topic = topic_candidate.rstrip("?.!")

        return clean_topic, detected_lang, detected_level, detected_mins

    def is_temporal_query(self, query: str) -> bool:
        """
        Detects if query requires real-time or recent web retrieval.
        """
        q_lower = query.lower()
        return any(k in q_lower for k in self.TEMPORAL_KEYWORDS)

    async def route_knowledge(
        self,
        pdf_bytes: Optional[bytes] = None,
        pdf_filename: Optional[str] = None,
        topic: Optional[str] = None,
        level: str = "beginner",
        time_minutes: int = 10,
        language: str = "en",
        force_web_search: bool = False,
        document_bytes: Optional[bytes] = None,
        document_filename: Optional[str] = None
    ) -> KnowledgeRoutingResult:
        """
        Executes dynamic routing and returns the unified knowledge result across documents, web, and LLM.
        """
        doc_bytes = document_bytes or pdf_bytes
        doc_name = document_filename or pdf_filename

        raw_query = topic or doc_name or "Core Educational Concepts"
        clean_topic, det_lang, det_level, det_mins = self.parse_natural_language_intent(
            raw_query, default_level=level, default_lang=language, default_mins=time_minutes
        )

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # -------------------------------------------------------------
        # ROUTE 1: UPLOADED DOCUMENT (PDF / DOCX / PPTX / TXT RAG)
        # -------------------------------------------------------------
        if doc_bytes and doc_name:
            try:
                doc_data = self.parser.extract_text_from_bytes(doc_bytes, filename=doc_name)
                is_scanned = doc_data.get("is_scanned", False)
                scan_warning = doc_data.get("scan_warning", "")

                chunks = self.chunker.chunk_document(doc_data)
                retriever = FAISSRetriever()
                retriever.add_chunks(chunks)

                search_query = clean_topic if (topic and topic != doc_name) else doc_data.get("title", "Core concepts and mechanisms")
                top_chunks = retriever.query(search_query, top_k=5)
                retrieval_confidence = retriever.compute_retrieval_confidence(top_chunks) if top_chunks else 0.0

                retrieved_context = retriever.get_combined_context(search_query, top_k=5, max_words=2500)
                if not retrieved_context and doc_data.get("full_text"):
                    retrieved_context = doc_data["full_text"][:3000]

                ext = os.path.splitext(doc_name)[1].upper().lstrip(".") or "DOC"
                source_desc = f"{ext} Ingestion ({doc_data.get('total_pages', 1)} pages/slides, {doc_data.get('total_words', 0)} words, confidence={retrieval_confidence:.2f})"
                if is_scanned:
                    source_desc += " [SCANNED DOCUMENT DETECTED]"

                doc_source = SourceMetadata(
                    title=f"{doc_name} (Uploaded Document)",
                    url="",
                    source=source_desc,
                    retrieved_at=now_iso,
                    snippet=retrieved_context[:300] if retrieved_context else scan_warning
                )

                retrieval_warning = scan_warning
                if retrieval_confidence < 0.35 and not retrieval_warning:
                    retrieval_warning = "The uploaded document contains limited direct overlap. General educational knowledge will supplement where appropriate."

                print(f"[KnowledgeRouter] Routed to PDF_RAG ({ext}): '{doc_name}' ({len(chunks)} chunks indexed, confidence: {retrieval_confidence}).")
                return KnowledgeRoutingResult(
                    route_type="pdf_rag",
                    grounded_context=retrieved_context,
                    sources=[doc_source],
                    source_name=doc_name,
                    clean_topic=clean_topic or doc_data.get("title", doc_name.rsplit('.', 1)[0]),
                    detected_language=det_lang,
                    detected_level=det_level,
                    detected_minutes=det_mins,
                    search_provider="FAISS Vector RAG",
                    retrieval_confidence=retrieval_confidence,
                    retrieval_warning=retrieval_warning,
                    is_scanned=is_scanned
                )
            except Exception as e:
                print(f"[KnowledgeRouter] Document RAG error: {e}. Falling back to general knowledge.")

        # -------------------------------------------------------------
        # ROUTE 2: EXTERNAL WEB RETRIEVAL (DuckDuckGo / Wikipedia / ArXiv)
        # -------------------------------------------------------------
        should_search = force_web_search or self.is_temporal_query(raw_query)
        if should_search:
            print(f"[KnowledgeRouter] Current/temporal topic detected or search requested: '{raw_query}'. Engaging External Search...")
            search_res = self.searcher.search_topic(clean_topic, max_results=4)
            if search_res["success"] and search_res["sources"]:
                print(f"[KnowledgeRouter] Retrieved {len(search_res['sources'])} live verified sources via {search_res.get('provider')}.")
                return KnowledgeRoutingResult(
                    route_type="external_web",
                    grounded_context=search_res["combined_context"],
                    sources=search_res["sources"],
                    source_name=clean_topic,
                    clean_topic=clean_topic,
                    detected_language=det_lang,
                    detected_level=det_level,
                    detected_minutes=det_mins,
                    search_provider=search_res.get("provider")
                )
            else:
                print(f"[KnowledgeRouter] External search returned zero sources. Gracefully falling back to universal LLM knowledge.")

        # -------------------------------------------------------------
        # ROUTE 3: UNIVERSAL GENERAL LLM KNOWLEDGE
        # -------------------------------------------------------------
        print(f"[KnowledgeRouter] Routed to LLM_KNOWLEDGE for stable concept: '{clean_topic}'.")
        return KnowledgeRoutingResult(
            route_type="llm_knowledge",
            grounded_context="",
            sources=[],
            source_name=clean_topic,
            clean_topic=clean_topic,
            detected_language=det_lang,
            detected_level=det_level,
            detected_minutes=det_mins,
            search_provider="LLM General Knowledge"
        )


# Global singleton
knowledge_router = KnowledgeRouter()
