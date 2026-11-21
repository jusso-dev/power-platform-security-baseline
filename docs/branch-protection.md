# Branch protection

This repository protects `main` to keep the baseline, assessor and Sentinel content verified and deployable at all times.

## Recommended GitHub ruleset for `main`

Configure a repository ruleset (or classic branch protection rule) targeting the default branch (`main`) with the following settings in GitHub Settings > Branches or Settings > Rules > Rulesets. For details on GitHub rulesets, see the [GitHub documentation on rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

- **Require a pull request before merging**: enabled. Direct pushes to `main` are blocked.
- **Require status checks to pass before merging**: enabled, with **Require branches to be up to date before merging** enabled. Required check:
  - `Lint, style, links and validation` (runs em dash and emoji style check, markdownlint, lychee link check, baseline schema validation, Sentinel validation and assessor tests)
- **Allowed merge methods**: squash merge only, with automatic deletion of head branches after merge.
- **Block force pushes**: enabled.
- **Restrict deletions**: enabled.
- **Require linear history**: enabled (aligned with squash merging).

## Contributor workflow

1. Create a branch from `main` (`feat/<issue-number>-short-name`).
2. Push commits and open a pull request linking the issue (`Closes #N`).
3. Confirm all required CI checks pass.
4. Squash-merge and delete the feature branch.
