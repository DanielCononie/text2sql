import json
from pathlib import Path

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

