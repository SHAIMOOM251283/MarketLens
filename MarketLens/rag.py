import json
import shutil
from pathlib import Path
from collections import Counter

import pandas as pd

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores.utils import filter_complex_metadata


class HybridRAG:
    def __init__(self, file_path="data/scored_data.json"):
        self.data_path = Path(file_path).resolve()
        if not self.data_path.exists():
            raise FileNotFoundError(f"JSON not found: {self.data_path}")

        self.raw_data = self._load_raw_json()
        self.df = self._load_to_dataframe()

        # RAG components (kept for showcase)
        self.docs = self._create_documents()
        self.splits = self._split_text()
        self.vectorstore = self._create_vectorstore()
        self.retriever = self._setup_retriever()

        self.llm = ChatOllama(model="llama3.2:1b", temperature=0.2)
        self.prompt = self._create_prompt()
        self.rag_chain = self._create_rag_chain()

        print(f"✅ Hybrid RAG Ready — {len(self.df)} products loaded")

    def _load_raw_json(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_to_dataframe(self):
        df = pd.DataFrame(self.raw_data)
        numeric_cols = ['demand_score', 'rating', 'review_count', 'recommendation_percent',
                        'sentiment_score', 'normalized_rating', 'normalized_review_count',
                        'recommendation_score', 'feature_score']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['current_price_clean'] = df['current_price'].replace('[\$,]', '', regex=True).astype(float)
        return df

    def _create_documents(self):
        documents = []
        for item in self.raw_data:
            content = self._format_product(item)
            doc = Document(page_content=content, metadata={"title": item.get("title")})
            documents.append(doc)
        return documents

    def _format_product(self, item):
        pros = "\n".join(f"  • {k}: {v} mentions" for k, v in item.get("pros", {}).items())
        cons = "\n".join(f"  • {k}: {v} mentions" for k, v in item.get("cons", {}).items())
        features = "\n".join(f"  • {k}: {v}/5" for k, v in item.get("feature_ratings", {}).items())

        return f"""
🔹 PRODUCT: {item.get("title")}
   Model: {item.get("model")} | Price: {item.get("current_price")}

   KEY METRICS:
   • Demand Score: {item.get("demand_score")} ({item.get("demand_label")})
   • Rating: {item.get("rating")} ({item.get("review_count")} reviews)
   • Recommendation: {item.get("recommendation_percent")}%
   • Sentiment: {item.get("sentiment_score")}

   FEATURE RATINGS:
{features}

   PROS:
{pros or "  • None listed"}

   CONS:
{cons or "  • None listed"}

   SUMMARY:
   {item.get("ai_summary") or "N/A"}
"""

    def _split_text(self):
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
        return splitter.split_documents(self.docs)

    def _create_vectorstore(self):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        persist_dir = Path("chroma_db").resolve()
        if persist_dir.exists():
            shutil.rmtree(persist_dir)

        print("Creating fresh Chroma DB...")
        vectorstore = Chroma(
            persist_directory=str(persist_dir),
            embedding_function=embeddings,
            collection_name="tv_products",
        )
        filtered = filter_complex_metadata(self.splits)
        vectorstore.add_documents(filtered)
        return vectorstore

    def _setup_retriever(self):
        return self.vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 6})

    def _create_prompt(self):
        return ChatPromptTemplate.from_template(
            """You are an expert product analyst. Use ONLY the context below.

Context:
{context}

Question:
{question}

Answer:"""
        )

    def _create_rag_chain(self):
        return (
            {"context": self.retriever | (lambda docs: "\n\n---\n\n".join(d.page_content for d in docs)),
             "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    # ====================== STRONG RULE-BASED LAYER ======================
    def _get_highest_demand(self):
        idx = self.df['demand_score'].idxmax()
        row = self.df.iloc[idx]
        return f"**Highest Demand Product:**\n🔹 {row['title']}\nDemand Score: {row['demand_score']} ({row.get('demand_label','')})\nRating: {row['rating']} ({row['review_count']} reviews)"

    def _get_lowest_demand(self):
        idx = self.df['demand_score'].idxmin()
        row = self.df.iloc[idx]
        return f"**Lowest Demand Product:**\n🔹 {row['title']}\nDemand Score: {row['demand_score']}"

    def _get_high_demand_products(self):
        high = self.df[self.df['demand_label'] == "High Demand"]
        lines = [f"• {row['title']} ({row['demand_score']})" for _, row in high.iterrows()]
        return "High Demand Products:\n" + "\n".join(lines)

    def _get_medium_demand_products(self):
        medium = self.df[self.df['demand_label'] == "Medium Demand"]
        lines = [f"• {row['title']} ({row['demand_score']})" for _, row in medium.iterrows()]
        return "Medium Demand Products:\n" + "\n".join(lines)

    def _get_top_n_demand(self, n=3):
        top = self.df.nlargest(n, 'demand_score')
        lines = [f"{i+1}. {row['title']} ({row['demand_score']})" for i, row in top.iterrows()]
        return f"Top {n} Products by Demand:\n" + "\n".join(lines)

    def _get_best_value(self):
        self.df['value_score'] = (
            self.df['demand_score'] + 
            self.df['rating'] * 10 + 
            self.df['recommendation_percent'] / 2 - 
            self.df['current_price_clean'] / 10
        )
        idx = self.df['value_score'].idxmax()
        row = self.df.iloc[idx]
        return f"**Best Value for Money:**\n🔹 {row['title']}\nValue Score: {row['value_score']:.1f}\nPrice: {row['current_price']}\nRating: {row['rating']}"

    def _get_investment_recommendation(self):
        self.df['investment_score'] = (
            self.df['demand_score'] * 0.45 +
            self.df.get('normalized_review_count', 0) * 30 +
            self.df.get('recommendation_score', 0) * 20 +
            self.df.get('feature_score', 0) * 10 +
            self.df.get('normalized_rating', 0) * 10
        )
        top3 = self.df.nlargest(3, 'investment_score')
        best = top3.iloc[0]
        return f"**Best Product to Invest In:**\n🔹 {best['title']}\nInvestment Score: {best['investment_score']:.1f}\n\nTop 3:\n" + "\n".join(f"{i+1}. {row['title']} ({row['investment_score']:.1f})" for i, row in top3.iterrows())

    def _get_common_complaints(self):
        all_cons = []
        for cons_dict in self.df.get('cons', []):
            if isinstance(cons_dict, dict):
                all_cons.extend(cons_dict.keys())
        common = Counter(all_cons).most_common(6)
        return "Common complaints across products:\n" + "\n".join(f"• {k} ({v} mentions)" for k, v in common)

    def _get_brand_sentiment(self, brand):
        brand_df = self.df[self.df['title'].str.contains(brand, case=False, na=False)]
        if brand_df.empty:
            return f"No {brand} TVs found."
        lines = [f"• {row['title']} → Sentiment: {row['sentiment_score']}" for _, row in brand_df.iterrows()]
        return f"Sentiment scores for {brand.title()} TVs:\n" + "\n".join(lines)

    def _get_high_demand_low_sentiment(self):
        filtered = self.df[(self.df['demand_score'] > 75) & (self.df['sentiment_score'] < 72)]
        if filtered.empty:
            return "No products with high demand but relatively poor sentiment found."
        lines = [f"• {row['title']} (Demand: {row['demand_score']}, Sentiment: {row['sentiment_score']})" for _, row in filtered.iterrows()]
        return "High Demand but Lower Sentiment:\n" + "\n".join(lines)

    def _get_balanced_recommendation(self):
        self.df['balanced_score'] = (
            self.df['demand_score'] * 0.4 +
            self.df['sentiment_score'] * 0.3 +
            (self.df['rating'] * 10 + self.df['recommendation_percent'] / 2 - self.df['current_price_clean'] / 10) * 0.3
        )
        best = self.df.nlargest(1, 'balanced_score').iloc[0]
        return f"**Best Balanced TV (High Demand + Good Sentiment + Value):**\n🔹 {best['title']}\nBalanced Score: {best['balanced_score']:.1f}"

    def _get_overpriced(self):
        self.df['price_per_rating'] = self.df['current_price_clean'] / self.df['rating']
        expensive = self.df.nlargest(3, 'price_per_rating')
        return "Potentially Overpriced TVs (high price relative to rating):\n" + "\n".join(f"• {row['title']} (${row['current_price_clean']:.0f})" for _, row in expensive.iterrows())

    # Improved Pairwise Comparison
    def _get_pairwise_comparison(self, question):
        # More robust parsing
        q_clean = question.lower().replace(" versus ", " vs ").replace("—", " vs ")
        if " vs " not in q_clean:
            return "Please ask in format 'Samsung vs TCL'."

        parts = q_clean.split(" vs ")
        if len(parts) < 2:
            return "Could not parse comparison."

        p1 = parts[0].strip()
        p2 = parts[1].split(" — ")[0].strip() if " — " in parts[1] else parts[1].strip()

        df1 = self.df[self.df['title'].str.contains(p1, case=False, na=False)]
        df2 = self.df[self.df['title'].str.contains(p2, case=False, na=False)]

        if df1.empty or df2.empty:
            return f"Could not find both '{p1}' and '{p2}' in the data. Please check the exact names."

        row1 = df1.iloc[0]
        row2 = df2.iloc[0]

        return f"""**Comparison: {row1['title']} vs {row2['title']}**

Demand Score     : {row1['demand_score']} vs {row2['demand_score']}
Sentiment Score  : {row1['sentiment_score']} vs {row2['sentiment_score']}
Rating           : {row1['rating']} vs {row2['rating']}
Price            : {row1['current_price']} vs {row2['current_price']}
Recommendation   : {row1['recommendation_percent']}% vs {row2['recommendation_percent']}%"""

    # Main ask method
    def ask(self, question: str):
        q = question.lower().strip()

        # Category 1: Factual Demand
        if any(x in q for x in ["highest demand", "most demand"]):
            return self._get_highest_demand()
        if "lowest demand" in q:
            return self._get_lowest_demand()
        if "high demand" in q:
            return self._get_high_demand_products()
        if "medium demand" in q:
            return self._get_medium_demand_products()
        if "top 3" in q and "demand" in q:
            return self._get_top_n_demand(3)

        # Category 2: Value for Money
        if any(x in q for x in ["best value", "value for money", "best budget", "most features for the lowest price"]):
            return self._get_best_value()

        # Category 3: Sentiment
        if "sentiment" in q and "insignia" in q:
            return self._get_brand_sentiment("insignia")
        if "sentiment" in q:
            return self._get_sentiment_ranking()
        if "high demand" in q and ("poor sentiment" in q or "low sentiment" in q):
            return self._get_high_demand_low_sentiment()

        # Category 4: Complaints
        if any(x in q for x in ["complaint", "complaints", "problems", "issues"]):
            return self._get_common_complaints()

        # Category 5 & 7: Investment + Multi-criteria
        if any(x in q for x in ["invest", "investment", "should i buy", "recommend", "best product", "best overall"]):
            return self._get_investment_recommendation()
        if any(x in q for x in ["high demand", "good sentiment", "good value", "balances demand"]):
            return self._get_balanced_recommendation()

        # Category 6: Comparison (Improved)
        if " vs " in q or " versus " in q:
            return self._get_pairwise_comparison(question)

        # Overpriced
        if "overpriced" in q:
            return self._get_overpriced()

        # All remaining questions → full context fallback
        try:
            context = self.df.to_string(max_rows=None, max_colwidth=120)
            chain = self.prompt | self.llm | StrOutputParser()
            return chain.invoke({"context": context, "question": question})
        except Exception as e:
            return f"Error processing question: {str(e)}"

    def run(self):
        print("\n📺 Hybrid TV RAG Ready (type 'q' to exit)\n")
        while True:
            question = input("Enter Question: ").strip()
            if question.lower() == "q":
                print("Goodbye!")
                break
            if not question:
                continue
            print("\nAnswer:\n")
            print(self.ask(question))
            print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    rag = HybridRAG()
    rag.run()