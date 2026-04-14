import json
from textblob import TextBlob
from pathlib import Path

class SentimentAnalysis:

    def __init__(self):
        self.INPUT_FILE = Path("data/raw.json")
        self.OUTPUT_FILE = Path("data/enriched.json")

    def compute_sentiment_score(self, reviews):
        if not reviews:
            return 0

        scores = []

        for review in reviews:
            try:
                # Extract correct field
                if isinstance(review, dict):
                    review = review.get("body", "")   # ✅ FIXED

                if not isinstance(review, str) or not review.strip():
                    continue

                polarity = TextBlob(review).sentiment.polarity
                scores.append(polarity)

            except Exception as e:
                print("Error processing review:", e)
                continue

        if not scores:
            return 0

        avg_score = sum(scores) / len(scores)
        normalized_score = (avg_score + 1) / 2 * 100

        return round(normalized_score, 2)

    def process_data(self, data):
        if isinstance(data, dict):
            data = [data]

        for product in data:
            reviews = product.get("reviews", [])   # ✅ FIXED
            sentiment_score = self.compute_sentiment_score(reviews)

            product["sentiment_score"] = sentiment_score

        return data

    def run(self):
        print("Loading raw data...")

        with open(self.INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("Computing sentiment scores...")

        enriched_data = self.process_data(data)

        print("Saving enriched data...")

        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(enriched_data, f, indent=4, ensure_ascii=False)

        print("Done! Saved to data/enriched.json")


if __name__ == "__main__":
    SentimentAnalysis().run()