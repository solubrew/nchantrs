# Contributing to Nchantrs

Thank you for your interest in contributing to Nchantrs!

## Development Setup

1. Clone the repository
2. Install dependencies: `pip install -e .`
3. Run tests: `pytest`

## Code Style

- Follow PEP 8
- Use Black for formatting
- Use isort for import sorting
- Run pylint before committing

## Testing

All new features must include tests. Run tests with:
```bash
pytest
```

## Submitting Changes

1. Create a feature branch
2. Make your changes
3. Run the test suite
4. Submit a pull request

## CI/CD Pipeline

The project uses GitHub Actions for CI/CD. See `.github/workflows/ci.yml` for details.

### Pipeline Steps
- Lint (pylint, flake8)
- Type Check (pyright)
- Test (pytest)
- Build (setuptools)

## Contact

For questions, contact the maintainers at solubrew@solutionsbrewer.com
