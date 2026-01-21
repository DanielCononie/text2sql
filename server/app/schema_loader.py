import json
from sqlalchemy import create_engine, inspect
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_schema() -> dict:
    """
    Reads schema/schema.json and returns it as a Python dict.
    """
    path = Path("schema/schema.json")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)



def schema_to_text(schema: dict) -> str:
    """
    Converts the JSON schema into a compact text form like:

    users(id (uuid), email (text))
    orders(id (uuid), user_id (uuid), total (numeric))
    """
    lines = []

    for table in schema.get("tables", []):
        column_strings = []

        for column in table.get("columns", []):
            column_strings.append(
                column["name"] + " (" + column["type"] + ")"
            )

        cols = ", ".join(column_strings)
        lines.append(table["name"] + "(" + cols + ")")

    return "\n".join(lines)

def auto_load_schema():
    # connect to postgres
    engine = create_engine(os.getenv("PG_URL"))

    stats_connection = inspect(engine)


    # go through each table in postgres
    tables = []
    for table in stats_connection.get_table_names(schema="public"):
        columns = []
        for column in stats_connection.get_columns(table, schema="public"):
            columns.append({
                "name": column["name"],
                "type": str(column["type"])

            })

        tables.append({
            "name": table,
            "columns": columns
        })

    schema_data = {
        "dialect": "postgres",
        "tables": tables
    }
    
    return schema_data

def write_to_schema(schema_data: dict):
    path = Path("schema/schema.json")
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=2)
