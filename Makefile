.DEFAULT_GOAL := help

DC := docker
DC_NAME := basicweatherapp
NAME := pyphercises/${DC_NAME}
IMG := ${NAME}:latest

################
# Main targets #
################
help: ## Show this help
	@echo "Usage: 'make build', 'make run' or 'make stop'"

build:
	@$(DC) build -t ${IMG} .

run:
	@$(DC) run -d -p 5000:5000 --name ${DC_NAME} ${IMG}

stop:
	@$(DC) rm -f ${DC_NAME}