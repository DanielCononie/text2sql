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
    ## 
    # 1) Build the prompt
    # 2) Call Ollama
    # 3) Parse the response
    # 4) Validate the SQL
    ##
    prompt = build_prompt(schema_text, question)
    print("prompt", prompt)

    raw = call_ollama(prompt)      # raw is a string (should be JSON)
    data = json.loads(raw)         # convert JSON string -> Python dict

    if not data.get("needs_clarification", False):
        sql = data.get("sql", "")
        validate_sql(sql)

    return data
