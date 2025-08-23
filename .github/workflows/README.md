# GitHub Actions Workflows

## Continuous Integration (ci.yml)
- Runs on every push to main and on pull requests
- Tests against Python 3.7 through 3.12
- Runs tests with coverage reporting
- Verifies the package can build

## Publishing (publish.yml)
- Triggered by:
  - Creating a new release on GitHub
  - Pushing a tag starting with 'v' (e.g., v0.1.0)
  - Manual workflow dispatch
- Uses PyPI Trusted Publishing (no tokens needed!)
- Automatically tests before publishing
- Publishes to PyPI using OIDC authentication

## Setup for Trusted Publishing

1. Go to PyPI.org and log in
2. Go to your project settings (or create the project first)
3. Under "Publishing", add a new publisher:
   - Owner: marcusbevans
   - Repository: pycwmanage
   - Workflow name: publish.yml
   - Environment: (leave blank)

This eliminates the need for API tokens!