from .base_adapter import BaseAdapter
from .ecommerce import EcommerceAdapter
from .news import NewsAdapter
from utils.logger import log

class GenericAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            # Auto-detect content type
            if self._is_article(soup):
                return self._extract_article(html, url)
            if self._is_product(soup):
                return EcommerceAdapter().extract(html, url)
            if self._is_listing(soup):
                return self._extract_listing(soup)
            # Fallback to main content extraction
            return {
                "type": "generic",
                "title": soup.title.get_text().strip() if soup.title else None,
                "content": self.parser.extract_content(),
                "metadata": self._extract_metadata(soup)
            }
        except Exception as e:
            log.error(f"Generic extraction error: {e}")
            return {"error": str(e), "type": "generic"}
    
    def _is_article(self, soup):
        return bool(soup.find('article'))
    
    def _is_product(self, soup):
        return bool(soup.select_one('[itemtype*="Product"]'))
    
    def _is_listing(self, soup):
        return len(soup.select('.item, .listing, .result')) > 5
    
    def _extract_article(self, html, url):
        return NewsAdapter().extract(html, url)
    
    def _extract_listing(self, soup):
        items = []
        for item in soup.select('.item, .listing, .result'):
            title = item.select_one('.title, .name, h3')
            description = item.select_one('.description, .summary')
            
            items.append({
                "title": title.get_text().strip() if title else None,
                "description": description.get_text().strip() if description else None,
                "url": item.get('href') if item.name == 'a' else None
            })
        
        return {"type": "listing", "items": items}
    
    def _extract_metadata(self, soup):
        return {
            "author": self._get_author(soup),
            "published_date": self._get_published_date(soup),
            "keywords": self._get_keywords(soup),
            "category": self._get_category(soup)
        }
    
    def _get_author(self, soup):
        author = soup.select_one('[itemprop="author"], .author, .byline')
        return author.get_text().strip() if author else None
    
    def _get_published_date(self, soup):
        date = soup.select_one('time[datetime], .date, .published, .pubdate')
        if date and hasattr(date, 'attrs') and 'datetime' in date.attrs:
            return date['datetime']
        return date.get_text().strip() if date else None
    
    def _get_keywords(self, soup):
        meta = soup.select_one('meta[name="keywords"]')
        if meta and 'content' in meta.attrs:
            return [k.strip() for k in meta['content'].split(',')]
        return []
    
    def _get_category(self, soup):
        cat = soup.select_one('.category, [itemprop="articleSection"]')
        return cat.get_text().strip() if cat else None
    
    # Metadata extraction helpers...