# 🤖 Autonomous Text-to-SQL Data Agent

### Agentic AI • RAG • Self-Correcting SQL • DuckDB • ChromaDB • Streamlit

> **Transform natural language into executable SQL, automatically recover from SQL execution errors, and turn query results into interactive business intelligence dashboards.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-Analytics-FFF000?logo=duckdb&logoColor=black)](https://duckdb.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-FF6F61)](https://www.trychroma.com/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![Google Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)

---

## 📌 Overview

**Autonomous Text-to-SQL Data Agent** is an agentic AI-powered analytics system that allows users to interact with structured databases using natural language.

Instead of manually writing SQL queries, users can simply ask questions such as:

> **"Show total revenue by region and customer count."**

The system automatically:

1. Understands the user's natural-language request.
2. Retrieves relevant database schema information using **RAG**.
3. Generates SQL using **Google Gemini**.
4. Executes the generated query using **DuckDB**.
5. Detects SQL/runtime errors automatically.
6. Sends execution feedback back to the LLM.
7. Repairs and retries the query.
8. Converts the final result into a Pandas DataFrame.
9. Generates interactive visualizations using **Plotly**.
10. Displays everything through a modern **Streamlit analytics interface**.

The result is a lightweight **self-correcting Text-to-SQL analytics agent** designed to demonstrate how LLMs, RAG, databases, and agentic workflows can work together.

---

# 🧠 System Architecture

```text
                    ┌─────────────────────────────┐
                    │      User Natural Query     │
                    │  "Revenue by region..."     │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       RAG Context Layer     │
                    │          ChromaDB            │
                    │                             │
                    │ • Table schemas             │
                    │ • Relationships             │
                    │ • Few-shot SQL examples     │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Google Gemini         │
                    │      SQL Generation         │
                    │                             │
                    │ Natural Language → SQL      │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │         DuckDB              │
                    │      Query Execution        │
                    └──────────────┬──────────────┘
                                   │
                         ┌─────────┴─────────┐
                         │                   │
                      SUCCESS              ERROR
                         │                   │
                         ▼                   ▼
              ┌─────────────────┐   ┌─────────────────────┐
              │ Fetch DataFrame │   │ Self-Correction     │
              │                 │   │ Feedback Loop       │
              └────────┬────────┘   └──────────┬──────────┘
                       │                       │
                       │                  Error + SQL
                       │                       │
                       │                       ▼
                       │              ┌─────────────────┐
                       │              │ Gemini Re-prompt│
                       │              └────────┬────────┘
                       │                       │
                       │                  Retry ≤ 3
                       │                       │
                       │              ┌────────▼────────┐
                       │              │ Corrected SQL   │
                       │              └────────┬────────┘
                       │                       │
                       └───────────────┬───────┘
                                       ▼
                         ┌──────────────────────────┐
                         │     Streamlit Dashboard  │
                         │                          │
                         │ • Data Table             │
                         │ • Metrics                │
                         │ • Bar Chart              │
                         │ • Line Chart             │
                         │ • Pie Chart              │
                         │ • CSV Export             │
                         └──────────────────────────┘
```

---

# ✨ Key Features

## 🤖 1. Agentic Text-to-SQL

Convert natural-language questions into executable SQL without requiring users to understand SQL syntax.

**Example:**

```text
User:
"Show total revenue by region."

        ↓

Gemini generates:

SELECT region, SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC;
```

---

## 🔄 2. Self-Correction & Automatic Retry

Traditional Text-to-SQL systems often fail when an LLM generates:

- Incorrect table names
- Incorrect column names
- Invalid SQL syntax
- Unsupported SQL operations
- Schema mismatches

This project introduces an automated **SQL self-correction loop**.

```text
Generated SQL
     │
     ▼
DuckDB Execution
     │
     ├── Success ──────► Return Data
     │
     └── Error
           │
           ▼
      Capture Error
           │
           ▼
    Send Error + SQL
      back to Gemini
           │
           ▼
      Generate Fix
           │
           ▼
       Retry Query
           │
      Maximum 3 Attempts
```

This makes the system more resilient to LLM-generated SQL errors.

---

## 🧠 3. RAG-Powered Schema Retrieval

Instead of sending the complete database schema to the LLM every time, the system uses **ChromaDB** to retrieve relevant context.

The vector store can contain:

- Table schemas
- Column descriptions
- Relationships
- Foreign-key information
- Domain-specific examples
- Few-shot SQL queries

### Query Flow

```text
User Question
      ↓
Semantic Search
      ↓
Relevant Schema Context
      ↓
Gemini
      ↓
SQL Generation
```

This helps reduce unnecessary context and improves SQL generation quality.

---

## ⚡ 4. DuckDB Analytical Engine

The project uses **DuckDB** as the analytical execution layer.

DuckDB is particularly suitable for analytical workloads because it provides:

- Columnar execution
- Fast aggregations
- SQL analytics
- In-process execution
- Python integration
- OLAP-oriented workloads

The generated SQL is executed directly against the local analytical database.

---

## 📊 5. Automatic Data Visualization

After successful SQL execution, the result is converted into a Pandas DataFrame.

The application dynamically analyzes:

- Numerical columns
- Categorical columns
- Date/time columns
- Aggregated values

Users can visualize results using:

- 📊 Bar Charts
- 📈 Line Charts
- 🥧 Pie Charts
- 📋 Data Tables

---

## 🖥️ 6. Streamlit Analytics Interface

The project provides a lightweight SaaS-style interface built with Streamlit.

The interface includes:

- Natural-language query input
- Database/schema inspection
- SQL generation
- Query execution
- Error feedback
- Result preview
- Row/column metrics
- Interactive Plotly charts
- CSV export

---

# 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python 3.11+ |
| LLM | Google Gemini |
| AI Orchestration | Custom Agentic Workflow |
| RAG | ChromaDB |
| Analytical Database | DuckDB |
| Data Processing | Pandas |
| Visualization | Plotly |
| Web Interface | Streamlit |
| Configuration | python-dotenv |
| Environment | Local / Streamlit Cloud |

---

# 📂 Project Structure

```text
text2sql-data-agent/
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
│
├── db_setup.py
│   └── Creates DuckDB schema and sample data
│
├── vector_store.py
│   └── Builds and queries ChromaDB schema context
│
├── agent.py
│   └── Core Text-to-SQL agent
│       ├── Prompt construction
│       ├── SQL generation
│       ├── SQL execution
│       ├── Error detection
│       └── Self-correction loop
│
└── app.py
    └── Streamlit application
        ├── Query interface
        ├── Results
        ├── Metrics
        ├── Visualizations
        └── CSV export
```

---

# 🔄 End-to-End Workflow

### Step 1 — User Query

The user enters a natural-language question.

```text
"Show the top 5 product categories by total sales."
```

### Step 2 — Retrieve Context

ChromaDB searches for the most relevant database schema and SQL examples.

### Step 3 — Generate SQL

Gemini receives:

```text
User Question
+
Relevant Schema
+
Few-shot Examples
+
SQL Instructions
```

and generates DuckDB-compatible SQL.

### Step 4 — Execute SQL

The generated SQL is executed against DuckDB.

### Step 5 — Detect Errors

If DuckDB returns an error:

```text
Binder Error:
Referenced column "sale_amount" not found
```

the error is captured.

### Step 6 — Self-Correction

The agent sends the failed SQL and execution error back to Gemini.

```text
Original SQL
+
DuckDB Error
+
Schema Context
```

Gemini generates a corrected query.

### Step 7 — Retry

The system retries the corrected query.

```text
Attempt 1 → Failed
Attempt 2 → Failed
Attempt 3 → Success
```

Maximum retry attempts are limited to prevent infinite loops.

### Step 8 — Analytics

The resulting dataset is converted into a Pandas DataFrame.

### Step 9 — Visualization

Plotly generates an interactive visualization.

### Step 10 — Export

Users can download the resulting data as CSV.

---

# 💬 Example Natural-Language Queries

Try questions such as:

```text
Show total revenue by region with customer count.
```

```text
Show the top selling product category by total sales.
```

```text
Show total amount sold by transaction date.
```

```text
Which region generated the highest revenue?
```

```text
Show the top 5 customers by total purchase amount.
```

```text
Compare sales performance across regions.
```

---

# 🧪 Example Agent Execution

```text
USER QUERY
    │
    ▼
"Which region generated the highest revenue?"
    │
    ▼
CHROMADB
Retrieve relevant sales schema
    │
    ▼
GEMINI
Generate SQL
    │
    ▼
DUCKDB
Execute SQL
    │
    ├── ❌ Error
    │      │
    │      ▼
    │   Error Feedback
    │      │
    │      ▼
    │   GEMINI
    │      │
    │      ▼
    │   Corrected SQL
    │      │
    │      ▼
    │   DUCKDB
    │
    └── ✅ Success
           │
           ▼
       PANDAS
           │
           ▼
       PLOTLY
           │
           ▼
    STREAMLIT DASHBOARD
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/uzaibsaiyed78616-hash/text2sql-data-agent.git

cd text2sql-data-agent
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

> ⚠️ **Never commit your `.env` file to GitHub.**

Make sure `.gitignore` contains:

```gitignore
.env
venv/
__pycache__/
*.duckdb
*.db
.chroma/
```

---

## 5. Initialize the Database

Run:

```bash
python db_setup.py
```

This creates the local DuckDB database and populates the sample analytical dataset.

---

## 6. Start the Application

```bash
streamlit run app.py
```

The application will start locally and Streamlit will provide a local URL.

---

# 🔐 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GEMINI_API_KEY` | Google Gemini API key | ✅ Yes |

---

# 📈 Project Highlights

### Why this project is different

Most basic Text-to-SQL projects follow:

```text
User → LLM → SQL → Database
```

This project extends that architecture:

```text
User
  ↓
RAG
  ↓
LLM
  ↓
SQL
  ↓
Database
  ↓
Error Detection
  ↓
LLM Self-Correction
  ↓
Retry
  ↓
DataFrame
  ↓
Visualization
```

This makes the project a practical demonstration of:

- **Generative AI**
- **Agentic AI**
- **Retrieval-Augmented Generation**
- **Text-to-SQL**
- **LLM Tool Use**
- **Automatic Error Recovery**
- **Data Analytics**
- **Business Intelligence**
- **Interactive Visualization**

---

# 🧩 Architecture Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Natural Language → SQL | Gemini |
| Retrieval-Augmented Generation | ChromaDB |
| Vector Search | ChromaDB |
| SQL Execution | DuckDB |
| Error Recovery | Self-correction loop |
| Data Processing | Pandas |
| Visualization | Plotly |
| UI | Streamlit |
| Environment Management | `.env` |
| Analytics | SQL + DataFrame |

---

# ☁️ Deployment

The application can be deployed using:

### Streamlit Community Cloud

1. Push the repository to GitHub.
2. Connect the repository to Streamlit Community Cloud.
3. Select `app.py` as the application entry point.
4. Add the `GEMINI_API_KEY` inside Streamlit Secrets.
5. Deploy.

### Production Considerations

For production deployment, consider:

- API rate limiting
- Authentication
- Query logging
- Database access controls
- SQL validation
- Prompt-injection protection
- Query timeout limits
- Cost monitoring
- Persistent vector storage
- Observability and logging

---

# 🔒 Security Considerations

Because this system generates SQL dynamically, production implementations should include additional safeguards.

Recommended controls:

```text
User Input
    ↓
Prompt Validation
    ↓
Schema-Constrained SQL Generation
    ↓
SQL Validation
    ↓
Read-Only Database Connection
    ↓
Query Execution
```

For production databases, avoid giving the LLM unrestricted write permissions.

A safer architecture is:

```text
LLM
 ↓
SELECT-only SQL
 ↓
Validator
 ↓
Read-only DB
```

---

# 🗺️ Future Roadmap

- [ ] Multi-database support
- [ ] PostgreSQL integration
- [ ] MySQL integration
- [ ] Natural-language database exploration
- [ ] Conversation memory
- [ ] Multi-turn analytics
- [ ] Advanced SQL validation
- [ ] SQL query optimization
- [ ] Query execution caching
- [ ] User authentication
- [ ] Role-based access control
- [ ] Production logging
- [ ] Query history
- [ ] Dashboard persistence
- [ ] Advanced chart recommendations
- [ ] LLM model selection
- [ ] Enterprise database connectors

---

# 🎯 Use Cases

This architecture can be adapted for:

### 📊 Business Intelligence

Business users can ask questions about sales, revenue, customers, and performance without writing SQL.

### 🏢 Enterprise Analytics

Organizations can build natural-language interfaces over internal analytical databases.

### 🎓 Education

Students can learn SQL and data analytics through natural-language interaction.

### 🧑‍💻 Developer Tools

Developers can use the agent to explore datasets and quickly generate analytical queries.

### 📈 SaaS Analytics

The architecture can be extended into a multi-user AI analytics SaaS platform.

---

# 🏆 Learning Outcomes

This project demonstrates practical experience with:

- Python application architecture
- Large Language Models
- Google Gemini API
- Retrieval-Augmented Generation
- Vector databases
- Text-to-SQL systems
- Agentic workflows
- SQL execution
- Error handling
- Self-correction loops
- Data analytics
- Data visualization
- Streamlit application development
- Git/GitHub
- Cloud deployment concepts

---

# 📸 Screenshots

Add your application screenshots here:

```text
docs/
├── dashboard.png
├── text-to-sql.png
├── self-correction.png
└── visualization.png
```

Example:

```markdown
![Dashboard](docs/dashboard.png)
```

> 💡 **Tip:** Add 2–4 real screenshots here. This significantly improves the presentation of the repository.

---

# 🌐 Live Demo

🚀 **Live Application:**  
Add your deployed Streamlit application URL here.

🔗 **Source Code:**  
https://github.com/uzaibsaiyed78616-hash/text2sql-data-agent

---

# 👨‍💻 Author

## Uzaib Saiyad

**BCA AI & Data Analytics Student | Full Stack Developer | AI/ML Learner**

Interested in:

- 🤖 Artificial Intelligence
- 🧠 Machine Learning
- 📊 Data Analytics
- 🌐 Full Stack Development
- 🔐 Cybersecurity
- ⚙️ Automation

### Connect With Me

- 💻 GitHub: [@uzaibsaiyed78616-hash](https://github.com/uzaibsaiyed78616-hash)
- 🔗 LinkedIn: [Uzaib Saiyad](https://www.linkedin.com/in/uzaib-saiyad-5a3893406/)
- 🌐 Portfolio: [uzaibsaiyad.vercel.app](https://uzaibsaiyad.vercel.app/)

---

# ⭐ Support

If you find this project useful:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report issues**

💡 **Suggest improvements**

Contributions and feedback are welcome.

---

# 📄 License

This project is licensed under the **MIT License**.

See the `LICENSE` file for details.

---

<div align="center">

### 🤖 Built with Python + Gemini + RAG + DuckDB + Streamlit

**Natural Language → SQL → Self-Correction → Analytics**

⭐ If you like the project, consider giving it a star!

</div>
