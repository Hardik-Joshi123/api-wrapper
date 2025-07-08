from abc import ABC, abstractmethod
from core.parser import SmartParser
from utils.logger import log

class BaseAdapter(ABC):
    def __init__(self):
        self.parser = SmartParser()
    
    @abstractmethod
    def extract(self, html, url):
        """Main extraction method to be implemented by subclasses"""
        pass
    
    def parse(self, html):
        try:
            self.parser.parse(html)
            return self.parser
        except Exception as e:
            log.error(f"Parsing error: {e}")
            raise

    def safe_extract(self, html, url):
        """Wrapper for extract with error handling."""
        try:
            return self.extract(html, url)
        except Exception as e:
            log.error(f"Extraction error in {self.__class__.__name__}: {e}")
            return {"error": str(e), "type": self.__class__.__name__}