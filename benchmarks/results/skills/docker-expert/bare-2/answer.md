Added a production Docker setup:

- [Dockerfile](/tmp/bench2-ukkfl96v/repo/Dockerfile): slim Node image, production-only dependencies, non-root runtime user, and `/health` health check.
- [.dockerignore](/tmp/bench2-ukkfl96v/repo/.dockerignore): excludes local dependencies, Git files, and environment secrets from the build context.
- [docker-compose.yml](/tmp/bench2-ukkfl96v/repo/docker-compose.yml): builds the image, restarts the service unless stopped, and publishes port 3000.

Run it with `docker compose up --build -d`. I checked the diff for whitespace errors; I did not build or run the container.