import re

BLOCKED = re.compile(
    r"\b(insert|update|delete|drop|alter|truncate|grant|revoke)\b",
    re.IGNORECASE
)

def validate_sql(sql: str) -> None:
    """
    Raises ValueError if SQL violates safety rules.
    (Even though we're not executing SQL yet.)
    """
    text = sql.strip()

    if BLOCKED.search(text):
        raise ValueError("Blocked SQL keyword detected (read-only only).")

    if not text.lower().startswith(("select", "with")):
        raise ValueError("Only SELECT/WITH queries allowed.")

    # Prevent multiple statements like: SELECT ...; DROP TABLE ...
    if ";" in text[:-1]:
        raise ValueError("Multiple SQL statements detected.")
