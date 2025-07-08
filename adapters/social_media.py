from .base_adapter import BaseAdapter
from utils.logger import log

class SocialMediaAdapter(BaseAdapter):
    def extract(self, html, url):
        self.parse(html)
        soup = self.parser.soup
        try:
            if 'twitter.com' in url:
                return self._extract_twitter(soup)
            elif 'instagram.com' in url:
                return self._extract_instagram(soup)
            elif 'reddit.com' in url:
                return self._extract_reddit(soup)
            elif 'facebook.com' in url:
                return self._extract_facebook(soup)
            else:
                return self._extract_generic(soup)
        except Exception as e:
            log.error(f"Social media extraction error: {e}")
            return {"error": str(e), "type": "social_media"}
    
    def _extract_twitter(self, soup):
        """Extract tweet data from Twitter"""
        author = soup.select_one('[data-testid="User-Name"] a')
        content = soup.select_one('div[data-testid="tweetText"]')
        stats = soup.select('[data-testid="reply"] span, [data-testid="retweet"] span, [data-testid="like"] span')
        return {
            "type": "social_media",
            "platform": "twitter",
            "author": author.get_text().strip() if author else None,
            "content": content.get_text().strip() if content else None,
            "replies": stats[0].get_text().strip() if len(stats) > 0 else None,
            "retweets": stats[1].get_text().strip() if len(stats) > 1 else None,
            "likes": stats[2].get_text().strip() if len(stats) > 2 else None,
            "timestamp": self._get_timestamp(soup)
        }
    
    def _extract_instagram(self, soup):
        """Extract Instagram post data"""
        author = soup.select_one('header h2 a')
        content = soup.select_one('div.C4VMK span')
        image = soup.select_one('img[style="object-fit: cover;"]')
        stats = soup.select('span._ac2a')
        return {
            "type": "social_media",
            "platform": "instagram",
            "author": author.get_text().strip() if author else None,
            "content": content.get_text().strip() if content else None,
            "image": image['src'] if image and 'src' in image.attrs else None,
            "likes": stats[0].get_text().strip() if len(stats) > 0 else None,
            "comments": stats[1].get_text().strip() if len(stats) > 1 else None,
            "timestamp": self._get_timestamp(soup)
        }
    
    def _extract_reddit(self, soup):
        """Extract Reddit post data"""
        author = soup.select_one('a[href^="/user/"], a[href^="/u/"]')
        title = soup.select_one('h1')
        content = soup.select_one('[data-test-id="post-content"]')
        votes = soup.select_one('[id^="vote-arrows"]')
        comments = soup.select_one('[data-test-id="comments-page-link-num-comments"]')
        return {
            "type": "social_media",
            "platform": "reddit",
            "author": author.get_text().strip() if author else None,
            "title": title.get_text().strip() if title else None,
            "content": content.get_text().strip() if content else None,
            "votes": votes.get_text().strip() if votes else None,
            "comments": comments.get_text().strip() if comments else None,
            "timestamp": self._get_timestamp(soup)
        }
    
    def _extract_facebook(self, soup):
        """Extract Facebook post data"""
        author = soup.select_one('a[role="link"]')
        content = soup.select_one('div[data-ad-preview="message"]')
        reactions = soup.select_one('[aria-label*="reactions"]')
        comments = soup.select_one('div[aria-label="Comment"] span')
        shares = soup.select_one('div[aria-label="Share"] span')
        return {
            "type": "social_media",
            "platform": "facebook",
            "author": author.get_text().strip() if author else None,
            "content": content.get_text().strip() if content else None,
            "reactions": reactions.get_text().strip() if reactions else None,
            "comments": comments.get_text().strip() if comments else None,
            "shares": shares.get_text().strip() if shares else None,
            "timestamp": self._get_timestamp(soup)
        }
    
    def _extract_generic(self, soup):
        """Fallback for other social platforms"""
        author = soup.select_one('[itemprop="author"], .author, .username, .user')
        content = soup.select_one('[itemprop="text"], .content, .post-content')
        timestamp = self._get_timestamp(soup)
        
        return {
            "type": "social_media",
            "platform": "generic",
            "author": author.get_text().strip() if author else None,
            "content": content.get_text().strip() if content else None,
            "timestamp": timestamp
        }
    
    def _get_timestamp(self, soup):
        """Extract timestamp from common locations"""
        time_elem = soup.select_one('time[datetime]')
        if time_elem:
            return time_elem['datetime']
        
        # Fallback to text-based time
        time_elem = soup.select_one('time, .timestamp, .date, .posted-on')
        return time_elem.get_text().strip() if time_elem else None