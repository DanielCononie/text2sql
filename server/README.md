# Text2SQL Project

## Setup

### activate virtual environment
source .venv/bin/activate

### install dependencies
pip install -r requirements.txt

### run server
uvicorn api:app --reload --port 8000

-----------------------------------------------------------------------------------

## Endpoints

### generate-sql
Type: POST

Request Body:
```json
{
    "question": "string"
}
```

Response Body:
```json
{
    "sql": "string",
    "needs_clarification": boolean,
    "questions": ["string"]
}
```


### health
Type: GET

Request Body: None

Response Body:
```json
{
    "ok": boolean
}
```



## Model

This project uses a locally running open-source LLM via Ollama.
The default model during development is **SQLCoder (7B)**.

The model is not bundled or redistributed with this repository.
Users are expected to install and run their own compatible model locally.

-----------------------------------------------------------------------------------