# Source Control — flowspec-cli

## Host
github.com/jpoley/flowspec (private)

## Branch Naming
```
{hostname}/task-{id}/{slug}
```
```bash
HOSTNAME=$(hostname -s | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')
git checkout -b "${HOSTNAME}/task-606/flowspec-doctor"
```

Current branch: `galway/task-606/flowspec-doctor`

## Commits
All commits require DCO sign-off:
```bash
git commit -s -m "feat: add flowspec doctor command"
```

Conventional prefix:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation only
- `refactor:` no behaviour change
- `test:` test-only change
- `chore:` maintenance

## Pre-Commit Gates (run before every commit)
```bash
uv run ruff format --check .   # must pass
uv run ruff check .             # must pass, zero errors
uv run pytest tests/ -x -q     # must pass, zero failures
```

## PRs
- Target branch: `main`
- Title: ≤ 70 chars, conventional prefix, references issue (e.g., `feat: add flowspec doctor command (closes #1221)`)
- Body template: `.github/PULL_REQUEST_TEMPLATE.md`
- **Never merge directly to `main`** — operator merges after CI passes
- **Never update a PR** — close and reopen (Copilot won't re-review amended PRs)
- CI must be green before requesting review

## Never
- `git push --force` to `main`
- `git reset --hard` without operator approval
- Skip `--no-verify` or DCO
- Merge your own PR
