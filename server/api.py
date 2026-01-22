from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.schema_loader import load_schema, schema_to_text, auto_load_schema, write_to_schema
from app.generator import generate_sql

from fastapi.middleware.cors import CORSMiddleware

from app.db import engine
from sqlalchemy import text
from decimal import Decimal
from datetime import date, datetime
from uuid import UUID
from main import json_safe




app = FastAPI(title="Text-to-SQL API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Auto generate schema
schema_data = auto_load_schema()
write_to_schema(schema_data)

# Load schema once at startup (fast + consistent)
_schema = load_schema()
_schema_text = schema_to_text(_schema)

class GenerateSqlRequest(BaseModel):
    question: str

class GenerateSqlResponse(BaseModel):
    sql: str | None
    needs_clarification: bool
    questions: list[str]
    columns: list[str]
    rows: list[dict]

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate-sql", response_model=GenerateSqlResponse)
def generate_sql_endpoint(body: GenerateSqlRequest):
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    try:
        result = generate_sql(question, _schema_text)
       
        if result["needs_clarification"]:
            print(json.dumps(result, indent=2))
            return

        sql = result["sql"]

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            columns = list(result.keys())          
            rows = result.fetchall()               
        
        # Convert rows to JSON-safe dicts
        rows_out = []
        for r in rows:
            row_dict = dict(r._mapping)
            safe_row = {}
            for key, value in row_dict.items():
                safe_row[key] = json_safe(value)
            rows_out.append(safe_row)

        response = {
            "sql": sql,
            "needs_clarification": False,
            "questions": [],
            "columns": columns,
            "rows": rows_out,
        }   

        return response

    except Exception as e:
        # Don't leak huge tracebacks to the client
        raise HTTPException(status_code=500, detail=str(e))