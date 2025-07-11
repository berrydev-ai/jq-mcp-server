# jq MCP Server

A lightweight API server that wraps `jq` queries over large JSON files and exposes them as an [MCP-compatible](https://github.com/OpenPipe/MCP) API.  
Now supports **optional JSON Schema retrieval** for enhanced LLM agent context!

---

## Features

- ✅ Query huge JSON files using `jq`
- ✅ Retrieve associated JSON Schema files via API
- ✅ REST API endpoints
- ✅ MCP tool listing for integration with LLM agents
- ✅ Dockerized and portable

---

## Endpoints

- `POST /query-json` — Run jq query on a JSON file  
- `POST /get-schema` — Retrieve a JSON Schema file to assist LLM reasoning  
- `GET /list-tools` — List available MCP tools for agent integration  
- `GET /health` — Simple health check

---

## Getting Started

### Running on Mac/Linux

1. **Clone the repo:**
    ```bash
    git clone https://github.com/berrydev-ai/jq-mcp-server.git
    cd jq-mcp-server
    ```
2. **Build the Docker image:**
    ```bash
    docker build -t jq-mcp-server .
    ```
3. **Run the server (mount your data directory):**
    ```bash
    docker run -p 8000:8000 -v /absolute/path/to/json/files:/data jq-mcp-server
    ```
    Replace `/absolute/path/to/json/files` with your own path.

4. **Test with curl:**
    ```bash
    curl -X POST http://localhost:8000/query-json \
      -H "Content-Type: application/json" \
      -d '{"filePath": "/data/largefile.json", "query": ".store.book[].title"}'
    ```

---

### Running on Windows

1. **Open PowerShell** and navigate to your repo:
    ```powershell
    cd C:\Users\YourName\github.com\berrydev-ai\jq-mcp-server
    ```
2. **Build the Docker image:**
    ```powershell
    docker build -t jq-mcp-server .
    ```
3. **Run the server (adjust data path):**
    ```powershell
    docker run -p 8000:8000 -v C:/Users/YourName/data:/data jq-mcp-server
    ```
    *(Use forward slashes or double-backslashes in the path)*

4. **Test with curl:**
    ```powershell
    curl -X POST http://localhost:8000/query-json `
      -H "Content-Type: application/json" `
      -d '{"filePath": "/data/largefile.json", "query": ".store.book[].title"}'
    ```

---

## Example Requests

**Query a JSON file:**
```bash
curl -X POST http://localhost:8000/query-json \
  -H "Content-Type: application/json" \
  -d '{"filePath": "/data/largefile.json", "query": ".store.book[].title"}'
```

**Retrieve a JSON Schema:**
```bash
curl -X POST http://localhost:8000/get-schema \
  -H "Content-Type: application/json" \
  -d '{"schemaPath": "/data/schema.json"}'
```

**List available tools (for agent/LLM integration):**
```bash
curl http://localhost:8000/list-tools
```

---

## Claude Desktop & Agent Integration

### With Claude Desktop

> **Claude Desktop does not (yet) support custom HTTP tools natively.**

- **Manual workflow:**  
    1. Query your JSON or schema using the above API (e.g., via curl or Postman).
    2. Copy the result.
    3. Paste the result into Claude Desktop as context.

- **Semi-automated:**  
    - Use a script or GUI client to streamline data extraction for Claude.

---

### With AI Agents (CrewAI, OpenPipe, LM Studio, etc.)

- Point your agent’s tool discovery/config at:  
    `http://localhost:8000/list-tools`
- Your agent can then:
    - Query large JSON data
    - Retrieve schemas to help generate valid jq expressions
    - Combine this with LLM-powered workflows

---

## Security & Usage Notes

- **Only use locally or behind a secure firewall!** The API executes jq on any file in the mounted directory.
- Always mount your data directory as `/data`, and reference files in API calls as `/data/yourfile.json` or `/data/schema.json`.

---

## MCP Tool List Output (example)

```json
{
  "tools": [
    {
      "name": "query-json",
      "description": "Query JSON data using jq expressions",
      "inputSchema": {
        "type": "object",
        "properties": {
          "filePath": {"type": "string"},
          "query": {"type": "string"}
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
          "schemaPath": {"type": "string"}
        },
        "required": ["schemaPath"]
      }
    }
  ]
}
```

---

## Development

- Python 3.12, FastAPI, Docker
- All endpoints are defined in `server.py`
- Easy to extend with new tools

---

## License

MIT License.  
Use at your own risk. Intended for internal, secure data workflows.