# drone-devpi

Drone plugin for publishing Python packages to a [devpi](http://doc.devpi.net/) index.

### Example drone pipeline

```
kind: pipeline
type: docker
name: release

platform:
  os: linux
  arch: amd64

steps:
- name: devpi release
  image: thomasf/drone-devpi:5
  settings:
    index: root/prod
    password:
      from_secret: devpi_password
    server: https://ci:vvhQmemP0X0T@devpi.example.com
    username: drone
```

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
