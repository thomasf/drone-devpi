# drone-devpi

Drone plugin for publishing Python packages to a [devpi](http://doc.devpi.net/) index.

### Usage

See [DOCS.md](DOCS.md)

I also maintain a docker container version of devpi server which is a good
match for this drone plugin:
[https://github.com/thomasf/docker-devpi](https://github.com/thomasf/docker-devpi)

## Local Development

Set up [drone-cli](https://github.com/drone/drone-cli) and use it to run through ``.drone.yml``, much like Drone itself will:

```sh
drone exec
```

## Docker

Build the container using `make`:

```sh
make docker
```
