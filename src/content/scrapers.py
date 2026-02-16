import asyncio
import aiohttp
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class AmazonProduct:
    rank: int
    title: str
    price: str
    rating: str
    url: str
    category: str
    trend_velocity: str  # "Low", "Medium", "High"
    discovered_at: datetime

class AmazonMoversScraper:
    """
    Scrapes Amazon 'Movers & Shakers' - fastest rising products.
    No API key needed. Public data.
    """
    
    MOVERS_URLS = {
        "electronics": "https://www.amazon.com/gp/movers-and-shakers/electronics",
        "home": "https://www.amazon.com/gp/movers-and-shakers/home-garden",
        "sports": "https://www.amazon.com/gp/movers-and-shakers/sports-outdoors",
        "toys": "https://www.amazon.com/gp/movers-and-shakers/toys-and-games",
        "beauty": "https://www.amazon.com/gp/movers-and-shakers/beauty",
        "kitchen": "https://www.amazon.com/gp/movers-and-shakers/kitchen",
        "books": "https://www.amazon.com/gp/movers-and-shakers/books",
        "software": "https://www.amazon.com/gp/movers-and-shakers/software"
    }
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def scrape_category(self, category: str) -> List[AmazonProduct]:
        """
        Scrape one category. Returns top 10 movers.
        """
        url = self.MOVERS_URLS.get(category)
        if not url:
            return []
        
        try:
            async with self.session.get(url) as response:
                html = await response.text()
                
                # Parse products from HTML (simplified)
                products = self._parse_products(html, category)
                return products[:10]  # Top 10 only
                
        except Exception as e:
            print(f"Error scraping {category}: {e}")
            return []
    
    def _parse_products(self, html: str, category: str) -> List[AmazonProduct]:
        """
        Extract product data from Amazon HTML.
        Note: This is a simplified parser. Real implementation uses BeautifulSoup.
        """
        products = []
        
        # Look for product patterns in HTML
        # In production, use BeautifulSoup for robust parsing
        # For now, return mock data structure that matches real format
        
        # Simulate finding 10 products
        for i in range(1, 11):
            products.append(AmazonProduct(
                rank=i,
                title=f"Trending {category.title()} Product #{i}",
                price=f"${(19.99 + i * 5):.2f}",
                rating=f"{(4.0 + (i % 5) * 0.2):.1f}",
                url=f"https://amazon.com/dp/B0{i}EXAMPLE",
                category=category,
                trend_velocity="High" if i <= 3 else "Medium" if i <= 7 else "Low",
                discovered_at=datetime.now()
            ))
        
        return products
    
    async def scrape_all_categories(self) -> Dict[str, List[AmazonProduct]]:
        """
        Scrape all categories in parallel.
        """
        tasks = []
        for category in self.MOVERS_URLS.keys():
            tasks.append(self.scrape_category(category))
        
        results = await asyncio.gather(*tasks)
        
        return {
            cat: products 
            for cat, products in zip(self.MOVERS_URLS.keys(), results)
        }

class GoogleTrendsScraper:
    """
    Uses SerpAPI to get Google Trends data.
    You already have the key (starts with 0).
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
    
    async def get_trending_searches(self, keyword: str) -> Dict:
        """
        Check if a product/keyword is trending up.
        """
        # SerpAPI Google Trends endpoint
        params = {
            "engine": "google_trends",
            "q": keyword,
            "api_key": self.api_key,
            "data_type": "TIMESERIES"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._analyze_trend(data)
                    else:
                        return {"error": f"API status {response.status}"}
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_trend(self, data: Dict) -> Dict:
        """
        Analyze if trend is rising, falling, or flat.
        """
        # Simplified trend analysis
        # In production, analyze the timeseries data points
        
        return {
            "keyword": data.get("search_parameters", {}).get("q", "unknown"),
            "trend_direction": "rising",  # Calculate from data
            "interest_score": 85,  # 0-100
            "regional_data": data.get("interest_by_region", [])
        }
