import streamlit as st
import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import plotly.express as px

# 1. Load Environment Variables
load_dotenv()

# Page Config
st.set_page_config(page_title="InsightGen", layout="wide")
st.title("📊 InsightGen: AI-Powered Dashboard Generator")

# 2. Sidebar - Configuration
with st.sidebar:
    st.header("Settings")
    # Tries to load from .env first, otherwise asks user
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Groq API Key:", type="password")
        if not api_key:
            st.warning("Please enter an API Key to proceed.")
            st.stop()

# 3. Setup Dummy Database (Automated)
@st.cache_resource
def init_database():
    db_path = 'sales_data.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY,
                    product_name TEXT,
                    category TEXT,
                    amount INTEGER,
                    date DATE)''')
    
    # Seed data if empty
    c.execute("SELECT count(*) FROM sales")
    if c.fetchone()[0] == 0:
        data = [
            ('Laptop', 'Electronics', 1200, '2023-01-15'),
            ('Mouse', 'Electronics', 25, '2023-01-16'),
            ('Chair', 'Furniture', 150, '2023-01-17'),
            ('Desk', 'Furniture', 300, '2023-02-01'),
            ('Headphones', 'Electronics', 100, '2023-02-10'),
            ('Laptop', 'Electronics', 1200, '2023-03-05'),
            ('Monitor', 'Electronics', 200, '2023-03-10'),
            ('Sofa', 'Furniture', 800, '2023-04-05'),
            ('Phone', 'Electronics', 900, '2023-04-12')
        ]
        c.executemany("INSERT INTO sales (product_name, category, amount, date) VALUES (?, ?, ?, ?)", data)
        conn.commit()
    conn.close()
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")

db = init_database()

# 4. Define LLM & Chains
# Llama 3.3 70B is the current high-performance replacement
llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile", temperature=0)

def get_sql_chain(db):
    template = """
    You are a data analyst. Based on the table schema below, write a SQL query that answers the user's question.
    Schema: {schema}
    
    Question: {question}
    Return ONLY the SQL query. Do not wrap it in markdown or code blocks.
    SQL Query:
    """
    prompt = ChatPromptTemplate.from_template(template)
    
    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# 5. Dashboard Generation UI
st.write("### Ask a question about your data:")
st.info("Sample Database includes: Products, Categories, Amounts, and Dates.")
st.write("Try: *'Show total sales by category'* or *'Sales trend over time'*")

user_question = st.text_input("Query")

if user_question:
    try:
        # Step A: Generate SQL
        sql_chain = get_sql_chain(db)
        generated_sql = sql_chain.invoke({"question": user_question})
        
        # Clean SQL
        clean_sql = generated_sql.replace("```sql", "").replace("```", "").strip()
        
        st.write("Generated SQL Query:")
        st.code(clean_sql, language='sql')
        
        # Step B: Execute SQL
        conn = sqlite3.connect('sales_data.db')
        df = pd.read_sql_query(clean_sql, conn)
        conn.close()
        
        st.write("### Data Result")
        st.dataframe(df)
        
        # Step C: Auto-Visualization Logic
        if not df.empty and len(df.columns) >= 2:
            st.write("### Generated Dashboard")
            
            numeric_cols = df.select_dtypes(include=['number']).columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            date_cols = [col for col in df.columns if 'date' in col.lower()]
            
            # Logic to choose chart
            if date_cols and numeric_cols.any():
                fig = px.line(df, x=date_cols[0], y=numeric_cols[0], title="Time Series Analysis")
                st.plotly_chart(fig)
            elif len(categorical_cols) > 0 and len(numeric_cols) > 0:
                fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0], title="Category Analysis")
                st.plotly_chart(fig)
            elif len(numeric_cols) >= 2:
                fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title="Correlation")
                st.plotly_chart(fig)
            else:
                st.info("Could not determine optimal chart type automatically.")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")

import warnings
warnings.filterwarnings("ignore", category=UserWarning)