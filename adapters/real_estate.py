from .base_adapter import BaseAdapter
from utils.logger import log
import re

class RealEstateAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        try:
            structured = self.parser.extract_structured_data()
            properties = []
            for item in structured.get('json-ld', []):
                if item.get('@type') in ['SingleFamilyResidence', 'Apartment']:
                    properties.append({
                        "address": item.get("address", {}).get("streetAddress"),
                        "price": item.get("offers", {}).get("price"),
                        "bedrooms": item.get("numberOfBedrooms"),
                        "bathrooms": item.get("numberOfBathrooms"),
                        "sqft": item.get("floorSize", {}).get("value")
                    })
            # HTML fallback
            if not properties:
                properties = self._html_fallback(html)
            return {"type": "real_estate", "properties": properties}
        except Exception as e:
            log.error(f"Real estate extraction error: {e}")
            return {"error": str(e), "type": "real_estate"}
    
    def _html_fallback(self, html):
        soup = self.parser.soup
        properties = []
        
        for prop in soup.select('.property, .listing, .result'):
            address = prop.select_one('.address, .location')
            price = prop.select_one('.price, .list-price')
            details = prop.select_one('.details, .specs')
            
            if address and price:
                property_data = {
                    "address": address.get_text().strip(),
                    "price": self._parse_price(price.get_text())
                }
                
                if details:
                    # Extract bedrooms/bathrooms from details text
                    details_text = details.get_text().lower()
                    property_data["bedrooms"] = self._extract_detail(details_text, r'(\d+)\s*bed')
                    property_data["bathrooms"] = self._extract_detail(details_text, r'(\d+)\s*bath')
                    property_data["sqft"] = self._extract_detail(details_text, r'(\d+)\s*sq\.?ft')
                
                properties.append(property_data)
        
        return properties
    
    def _parse_price(self, price_text):
        # Convert "$1.2M" to 1200000, "$750K" to 750000
        if 'M' in price_text:
            return float(re.sub(r'[^\d.]', '', price_text)) * 1000000
        if 'K' in price_text:
            return float(re.sub(r'[^\d.]', '', price_text)) * 1000
        return float(re.sub(r'[^\d.]', '', price_text))
    
    def _extract_detail(self, text, pattern):
        match = re.search(pattern, text)
        return int(match.group(1)) if match else None