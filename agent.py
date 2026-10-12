# agent.py
import os
import duckdb
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai
from vector_store import SchemaVectorStore

load_dotenv()

class Text2SQLAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        # Using the standard Google GenAI latest stable alias
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.vector_store = SchemaVectorStore()
        self.db_path = "sales.duckdb"

    def generate_sql(self, user_query: str, previous_error: str = None, failed_sql: str = None) -> str:
        context = self.vector_store.get_relevant_context(user_query)
        
        error_instruction = ""
        if previous_error and failed_sql:
            error_instruction = f"""
            PREVIOUS ATTEMPT FAILED!
            Failed SQL: {failed_sql}
            Error Message: {previous_error}
            FIX the SQL query so it runs properly on DuckDB. Return ONLY the raw SQL.
            """

        prompt = f"""
        You are an expert SQL Data Analyst. Your job is to convert user queries into valid DuckDB SQL queries.
        
        Database Context & Schema:
        {context}
        
        Rules:
        - Return ONLY valid executable DuckDB SQL.
        - Do NOT wrap SQL in markdown blocks like ```sql ... ``` or ```.
        - Do NOT include any explanations or commentary.
        {error_instruction}
        
        User Query: {user_query}
        """

        response = self.model.generate_content(prompt)
        sql = response.text.strip()
        
        if sql.startswith("```"):
            sql = sql.split("\n", 1)[-1].rsplit("\n", 1)[0].strip()
            if sql.startswith("sql"):
                sql = sql[3:].strip()
                
        return sql

    def execute_with_self_correction(self, user_query: str, max_retries: int = 3):
        conn = duckdb.connect(self.db_path)
        last_error = None
        last_sql = None

        for attempt in range(max_retries):
            try:
                sql_query = self.generate_sql(user_query, previous_error=last_error, failed_sql=last_sql)
                last_sql = sql_query
                
                df = conn.execute(sql_query).df()
                conn.close()
                return {"status": "success", "sql": sql_query, "data": df, "attempts": attempt + 1}

            except Exception as e:
                last_error = str(e)
                print(f"[Attempt {attempt + 1} Failed] Error: {last_error}")

        conn.close()
        return {"status": "error", "sql": last_sql, "error": last_error, "attempts": max_retries}