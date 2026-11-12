Added a production Docker setup:

- [Dockerfile](/tmp/bench2-81_zx2z5/repo/Dockerfile) builds a small Node 22 Alpine image, installs production dependencies, runs as a non-root user, and checks `/health`.
- [.dockerignore](/tmp/bench2-81_zx2z5/repo/.dockerignore) excludes secrets, local dependencies, and build artifacts.
- [compose.yaml](/tmp/bench2-81_zx2z5/repo/compose.yaml) sets restart behavior, read-only filesystem, dropped capabilities, and resource limits.

Deploy with `docker compose up -d --build`; set `PORT` to change the host port. I couldn’t verify the image build because access to the Docker daemon was denied.