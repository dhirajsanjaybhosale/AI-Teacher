import re
from typing import List, Dict, Any


class TextChunker:
    """
    Splits document text into semantic, overlapping chunks optimized for embedding & retrieval.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 80):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunks pages and paragraphs while preserving metadata.
        """
        chunks = []
        chunk_id = 0
        pages = parsed_doc.get("pages", [])
        
        if not pages and parsed_doc.get("full_text"):
            # Fallback if pages not structured
            return self.chunk_raw_text(parsed_doc["full_text"], source=parsed_doc.get("filename", "unknown"))

        for page in pages:
            page_num = page["page_number"]
            page_text = page["text"]
            paragraphs = [p.strip() for p in page_text.split("\n\n") if p.strip()]

            current_chunk_words = []
            
            for para in paragraphs:
                para_words = para.split()
                if len(current_chunk_words) + len(para_words) <= self.chunk_size:
                    current_chunk_words.extend(para_words)
                else:
                    if current_chunk_words:
                        chunk_text = " ".join(current_chunk_words)
                        chunks.append({
                            "chunk_id": f"chunk_{chunk_id}",
                            "text": chunk_text,
                            "page": page_num,
                            "source": parsed_doc.get("filename", "document.pdf"),
                            "word_count": len(current_chunk_words)
                        })
                        chunk_id += 1
                        # Overlap
                        overlap_words = current_chunk_words[-self.chunk_overlap:] if self.chunk_overlap > 0 else []
                        current_chunk_words = overlap_words + para_words
                    else:
                        # Paragraph itself is larger than chunk_size
                        for i in range(0, len(para_words), self.chunk_size - self.chunk_overlap):
                            sub_words = para_words[i:i + self.chunk_size]
                            chunks.append({
                                "chunk_id": f"chunk_{chunk_id}",
                                "text": " ".join(sub_words),
                                "page": page_num,
                                "source": parsed_doc.get("filename", "document.pdf"),
                                "word_count": len(sub_words)
                            })
                            chunk_id += 1
                        current_chunk_words = []

            if current_chunk_words:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "text": " ".join(current_chunk_words),
                    "page": page_num,
                    "source": parsed_doc.get("filename", "document.pdf"),
                    "word_count": len(current_chunk_words)
                })
                chunk_id += 1

        return chunks

    def chunk_raw_text(self, text: str, source: str = "text") -> List[Dict[str, Any]]:
        words = text.split()
        chunks = []
        chunk_id = 0
        step = max(1, self.chunk_size - self.chunk_overlap)
        
        for i in range(0, len(words), step):
            slice_words = words[i:i + self.chunk_size]
            if slice_words:
                chunks.append({
                    "chunk_id": f"chunk_{chunk_id}",
                    "text": " ".join(slice_words),
                    "page": 1,
                    "source": source,
                    "word_count": len(slice_words)
                })
                chunk_id += 1
        return chunks
