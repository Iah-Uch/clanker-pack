Treat it like a release with a rollback plan, not a one-way migration.

**Before you upgrade**

- Commit or tag the current working version so you can return to it.
- Make the upgrade on a branch and keep the change set small.
- Check React’s official [upgrade guide](https://react.dev/blog/2024/04/25/react-19-upgrade-guide) and run the React 19 codemods.
- Confirm your framework, router, UI libraries, test tools, and React types support React 19. Upgrade incompatible dependencies before or alongside React.
- Run your existing tests and build on React 18 first. Save the results as a baseline.
- Make sure you know how to redeploy the current React 18 build. If you can, stage the React 19 release or roll it out to a small percentage of users first.

**If it breaks**

1. Capture the error and identify whether it’s a build failure, a runtime error, or a dependency incompatibility.
2. If users are affected, redeploy the last known good React 18 build first.
3. Otherwise, revert the upgrade commit or switch back to the React 18 lockfile and dependency versions.
4. Reproduce the issue in a small test, fix it on the branch, and rerun the checks before trying again.

Avoid changing application code, React, and a large set of dependencies all at once; that makes failures much harder to trace.