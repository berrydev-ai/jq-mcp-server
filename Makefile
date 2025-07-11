.PHONY: build run

DATA_PATH ?= ./data
JSON_FILE_PATH ?= 
JSON_SCHEMA_FILE_PATH ?= 

build:
	docker build -t jq-mcp-server .

run:
	docker run -p 8000:8000 \
		-e DATA_PATH=/data \
		$(if $(JSON_FILE_PATH),-e JSON_FILE_PATH=$(JSON_FILE_PATH)) \
		$(if $(JSON_SCHEMA_FILE_PATH),-e JSON_SCHEMA_FILE_PATH=$(JSON_SCHEMA_FILE_PATH)) \
		-v $(DATA_PATH):/data \
		jq-mcp-server
