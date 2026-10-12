# 🤖 Autonomous Text-to-SQL Data Agent & Self-Correction Analytics Engine

An end-to-end Agentic AI system that transforms natural language prompts into optimized SQL queries, handles self-correction on execution errors, and dynamically auto-generates data visualizations.

## 🌟 Key Features

- **Agentic Self-Correction Loop**: Catches SQL execution runtime errors and re-prompts the LLM with backtrace feedback (up to 3 retries).
- **RAG Schema Contextualization**: Uses **ChromaDB** vector embedding store to inject database schema and few-shot query patterns.
- **Fast Local/In-Memory Analytics**: Powered by **DuckDB** for lightning-fast OLAP query execution.
- **Auto-Visualization**: Automatically identifies categorical and numerical aggregations to build live **Plotly** charts.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **LLM Engine**: Groq API (`llama-3.3-70b-versatile`)
- **Vector DB**: ChromaDB
- **Database Layer**: DuckDB
- **UI Framework**: Streamlit

## 🚀 Quickstart

1. Clone repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/text2sql-data-agent.git](https://github.com/YOUR_USERNAME/text2sql-data-agent.git)
   cd text2sql-data-agent
   ```
