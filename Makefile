sample := $(or $(sample), 'sample/data.csv')
model := $(or $(model), 'sample/model.bin')

.PHONY: help
.DEFAULT_GOAL := help
help:
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: generate
generate: ## Generates train data for the model
	@python3 main.py generate $(sample)
	@echo "Train data is generated and saved to $(sample)!"

.PHONY: build
build: ## Builds model
	@python3 main.py build $(sample) $(model)
	@echo "Model is built and saved!"

.PHONY: start
start: ## Starts server application
	@python3 main.py start $(model)
