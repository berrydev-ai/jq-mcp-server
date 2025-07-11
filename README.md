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
    make build
    ```
3. **Run the server (mount your data directory):**
    ```bash
    make run DATA_PATH=/absolute/path/to/json/files
    ```
    Or with specific file paths:
    ```bash
    make run DATA_PATH=/absolute/path/to/json/files \
              JSON_FILE_PATH=/absolute/path/to/json/files/main.json \
              JSON_SCHEMA_FILE_PATH=/absolute/path/to/json/files/schema.json
    ```
    Or using Docker directly:
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
    make build
    ```
3. **Run the server (adjust data path):**
    ```powershell
    make run DATA_PATH=C:/Users/YourName/data
    ```
    Or with specific file paths:
    ```powershell
    make run DATA_PATH=C:/Users/YourName/data `
              JSON_FILE_PATH=C:/Users/YourName/data/main.json `
              JSON_SCHEMA_FILE_PATH=C:/Users/YourName/data/schema.json
    ```
    Or using Docker directly:
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

**Query using environment variable (when JSON_FILE_PATH is set):**
```bash
curl -X POST http://localhost:8000/query-json \
  -H "Content-Type: application/json" \
  -d '{"query": ".store.book[].title"}'
```

**Retrieve a JSON Schema:**
```bash
curl -X POST http://localhost:8000/get-schema \
  -H "Content-Type: application/json" \
  -d '{"schemaPath": "/data/schema.json"}'
```

**Retrieve schema using environment variable (when JSON_SCHEMA_FILE_PATH is set):**
```bash
curl -X POST http://localhost:8000/get-schema \
  -H "Content-Type: application/json" \
  -d '{}'
```

**List available tools (for agent/LLM integration):**
```bash
curl http://localhost:8000/list-tools
```

---

## Claude Desktop & Agent Integration

### With Claude Desktop (MCP Server)

**Direct Claude Desktop integration via MCP server!**

1. **Install MCP dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Configure Claude Desktop** by adding to your `claude_desktop_config.json`:
    ```json
    {
      "mcpServers": {
        "jq-mcp-server": {
          "command": "python",
          "args": ["/absolute/path/to/jq-mcp-server/mcp_server.py"],
          "env": {
            "DATA_PATH": "/absolute/path/to/your/data/directory",
            "JSON_FILE_PATH": "main.json",
            "JSON_SCHEMA_FILE_PATH": "schema.json"
          }
        }
      }
    }
    ```

    **Configuration Notes:**
    - Replace `/absolute/path/to/jq-mcp-server/` with the actual path to your cloned repository
    - Replace `/absolute/path/to/your/data/directory` with the path to your JSON data directory
    - `JSON_FILE_PATH` and `JSON_SCHEMA_FILE_PATH` use relative paths (relative to `DATA_PATH`)
    - With this configuration, file paths become optional in tool calls - the server will use the configured defaults

3. **Restart Claude Desktop** - The jq tools will now be available directly in Claude Desktop!

4. **Usage in Claude Desktop:**
   - **Query JSON data:** Use the `query_json` tool with just your jq expression (file path is optional)
   - **Get schema:** Use the `get_jsonschema` tool without specifying a path (uses configured default)
   - **Override defaults:** You can still provide file paths in tool calls to use different files

### With Claude Desktop (HTTP API - Legacy)

> **Note: The HTTP API method is now deprecated. Use the MCP server above for direct integration.**

- **Manual workflow:**  
    1. Query your JSON or schema using the above API (e.g., via curl or Postman).
    2. Copy the result.
    3. Paste the result into Claude Desktop as context.

---

### With AI Agents (CrewAI, OpenPipe, LM Studio, etc.)

- Point your agent’s tool discovery/config at:  
    `http://localhost:8000/list-tools`
- Your agent can then:
    - Query large JSON data
    - Retrieve schemas to help generate valid jq expressions
    - Combine this with LLM-powered workflows

---

## Environment Variables

You can configure the server using environment variables to specify default file paths:

- **DATA_PATH**: Parent directory containing JSON files and schemas (default: `/data`)
- **JSON_FILE_PATH**: Path to your main JSON file (optional) - can be absolute or relative to DATA_PATH
- **JSON_SCHEMA_FILE_PATH**: Path to your JSON schema file (optional) - can be absolute or relative to DATA_PATH

### Using Environment Variables

**With Docker (absolute paths):**
```bash
docker run -p 8000:8000 \
  -e DATA_PATH=/data \
  -e JSON_FILE_PATH=/data/large-file.json \
  -e JSON_SCHEMA_FILE_PATH=/data/schema.json \
  -v /absolute/path/to/json/files:/data \
  jq-mcp-server
```

**With Docker (relative paths):**
```bash
docker run -p 8000:8000 \
  -e DATA_PATH=/data \
  -e JSON_FILE_PATH=large-file.json \
  -e JSON_SCHEMA_FILE_PATH=schema.json \
  -v /absolute/path/to/json/files:/data \
  jq-mcp-server
```

**With local development:**
```bash
export DATA_PATH=/path/to/your/data
export JSON_FILE_PATH=main.json  # relative to DATA_PATH
export JSON_SCHEMA_FILE_PATH=schema.json  # relative to DATA_PATH
python mcp_server.py
```

When environment variables are set, you can use relative paths or empty strings in your API calls, and the server will automatically resolve them using the configured paths.

**Parameter Behavior:**
- `filePath` parameter becomes **optional** when `JSON_FILE_PATH` is set
- `schemaPath` parameter becomes **optional** when `JSON_SCHEMA_FILE_PATH` is set
- If environment variables are not set, the respective parameters are **required**

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

### Local Development Scripts

- **run.sh**: Runs the HTTP server locally with virtual environment activation
- **dev.sh**: Runs the HTTP server in development mode with auto-reload
- **mcp_server.py**: MCP server for direct Claude Desktop integration

### Makefile Commands

- `make build`: Build the Docker image
- `make run`: Run the Docker container (use `DATA_PATH` to specify data directory)

### Example Files

The repository includes example files in the `data/` directory:
- `example.json`: Sample JSON data for testing queries
- `example-schema.json`: Sample JSON schema for testing schema retrieval

---

## License

MIT License.  
Use at your own risk. Intended for internal, secure data workflows.