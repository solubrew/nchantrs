# CI/CD

Nchantrs is published and verified through GitHub Actions.

## Pipelines

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| CI | `.github/workflows/ci.yml` | push, pull_request | Run `pytest` matrix on Python 3.10, 3.11, 3.12 |
| Build | `.github/workflows/build.yml` | tag (`v*`) | Build sdist + wheel, publish to PyPI |

## Local checks

Before opening a PR, run the audit + test loop locally:

```bash
# 1. Install nchantrs in editable mode with all extras
uv sync --extra dev --extra test

# 2. Run the test suite
QT_QPA_PLATFORM=offscreen pytest tests/ -v

# 3. Run the sasquatch audit (produces PROJECT_TRACKER.yaml)
/home/solubrew/ENVs/sasquatch/bin/sasquatch analyze -p . --skip-pii-secrets
```

## Release process

1. Bump the version in `pyproject.toml` and `nchantrs/__init__.py:__version__`.
2. Update `CHANGES.md` with the release notes.
3. Push a `v<version>` tag (`git push origin v<version>`).
4. The Build workflow publishes the sdist + wheel to PyPI and creates a GitHub Release.

## Secrets

- `PYPI_API_TOKEN` — required by the Build workflow to publish to PyPI.
- `SB_STACK_PAT` — read-only GitHub token for pulling private sibling packages (kahndor, squirl, pyffice, nchantdoffice) during the test matrix.

## Branch policy

- `gamma` — integration branch, protected. All PRs land here.
- `arthr-ws` — release-candidate branch. CI passes on `gamma` before merge.
- All feature work happens on short-lived branches (`<issue>-<slug>`), merged to `gamma` via squash.
