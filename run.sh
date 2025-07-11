#!/bin/bash

source .venv/bin/activate && uvicorn server:app --host "0.0.0.0" --port 8000 --reload --workers 1 --timeout-keep-alive 60