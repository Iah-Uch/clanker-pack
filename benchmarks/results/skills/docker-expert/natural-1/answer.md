Added a production Docker setup:

- [Dockerfile](/tmp/bench2-jz4lzz6y/repo/Dockerfile) installs production dependencies, runs as a non-root user, and defines a health check.
- [compose.yaml](/tmp/bench2-jz4lzz6y/repo/compose.yaml) builds and runs the service with restart and health-check settings.
- [server.js](/tmp/bench2-jz4lzz6y/repo/server.js) now reads `PORT`, binds to the container interface, and shuts down gracefully.
- [.dockerignore](/tmp/bench2-jz4lzz6y/repo/.dockerignore) excludes local and secret files from the build context.
- [README.md](/tmp/bench2-jz4lzz6y/repo/README.md) documents how to build and run it.

Deploy with `docker compose up --build -d`. The install check stalled, so I couldn’t confirm the image builds here. `git diff --check` passed.