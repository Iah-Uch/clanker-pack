React 18 → 19 is a dependency upgrade. In this repo, `react` and `react-dom` are both `18.2.0`, and `package-lock.json` is tracked. The working tree is clean on `main`, at commit `2150c55` (`base`).

1. **Before upgrading:** create a separate branch and record the starting commit: `git switch -c upgrade/react-19` and `git rev-parse HEAD`. Keep the upgrade in its own commit.
2. **If it breaks before merging:** switch back to `main`. If you need to undo the upgrade on its branch, run `git revert <upgrade-commit>`.
3. **Restore dependencies:** use `git restore --source=main -- package.json package-lock.json`, then run `npm ci` to reinstall from the React 18 lockfile. This works because `package-lock.json` is tracked in Git.
4. **If it breaks after deployment:** redeploy the last known-good release using your deployment host’s rollback. The repo doesn’t reveal which host you use, so confirm that release remains available before deploying.

There’s no data migration in the React version change itself. The point where Git rollback stops being enough is if the deployment also changes external data or services; those need their own recovery plan.