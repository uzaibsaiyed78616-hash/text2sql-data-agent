# app.py
import streamlit as st
import plotly.express as px
import pandas as pd
import duckdb
from agent import Text2SQLAgent

# Page Configuration
st.set_page_config(
    page_title="DataQuery AI | Autonomous Analytics Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI Enhancement
st.markdown("""
<style>
    /* Metric Card Styling */
    .metric-card {
        background-color: #1e222d;
        border: 1px solid #2e3440;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
        background-color: #4F46E5;
        color: white;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Agent Initialization
@st.cache_resource
def load_agent():
    return Text2SQLAgent()

agent = load_agent()

# --- SIDEBAR: Database Info & Schema Explorer ---
with st.sidebar:
    st.title("⚡ DataQuery AI")
    st.caption("Autonomous Agentic SQL Workspace")
    st.divider()

    st.subheader("📊 Database Overview")
    try:
        conn = duckdb.connect("sales.duckdb")
        tables = conn.execute("SHOW TABLES").fetchall()
        table_names = [t[0] for t in tables]
        
        st.write(f"**Connected DB:** `sales.duckdb`")
        st.write(f"**Total Tables:** `{len(table_names)}`")
        
        with st.expander("🔍 Schema Explorer"):
            for table in table_names:
                st.markdown(f"**Table:** `{table}`")
                schema_df = conn.execute(f"DESCRIBE {table}").df()[['column_name', 'column_type']]
                st.dataframe(schema_df, width='stretch', hide_index=True)
        conn.close()
    except Exception as e:
        st.error("Database connection failed. Run `python db_setup.py` first.")

    st.divider()
    max_retries = st.slider("Self-Correction Max Retries", min_value=1, max_value=5, value=3)
    st.info("💡 **Tip:** Ask questions like *'Total sales by region'* or *'Which category has highest revenue?'*")

# --- MAIN CONTENT AREA ---
st.title("🤖 Autonomous Data Agent & Analytics")
st.markdown("Query your enterprise database in natural language with automatic SQL error self-correction and chart generation.")

# Sample Prompts / Quick Chips
st.markdown("**Quick Prompts:**")
chip_cols = st.columns(3)
selected_prompt = None

if chip_cols[0].button("📊 Regional Sales Summary"):
    selected_prompt = "Find total revenue by region with customer count"
if chip_cols[1].button("🏆 Top Selling Category"):
    selected_prompt = "Show top selling product category by total sales"
if chip_cols[2].button("📈 Sales Over Time"):
    selected_prompt = "Show total amount sold by transaction date"

# Input Text Area
default_val = selected_prompt if selected_prompt else ""
user_query = st.text_input("Ask a question about your data:", value=default_val, placeholder="e.g., Show total sales by product category as a bar chart")

run_clicked = st.button("🚀 Execute Query Agent")

# Processing and Output Setup
if (run_clicked or selected_prompt) and user_query:
    with st.spinner("⚡ Agent analyzing schema, drafting SQL, and executing..."):
        result = agent.execute_with_self_correction(user_query, max_retries=max_retries)

    if result["status"] == "success":
        df = result["data"]
        attempts = result["attempts"]
        
        # Success Banner
        if attempts == 1:
            st.success("✅ Query executed successfully on **1st attempt**!")
        else:
            st.warning(f"⚠️ Query required **{attempts} attempts** (Self-corrected runtime error automatically).")

        # Top Summary Metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Total Rows Fetched", len(df))
        with m2:
            st.metric("Columns Returned", len(df.columns))
        with m3:
            st.metric("Agent Execution Status", "Success" if attempts <= max_retries else "Failed")

        st.divider()

        # TABBED INTERFACE FOR RESULTS
        tab_data, tab_viz, tab_sql = st.tabs(["📋 Data Table", "📊 Auto Visualization", "💻 Generated SQL"])

        with tab_data:
            st.subheader("Query Results")
            st.dataframe(df, width='stretch', hide_index=True)
            
            # CSV Download Option
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results as CSV", csv, "query_results.csv", "text/csv")

        with tab_viz:
            st.subheader("Dynamic Visualization")
            if len(df) > 0 and len(df.columns) >= 2:
                num_cols = df.select_dtypes(include=['number']).columns.tolist()
                cat_cols = df.select_dtypes(include=['object', 'string', 'category', 'datetime']).columns.tolist()

                if len(num_cols) >= 1 and len(cat_cols) >= 1:
                    chart_type = st.radio("Select Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"], horizontal=True)
                    
                    x_col = cat_cols[0]
                    y_col = num_cols[0]

                    if chart_type == "Bar Chart":
                        fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}", template="plotly_dark")
                    elif chart_type == "Line Chart":
                        fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} over {x_col}", markers=True, template="plotly_dark")
                    else:
                        fig = px.pie(df, names=x_col, values=y_col, title=f"{y_col} Distribution", template="plotly_dark")
                    
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("ℹ️ Needs at least one categorical and one numeric column to auto-plot standard charts.")
            else:
                st.info("ℹ️ Single row or single column result - Chart generation skipped.")

        with tab_sql:
            st.subheader("Validated DuckDB SQL")
            st.code(result["sql"], language="sql")
            st.caption(f"Executed against local DuckDB instance in {attempts} attempt(s).")

    else:
        st.error(f"❌ Query execution failed after {result['attempts']} attempts.")
        st.subheader("Failed SQL Attempt")
        st.code(result["sql"], language="sql")
        st.subheader("Error Traceback")
        st.error(result["error"])