# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-XX

### Added
- New `return_response` parameter for all API methods to access full Response objects
- Access to response headers, status codes, and other metadata
- Comprehensive test suite with automatic .env loading
- Full documentation and examples
- Security best practices documentation
- Python 3.7+ support

### Changed
- Improved error handling for connection issues
- Better project structure for public distribution
- Enhanced documentation for public use

### Security
- Added .env.example template
- Improved .gitignore to prevent credential leaks
- Added security best practices to documentation

## [0.0.2.7] - Previous Version

### Added
- Initial implementation of ConnectWise Manage API client
- Basic CRUD operations
- Pagination support
- Multi-threaded pagination