from .base_adapter import BaseAdapter
from utils.logger import log

class NewsAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            # Try structured data first
            structured = self.parser.extract_structured_data()
            article_data = None
            for item in structured.get('json-ld', []):
                if item.get('@type') in ('NewsArticle', 'Article'):
                    article_data = self._parse_article_json(item)
                    break
            if not article_data:
                article_data = self._html_fallback(soup)
            return {"type": "news", "data": article_data}
        except Exception as e:
            log.error(f"News extraction error: {e}")
            return {"error": str(e), "type": "news"}
    
    def _parse_article_json(self, data):
        """Extract from JSON-LD article data"""
        return {
            "headline": data.get("headline"),
            "author": self._parse_author(data.get("author")),
            "published_date": data.get("datePublished"),
            "modified_date": data.get("dateModified"),
            "publisher": data.get("publisher", {}).get("name"),
            "description": data.get("description"),
            "content": data.get("articleBody"),
            "image": data.get("image", {}).get("url") if isinstance(data.get("image"), dict) else data.get("image")
        }
    
    def _parse_author(self, author):
        """Normalize author information"""
        if isinstance(author, str):
            return author
        if isinstance(author, list) and author:
            return author[0].get("name") if isinstance(author[0], dict) else author[0]
        if isinstance(author, dict):
            return author.get("name")
        return None
    
    def _html_fallback(self, soup):
        """Fallback to HTML parsing when structured data is missing"""
        headline = soup.select_one('h1[itemprop="headline"], h1.article-title, h1.headline')
        
        # Try to find main content area
        content = soup.select_one('article') or \
                 soup.select_one('[itemprop="articleBody"]') or \
                 soup.select_one('.article-content')
        
        # Clean up content by removing unwanted elements
        if content:
            for element in content.select('script, style, aside, .ad-container, .comments-section'):
                element.decompose()
        
        # Extract author information
        author = soup.select_one('[itemprop="author"], .author-name, .byline')
        
        # Extract date information
        date_published = soup.select_one('[itemprop="datePublished"], time[datetime], .date-published')
        if date_published and hasattr(date_published, 'attrs') and 'datetime' in date_published.attrs:
            date_published = date_published['datetime']
        
        # Extract image
        image = soup.select_one('article img[src], .article-image img[src]')
        
        return {
            "headline": headline.get_text().strip() if headline else None,
            "author": author.get_text().strip() if author else None,
            "published_date": date_published.get_text().strip() if hasattr(date_published, 'get_text') else date_published,
            "content": content.get_text().strip() if content else None,
            "content_html": str(content) if content else None,
            "image": image['src'] if image and 'src' in image.attrs else None
        }