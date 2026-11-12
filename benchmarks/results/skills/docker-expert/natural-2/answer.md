Added production Docker support: a minimal Node 22 Alpine image, non-root runtime, Docker health check, and `.dockerignore`. Updated the server to listen on `0.0.0.0`, accept a configurable `PORT`, and shut down gracefully. Added build and run instructions in [README.md](/tmp/bench2-c52x91ff/repo/README.md).

`git diff --check` passed. I did not build the image or run tests.

```sh
docker build -t api:latest .
docker run --rm -p 3000:3000 api:latest
```