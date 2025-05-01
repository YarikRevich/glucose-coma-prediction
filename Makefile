sample := $(or $(sample), 'sample/data.csv')
train := $(or $(train), 'sample/data.csv.train')
model := $(or $(model), 'sample/model.bin')
server := $(or $(server), 'http://localhost:8089')

.PHONY: help
.DEFAULT_GOAL := help
help:
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: generate
generate: ## Generates train and example data for the model
	@python3 main.py generate $(sample)
	@echo "Train and example data is generated and saved to $(sample)!"

.PHONY: build
build: ## Builds model
	@python3 main.py build $(train) $(model)
	@echo "Model is built and saved!"

.PHONY: start-demo
start-demo: ## Starts demo application
	@cd demo/glucose-coma-prediction-demo && NEXT_PUBLIC_SERVER=$(server) npm run dev 

.PHONY: start-server
start-server: ## Starts server application
	@python3 main.py start $(model)
