# Variables
IMAGE_NAME=ghcr.io/byronmoreno/practica
TAG=latest

.PHONY: build push deploy logs restart rm test

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

push:
	docker push $(IMAGE_NAME):$(TAG)

deploy:
	docker stack deploy -c stack.yml practica

logs:
	docker service logs -f practica_practica

restart:
	docker service update --force practica_practica

rm:
	docker stack rm practica

test:
	python -m pytest
