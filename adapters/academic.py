from .base_adapter import BaseAdapter
from utils.logger import log

class AcademicAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            structured = self.parser.extract_structured_data()
            paper_data = None
            for item in structured.get('json-ld', []):
                if item.get('@type') == 'ScholarlyArticle':
                    paper_data = self._parse_scholarly_json(item)
                    break
            if not paper_data:
                paper_data = self._html_fallback(soup)
            citations = self._extract_citations(soup)
            return {"type": "academic", "paper": paper_data, "citations": citations}
        except Exception as e:
            log.error(f"Academic extraction error: {e}")
            return {"error": str(e), "type": "academic"}
    
    def _parse_scholarly_json(self, data):
        """Extract from scholarly JSON-LD data"""
        authors = [author.get('name') for author in data.get('author', [])] if isinstance(data.get('author'), list) else []
        
        return {
            "title": data.get("headline") or data.get("name"),
            "authors": authors,
            "date_published": data.get("datePublished"),
            "journal": data.get("publisher", {}).get("name"),
            "abstract": data.get("description"),
            "doi": data.get("doi"),
            "url": data.get("url"),
            "citation_count": data.get("citationCount")
        }
    
    def _html_fallback(self, soup):
        """Fallback to HTML parsing"""
        title = soup.select_one('h1.article-title, h1.title')
        
        # Extract authors
        authors = [a.get_text().strip() for a in soup.select('.authors-list a, .author-name, [itemprop="author"]')]
        
        # Extract abstract
        abstract = soup.select_one('div.abstract, section.abstract')
        
        # Extract publication info
        journal = soup.select_one('.journal-title, .publication-title')
        date = soup.select_one('.article-date, .published-on')
        doi = soup.select_one('a[href*="doi.org"], .doi-value')
        
        # Extract full text PDF
        pdf = soup.select_one('a[href$=".pdf"]')
        
        return {
            "title": title.get_text().strip() if title else None,
            "authors": authors,
            "abstract": abstract.get_text().strip() if abstract else None,
            "journal": journal.get_text().strip() if journal else None,
            "date_published": date.get_text().strip() if date else None,
            "doi": doi.get_text().strip() if doi else None,
            "pdf_url": pdf['href'] if pdf else None
        }
    
    def _extract_citations(self, soup):
        """Extract citation information"""
        citations = []
        
        # Extract citation count
        citation_count = soup.select_one('.citation-count, .cited-by-count')
        
        # Extract reference list
        references = soup.select('.references li, .citation')
        for ref in references:
            text = ref.get_text().strip()
            link = ref.select_one('a')
            
            citations.append({
                "text": text,
                "url": link['href'] if link else None
            })
        
        return {
            "count": citation_count.get_text().strip() if citation_count else len(citations),
            "references": citations
        }