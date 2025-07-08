from .base_adapter import BaseAdapter
from utils.logger import log

class ForumAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            thread = {
                "title": self._get_title(soup),
                "author": self._get_author(soup),
                "content": self._get_content(soup),
                "replies": self._get_replies(soup)
            }
            return {"type": "forum", "data": thread}
        except Exception as e:
            log.error(f"Forum extraction error: {e}")
            return {"error": str(e), "type": "forum"}
    
    def _get_title(self, soup):
        return (soup.select_one('h1.title, h1.thread-title, h1[itemprop=name]') 
                or soup.title).get_text().strip()
    
    def _get_author(self, soup):
        author_elem = soup.select_one('.post-author, .username, [itemprop=author]')
        return author_elem.get_text().strip() if author_elem else "Unknown"
    
    def _get_content(self, soup):
        content = soup.select_one('.post-content, .message-content, [itemprop=text]')
        return content.get_text().strip() if content else ""
    
    def _get_replies(self, soup):
        replies = []
        for post in soup.select('.post, .comment, .message'):
            # Skip main post
            if 'first-post' in post.get('class', []):
                continue
                
            author = post.select_one('.username, .author')
            content = post.select_one('.content, .message-body')
            
            if author and content:
                replies.append({
                    "author": author.get_text().strip(),
                    "content": content.get_text().strip(),
                    "timestamp": self._get_timestamp(post)
                })
        
        return replies
    
    def _get_timestamp(self, element):
        time_elem = element.select_one('time, .post-time')
        if time_elem and 'datetime' in time_elem.attrs:
            return time_elem['datetime']
        return time_elem.get_text().strip() if time_elem else None