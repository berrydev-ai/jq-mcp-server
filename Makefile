.PHONY: build run

DATA_PATH ?= ./data

build:
	docker build -t jq-mcp-server .

run:
	docker run -p 8000:8000 -v $(DATA_PATH):/data jq-mcp-server
