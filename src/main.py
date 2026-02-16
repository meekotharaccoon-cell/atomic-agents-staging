import asyncio
from datetime import datetime
import os

class GumroadManual:
    def generate_product(self, trend: str, price: float = 19):
        templates = {
            "notion": {
                "name": f"Ultimate {trend.title()} Notion System",
                "description": f"""The complete {trend} workspace 2000+ people use.

**What is Inside:**
- 12 pre-built Notion templates
- 3 automated dashboards  
- Step-by-step video setup (15 min)
- Lifetime updates

**Price:** ${price}""",
                "price": price,
                "tags": "notion, template, productivity"
            },
            "budget": {
                "name": f"{trend.title()} Budget Mastery Kit",
                "description": f"""Stop living paycheck to paycheck.

**Includes:**
- Automated budget spreadsheet
- 7-day video course
- Expense tracker with 50+ categories
- Savings goal calculator

**Price:** ${price}""",
                "price": price,
                "tags": "budget, finance, money"
            },
            "business": {
                "name": f"{trend.title()} Business Launch Pack",
                "description": f"""Start your {trend} business in 7 days.

**Everything you need:**
- Legal contract templates
- Client acquisition scripts
- Pricing calculator
- 30-day launch checklist

**Price:** ${price}""",
                "price": price,
                "tags": "business, entrepreneur, templates"
            }
        }
        
        template = templates["notion"]
        if any(word in trend.lower() for word in ["budget", "money", "finance", "save"]):
            template = templates["budget"]
        elif any(word in trend.lower() for word in ["business", "client", "freelance", "agency"]):
            template = templates["business"]
        
        return {
            "platform": "Gumroad",
            "url": "https://gumroad.com/products/new",
            "name": template["name"],
            "price": template["price"],
            "description": template["description"],
            "tags": template["tags"]
        }

async def main():
    print("FRICTIONLESS BLITZ")
    print("==================")
    print("No APIs. No gates. Just copy/paste and earn.")
    print("==================\n")
    
    gumroad = GumroadManual()
    
    print("COMMANDS:")
    print("  'launch <trend>' - Generate product")
    print("  'multi' - Generate 3 products")
    print("  'quit' - Exit")
    print("\n")
    
    while True:
        cmd = input("Blitz: ").strip()
        
        if cmd == 'quit':
            break
        
        elif cmd.startswith('launch '):
            trend = cmd[7:]
            g = gumroad.generate_product(trend)
            
            print(f"\n{'='*60}")
            print(f"GUMROAD PRODUCT: {g['name']}")
            print(f"{'='*60}")
            print(f"\nURL: {g['url']}")
            print(f"\nNAME:\n{g['name']}")
            print(f"\nPRICE: ${g['price']}")
            print(f"\nTAGS: {g['tags']}")
            print(f"\nDESCRIPTION:\n{g['description']}")
            print(f"\n{'='*60}")
            print("COPY/PASTE INSTRUCTIONS:")
            print("1. Go to gumroad.com/products/new")
            print("2. Copy NAME above → paste in Name field")
            print("3. Set PRICE to $" + str(g['price']))
            print("4. Copy DESCRIPTION above → paste in Description")
            print("5. Add TAGS above to Tags field")
            print("6. Click PUBLISH")
            print(f"{'='*60}")
            
            os.makedirs("../data/products", exist_ok=True)
            filename = f"../data/products/{trend.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"PRODUCT: {g['name']}\n")
                f.write(f"PRICE: ${g['price']}\n")
                f.write(f"URL: {g['url']}\n\n")
                f.write(f"DESCRIPTION:\n{g['description']}\n")
            print(f"\nSaved to: {filename}")
        
        elif cmd == 'multi':
            trends = ["notion budget template", "freelance client tracker", "content calendar system"]
            for trend in trends:
                g = gumroad.generate_product(trend)
                print(f"\n{'='*60}")
                print(f"PRODUCT: {g['name']}")
                print(f"PRICE: ${g['price']}")
                print(f"TAGS: {g['tags']}")
                print(f"{'='*60}")
                
                os.makedirs("../data/products", exist_ok=True)
                filename = f"../data/products/{trend.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"PRODUCT: {g['name']}\n")
                    f.write(f"PRICE: ${g['price']}\n")
                    f.write(f"URL: {g['url']}\n\n")
                    f.write(f"DESCRIPTION:\n{g['description']}\n")
            
            print(f"\n{'='*60}")
            print(f"3 PRODUCTS GENERATED!")
            print("Check data/products/ folder")
            print("Copy each to Gumroad and publish!")
            print(f"{'='*60}")
        
        else:
            print("Commands: launch <trend>, multi, quit")

if __name__ == "__main__":
    asyncio.run(main())
