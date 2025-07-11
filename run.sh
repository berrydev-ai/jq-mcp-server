#!/bin/bash

# If the .env file exists, load it
if [ -f .env ]; then
  echo "Loading environment variables from .env file"
  export $(grep -v '^#' .env | xargs)
else
  echo ".env file not found. Using default environment variables."
fi

if [ -z "$DATA_PATH" ]; then
  echo "DATA_PATH is not set. Using default ./data"
  DATA_PATH=./data
fi

if [ -z "$JSON_FILE_PATH" ]; then
  echo "JSON_FILE_PATH is not set. Using default example.json"
  JSON_FILE_PATH=orca-schema.json
fi

if [ -z "$JSON_SCHEMA_FILE_PATH" ]; then
  echo "JSON_SCHEMA_FILE_PATH is not set. Using default example-schema.json"
  JSON_SCHEMA_FILE_PATH=orca-json-schema.json
fi

source .venv/bin/activate && \
  uvicorn server:app --host "0.0.0.0" --port 8000 --workers 1 --timeout-keep-alive 60