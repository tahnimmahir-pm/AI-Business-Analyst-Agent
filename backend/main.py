from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import base64
import io
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

app = FastAPI(title="Michael - The AI Business Analyst Agent")

POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:password@localhost:5433/ecommerce")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

engine: Engine = create_engine(POSTGRES_URI)

class AskRequest(BaseModel):
    question: str
    want_chart: Optional[bool] = True

class AskResponse(BaseModel):
    answer: str
    table: Optional[List[dict]] = None
    chart_png_base64: Optional[str] = None
    generated_sql: Optional[str] = None

# NL -> SQL prompt
sql_prompt = PromptTemplate.from_template(
    """You are an expert Business Analyst generating PostgreSQL SQL for a database with tables:
- customers(customer_id, name, email, created_at)
- products(product_id, product_name, description)
- sales(order_id, product_id, customer_id, quantity, unit_price, order_date)

Write a valid PostgreSQL query to answer: {question}
Rules:
- Use correct table and column names as listed above.
- Use ISO 8601 timestamps.
- Return only the SQL, no markdown or explanations.
"""
)

llm = ChatGroq(model="llama3-70b-8192", groq_api_key=GROQ_API_KEY) if GROQ_API_KEY else None


def clean_sql_query(query: str) -> str:
    return query.strip().replace("```sql", "").replace("```", "").strip()


def run_sql(sql: str) -> List[dict]:
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        if result.returns_rows:
            rows = [dict(r._mapping) for r in result.fetchall()]
            return rows
        return []


def dataframe_to_chart_png_base64(df: pd.DataFrame) -> Optional[str]:
    if df.empty:
        return None
    try:
        fig, ax = plt.subplots(figsize=(6, 3))
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if len(numeric_cols) == 0:
            return None
        y_col = numeric_cols[0]
        x_col = df.columns[0] if df.columns[0] != y_col else (df.columns[1] if len(df.columns) > 1 else None)
        if x_col is None:
            return None
        df.plot(x=x_col, y=y_col, kind="line", ax=ax, marker="o")
        ax.set_title("Trend")
        ax.set_xlabel(str(x_col))
        ax.set_ylabel(str(y_col))
        buf = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buf, format="png")
        plt.close(fig)
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception:
        return None


@app.get("/schema")
def get_schema():
    sql = """
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema='public'
    ORDER BY table_name, ordinal_position;
    """
    try:
        rows = run_sql(sql)
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
def get_history():
    try:
        rows = run_sql("SELECT id, question, generated_sql, answer_text, created_at FROM conversations ORDER BY id DESC LIMIT 100;")
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    if not llm:
        raise HTTPException(status_code=400, detail="GROQ_API_KEY not configured")
    try:
        chain = sql_prompt | llm | StrOutputParser() | clean_sql_query
        sql = chain.invoke({"question": req.question})
        table = run_sql(sql)
        # Build human-friendly answer
        if len(table) == 0:
            answer = "No data found for the query."
        else:
            df = pd.DataFrame(table)
            # Simple heuristic summary
            answer = f"Returned {len(df)} rows with columns: {', '.join(df.columns)}."
        chart = dataframe_to_chart_png_base64(pd.DataFrame(table)) if req.want_chart else None
        # Save conversation
        insert_sql = text("""
            INSERT INTO conversations (question, generated_sql, answer_text)
            VALUES (:q, :s, :a)
        """)
        with engine.begin() as conn:
            conn.execute(insert_sql, {"q": req.question, "s": sql, "a": answer})
        return AskResponse(answer=answer, table=table, chart_png_base64=chart, generated_sql=sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"message": "Michael - The AI Business Analyst Agent is running."}
