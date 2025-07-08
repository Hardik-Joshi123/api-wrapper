from .base_adapter import BaseAdapter
from utils.logger import log

class FinancialAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            # Detect financial statement types
            if 'income-statement' in url:
                return self._extract_income_statement(soup)
            if 'balance-sheet' in url:
                return self._extract_balance_sheet(soup)
            if 'cash-flow' in url:
                return self._extract_cash_flow(soup)
            # Default to stock data extraction
            return self._extract_stock_data(soup)
        except Exception as e:
            log.error(f"Financial extraction error: {e}")
            return {"error": str(e), "type": "financial"}
    
    def _extract_stock_data(self, soup):
        return {
            "type": "stock_data",
            "symbol": self._get_symbol(soup) if hasattr(self, '_get_symbol') else None,
            "price": self._get_price(soup) if hasattr(self, '_get_price') else None,
            "change": self._get_change(soup) if hasattr(self, '_get_change') else None,
            "key_metrics": self._get_key_metrics(soup) if hasattr(self, '_get_key_metrics') else None
        }
    
    def _extract_income_statement(self, soup):
        # Table-based extraction
        tables = soup.find_all('table')
        for table in tables:
            if 'revenue' in table.get_text().lower():
                return self._parse_financial_table(table)
        return {}
    
    def _parse_financial_table(self, table):
        # Simplified financial table parser
        headers = [th.get_text().strip() for th in table.select('tr:first-child th')]
        data = {}
        
        for row in table.select('tr'):
            label = row.select_one('td:first-child').get_text().strip()
            values = [td.get_text().strip() for td in row.select('td')[1:]]
            
            if label and values:
                data[label] = dict(zip(headers[1:], values))
        
        return data
    
    # Helper methods for stock data extraction...