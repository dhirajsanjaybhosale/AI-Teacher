import os
try:
    import pymupdf as fitz
except ImportError:
    import fitz
from typing import Dict, Any, List


class PDFParser:
    """
    Extracts structured text, chapters, and metadata from uploaded PDF documents.
    """

    def __init__(self):
        pass

    def extract_text_from_bytes(self, pdf_bytes: bytes, filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Parses raw bytes of a PDF file using PyMuPDF.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        return self._process_doc(doc, filename)

    def extract_text_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parses a local PDF file path using PyMuPDF.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at: {file_path}")
        doc = fitz.open(file_path)
        return self._process_doc(doc, os.path.basename(file_path))

    def _process_doc(self, doc: fitz.Document, filename: str) -> Dict[str, Any]:
        pages_content = []
        full_text_list = []
        toc = doc.get_toc()

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                pages_content.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "word_count": len(text.split())
                })
                full_text_list.append(text)

        full_text = "\n\n".join(full_text_list)
        metadata = doc.metadata or {}

        # Fallback title if metadata title is empty
        title = metadata.get("title") or filename.replace(".pdf", "").replace("_", " ").title()

        return {
            "filename": filename,
            "title": title,
            "author": metadata.get("author", "Unknown"),
            "total_pages": len(doc),
            "total_words": len(full_text.split()),
            "full_text": full_text,
            "pages": pages_content,
            "toc": toc
        }
