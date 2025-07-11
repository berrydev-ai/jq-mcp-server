FROM python:3.12-slim

# Install system dependencies including jq
RUN apt-get update && \
    apt-get install -y jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY mcp_server.py .
COPY data/ ./data/

# Set default environment variables
ENV DATA_PATH=/app/data
ENV JSON_FILE_PATH=orca-schema.json
ENV JSON_SCHEMA_FILE_PATH=orca-json-schema.json

# Expose MCP stdio interface
CMD ["python", "mcp_server.py"]
