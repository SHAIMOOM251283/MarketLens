import json
from pathlib import Path

class DemandScore:

    def __init__(self):
        self.INPUT_FILE = Path("data/final_features.json")
        self.OUTPUT_FILE = Path("data/scored_data.json")

    def normalize_review_counts(self, data):
        values = [p.get("log_review_count", 0) for p in data if p.get("log_review_count")]

        if not values:
            return {}

        min_val = min(values)
        max_val = max(values)

        normalized = {}

        for p in data:
            val = p.get("log_review_count", 0)

            if max_val == min_val:
                score = 0.5
            else:
                score = (val - min_val) / (max_val - min_val)

            normalized[id(p)] = round(score, 4)

        return normalized

    def normalize_recommendation(self, percent):
        if percent is None:
            return 0.5
        return round(percent / 100, 4)

    def compute_demand_score(self, p, review_scores):
        
        rating = p.get("normalized_rating", 0)
        reviews = review_scores.get(id(p), 0)
        sentiment = p.get("normalized_sentiment", 0)
        feature = p.get("feature_score", 0)
        price = p.get("price_score", 0)

        recommendation_percent = p.get("recommendation_percent")
        recommendation = self.normalize_recommendation(recommendation_percent)

        score = (
            0.25 * rating +
            0.20 * reviews +
            0.20 * sentiment +
            0.15 * feature +
            0.10 * price +
            0.10 * recommendation
        )

        return round(score * 100, 2)

    def assign_label(self, score):
        if score >= 75:
            return "High Demand"
        elif score >= 50:
            return "Medium Demand"
        else:
            return "Low Demand"


    def process_data(self, data):

        if isinstance(data, dict):
            data = [data]

        review_scores = self.normalize_review_counts(data)

        for p in data:
            demand_score = self.compute_demand_score(p, review_scores)
            demand_label = self.assign_label(demand_score)

            p["normalized_review_count"] = review_scores.get(id(p), 0)
            p["recommendation_score"] = self.normalize_recommendation(p.get("recommendation_percent"))

            p["demand_score"] = demand_score
            p["demand_label"] = demand_label

        return data

    def run(self):
        print("Loading feature data...")

        with open(self.INPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("Calculating demand scores...")

        scored_data = self.process_data(data)

        print("Saving scored data...")

        with open(self.OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(scored_data, f, indent=4, ensure_ascii=False)

        print("Done! Saved to data/scored_data.json")

if __name__ == "__main__":
    DemandScore().run()