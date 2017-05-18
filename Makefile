.PHONY: docker

IMAGE ?= thomasf/drone-devpi

docker:
		docker build --rm -t $(IMAGE) .

