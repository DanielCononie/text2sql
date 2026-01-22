import json
from pathlib import Path

from app.ollama_client import call_ollama
from app.validator import validate_sql

def build_prompt(schema_text: str, question: str) -> str:
    template = Path("prompts/generate_sql.txt").read_text(encoding="utf-8")
    return (
        template
        .replace("{{SCHEMA}}", schema_text)
        .replace("{{QUESTION}}", question)
    )

def generate_sql(question: str, schema_text: str) -> dict:
    prompt = build_prompt(schema_text, question)
    print("prompt", prompt)

    raw = call_ollama(prompt)     
    data = json.loads(raw)      

    if not data.get("needs_clarification", False):
        sql = data.get("sql", "")
        validate_sql(sql)

    return data
