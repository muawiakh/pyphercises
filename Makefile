.DEFAULT_GOAL := help

DC := docker
PY := python
APP_ID = ${WEATHER_APP_ID}
TEST_FILE := test_weatherapi.py
TAG := $(shell git tag -l --sort=-v:refname | head -n 1)
DC_NAME := basicweatherapp
NAME := pyphercises/${DC_NAME}
IMG := ${NAME}:${TAG}

################
# Main targets #
################
help: ## Show this help
	@echo "Usage: 'make build', 'make run', 'make stop', 'make logs', 'make clean' or 'make test'"

build:
	@$(DC) build -t ${IMG} --build-arg APP_ID=${APP_ID} .

run:
	@$(DC) run -d -p 5000:5000 --name ${DC_NAME} ${IMG}

stop:
	@$(DC) rm -f ${DC_NAME}

logs:
	@$(DC) logs ${DC_NAME}

test:
	@$(PY) ${TEST_FILE}

clean:
	@$(DC) rm -f ${DC_NAME}
	@$(DC) rmi ${IMG}
