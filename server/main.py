from app.schema_loader import load_schema, schema_to_text
from app.generator import generate_sql
import json

def main():
    # 1) Load the schema from schema/schema.json
    schema = load_schema()

    # 2) Convert that schema into a compact text format for the model
    schema_text = schema_to_text(schema)

    # 3) Ask the user for a question
    question = input("Ask a question: ").strip()

    # 4) Generate SQL from the model
    result = generate_sql(question, schema_text)

    # 5) Print the model result nicely
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
