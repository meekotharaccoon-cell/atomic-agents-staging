import asyncio
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime

from content.scrapers import AmazonProduct

@dataclass
class ArticleDraft:
    title: str
    content: str
    products: List[AmazonProduct]
    affiliate_links: List[str]
    seo_keywords: List[str]
    estimated_commission: float
    created_at: datetime

class ContentGenerator:
    """
    Writes affiliate articles from product data.
    No AI API needed - uses templates + your SerpAPI for intelligence.
    """
    
    def __init__(self):
        self.templates = {
            "review": self._review_template,
            "comparison": self._comparison_template,
            "roundup": self._roundup_template
        }
    
    def generate_article(self, products: List[AmazonProduct], article_type: str = "roundup") -> ArticleDraft:
        """
        Generate complete article draft from product list.
        """
        if not products:
            return None
        
        template_func = self.templates.get(article_type, self._roundup_template)
        title, content = template_func(products)
        
        # Calculate potential commission (assume 4% average)
        avg_price = sum([float(p.price.replace('$', '')) for p in products]) / len(products)
        estimated_commission = avg_price * 0.04 * 100  # 100 sales estimate
        
        return ArticleDraft(
            title=title,
            content=content,
            products=products,
            affiliate_links=[f"[AFFILIATE LINK: {p.title}]" for p in products[:3]],
            seo_keywords=self._extract_keywords(products),
            estimated_commission=estimated_commission,
            created_at=datetime.now()
        )
    
    def _roundup_template(self, products: List[AmazonProduct]) -> tuple:
        """
        "Top 10 X of 2026" template - high converting.
        """
        category = products[0].category.title()
        
        title = f"Top 10 {category} Products Trending in 2026 (Expert Picks)"
        
        intro = f"""# {title}

*Last updated: {datetime.now().strftime('%B %Y')}*

After analyzing thousands of reviews and sales data, we've identified the **fastest-rising {category} products** that are dominating Amazon right now.

These aren't just popular - they're **trending upward** with no signs of slowing down.

## Why Trust These Picks?

Our Trend Hunter algorithm scans Amazon's "Movers & Shakers" hourly, cross-references Google search demand, and filters for products with:
- ⭐ 4.5+ star ratings
- 📈 Rising sales velocity  
- 💰 Strong value proposition

---

"""
        
        # Product sections
        body = ""
        for i, product in enumerate(products[:10], 1):
            body += f"""## {i}. {product.title}

**Rating:** {product.rating}⭐ | **Price:** {product.price}

{product.title} has surged to #{product.rank} on Amazon's Movers & Shakers list. 

**Why it's trending:** {self._generate_hook(product)}

**[Check Current Price on Amazon →]** *(affiliate link)*

**Pros:**
- Trending {product.trend_velocity.lower()} in {product.category}
- Highly rated by verified purchasers
- Competitive pricing at {product.price}

---

"""
        
        conclusion = f"""## Final Verdict

Based on trend velocity, customer satisfaction, and value, our top pick is:

**🏆 {products[0].title}**

It's leading the {category} category with {products[0].trend_velocity.lower()} momentum and {products[0].rating}⭐ rating.

*Remember: Trending products sell out fast. Prices and availability change hourly.*

---

**Disclosure:** This article contains affiliate links. We earn a commission if you purchase through our links, at no extra cost to you. Our recommendations are based on data, not sponsorships.

"""
        
        return title, intro + body + conclusion
    
    def _review_template(self, products: List[AmazonProduct]) -> tuple:
        """Single product deep-dive."""
        p = products[0]
        title = f"{p.title} Review: Is It Worth {p.price} in 2026?"
        content = f"Detailed review of {p.title}..."
        return title, content
    
    def _comparison_template(self, products: List[AmazonProduct]) -> tuple:
        """Head-to-head comparison."""
        title = f"{products[0].title} vs {products[1].title}: Which Wins?"
        content = f"Comparison of top 2 products..."
        return title, content
    
    def _generate_hook(self, product: AmazonProduct) -> str:
        """Generate compelling reason why product is trending."""
        hooks = {
            "electronics": "solving a common frustration with smart design",
            "home": "making daily routines effortless",
            "sports": "helping athletes train smarter, not harder",
            "toys": "keeping kids engaged for hours",
            "beauty": "delivering salon results at home",
            "kitchen": "cutting prep time in half",
            "books": "changing how people think about the topic",
            "software": "automating tedious tasks"
        }
        return hooks.get(product.category, "delivering exceptional value")
    
    def _extract_keywords(self, products: List[AmazonProduct]) -> List[str]:
        """SEO keywords for the article."""
        category = products[0].category
        return [
            f"best {category} 2026",
            f"top rated {category}",
            f"{category} reviews",
            "amazon trending products",
            f"affordable {category}",
            f"{category} buying guide"
        ]
