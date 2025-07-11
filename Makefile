.PHONY: dev docker-run

dev:
	PYTHONPATH=. uvicorn server:app --host "0.0.0.0" --port 8000 --reload --workers 1 --timeout-keep-alive 60

run:
	PYTHONPATH=. uvicorn server:app --host "0.0.0.0" --port 8000 --workers 1 --timeout-keep-alive 60

docker-run:
	docker run -p 8000:8000 -v ./data:/data jq-mcp-server

