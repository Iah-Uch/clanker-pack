If it breaks, the goal is to get production stable first, then diagnose from a clean comparison.

**Before upgrading tomorrow:**

- Start from a clean Git working tree and make a dedicated upgrade branch.
- Confirm you can redeploy the current React 18 build quickly. Keep the lockfile and deployment artifact from that build.
- Upgrade `react` and `react-dom` together, plus their type packages if you use TypeScript. Check your framework’s React 19 compatibility too.
- Run your usual build and critical user flows in staging before production. If you can, release gradually and watch errors and key metrics.

**If something breaks:**

1. If users are affected, roll back to the known-good React 18 deployment.
2. If it’s only in development, capture the error and smallest reproduction; check peer dependency warnings and the [official React 19 upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide).
3. Revert the upgrade commit or restore the React 18 dependency versions **and lockfile**, then reinstall from that lockfile. Don’t just change `package.json` and leave the lockfile on React 19.
4. Fix and retry in staging. Avoid making unrelated changes during the rollback.

You don’t need to solve every migration issue tomorrow. A working rollback path turns “breaks everything” into “pause the upgrade, restore the last known-good build, and investigate.”