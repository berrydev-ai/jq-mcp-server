# jq MCP Server

A Python MCP (Model Context Protocol) server that wraps `jq` queries over large JSON files.  
Provides MCP tools for **JSON querying** and **JSON Schema retrieval** for enhanced LLM agent context!

---

## Features

- ✅ Query huge JSON files using `jq`
- ✅ Retrieve associated JSON Schema files via MCP tools
- ✅ Native MCP server integration with Claude Desktop, VS Code, and other MCP clients
- ✅ Lightweight and portable

---

## MCP Tools

- `query_json` — Run jq query on a JSON file  
- `get_jsonschema` — Retrieve a JSON Schema file to assist LLM reasoning

---

## Getting Started

### Installation & Setup

1. **Clone the repo:**
    ```bash
    git clone https://github.com/berrydev-ai/jq-mcp-server.git
    cd jq-mcp-server
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Install jq (if not already installed):**
    ```bash
    # On macOS
    brew install jq
    
    # On Ubuntu/Debian
    sudo apt-get install jq
    
    # On other systems, see: https://jqlang.github.io/jq/download/
    ```

4. **Run the MCP server:**
    ```bash
    python mcp_server.py
    ```
    
    Or with environment variables:
    ```bash
    DATA_PATH=/path/to/data JSON_FILE_PATH=main.json python mcp_server.py
    ```

---

### Setup on Windows

1. **Open PowerShell** and navigate to your repo:
    ```powershell
    cd C:\Users\YourName\github.com\berrydev-ai\jq-mcp-server
    ```

2. **Install dependencies:**
    ```powershell
    pip install -r requirements.txt
    ```

3. **Install jq:**
    - Download jq from https://jqlang.github.io/jq/download/
    - Or use chocolatey: `choco install jq`
    - Or use scoop: `scoop install jq`

4. **Run the MCP server:**
    ```powershell
    python mcp_server.py
    ```
    
    Or with environment variables:
    ```powershell
    $env:DATA_PATH="C:/Users/YourName/data"; $env:JSON_FILE_PATH="main.json"; python mcp_server.py
    ```

---

## Usage with MCP Clients

Once the server is running, it can be used with any MCP-compatible client. The server provides two tools:

- **`query_json`**: Run jq queries against JSON files
- **`get_jsonschema`**: Retrieve JSON schema files for better LLM understanding

When environment variables are configured, file paths become optional in tool calls.

---

## Claude Desktop Integration

**Direct Claude Desktop integration via MCP server!**

1. **Configure Claude Desktop** by adding to your `claude_desktop_config.json`:
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

2. **Restart Claude Desktop** - The jq tools will now be available directly in Claude Desktop!

3. **Usage in Claude Desktop:**
   - **Query JSON data:** Use the `query_json` tool with just your jq expression (file path is optional)
   - **Get schema:** Use the `get_jsonschema` tool without specifying a path (uses configured default)
   - **Override defaults:** You can still provide file paths in tool calls to use different files

---

## Other MCP Clients

This server works with any MCP-compatible client including:
- VS Code with GitHub Copilot
- Continue.dev
- Cursor
- Cline
- And many others (see MCP client documentation)

Each client may have different configuration methods, but all can use the MCP stdio transport that this server provides.

---

## Environment Variables

You can configure the server using environment variables to specify default file paths:

- **DATA_PATH**: Parent directory containing JSON files and schemas (default: `/data`)
- **JSON_FILE_PATH**: Path to your main JSON file (optional) - can be absolute or relative to DATA_PATH
- **JSON_SCHEMA_FILE_PATH**: Path to your JSON schema file (optional) - can be absolute or relative to DATA_PATH

### Using Environment Variables

**With local development:**
```bash
export DATA_PATH=/path/to/your/data
export JSON_FILE_PATH=main.json  # relative to DATA_PATH
export JSON_SCHEMA_FILE_PATH=schema.json  # relative to DATA_PATH
python mcp_server.py
```

When environment variables are set, you can use relative paths or empty strings in your tool calls, and the server will automatically resolve them using the configured paths.

**Parameter Behavior:**
- `file_path` parameter becomes **optional** when `JSON_FILE_PATH` is set
- `schema_path` parameter becomes **optional** when `JSON_SCHEMA_FILE_PATH` is set
- If environment variables are not set, the respective parameters are **required**

---

## Security & Usage Notes

- **Only use locally or behind a secure firewall!** The server executes jq on any file in the configured directories.
- Ensure proper file path validation and access controls for your data files.

---

## MCP Tools Available

- **`query_json`**: Query JSON data using jq expressions
  - Parameters: `file_path` (optional if JSON_FILE_PATH is set), `query` (required)
  - Returns: Query result, execution duration, and any errors

- **`get_jsonschema`**: Retrieve JSON Schema files
  - Parameters: `schema_path` (optional if JSON_SCHEMA_FILE_PATH is set) 
  - Returns: Schema content, execution duration, and any errors

---

## Development

- Python 3.12+ with MCP Python SDK
- All tools are defined in `mcp_server.py` 
- Easy to extend with new MCP tools

### Local Development Scripts

The repository includes convenient shell scripts for development:

- **run.sh**: Runs the MCP server locally with virtual environment activation
- **dev.sh**: Development script with auto-reload (if needed)
- **mcp_server.py**: Main MCP server application

#### Using Development Scripts

Both scripts automatically handle environment variable loading and virtual environment activation:

```bash
# Run the server in production mode
./run.sh

# Run the server in development mode
./dev.sh
```

**Script Features:**
- Automatically loads `.env` file if present
- Sets default environment variables if not configured:
  - `DATA_PATH` defaults to `./data`
  - `JSON_FILE_PATH` defaults to `orca-schema.json`
  - `JSON_SCHEMA_FILE_PATH` defaults to `orca-json-schema.json`
- Activates virtual environment from `.venv/bin/activate`
- Runs the MCP server with proper environment setup

**Environment File Setup:**
Create a `.env` file in the project root to customize your development environment:
```bash
DATA_PATH=/path/to/your/data
JSON_FILE_PATH=your-main-file.json
JSON_SCHEMA_FILE_PATH=your-schema.json
```

### Example Files

The repository includes example files in the `data/` directory:
- `example.json`: Sample JSON data for testing queries
- `example-schema.json`: Sample JSON schema for testing schema retrieval

---

## License

MIT License.  
Use at your own risk. Intended for internal, secure data workflows.