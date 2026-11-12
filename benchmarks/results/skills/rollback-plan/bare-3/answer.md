You’ve got a straightforward rollback available: this repo is on React and React DOM **18.2.0**, and the working tree is clean.

Before upgrading tomorrow:

1. Start from a clean branch and keep the current commit as your rollback point:
   ```bash
   git switch -c react-19-upgrade
   git rev-parse HEAD
   ```
2. Upgrade React and React DOM together, and commit the upgrade separately from any fixes.
3. If it breaks, return to the last working commit:
   ```bash
   git switch main
   ```
   Or, if you need to keep working on the upgrade branch, revert its upgrade commit:
   ```bash
   git revert <upgrade-commit>
   ```

If the failure is only in production, redeploy the last known-good release while you investigate; changing the code branch alone won’t restore a deployed app. Keep `package-lock.json` with the dependency changes so the rollback restores the same install state.