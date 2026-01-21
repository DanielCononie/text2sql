from app.schema_loader import load_schema, schema_to_text, auto_load_schema, write_to_schema
from app.generator import generate_sql
import json
from app.db import engine
from sqlalchemy import text
from decimal import Decimal
from datetime import date, datetime
from uuid import UUID


def main():

    # 1) auto generate the schema.json file
    schema_data = auto_load_schema()
    write_to_schema(schema_data)

    # 2) Load the schema from schema/schema.json
    schema = load_schema()

    # 3) Convert that schema into a compact text format for the model
    schema_text = schema_to_text(schema)

    # 4) Ask the user for a question
    question = input("Ask a question: ").strip()

    # 5) Generate SQL from the model
    result = generate_sql(question, schema_text)

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

    # 6) Print the model result nicely

    print(json.dumps(response, indent=2))

def json_safe(v):
    if isinstance(v, Decimal):
        return float(v)  # or str(v) if you want exact precision
    if isinstance(v, (datetime, date, UUID)):
        return str(v)
    return v


if __name__ == "__main__":
    main()
