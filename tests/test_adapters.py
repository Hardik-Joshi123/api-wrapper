import pytest
from adapters.ecommerce import EcommerceAdapter
from adapters.news import NewsAdapter
from adapters.social_media import SocialMediaAdapter
from adapters.forums import ForumAdapter
from adapters.job_boards import JobBoardAdapter
from adapters.real_estate import RealEstateAdapter
from adapters.financial import FinancialAdapter
from adapters.government import GovernmentAdapter
from adapters.academic import AcademicAdapter
from adapters.travel import TravelAdapter
from adapters.generic import GenericAdapter

# Example minimal HTML for each adapter
ecommerce_html = '<div class="product"><span class="product-name">Test Product</span><span class="price">$19.99</span></div>'
news_html = '<article><h1 class="headline">Test News</h1><div class="article-content">Content</div></article>'
social_html = '<div data-testid="tweetText">Hello Twitter!</div>'
forum_html = '<h1 class="title">Test Thread</h1><div class="post-content">First post</div>'
job_html = '<div class="job"><span class="title">Engineer</span><span class="company">Acme</span></div>'
real_estate_html = '<div class="property"><span class="address">123 Main</span><span class="price">$500K</span></div>'
financial_html = '<table><tr><th>Revenue</th></tr><tr><td>2023</td><td>$1M</td></tr></table>'
government_html = '<h1 class="page-title">Gov Page</h1>'
academic_html = '<h1 class="article-title">Research Paper</h1><div class="abstract">Abstract</div>'
travel_html = '<h1 class="hotel-name">Hotel Test</h1>'
generic_html = '<h1>Generic Page</h1>'

def test_ecommerce_extract():
    adapter = EcommerceAdapter()
    result = adapter.extract(ecommerce_html, "https://shop.com/product/1")
    assert result["type"] == "ecommerce"

def test_news_extract():
    adapter = NewsAdapter()
    result = adapter.extract(news_html, "https://news.com/article/1")
    assert result["type"] == "news"

def test_social_media_extract():
    adapter = SocialMediaAdapter()
    result = adapter.extract(social_html, "https://twitter.com/test/status/1")
    assert result["type"] == "social_media"

def test_forum_extract():
    adapter = ForumAdapter()
    result = adapter.extract(forum_html, "https://forum.com/thread/1")
    assert result["type"] == "forum"

def test_job_board_extract():
    adapter = JobBoardAdapter()
    result = adapter.extract(job_html, "https://jobs.com/listing/1")
    assert result["type"] == "job_board"

def test_real_estate_extract():
    adapter = RealEstateAdapter()
    result = adapter.extract(real_estate_html, "https://realestate.com/listing/1")
    assert result["type"] == "real_estate"

def test_financial_extract():
    adapter = FinancialAdapter()
    result = adapter.extract(financial_html, "https://finance.com/income-statement")
    assert result["type"] == "stock_data" or "income-statement" in str(result).lower()

def test_government_extract():
    adapter = GovernmentAdapter()
    result = adapter.extract(government_html, "https://gov.com/page/1")
    assert result["type"] in ("government_document", "government_form", "data_catalog", "government_page")

def test_academic_extract():
    adapter = AcademicAdapter()
    result = adapter.extract(academic_html, "https://journals.com/paper/1")
    assert result["type"] == "academic"

def test_travel_extract():
    adapter = TravelAdapter()
    result = adapter.extract(travel_html, "https://travel.com/hotel/1")
    assert result["type"].startswith("travel_")

def test_generic_extract():
    adapter = GenericAdapter()
    result = adapter.extract(generic_html, "https://generic.com/page/1")
    assert result["type"] == "generic" 