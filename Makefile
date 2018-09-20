.DEFAULT_GOAL := help

DC := docker
DC_NAME := versionApp
NAME := pyphercises/app
TAG_LATEST := $(shell git tag -l --sort=-v:refname | head -n 1)
TAG_OLDEST := v3.0.0
IMG_LATEST := ${NAME}:${TAG_LATEST}
IMG_OLDEST := ${NAME}:${TAG_OLDEST}

################
# Main targets #
################
help: ## Show this help
	@echo "Usage: 'make build-oldest' OR 'make build-latest'"

build-oldest:
	@$(DC) build -t ${IMG_OLDEST} --build-arg APPVERSION=${TAG_OLDEST} .

build-latest:
	@$(DC) build -t ${IMG_LATEST} --build-arg APPVERSION=${TAG_LATEST} .

run:
	@$(DC) run -d -p 5000:5000 --name ${DC_NAME} ${IMG_LATEST}

stop:
	@$(DC) rm -f ${DC_NAME}