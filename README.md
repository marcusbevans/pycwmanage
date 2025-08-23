# pyCWManage

A Python client library for the ConnectWise Manage REST API. This library simplifies interaction with ConnectWise Manage by providing a clean, Pythonic interface for common operations.

## Features

- Simple, intuitive API client for ConnectWise Manage
- Support for all CRUD operations (GET, POST, PUT, PATCH, DELETE)
- Automatic pagination handling
- Multi-threaded pagination for improved performance
- Access to raw HTTP response objects (headers, status codes, etc.)
- Proper authentication handling
- Comprehensive error handling

## Installation

Install from PyPI:

```bash
pip install pycwmanage
```

Or install from source:

```bash
git clone https://github.com/marcusbevans/pycwmanage.git
cd pycwmanage
pip install -e .
```

## Quick Start

```python
from pycwmanage import CWManage

# Initialize the client
api = CWManage(
    connectwise_site='your.connectwise.net',
    company_id='your_company',
    public_key='your_public_key',
    private_key='your_private_key',
    client_id='your_client_id'
)

# Get all companies
companies = api.get('/company/companies')

# Get a specific company
company = api.get('/company/companies/1')

# Create a new ticket
ticket_data = {
    'summary': 'New ticket',
    'board': {'id': 1},
    'company': {'id': 1}
}
new_ticket = api.post('/service/tickets', ticket_data)

# Access raw response data
response = api.get('/company/companies', return_response=True)
print(response.headers)
print(response.status_code)
data = response.json()
```

## Configuration

### Environment Variables

Create a `.env` file in your project root (see `.env.example` for template):

```bash
CW_API_URL=your.connectwise.net
CW_COMPANY_ID=your_company_id
CW_PUBLIC_KEY=your_public_key
CW_PRIVATE_KEY=your_private_key
CW_CLIENT_ID=your_client_id
```

Then load them in your code:

```python
import os
from dotenv import load_dotenv
from pycwmanage import CWManage

load_dotenv()

api = CWManage(
    connectwise_site=os.getenv('CW_API_URL'),
    company_id=os.getenv('CW_COMPANY_ID'),
    public_key=os.getenv('CW_PUBLIC_KEY'),
    private_key=os.getenv('CW_PRIVATE_KEY'),
    client_id=os.getenv('CW_CLIENT_ID')
)
```

## API Methods

### Basic Operations

All methods support optional parameters:
- `verbose`: Enable detailed logging
- `log_endpoint`: Log the API endpoint being called
- `return_response`: Return the full Response object instead of JSON data

```python
# GET request
data = api.get('/endpoint')

# POST request
new_item = api.post('/endpoint', {'key': 'value'})

# PUT request
updated_item = api.put('/endpoint/id', {'key': 'new_value'})

# PATCH request
patched_item = api.patch('/endpoint/id', [{'op': 'replace', 'path': '/key', 'value': 'new_value'}])

# DELETE request
success = api.delete('/endpoint/id')
```

### Pagination

```python
# Automatic pagination - fetches all pages
all_companies = api.get_all_pages('/company/companies')

# Multi-threaded pagination for better performance
all_tickets = api.get_all_pages_mt('/service/tickets')
```

### Accessing Response Headers

```python
# Get full response object
response = api.get('/company/companies', return_response=True)

# Access response details
headers = response.headers
status_code = response.status_code
json_data = response.json()

# This works with all methods
response = api.post('/service/tickets', ticket_data, return_response=True)
location_header = response.headers.get('Location')
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/marcusbevans/pycwmanage.git
cd pycwmanage

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Running Tests

```bash
# Run all tests
pytest -vv

# Run with coverage
pytest --cov=pycwmanage tests/
```

## Security Best Practices

⚠️ **Never commit credentials to version control**

1. Always use environment variables or secure credential management systems
2. Add `.env` to your `.gitignore` file
3. Use read-only API keys when possible
4. Regularly rotate your API keys
5. Monitor API key usage in ConnectWise

## API Documentation

For detailed information about the ConnectWise Manage API endpoints, refer to the [official ConnectWise API documentation](https://developer.connectwise.com/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/marcusbevans/pycwmanage/issues) on GitHub.

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by ConnectWise. ConnectWise and ConnectWise Manage are trademarks of ConnectWise, LLC.