## Overview

This is a Python MCP (Model Context Protocol) server that wraps jq queries over large JSON files. The server provides MCP tools for querying JSON data using jq expressions and retrieving JSON schemas to assist with LLM reasoning.

## Mandatory Context Loading

You must first read and understand the following files before responding to the USER. These files provide context into how to build MCP servers uging Python.

- [MCP Python SDK](@docs/mcp-python-sdk.md)
- [LLMS Full](@docs/llms-full.txt) - Please use offset and limit parameters to read specific portions of the file, or use the GrepTool to search for specific
     content as the file is too large.
- [Docker MCP Toolkit](@docs/mcp-toolkit-docker.md)

Once you have read and understand these documents, say "I have read the mandatory context and am now ready to help!".

## Architecture

### Core Components

- **mcp_server.py**: Main MCP server application providing two MCP tools:
  - `query_json`: Executes jq queries against JSON files using subprocess calls
  - `get_jsonschema`: Retrieves JSON schema files to assist with data structure understanding

### Data Structure

- **data/**: Directory containing JSON files and schemas (mounted as volume in Docker)
- **orca-schema.json**: Large JSON schema file (20.9MB+) used for data validation/understanding

## Common Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the MCP server
python mcp_server.py

# Or with environment variables
DATA_PATH=/path/to/data JSON_FILE_PATH=main.json python mcp_server.py
```

## Security Considerations

- The server executes jq commands via subprocess, which requires careful handling of file paths
- JSON files are accessed directly from the filesystem, so proper path validation is critical
- The `get_jsonschema` tool reads arbitrary files from the filesystem - ensure proper access controls

## MCP Integration

The server exposes two MCP tools:
1. **query_json**: For running jq expressions against JSON files
2. **get_jsonschema**: For retrieving schema files to help with data structure understanding

The server is compatible with MCP clients like Claude Desktop, VS Code, and other MCP-compatible agents.

## Dependencies

- **mcp**: MCP Python SDK for server implementation
- **jq**: Command-line JSON processor (system dependency)