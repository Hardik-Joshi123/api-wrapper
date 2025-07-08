from .base_adapter import BaseAdapter
from utils.logger import log

class TravelAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            if '/hotel/' in url:
                return self._extract_hotel(soup)
            elif '/flights/' in url or '/airlines/' in url:
                return self._extract_flight(soup)
            elif '/restaurant/' in url:
                return self._extract_restaurant(soup)
            elif '/attraction/' in url:
                return self._extract_attraction(soup)
            elif '/reviews' in url:
                return self._extract_reviews(soup)
            else:
                return self._extract_generic_travel(soup)
        except Exception as e:
            log.error(f"Travel extraction error: {e}")
            return {"error": str(e), "type": "travel"}
    
    def _extract_hotel(self, soup):
        """Extract hotel information"""
        name = soup.select_one('h1.hotel-name, [data-testid="hotel-name"]')
        
        # Extract rating
        rating = soup.select_one('[itemprop="ratingValue"], .rating-value')
        review_count = soup.select_one('[itemprop="reviewCount"], .review-count')
        
        # Extract price
        price = soup.select_one('.price, .prco-valign-middle-helper')
        
        # Extract amenities
        amenities = []
        for amenity in soup.select('.amenity, .hotel-facilities li'):
            amenities.append(amenity.get_text().strip())
        
        # Extract location
        location = soup.select_one('.address, [data-testid="address"]')
        
        return {
            "type": "travel_hotel",
            "name": name.get_text().strip() if name else None,
            "rating": rating.get_text().strip() if rating else None,
            "review_count": review_count.get_text().strip() if review_count else None,
            "price": price.get_text().strip() if price else None,
            "amenities": amenities,
            "location": location.get_text().strip() if location else None
        }
    
    def _extract_flight(self, soup):
        """Extract flight information"""
        route = soup.select_one('.route, [data-testid="route"]')
        price = soup.select_one('.price-text, .f8F1-price-text')
        duration = soup.select_one('.duration, .durationTime')
        stops = soup.select_one('.stops, .stopsText')
        airlines = soup.select_one('.airline-name, .airlineText')
        
        return {
            "type": "travel_flight",
            "route": route.get_text().strip() if route else None,
            "price": price.get_text().strip() if price else None,
            "duration": duration.get_text().strip() if duration else None,
            "stops": stops.get_text().strip() if stops else None,
            "airlines": airlines.get_text().strip() if airlines else None
        }
    
    def _extract_restaurant(self, soup):
        """Extract restaurant information"""
        name = soup.select_one('h1.restaurant-name, [data-testid="restaurant-detail-name"]')
        cuisine = soup.select_one('.cuisine, .restaurant-detail-overview-cuisines')
        rating = soup.select_one('.rating, [data-testid="review-rating"]')
        price_range = soup.select_one('.price-range, .restaurant-details-info-price')
        address = soup.select_one('.address, [data-testid="restaurant-detail-address"]')
        
        return {
            "type": "travel_restaurant",
            "name": name.get_text().strip() if name else None,
            "cuisine": cuisine.get_text().strip() if cuisine else None,
            "rating": rating.get_text().strip() if rating else None,
            "price_range": price_range.get_text().strip() if price_range else None,
            "address": address.get_text().strip() if address else None
        }
    
    def _extract_attraction(self, soup):
        """Extract attraction information"""
        name = soup.select_one('h1.attraction-name, [data-testid="heading-title"]')
        rating = soup.select_one('.rating, .reviewCountAndRating')
        description = soup.select_one('.description, .attraction-overview-description')
        duration = soup.select_one('.duration, .recommended-duration')
        
        return {
            "type": "travel_attraction",
            "name": name.get_text().strip() if name else None,
            "rating": rating.get_text().strip() if rating else None,
            "description": description.get_text().strip() if description else None,
            "duration": duration.get_text().strip() if duration else None
        }
    
    def _extract_reviews(self, soup):
        """Extract travel reviews"""
        reviews = []
        
        for review in soup.select('.review, .review-container'):
            title = review.select_one('.quote, .reviewTitle')
            rating = review.select_one('.rating, .ui_bubble_rating')
            date = review.select_one('.ratingDate, .review-date')
            content = review.select_one('.partial_entry, .reviewText')
            author = review.select_one('.username, .member_info')
            
            # Extract rating from class (e.g., "bubble_50" → 5.0)
            rating_value = None
            if rating and 'class' in rating.attrs:
                classes = rating['class']
                for cls in classes:
                    if 'bubble_' in cls:
                        rating_value = int(cls.split('_')[-1]) / 10
            
            reviews.append({
                "title": title.get_text().strip() if title else None,
                "rating": rating_value or rating.get_text().strip() if rating else None,
                "date": date.get_text().strip() if date else None,
                "content": content.get_text().strip() if content else None,
                "author": author.get_text().strip() if author else None
            })
        
        return {
            "type": "travel_reviews",
            "count": len(reviews),
            "reviews": reviews
        }
    
    def _extract_generic_travel(self, soup):
        """Generic travel page extraction"""
        title = soup.select_one('h1')
        description = self._get_meta_description(soup)
        images = [img['src'] for img in soup.select('img[src]') if img['src'].startswith('http')]
        
        return {
            "type": "travel_generic",
            "title": title.get_text().strip() if title else None,
            "description": description,
            "images": images[:5]  # Return first 5 images
        }

    def _get_meta_description(self, soup):
        desc = soup.select_one('meta[name="description"]')
        return desc['content'].strip() if desc and 'content' in desc.attrs else None