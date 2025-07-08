from .base_adapter import BaseAdapter
from utils.logger import log
import re

class JobBoardAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        try:
            structured = self.parser.extract_structured_data()
            jobs = []
            for item in structured.get('json-ld', []):
                if item.get('@type') == 'JobPosting':
                    jobs.append({
                        "title": item.get("title"),
                        "company": item.get("hiringOrganization", {}).get("name"),
                        "location": item.get("jobLocation", {}).get("address", {}).get("addressLocality"),
                        "salary": item.get("baseSalary", {}).get("value", {}).get("value")
                    })
            # HTML fallback
            if not jobs:
                jobs = self._html_fallback(html)
            return {"type": "job_board", "jobs": jobs}
        except Exception as e:
            log.error(f"Job board extraction error: {e}")
            return {"error": str(e), "type": "job_board"}
    
    def _html_fallback(self, html):
        soup = self.parser.soup
        jobs = []
        
        for job in soup.select('.job, .result, .listing'):
            title = job.select_one('.title, .job-title')
            company = job.select_one('.company, .employer')
            location = job.select_one('.location, .geo')
            salary = job.select_one('.salary, .compensation')
            
            if title:
                jobs.append({
                    "title": title.get_text().strip(),
                    "company": company.get_text().strip() if company else None,
                    "location": location.get_text().strip() if location else None,
                    "salary": self._parse_salary(salary.get_text() if salary else None)
                })
        
        return jobs
    
    def _parse_salary(self, salary_text):
        if not salary_text:
            return None
            
        # Simple salary parser
        if 'k' in salary_text.lower():
            return float(re.sub(r'[^\d.]', '', salary_text)) * 1000
        return float(re.sub(r'[^\d.]', '', salary_text))