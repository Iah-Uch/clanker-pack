Added production Docker support with a multi-stage image, a non-root runtime user, health checks, and a Compose service with resource limits and basic hardening. The app now listens on `0.0.0.0` and honors `PORT`.

`docker compose config` succeeds. I couldn’t build or run the image because this environment can’t access the Docker daemon.

Start it on a Docker host with `docker compose up -d --build`. See [README.md](/tmp/bench2-c6g1c9f5/repo/README.md) for deployment notes. Files added: [Dockerfile](/tmp/bench2-c6g1c9f5/repo/Dockerfile), [.dockerignore](/tmp/bench2-c6g1c9f5/repo/.dockerignore), and [compose.yaml](/tmp/bench2-c6g1c9f5/repo/compose.yaml).