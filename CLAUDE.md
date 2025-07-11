# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Python FastAPI server that wraps jq queries over large JSON files and exposes them as an MCP (Model Context Protocol) compatible API. The server provides endpoints for querying JSON data using jq expressions and retrieving JSON schemas to assist with LLM reasoning.

## Architecture

### Core Components

- **server.py**: Main FastAPI application with three primary endpoints:
  - `/query-json`: Executes jq queries against JSON files using subprocess calls
  - `/get-schema`: Retrieves JSON schema files to assist with data structure understanding
  - `/list-tools`: Returns MCP tool definitions for integration with LLM agents
  - `/health`: Basic health check endpoint

### Data Structure

- **data/**: Directory containing JSON files and schemas (mounted as volume in Docker)
- **orca-schema.json**: Large JSON schema file (20.9MB+) used for data validation/understanding

## Common Development Commands

### Docker Operations
```bash
# Build the Docker image
docker build -t jq-mcp-server .

# Run the container with data volume mounted
docker run -p 8000:8000 -v /path/to/json/files:/data jq-mcp-server

# Quick run with local data directory (from Makefile)
make docker-run
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server locally
uvicorn server:app --host 0.0.0.0 --port 8000

# Run with auto-reload for development
uvicorn server:app --reload
```

## Security Considerations

- The server executes jq commands via subprocess, which requires careful handling of file paths
- JSON files are accessed directly from the filesystem, so proper volume mounting and path validation is critical
- The `/get-schema` endpoint reads arbitrary files from the filesystem - ensure proper access controls

## MCP Integration

The server exposes two MCP tools:
1. **query-json**: For running jq expressions against JSON files
2. **get-jsonschema**: For retrieving schema files to help with data structure understanding

The `/list-tools` endpoint provides the tool definitions that MCP-compatible agents can use to interact with the server.

## Dependencies

- **FastAPI**: Web framework
- **Pydantic**: Data validation and settings management
- **uvicorn**: ASGI web server
- **jq**: Command-line JSON processor (installed in Docker container)