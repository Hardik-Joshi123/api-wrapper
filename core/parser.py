from bs4 import BeautifulSoup
from extruct import extract
import re
import json
from utils.logger import log

class SmartParser:
    def __init__(self):
        self.soup = None
    
    def parse(self, html):
        self.soup = BeautifulSoup(html, 'lxml')
        return self
    
    def extract_structured_data(self):
        """Extract schema.org, OpenGraph, etc."""
        return extract(self.soup.prettify())
    
    def extract_content(self):
        """Main content extraction with fallback strategies"""
        # Strategy 1: JSON-LD
        structured = self.extract_structured_data()
        if structured.get('json-ld'):
            return self._process_json_ld(structured['json-ld'])
        
        # Strategy 2: Article detection
        article = self.soup.find('article')
        if article:
            return self._clean_text(article.get_text(separator=' ', strip=True))
        
        # Strategy 3: Generic body text
        return self._clean_text(self.soup.get_text())
    
    def _process_json_ld(self, data):
        """Extract key info from JSON-LD"""
        if isinstance(data, list):
            data = data[0]
        
        if data.get('@type') == 'Product':
            return {
                "type": "product",
                "name": data.get("name"),
                "price": data.get("offers", {}).get("price"),
                "description": data.get("description")
            }
        elif data.get('@type') == 'Article':
            return {
                "type": "article",
                "headline": data.get("headline"),
                "author": data.get("author"),
                "content": data.get("articleBody")
            }
        return data
    
    def _clean_text(self, text):
        """Clean and normalize text"""
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        return text.strip()