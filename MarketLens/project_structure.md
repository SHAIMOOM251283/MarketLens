### Step 1: Normalize Price

We invert it (because lower price = higher demand):

```python
price_score = (max_price - price) / (max_price - min_price) * 100
```

---

### Step 2: Add to Demand Formula

Updated weights:

| Factor              | Weight |
| ------------------- | ------ |
| Rating              | 30%    |
| Review Count        | 25%    |
| Recommendation %    | 20%    |
| Feature + Pros/Cons | 10%    |
| Sentiment           | 10%    |
| **Price**           | **5%** |

---

# 🏗️ Recommended Structure (VERY IMPORTANT)

## 📁 Project Layout

```
MarketLens/
│
├── data/
│   ├── raw.json
│   ├── enriched.json
│   ├── final_features.json
│   └── scored_data.json
│
├── images/
│   ├── home_page.png
│   ├── processing.png
│   └── chat.png
│
├── scripts/
│   ├── data_extraction.py
│   ├── sentiment_analysis.py
│   ├── feature_engineering.py
│   ├── demand_scoring.py
│   ├── rag.py
│   ├── app.py
│   ├── index.html
│   ├── styles.css
│   └── script.js   

---

# ⚙️ Step-by-Step Execution Plan

## ✅ Step 1: Raw Data (DONE)

You already have:

```
output.json → rename to raw.json
```

---

## ✅ Step 2: Sentiment Analysis (Separate Script)

### ✔️ YES — you should create a separate script

### Why?

* Keeps NLP logic isolated
* Easy to upgrade later (e.g., switch to better models)
* Cleaner debugging

---

### 📜 `1_sentiment_analysis.py`

**Input:**

```json
raw.json
```

**Output:**

```json
enriched.json
```

**Adds:**

```json
"sentiment_score": 78.5
```

---

👉 This script:

* Reads reviews
* Computes sentiment
* Saves updated JSON

---

## ✅ Step 3: Feature Engineering

### 📜 `2_feature_engineering.py`

**Input:**

```
enriched.json
```

**Output:**

```
final_features.json
```

---

### This script computes:

* Normalized rating
* Log review count
* Feature score
* Price score
* (Uses sentiment from previous step)

---

👉 This keeps all math in one place

---

## ✅ Step 4: Demand Scoring

### 📜 `3_demand_scoring.py`

**Input:**

```
final_features.json
```

**Output:**

```
scored_data.json
```

---

### This script:

* Applies final formula
* Outputs:

```json
"demand_score": 87.4,
"demand_label": "High"
```

---
