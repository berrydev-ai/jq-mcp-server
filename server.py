from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI(title="jq MCP Server with Schema Support")


class QueryRequest(BaseModel):
    filePath: str
    query: str

class SchemaRequest(BaseModel):
    schemaPath: str

class JqResponse(BaseModel):
    result: str
    query: str
    duration: float

@app.post(
    "/query-json",
    response_model=JqResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "example": {
                            "summary": "User names over 25",
                            "value": {
                              "filePath": "/data/example.json",
                              "query": ".users[] | select(.age > 25) | .name"
                            },
                        },
                    }
                }
            }
        }
    },
)
def query_json(req: QueryRequest):
    """
    Execute jq queries against JSON files
    
    Example:
    - filePath: "/data/example.json"
    - query: ".users[] | select(.age > 25) | .name"
    """
    import time
    start = time.time()

    try:
        result = subprocess.check_output(
            ["jq", req.query, req.filePath],
            stderr=subprocess.STDOUT
        )
        duration = time.time() - start

        return JqResponse(
            result=result.decode().strip(),
            query=req.query,
            duration=duration
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=400, detail=e.output.decode())


@app.post("/get-schema",
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "docker-example": {
                            "summary": "Example (docker)",
                            "value": {
                                "schemaPath": "/data/example-schema.json",
                            },
                        },
                        "eberry-example": {
                            "summary": "Example (eberry)",
                            "value": {
                                "schemaPath": "/Users/eberry/github.com/berrydev-ai/jq-mcp-server/data/example-schema.json",
                            },
                        },
                    }
                }
            }
        }
    },
)
def get_schema(req: SchemaRequest):
    try:
        with open(req.schemaPath, "r") as f:
            schema_content = f.read()

        schema_str = schema_content.strip()
        if not schema_str:
            raise HTTPException(status_code=400, detail="Schema file is empty.")

        # Validate JSON schema format
        import json

        try:
            schema_json = json.loads(schema_str)
            return {"schema": schema_json}
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON schema: {str(e)}")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Schema file not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/list-tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "query-json",
                "description": "Query JSON data using jq expressions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filePath": {
                            "type": "string",
                            "description": "Path to JSON file"
                        },
                        "query": {
                            "type": "string",
                            "description": "jq expression (e.g., .store.book[].title)"
                        }
                    },
                    "required": ["filePath", "query"]
                }
            },
            {
                "name": "get-jsonschema",
                "description": "Retrieve the JSON Schema associated with a data file (optional, assists LLM reasoning)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "schemaPath": {
                            "type": "string",
                            "description": "Path to JSON Schema file"
                        }
                    },
                    "required": ["schemaPath"]
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)