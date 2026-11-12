---
name: deploy-recipes
description: Use when the user wants to deploy, publish, host or put an app online - to Vercel, Netlify, Cloudflare, Fly.io, Railway, Render, a VPS or any other host. Gives a provider-neutral pre-deploy gate, environment-variable rules and a post-deploy check. Uses the host's current docs for provider commands.
---

# Deploy recipes

This skill covers what is the same on every host: the checks before, the secrets during, the proof after. For the provider's own commands, read the provider's current docs. Do not type commands from memory.

## Before the deploy

1. Run the `ship-checklist` skill on the diff.
2. Run the project's build, test and type-check commands. The production build must pass locally.
3. Find every environment variable the app reads. List them. Mark each as public or secret.
4. Check that no secret has a public prefix (for example `NEXT_PUBLIC_`, `VITE_`, `PUBLIC_`). Anything with such a prefix ships to every visitor's browser.
5. Check that `.env` files are in `.gitignore`. Set secrets in the host's secret store, never in the repo.
6. Check the database the production app will use. It must not be the development database. If a migration is needed, use the `db-migration-safe` skill.
7. Write the rollback step. Use the `rollback-plan` skill.

## Deploy

1. Look up the host's current docs for the exact command or setting. Quote the source.
2. Deploy to a preview or staging target first, if the host has one.
3. Do not run a production deploy until the user says to.

## After the deploy

1. Open the live URL. Check the main page loads.
2. Exercise the one thing the change was for. Report what you saw.
3. Check the host's logs for errors in the first minutes.
4. Check that a signed-out visitor cannot reach a protected page.
5. Report what you verified and what you could not verify.

## Never

- Put a secret in the repo, in a build log or in client code.
- Point a preview deploy at the production database.
- Deploy on a failing build because "it works locally".
