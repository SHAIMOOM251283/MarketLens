import asyncio
import re
import json
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

class DataExtraction:

    def __init__(self):
        self.main_url = ""
        self.reviews_urls = []
        self.all_data = []
        self.semaphore = asyncio.Semaphore(5)  # limit concurrency

    # -----------------------------------
    # STEP 1: EXTRACT REVIEW URLS
    # -----------------------------------
    async def extract_reviews_url(self, page):
        print(f"🌐 Navigating to main page...")
        await page.goto(self.main_url, timeout=60000, wait_until="domcontentloaded")

        # DM for full code.

    # -----------------------------------
    # STEP 2: YOUR ORIGINAL LOGIC (UNCHANGED)
    # -----------------------------------
    async def extract_data_from_page(self, context, url):
        async with self.semaphore:
            page = await context.new_page()

            try:
                print(f"🔎 Scraping: {url}")
                await page.goto(url, timeout=90000, wait_until="domcontentloaded")

                await page.wait_for_selector('.product-info-container')

                # -------------------------------
                # PRODUCT INFO
                # -------------------------------

                # DM for full code.

                # -------------------------------
                # PRICING INFO
                # -------------------------------
                
                # DM for full code.

                # -------------------------------
                # RATING SUMMARY
                # -------------------------------
                
                # DM for full code.

                # -------------------------------
                # RATING DISTRIBUTION
                # -------------------------------
                
                # DM for full code.

                # -------------------------------
                # FEATURE RATINGS
                # -------------------------------
                
                # DM for full code. 

                # -------------------------------
                # PROS & CONS
                # -------------------------------
                
                pros = {}
                cons = {}

                # -------- PROS --------
                
                # DM for full code.

                # -------- CONS --------
                
                # DM for full code.

                # -------------------------------
                # RECOMMENDATION PERCENT
                # -------------------------------
                
                # DM for full code.
            
                # -------------------------------
                # AI SUMMARY
                # -------------------------------
                
                # DM for full code.
            
                # -------------------------------
                # SAMPLE REVIEWS
                # -------------------------------
                
                # DM for full code.

                return {
                    "url": url,
                    "title": title,
                    "model": model,
                    "sku": sku,
                    "current_price": current_price,
                    "original_price": original_price,
                    "savings": savings,
                    "rating": rating,
                    "review_count": review_count,
                    "rating_distribution": rating_distribution,
                    "feature_ratings": feature_ratings,
                    "pros": pros,
                    "cons": cons,
                    "recommendation_percent": recommendation_percent,
                    "ai_summary": ai_summary,
                    "reviews": reviews
                }

            except Exception as e:
                print(f"❌ Error: {url} -> {e}")
                return None

            finally:
                await page.close()

    # -----------------------------------
    # MAIN
    # -----------------------------------
    async def run(self):
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await self.extract_reviews_url(page)

            tasks = [
                self.extract_data_from_page(context, url)
                for url in self.reviews_urls
            ]

            results = await asyncio.gather(*tasks)

            self.all_data = [r for r in results if r]

            await browser.close()

        # SAVE JSON
        with open("data/raw.json", "w", encoding="utf-8") as f:
            json.dump(self.all_data, f, indent=4, ensure_ascii=False)

        print("\n✅ Data saved to output.json")


if __name__ == "__main__":
    asyncio.run(DataExtraction().run())