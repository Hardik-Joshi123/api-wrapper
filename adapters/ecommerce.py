from .base_adapter import BaseAdapter
from utils.logger import log
import re

class EcommerceAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        try:
            structured = self.parser.extract_structured_data()
            products = []
            for item in structured.get('json-ld', []):
                if item.get('@type') == 'Product':
                    products.append({
                        "name": item.get("name"),
                        "price": item.get("offers", {}).get("price"),
                        "currency": item.get("offers", {}).get("priceCurrency"),
                        "description": item.get("description"),
                        "category": self._detect_category(url)
                    })
            # Fallback to HTML parsing
            if not products:
                products = self._html_fallback(html)
            return {"type": "ecommerce", "products": products}
        except Exception as e:
            log.error(f"Ecommerce extraction error: {e}")
            return {"error": str(e), "type": "ecommerce"}
    
    def _detect_category(self, url):
        """Auto-detect product category from URL"""
        if '/electronics/' in url: return 'electronics'
        if '/clothing/' in url: return 'clothing'
        if '/books/' in url: return 'books'
        return 'general'
    
    def _html_fallback(self, html):
        # Simplified HTML fallback parser
        soup = self.parser.soup
        products = []
        
        for product in soup.select('.product, .item'):
            name_elem = product.select_one('.product-name, .title, [itemprop=name]')
            price_elem = product.select_one('.price, .product-price, [itemprop=price]')
            
            if name_elem and price_elem:
                price_text = price_elem.get_text()
                price = float(re.sub(r'[^\d.]', '', price_text)) if price_text else None
                
                products.append({
                    "name": name_elem.get_text().strip(),
                    "price": price,
                    "currency": 'USD' if '$' in price_text else None
                })
        
        return products