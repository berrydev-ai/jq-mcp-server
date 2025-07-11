#!/usr/bin/env python3

import subprocess
import json
import time
import os
from pathlib import Path
from typing import Dict, Any

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("jq-mcp-server")

# Environment variables for file paths
DATA_PATH = os.getenv("DATA_PATH", "/data")
JSON_FILE_PATH = os.getenv("JSON_FILE_PATH")
JSON_SCHEMA_FILE_PATH = os.getenv("JSON_SCHEMA_FILE_PATH")

# Resolve relative paths in environment variables
if JSON_FILE_PATH and not Path(JSON_FILE_PATH).is_absolute():
    JSON_FILE_PATH = str(Path(DATA_PATH) / JSON_FILE_PATH)

if JSON_SCHEMA_FILE_PATH and not Path(JSON_SCHEMA_FILE_PATH).is_absolute():
    JSON_SCHEMA_FILE_PATH = str(Path(DATA_PATH) / JSON_SCHEMA_FILE_PATH)


@mcp.tool()
def query_json(file_path: str = "", query: str = "") -> Dict[str, Any]:
    """
    Query JSON data using jq expressions.
    
    Args:
        file_path: Path to the JSON file to query (or use JSON_FILE_PATH env var)
        query: jq expression to execute
        
    Returns:
        Dictionary with result, query, and execution duration
    """
    try:
        # Validate query parameter
        if not query:
            return {
                "error": "query parameter is required",
                "query": query,
                "duration": 0
            }
        
        # Use environment variable if file_path is not provided or is relative
        if JSON_FILE_PATH and (not file_path or not Path(file_path).is_absolute()):
            resolved_path = JSON_FILE_PATH
        elif not file_path:
            return {
                "error": "file_path is required when JSON_FILE_PATH environment variable is not set",
                "query": query,
                "duration": 0
            }
        elif not Path(file_path).is_absolute():
            resolved_path = str(Path(DATA_PATH) / file_path)
        else:
            resolved_path = file_path
        
        # Validate file exists
        if not Path(resolved_path).exists():
            return {
                "error": f"File not found: {resolved_path}",
                "query": query,
                "duration": 0
            }
        
        start = time.time()
        
        # Execute jq command
        result = subprocess.run(
            ["jq", query, resolved_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        duration = time.time() - start
        
        if result.returncode != 0:
            return {
                "error": f"jq error: {result.stderr}",
                "query": query,
                "duration": duration
            }
        
        return {
            "result": result.stdout.strip(),
            "query": query,
            "duration": duration
        }
        
    except subprocess.TimeoutExpired:
        return {
            "error": "Query timed out after 30 seconds",
            "query": query,
            "duration": 30
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "query": query,
            "duration": 0
        }


@mcp.tool()
def get_jsonschema(schema_path: str = "") -> Dict[str, Any]:
    """
    Retrieve JSON schema file to assist with data structure understanding.
    
    Args:
        schema_path: Path to the JSON schema file (or use JSON_SCHEMA_FILE_PATH env var)
        
    Returns:
        Dictionary with schema content and execution duration
    """
    try:
        # Use environment variable if schema_path is not provided or is relative
        if JSON_SCHEMA_FILE_PATH and (not schema_path or not Path(schema_path).is_absolute()):
            resolved_path = JSON_SCHEMA_FILE_PATH
        elif not schema_path:
            return {
                "error": "schema_path is required when JSON_SCHEMA_FILE_PATH environment variable is not set",
                "duration": 0
            }
        elif not Path(schema_path).is_absolute():
            resolved_path = str(Path(DATA_PATH) / schema_path)
        else:
            resolved_path = schema_path
        
        # Validate file exists
        if not Path(resolved_path).exists():
            return {
                "error": f"Schema file not found: {resolved_path}",
                "duration": 0
            }
        
        start = time.time()
        
        with open(resolved_path, "r") as f:
            schema_content = f.read()
        
        if not schema_content.strip():
            return {
                "error": "Schema file is empty",
                "duration": time.time() - start
            }
        
        try:
            schema_json = json.loads(schema_content)
            duration = time.time() - start
            
            return {
                "result": schema_json,
                "duration": duration
            }
            
        except json.JSONDecodeError as e:
            return {
                "error": f"Invalid JSON schema: {str(e)}",
                "duration": time.time() - start
            }
            
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "duration": 0
        }


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()