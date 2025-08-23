# Contributing to pyCWManage

First off, thank you for considering contributing to pyCWManage! It's people like you that make pyCWManage such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible using the issue template.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please use the feature request template and include as many details as possible.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code follows the existing style.
6. Issue that pull request!

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/pycwmanage.git
cd pycwmanage

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Run tests
pytest tests/
```

## Style Guide

- Follow PEP 8
- Use meaningful variable names
- Add docstrings to all functions and classes
- Keep functions focused and small
- Write tests for new functionality

## Testing

- All new features must include tests
- All bug fixes must include a test that reproduces the issue
- Maintain or improve code coverage

```bash
# Run tests with coverage
pytest --cov=pycwmanage tests/
```

## Documentation

- Update README.md if you change functionality
- Add docstrings to new functions/classes
- Update CHANGELOG.md with your changes

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉