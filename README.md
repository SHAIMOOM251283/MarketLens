# MarketLens

**AI-Powered Product Intelligence from Real-World Data**

---

## 🚀 Overview

MarketLens is an end-to-end AI-driven market intelligence system designed to transform real-world e-commerce data into actionable investment insights.

It enables data-driven decision-making by analyzing product demand, customer sentiment, pricing behavior, and feature-level feedback to identify high-potential products for investment and resale opportunities.

The system combines **automated data processing**, **multi-stage analytical modeling**, and a **hybrid RAG-based reasoning engine** to deliver intelligent, natural language insights over structured market data.

---

## 🧠 Core Objective

MarketLens is built for **product investment intelligence**, enabling users to:

- Identify high-demand products with strong market signals
- Detect undervalued products with high potential return
- Compare competing products based on multi-factor analysis
- Evaluate pricing inefficiencies and value opportunities
- Support data-driven product investment decisions

---

## 🔄 System Architecture

MarketLens follows a complete end-to-end intelligence pipeline:

---

### 1. Data Acquisition Layer (Abstracted)

The system is designed around real-world e-commerce data extraction pipelines.

- Automated browser-based data collection from product listing platforms
- Stealth-enabled extraction framework for robust data retrieval
- Collection of:
  - Product metadata (title, model, pricing)
  - Ratings and reviews
  - Feature-level feedback
  - Pros and cons from customer reviews
  - Summary-level insights

---

### 2. Data Processing & Intelligence Layer

Raw data is transformed into structured investment signals using:

- Sentiment analysis
- Feature engineering
- Demand scoring models
- Recommendation scoring
- Price normalization
- Value-based feature weighting

This layer converts unstructured market data into **quantifiable investment indicators**.

---

### 3. AI Reasoning Layer (Hybrid RAG Engine)

MarketLens uses a hybrid intelligence approach combining:

- Vector-based semantic retrieval (ChromaDB)
- Embedding generation (Ollama)
- Large language model reasoning (Llama-based model)
- Rule-based analytical decision system

This enables both:

- Deterministic analytics (ranking, scoring, comparisons)
- Natural language reasoning over structured market intelligence

---

### 4. Interactive Decision Interface (Flask App)

A lightweight web application allows users to:

- Upload structured product datasets (JSON)
- Ask natural language investment questions
- Receive real-time analytical insights
- Perform product comparisons and evaluations

---

## 💡 Key Features

- End-to-end data processing pipeline from raw product data to structured intelligence
- Review-level sentiment analysis with normalized scoring (0–100 → 0–1)
- Multi-factor feature engineering across rating, sentiment, price, and product attributes
- Log-scaled and normalized review count modeling to capture relative popularity
- Relative price normalization for value-based comparison within datasets
- Aggregation of feature-level ratings into unified product quality scores
- Weighted demand scoring model combining multiple product signals
- Rule-based demand classification (High / Medium / Low)
- Structured dataset enrichment for downstream AI reasoning (RAG integration)
- Dynamic dataset ingestion and querying via Flask interface

---

## 💰 Investment-Oriented Use Cases

MarketLens is designed for **market opportunity and product investment analysis**, including:

- Identifying high-demand products for resale potential
- Detecting undervalued products with strong sentiment signals
- Comparing competing brands to identify market leaders
- Finding price-to-demand inefficiencies in product categories
- Evaluating product viability using multi-signal scoring models
- Supporting strategic product investment decisions

---

## 🛠️ Tech Stack

- Python
- Flask
- Pandas
- LangChain
- ChromaDB
- Ollama (LLM + embeddings)
- Playwright (stealth-enabled browser automation)
- Tailwind CSS

---

## 📊 Data Pipeline

```

Raw E-commerce Data
↓
Data Processing & Cleaning
↓
Feature Engineering & Scoring
↓
Structured Investment Dataset
↓
Hybrid RAG Knowledge Engine
↓
AI-Powered Decision Interface

```

---

## 📁 Project Structure

```
MarketLens-Repo/
│
├── images/
│   ├── home_page.png
│   ├── processing.png
│   └── chat.png
│
├── MarketLens/
│   │
│   ├── data/
│   │   ├── raw.json
│   │   ├── enriched.json
│   │   ├── final_features.json
│   │   └── scored_data.json
│   │
│   ├── data_extraction.py 
│   ├── sentiment_analysis.py
│   ├── feature_engineering.py
│   ├── demand_scoring.py
│   ├── rag.py
│   ├── app.py
│   ├── index.html
│   ├── styles.css
│   └── script.js
│
├── README.md
└── LICENSE

---

## ⚙️ Installation & Setup

### 1. Clone repository

```bash
git clone https://github.com/SHAIMOOM251283/MarketLens
cd MarketLens
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the application

The system uses preprocessed datasets for inference.

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

## 🖼️ Interface Preview

*Home Page (Data Upload Interface)*
![Home Page](https://github.com/SHAIMOOM251283/MarketLens/blob/main/images/home_page.png)

*Processing Dashboard overlay*
![Processing Dashboard overlay](https://github.com/SHAIMOOM251283/MarketLens/blob/main/images/processing.png)

*AI Chat & Decision Interface*
![AI Chat & Decision Interface](https://github.com/SHAIMOOM251283/MarketLens/blob/main/images/chat_interface.png)

---

## ⚡ What Makes MarketLens Unique

MarketLens is not a chatbot or a simple RAG application.

It is a **full-scale decision intelligence system** that combines:

* Real-world data acquisition pipelines
* Multi-layer analytical scoring models
* Hybrid AI reasoning (rules + retrieval)
* Investment-oriented decision support system

It bridges the gap between raw market data and actionable investment intelligence.

---

## 📄 License

This project is licensed under the MIT License.

---
