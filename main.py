"""
Free API Wrapper for Non-API Websites
Production-ready, commercial-grade solution with automatic site detection
"""

import re
import json
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, Tag
from core.requester import SmartRequester
from core.captcha import CaptchaSolver
from core.parser import SmartParser
from utils.logger import log


class BaseAdapter:
    """Abstract base class for all adapters"""
    def __init__(self):
        self.parser = SmartParser()
    
    def extract(self, html, url):
        """Main extraction method to be implemented by subclasses"""
        pass
    
    def parse(self, html):
        self.parser.parse(html)
        return self.parser


class ScraperAPI:
    """Main API class for scraping any website with automatic content detection"""
    
    def __init__(self, enable_captcha=True, enable_cache=True):
        """
        Initialize the API wrapper
        :param enable_captcha: Enable CAPTCHA solving features
        :param enable_cache: Enable response caching
        """
        self.requester = SmartRequester(enable_cache=enable_cache)
        self.captcha_solver = CaptchaSolver() if enable_captcha else None
        self.parser = SmartParser()
        self.adapter_map = self._initialize_adapter_map()
        
    def _initialize_adapter_map(self):
        """Create pattern-based adapter mapping"""
        return [
            # E-commerce
            (r"amazon\.|ebay\.|shopify\.|etsy\.|alibaba\.|walmart\.", EcommerceAdapter),
            # Social Media
            (r"twitter\.|facebook\.|instagram\.|reddit\.|pinterest\.|tiktok\.", SocialMediaAdapter),
            # Forums
            (r"reddit\./r/|stackexchange\.|forum\.|discourse\.|phpbb\.", ForumAdapter),
            # Job Boards
            (r"indeed\.|linkedin\./jobs|glassdoor\.|monster\.|careerbuilder\.", JobBoardAdapter),
            # Real Estate
            (r"zillow\.|realtor\.|redfin\.|trulia\.|century21\.|remax\.", RealEstateAdapter),
            # Financial
            (r"finance\.yahoo\.|sec\.gov|bloomberg\.|marketwatch\.|investing\.", FinancialAdapter),
            # Government
            (r"\.gov$|wikipedia\.|data\.gov|usa\.gov", GovernmentAdapter),
            # Academic
            (r"arxiv\.|researchgate\.|jstor\.|springer\.|sciencedirect\.", AcademicAdapter),
            # Travel
            (r"booking\.|tripadvisor\.|expedia\.|airbnb\.|kayak\.", TravelAdapter),
            # News
            (r"nytimes\.|bbc\.|cnn\.|medium\.|reuters\.|theguardian\.", NewsAdapter),
        ]
    
    def get_adapter(self, url):
        """
        Detect and return the appropriate content adapter
        :param url: Target URL
        :return: Content adapter instance
        """
        domain = urlparse(url).netloc
        path = urlparse(url).path
        
        for pattern, adapter in self.adapter_map:
            if re.search(pattern, domain + path, re.IGNORECASE):
                return adapter()
        
        return GenericAdapter()
    
    def get_content(self, url, force_captcha=False):
        """
        Fetch HTML content with CAPTCHA bypass if needed
        :param url: Target URL
        :param force_captcha: Always use CAPTCHA solver
        :return: HTML content
        """
        try:
            # First attempt with standard request
            response = self.requester.get(url)
            html = response.text
            
            # Check if CAPTCHA solving is needed
            if force_captcha or self._is_captcha_page(html):
                if not self.captcha_solver:
                    log.warning("CAPTCHA detected but solver disabled")
                    return html
                
                log.warning("CAPTCHA detected, solving...")
                return self.captcha_solver.solve(url)
                
            return html
        except Exception as e:
            log.critical(f"Scraping failed: {e}")
            raise
    
    def extract_data(self, url, html=None, structured_output=True):
        """
        Extract structured data from a URL
        :param url: Target URL
        :param html: Pre-fetched HTML (optional)
        :param structured_output: Return parsed data instead of raw HTML
        :return: Extracted content data
        """
        if not html:
            html = self.get_content(url)
        
        adapter = self.get_adapter(url)
        result = adapter.extract(html, url)
        
        if structured_output:
            return result
        return html
    
    def extract_products(self, url):
        """
        Specialized method for e-commerce product extraction
        :param url: Target product listing URL
        :return: List of product dictionaries
        """
        html = self.get_content(url)
        adapter = EcommerceAdapter()
        return adapter.extract(html, url)
    
    def extract_article(self, url):
        """
        Specialized method for news/article extraction
        :param url: Target article URL
        :return: Article content dictionary
        """
        html = self.get_content(url)
        adapter = NewsAdapter()
        return adapter.extract(html, url)
    
    def search(self, query, site=None, limit=10):
        """
        Basic site search implementation
        :param query: Search query
        :param site: Domain to limit search (optional)
        :param limit: Maximum results to return
        :return: List of search results
        """
        search_url = f"https://www.google.com/search?q={query}"
        if site:
            search_url += f"+site:{site}"
        
        html = self.get_content(search_url)
        soup = BeautifulSoup(html, 'lxml')
        
        results = []
        for i, result in enumerate(soup.select('.tF2Cxc')):
            if i >= limit:
                break
                
            title = result.select_one('h3').get_text()
            link = result.select_one('a')['href']
            snippet = result.select_one('.IsZvec').get_text() if result.select_one('.IsZvec') else ""
            
            results.append({
                "title": title,
                "url": link,
                "snippet": snippet
            })
        
        return results
    
    def _is_captcha_page(self, html):
        """Detect common CAPTCHA indicators"""
        captcha_indicators = [
            "captcha", "cloudflare", "challenge", "are you human",
            "recaptcha", "hcaptcha", "turnstile", "security check"
        ]
        lower_html = html.lower()
        return any(indicator in lower_html for indicator in captcha_indicators)


def run_demo():
    """Demonstration of API capabilities"""
    api = ScraperAPI()
    
    print("=" * 60)
    print("E-COMMERCE PRODUCT SCRAPING DEMO")
    print("=" * 60)
    products = api.extract_products("https://www.example-store.com/electronics")
    for i, product in enumerate(products[:3]):
        print(f"{i+1}. {product.get('name')} - ${product.get('price')}")
    print(f"Total products: {len(products)}\n")
    
    print("=" * 60)
    print("NEWS ARTICLE EXTRACTION DEMO")
    print("=" * 60)
    article = api.extract_article("https://news.example.com/important-news")
    print(f"Title: {article.get('title')}")
    print(f"Author: {article.get('author')}")
    print(f"Published: {article.get('published_date')}")
    print(f"Content: {article.get('content')[:200]}...\n")
    
    print("=" * 60)
    print("SOCIAL MEDIA EXTRACTION DEMO")
    print("=" * 60)
    tweet = api.extract_data("https://twitter.com/username/status/123456789")
    print(f"Author: {tweet.get('author')}")
    print(f"Content: {tweet.get('content')[:100]}...")
    print(f"Likes: {tweet.get('likes')}\n")
    
    print("=" * 60)
    print("GOVERNMENT DATA EXTRACTION DEMO")
    print("=" * 60)
    gov_data = api.extract_data("https://data.gov/dataset/example-data")
    print(f"Dataset title: {gov_data.get('title')}")
    print(f"Formats available: {', '.join(set(d['format'] for d in gov_data.get('datasets', [])))}\n")
    
    print("=" * 60)
    print("ACADEMIC PAPER EXTRACTION DEMO")
    print("=" * 60)
    paper = api.extract_data("https://arxiv.org/abs/1234.56789")
    print(f"Title: {paper.get('title')}")
    print(f"Authors: {', '.join(paper.get('authors', [])[:2])}...")
    print(f"Abstract: {paper.get('abstract')[:100]}...\n")

if __name__ == "__main__":
    run_demo()