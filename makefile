#!make
VERSION=0.0.1
IMAGE_NAME=secret-manager
REGISTRY_IMAGE_NAME=maissacrement/${IMAGE_NAME}

build:
	docker build -t ${IMAGE_NAME} .

run:
	docker run -e USER=tgy --rm -it \
		-v /var/run/docker.sock:/var/run/docker.sock -u root \
	${IMAGE_NAME}

tag:
	docker tag ${IMAGE_NAME} ${REGISTRY_IMAGE_NAME}:${VERSION}
	docker tag ${IMAGE_NAME} ${REGISTRY_IMAGE_NAME}:latest

push: build tag
	docker push ${REGISTRY_IMAGE_NAME}:${VERSION}
	docker push ${REGISTRY_IMAGE_NAME}:latest

pull:
	docker push ${REGISTRY_IMAGE_NAME}:${VERSION}
