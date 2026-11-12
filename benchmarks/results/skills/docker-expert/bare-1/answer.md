Added a production-oriented Docker setup:

- [Dockerfile](/tmp/bench2-7nv4w59f/repo/Dockerfile) uses Node 22 Alpine, installs production dependencies, runs as the non-root `node` user, and defines a health check.
- [compose.yaml](/tmp/bench2-7nv4w59f/repo/compose.yaml) configures restart behavior, a read-only filesystem, and reduced container privileges.
- [.dockerignore](/tmp/bench2-7nv4w59f/repo/.dockerignore) excludes local dependencies, Git files, and environment secrets from the build context.
- [server.js](/tmp/bench2-7nv4w59f/repo/server.js) now listens on `PORT` (default `3000`) and all interfaces.

Run it with `docker compose up --build -d`; set `PORT` to change the host port. I didn’t run the container or verify a deployment.