# vector_store.py
import chromadb

class SchemaVectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name="db_schema_context")
        self._seed_context()

    def _seed_context(self):
        schemas = [
            "Table: customers (customer_id INTEGER, name VARCHAR, region VARCHAR, signup_date DATE)",
            "Table: sales (transaction_id INTEGER, customer_id INTEGER, product_category VARCHAR, amount DOUBLE, transaction_date DATE)",
            "Example Query: Find total revenue by region -> SELECT c.region, SUM(s.amount) as total_sales FROM sales s JOIN customers c ON s.customer_id = c.customer_id GROUP BY c.region",
            "Example Query: Top selling product category -> SELECT product_category, SUM(amount) as total_revenue FROM sales GROUP BY product_category ORDER BY total_revenue DESC LIMIT 1"
        ]
        ids = [f"doc_{i}" for i in range(len(schemas))]
        self.collection.add(documents=schemas, ids=ids)

    def get_relevant_context(self, user_query: str) -> str:
        results = self.collection.query(query_texts=[user_query], n_results=2)
        retrieved_docs = results['documents'][0]
        return "\n".join(retrieved_docs)