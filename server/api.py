from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.schema_loader import load_schema, schema_to_text
from app.generator import generate_sql

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app = FastAPI(title="Text-to-SQL API", version="0.1.0")

# Load schema once at startup (fast + consistent)
_schema = load_schema()
_schema_text = schema_to_text(_schema)

class GenerateSqlRequest(BaseModel):
    question: str

class GenerateSqlResponse(BaseModel):
    sql: str | None
    needs_clarification: bool
    questions: list[str]

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
        return result
    except Exception as e:
        # Don't leak huge tracebacks to the client
        raise HTTPException(status_code=500, detail=str(e))
