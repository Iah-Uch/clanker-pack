React is the only dependency listed in this repo’s `package.json`, and the working tree is clean on `main` at commit `26a2291`. That gives you a clear code and lockfile rollback point.

1. **Before upgrading tomorrow**, create a branch and commit the React 19 change separately. Keep the current commit as your known-good point.
2. **If the upgrade breaks things**, revert that upgrade commit with `git revert <upgrade-commit>`, then restore dependencies from the reverted lockfile with `npm ci`.
3. **If it has already been deployed**, redeploy the previous known-good build as well; reverting the code alone won’t change what’s live.
4. **Check the repo’s lockfile first:** it’s present, but the initial file listing didn’t reveal whether it’s tracked. Confirm with `git ls-files package-lock.json`. If it’s tracked, the upgrade commit and revert will capture the dependency rollback. If it isn’t, make sure the known-good lockfile is saved before changing dependencies.

There’s no data migration in this React version change, so the rollback point is the upgrade commit and previous deployment. The main practical risk is deploying before you’ve confirmed the app builds and its critical flows work.