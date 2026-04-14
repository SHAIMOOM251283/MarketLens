import json
import math
from pathlib import Path

class Features:

    def __init__(self):
        self.INPUT_FILE = Path("data/enriched.json")
        self.OUTPUT_FILE = Path("data/final_features.json")

    def normalize_rating(self, rating):
        return round(rating / 5, 4) if rating else 0

    def compute_log_review_count(self, count):
        return round(math.log(count + 1), 4) if count else 0

    def compute_feature_score(self, feature_ratings):
        if not feature_ratings:
            return 0

        values = []

        for v in feature_ratings.values():
            try:
                values.append(float(v))
            except:
                continue

        if not values:
            return 0

        avg = sum(values) / len(values)
        return round(avg / 5, 4)  # normalize

    def normalize_prices(self, data):
        prices = []

        for product in data:
            price = product.get("price")
            if isinstance(price, (int, float)):
                prices.append(price)

        if not prices:
            return {}

        min_price = min(prices)
        max_price = max(prices)

        price_scores = {}

        for product in data:
            price = product.get("price")

            if not isinstance(price, (int, float)) or max_price == min_price:
                score = 0.5
            else:
                score = 1 - (price - min_price) / (max_price - min_price)

            price_scores[id(product)] = round(score, 4)

        return price_scores

    def process_data(self, data):
        # Ensure list
        if isinstance(data, dict):
            data = [data]

        price_scores = self.normalize_prices(data)

        for product in data:

            # --- Rating ---
            rating = product.get("rating", 0)
            product["normalized_rating"] = self.normalize_rating(rating)

            # --- Review Count ---
            review_count = product.get("review_count", 0)
            product["log_review_count"] = self.compute_log_review_count(review_count)

            # --- Feature Score ---
            feature_ratings = product.get("feature_ratings", {})
            product["feature_score"] = self.compute_feature_score(feature_ratings)

            # --- Price Score ---
            product["price_score"] = price_scores.get(id(product), 0.5)

            # --- Sentiment ---
            sentiment = product.get("sentiment_score", 0)
            product["normalized_sentiment"] = round(sentiment / 100, 4)

        return data

    def run(self):
        print("Loading enriched data...")

        with open(self.INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("Engineering features...")

        processed_data = self.process_data(data)

        print("Saving final features...")

        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=4, ensure_ascii=False)

        print("Done! Saved to data/final_features.json")

if __name__ == "__main__":
    Features().run()