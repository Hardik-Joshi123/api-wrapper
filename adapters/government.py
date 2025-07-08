from .base_adapter import BaseAdapter
from utils.logger import log
from urllib.parse import urljoin

class GovernmentAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            if self._is_pdf_page(soup):
                return self._extract_pdf_metadata(soup, url)
            if 'forms/' in url.lower():
                return self._extract_form(soup)
            if self._is_data_catalog(soup):
                return self._extract_data_catalog(soup)
            return self._extract_generic_government(soup)
        except Exception as e:
            log.error(f"Government extraction error: {e}")
            return {"error": str(e), "type": "government"}
    
    def _is_pdf_page(self, soup):
        """Check if page is linking to a PDF document"""
        return bool(soup.select_one('a[href$=".pdf"]'))
    
    def _extract_pdf_metadata(self, soup, url):
        """Extract metadata for PDF documents"""
        pdf_link = soup.select_one('a[href$=".pdf"]')
        return {
            "type": "government_document",
            "document_type": "pdf",
            "title": pdf_link.get_text().strip() if pdf_link else None,
            "url": urljoin(url, pdf_link['href']) if pdf_link else None,
            "description": self._get_meta_description(soup),
            "published_date": self._get_published_date(soup),
            "agency": self._extract_agency(soup)
        }
    
    def _extract_form(self, soup):
        """Extract government form information"""
        title = soup.select_one('h1.form-title') or soup.title
        form = soup.select_one('form')
        fields = []
        
        if form:
            for input_elem in form.select('input, select, textarea'):
                fields.append({
                    "name": input_elem.get('name'),
                    "type": input_elem.name,
                    "label": self._get_input_label(input_elem)
                })
        
        return {
            "type": "government_form",
            "title": title.get_text().strip() if title else None,
            "description": self._get_meta_description(soup),
            "fields": fields
        }
    
    def _is_data_catalog(self, soup):
        """Check if this is a data catalog page"""
        return bool(soup.select('.dataset, .data-catalog'))
    
    def _extract_data_catalog(self, soup):
        """Extract data catalog information"""
        datasets = []
        
        for dataset in soup.select('.dataset, .catalog-item'):
            title = dataset.select_one('.dataset-title, .catalog-title')
            description = dataset.select_one('.dataset-description, .catalog-desc')
            download = dataset.select_one('a[href$=".csv"], a[href$=".json"], a[href$=".xml"]')
            
            datasets.append({
                "title": title.get_text().strip() if title else None,
                "description": description.get_text().strip() if description else None,
                "download_url": download['href'] if download else None,
                "format": download['href'].split('.')[-1] if download else None
            })
        
        return {
            "type": "data_catalog",
            "count": len(datasets),
            "datasets": datasets
        }
    
    def _extract_generic_government(self, soup):
        """Extract generic government page information"""
        title = soup.select_one('h1.documentFirstHeading, h1.page-title')
        content = soup.select_one('#content-core, #main-content, .document-content')
        
        # Extract notices/alerts
        notices = []
        for notice in soup.select('.notice, .alert'):
            notices.append({
                "text": notice.get_text().strip(),
                "level": ' '.join(notice.get('class', []))
            })
        
        # Extract related links
        related_links = []
        for link in soup.select('.related-links a, .sidebar a'):
            related_links.append({
                "title": link.get_text().strip(),
                "url": link['href']
            })
        
        return {
            "type": "government_page",
            "title": title.get_text().strip() if title else None,
            "content": content.get_text().strip() if content else None,
            "agency": self._extract_agency(soup),
            "notices": notices,
            "related_links": related_links
        }
    
    def _extract_agency(self, soup):
        """Extract government agency information"""
        agency = soup.select_one('.agency-name, .department-name')
        return agency.get_text().strip() if agency else None

    def _get_meta_description(self, soup):
        desc = soup.select_one('meta[name="description"]')
        return desc['content'].strip() if desc and 'content' in desc.attrs else None

    def _get_published_date(self, soup):
        date = soup.select_one('meta[property="article:published_time"]')
        return date['content'] if date and 'content' in date.attrs else None

    def _get_input_label(self, input_elem):
        label = input_elem.find_previous('label')
        return label.get_text().strip() if label else None