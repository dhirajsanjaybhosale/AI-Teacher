import os
import datetime
import urllib.parse
from typing import List, Dict, Any, Optional
import httpx

from app.lesson_planning.schemas import SourceMetadata

# Check DDGS availability
_DDGS_AVAILABLE = False
try:
    from duckduckgo_search import DDGS
    _DDGS_AVAILABLE = True
except ImportError:
    try:
        from ddgs import DDGS
        _DDGS_AVAILABLE = True
    except ImportError:
        pass


class SearchRetriever:
    """
    Free, open external search and knowledge retriever.
    Queries DuckDuckGo, Wikipedia REST API, and ArXiv without requiring paid API keys.
    Collects verified URLs, source titles, publication snippets, and retrieval timestamps.
    """

    def __init__(self):
        self.client = httpx.Client(timeout=8.0, follow_redirects=True, headers={
            "User-Agent": "AITeacher/2.0 (Open-Source Educational Assistant; mailto:contact@aiteacher.internal)"
        })

    def search_topic(self, query: str, max_results: int = 4) -> Dict[str, Any]:
        """
        Retrieves real external search results for a topic query.
        Returns: {
            "sources": List[SourceMetadata],
            "combined_context": str,
            "success": bool,
            "provider": str
        }
        """
        cleaned_query = query.strip()
        if not cleaned_query:
            return {"sources": [], "combined_context": "", "success": False, "provider": "none"}

        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        sources: List[SourceMetadata] = []
        context_chunks: List[str] = []

        # 1. Primary: DuckDuckGo Web Search
        if _DDGS_AVAILABLE:
            try:
                with DDGS() as ddgs:
                    ddg_results = list(ddgs.text(cleaned_query, max_results=max_results))
                for item in ddg_results:
                    title = item.get("title", "Web Source")
                    url = item.get("href") or item.get("url", "")
                    body = item.get("body") or item.get("snippet", "")
                    if url and body:
                        # Extract domain as source
                        domain = urllib.parse.urlparse(url).netloc or "DuckDuckGo Web"
                        sources.append(SourceMetadata(
                            title=title,
                            url=url,
                            source=domain,
                            retrieved_at=now_iso,
                            snippet=body[:300]
                        ))
                        context_chunks.append(f"SOURCE: {title} ({domain})\nURL: {url}\nEXCERPT: {body}\n")
                if sources:
                    return {
                        "sources": sources,
                        "combined_context": "\n".join(context_chunks),
                        "success": True,
                        "provider": "DuckDuckGo"
                    }
            except Exception as e:
                print(f"[SearchRetriever] DuckDuckGo search error: {e}. Trying Wikipedia fallback.")

        # 2. Secondary: Wikipedia REST API & Search API
        try:
            wiki_sources = self._search_wikipedia(cleaned_query, now_iso)
            if wiki_sources:
                for s in wiki_sources:
                    sources.append(s)
                    context_chunks.append(f"SOURCE: {s.title} (Wikipedia)\nURL: {s.url}\nEXCERPT: {s.snippet}\n")
                return {
                    "sources": sources,
                    "combined_context": "\n".join(context_chunks),
                    "success": True,
                    "provider": "Wikipedia"
                }
        except Exception as e:
            print(f"[SearchRetriever] Wikipedia API error: {e}")

        # 3. Tertiary: ArXiv Search API (for academic & technical research queries)
        if any(term in cleaned_query.lower() for term in ["research", "paper", "algorithm", "quantum", "neural", "ai", "agents", "model"]):
            try:
                arxiv_sources = self._search_arxiv(cleaned_query, now_iso)
                if arxiv_sources:
                    for s in arxiv_sources:
                        sources.append(s)
                        context_chunks.append(f"SOURCE: {s.title} (arXiv Research)\nURL: {s.url}\nEXCERPT: {s.snippet}\n")
                    return {
                        "sources": sources,
                        "combined_context": "\n".join(context_chunks),
                        "success": True,
                        "provider": "ArXiv"
                    }
            except Exception as e:
                print(f"[SearchRetriever] ArXiv API error: {e}")

        return {
            "sources": sources,
            "combined_context": "\n".join(context_chunks) if context_chunks else "",
            "success": len(sources) > 0,
            "provider": "none"
        }

    def _search_wikipedia(self, query: str, timestamp: str) -> List[SourceMetadata]:
        """
        Queries Wikipedia REST API for search matches and summaries.
        """
        results: List[SourceMetadata] = []
        search_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={urllib.parse.quote(query)}&limit=3&namespace=0&format=json"
        res = self.client.get(search_url)
        if res.status_code == 200:
            data = res.json()
            titles = data[1] if len(data) > 1 else []
            snippets = data[2] if len(data) > 2 else []
            urls = data[3] if len(data) > 3 else []

            for i in range(len(titles)):
                title = titles[i]
                url = urls[i] if i < len(urls) else f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}"
                snippet = snippets[i] if i < len(snippets) else ""
                
                # Fetch rich summary if snippet is short
                if len(snippet) < 60:
                    try:
                        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title.replace(' ', '_'))}"
                        s_res = self.client.get(summary_url)
                        if s_res.status_code == 200:
                            s_data = s_res.json()
                            snippet = s_data.get("extract", snippet)
                    except Exception:
                        pass

                if snippet:
                    results.append(SourceMetadata(
                        title=f"{title} — Wikipedia",
                        url=url,
                        source="en.wikipedia.org",
                        retrieved_at=timestamp,
                        snippet=snippet[:400]
                    ))
        return results

    def _search_arxiv(self, query: str, timestamp: str) -> List[SourceMetadata]:
        """
        Queries ArXiv Open API for research papers.
        """
        import xml.etree.ElementTree as ET
        results: List[SourceMetadata] = []
        clean_q = urllib.parse.quote(query)
        url = f"http://export.arxiv.org/api/query?search_query=all:{clean_q}&start=0&max_results=2"
        res = self.client.get(url)
        if res.status_code == 200:
            root = ET.fromstring(res.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns):
                title_elem = entry.find('atom:title', ns)
                summary_elem = entry.find('atom:summary', ns)
                id_elem = entry.find('atom:id', ns)

                title = title_elem.text.strip().replace('\n', ' ') if title_elem is not None and title_elem.text else "arXiv Research"
                summary = summary_elem.text.strip().replace('\n', ' ') if summary_elem is not None and summary_elem.text else ""
                arxiv_url = id_elem.text.strip() if id_elem is not None and id_elem.text else "https://arxiv.org"

                results.append(SourceMetadata(
                    title=title,
                    url=arxiv_url,
                    source="arxiv.org",
                    retrieved_at=timestamp,
                    snippet=summary[:350]
                ))
        return results


# Global singleton
search_retriever = SearchRetriever()
