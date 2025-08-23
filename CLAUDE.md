# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

pyCWManage is a Python 3.x package for interacting with the ConnectWise Manage REST API. It provides a clean interface for performing CRUD operations on ConnectWise resources.

## Architecture

### Core Components

1. **Main API Client** (`pycwmanage/cwmanage.py`):
   - `CWManage` dataclass: The main API client that handles authentication and provides methods for all HTTP operations
   - Key methods: `get()`, `get_all_pages()`, `get_all_pages_mt()` (multi-threaded), `post()`, `put()`, `patch()`, `delete()`
   - Handles automatic URL discovery via ConnectWise's company info endpoint
   - Built on `requests` library with proper error handling
   - All methods support `return_response=True` parameter to access full Response objects

2. **Tests** (`tests/test_cwmanage.py`):
   - Unit tests with mocked API responses
   - Integration tests that use actual API credentials (when available)
   - Automatically loads `.env` file via `conftest.py`

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode for development
pip install -e .
```

### Testing
```bash
# Run all tests (automatically loads .env file)
pytest -vv

# Run specific test class
pytest tests/test_cwmanage.py::TestReturnResponseFeature -vv

# Run tests with coverage
pytest --cov=pycwmanage tests/
```

## Environment Variables

The following environment variables must be set for the API client to work:
- `CW_SITE`: ConnectWise site URL (e.g., 'na.myconnectwise.net')
- `CW_COMPANY_ID`: Your company ID in ConnectWise
- `CW_PUBLIC_KEY`: API public key
- `CW_PRIVATE_KEY`: API private key
- `CW_CLIENT_ID`: Client ID for the integration

## Key Implementation Details

- The API client uses Basic authentication with base64-encoded credentials
- Automatic pagination handling with `get_all_pages()` method
- Multi-threaded pagination support via `get_all_pages_mt()` for better performance
- All API responses return JSON data or empty lists on failure by default
- **NEW**: All methods support `return_response=True` parameter to get full Response objects with headers
- Verbose logging available via `verbose=True` parameter on all methods
- The client automatically discovers the correct API URL based on the company's ConnectWise instance

### Accessing Raw Response Data

All API methods now support a `return_response` parameter that allows you to access the full response object:

```python
# Traditional usage (returns parsed JSON data)
data = api.get('/company/companies')

# New usage (returns requests.Response object)
response = api.get('/company/companies', return_response=True)

# Access response details
headers = response.headers
status_code = response.status_code
json_data = response.json()
raw_content = response.content
```

This works for all methods: `get()`, `get_all_pages()`, `get_all_pages_mt()`, `post()`, `put()`, `patch()`, and `delete()`.