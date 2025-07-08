from urllib.parse import urlparse
from adapters import (
    EcommerceAdapter,
    SocialMediaAdapter,
    NewsAdapter,
    ForumAdapter,
    JobBoardAdapter,
    RealEstateAdapter,
    FinancialAdapter,
    GovernmentAdapter,
    AcademicAdapter,
    TravelAdapter,
    GenericAdapter
)

class AdapterDetector:
    ADAPTER_MAP = [
        (r"amazon\.|ebay\.|shopify\.|etsy\.|alibaba\.", EcommerceAdapter),
        (r"twitter\.|facebook\.|instagram\.|reddit\./r/", SocialMediaAdapter),
        (r"reddit\./comments/|stackexchange\.|forum\.", ForumAdapter),
        (r"indeed\.|linkedin\./jobs|glassdoor\.", JobBoardAdapter),
        (r"zillow\.|realtor\.|redfin\.|trulia\.", RealEstateAdapter),
        (r"finance\.yahoo\.|sec\.gov|bloomberg\.", FinancialAdapter),
        (r"\.gov|wikipedia\.", GovernmentAdapter),
        (r"arxiv\.|researchgate\.|jstor\.", AcademicAdapter),
        (r"booking\.|tripadvisor\.|expedia\.", TravelAdapter),
        (r"nytimes\.|bbc\.|cnn\.|medium\.", NewsAdapter)
    ]
    
    @classmethod
    def get_adapter(cls, url):
        domain = urlparse(url).netloc
        
        for pattern, adapter in cls.ADAPTER_MAP:
            if re.search(pattern, domain + url):
                return adapter()
        
        return GenericAdapter()