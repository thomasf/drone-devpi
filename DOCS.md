Use the devpi plugin to deploy a Python package to a [devpi](http://doc.devpi.net) server.

Recommended for use with
[setuptools_scm](https://pypi.org/project/setuptools-scm/) for a simple python
package release process.

**Note: Your setup.py will be ran interpreted Python 3.8 during packaging.**

* `server` - The full path to the root of the devpi server. Make sure to include a port if it's not 80 or 443.
* `index` - The ``<user>/<repo>`` combo pointing of the index to upload to.
* `username` - The username to login with.
* `password` - A password to login with.

The following is an example configuration for your `.drone.yml` with two
pipelines that release to different indexes:

```yaml
---
kind: pipeline
type: docker
name: dev

platform:
  os: linux
  arch: amd64

steps:
- name: devpi release
  image: thomasf/drone-devpi:5
  settings:
    index: root/dev
    password:
      from_secret: devpi_password
    server: https://ci:Jjpf1L99i96Q@devpi.example.com
    username: drone

trigger:
  branch:
  - master
  event:
  - push
  status:
  - success

---
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
    server: https://ciJjpf1L99i96Q@devpi.example.com
    username: drone

trigger:
  event:
  - push
  - tag
  ref:
  - refs/tags/0.1.*
  status:
  - success
```
