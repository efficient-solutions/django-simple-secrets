# django-simple-secrets

A Django integration for AWS Secrets Manager with caching and lazy loading support.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 4-5](https://img.shields.io/badge/django-4.x|5.x-green.svg)](https://www.djangoproject.com/)

## Overview

`django-simple-secrets` provides a clean and efficient way to access AWS Secrets Manager from a Django applications. It features built-in caching to reduce API calls and supports lazy loading of secrets through Django's `SimpleLazyObject`.

⚠️ **Important Note**: This module is not thread-safe. The caching mechanism uses a simple dictionary that is not protected against concurrent access. If you need thread-safety, consider implementing your own synchronization mechanism or disabling caching with `use_cache=False`.

### Key Features

- Simple, intuitive API for accessing AWS Secrets Manager
- Built-in caching mechanism to minimize API calls
- Lazy loading support for improved performance
- Configured retry logic and timeouts
- Type hints for better IDE support
- Compatible with Python 3.10+ and Django 4.x/5.x

## Installation

```bash
pip install django-simple-secrets
```

Note: This package requires `boto3`, which must be installed separately:

```bash
pip install boto3
```

## Configuration

Ensure your AWS credentials are properly configured either through:
- Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- AWS credentials file
- IAM role (when running on AWS infrastructure)

## Usage

### Basic Usage

```python
from django_secrets import get_secret

# Get an entire secret
database_config = get_secret('prod/database')

# Get a specific key from a secret
database_password = get_secret('prod/database', key='password')
```

### Lazy Loading

```python
from django_secrets import get_secret_lazy

# Secret won't be fetched until actually accessed
database_config = get_secret_lazy('prod/database')
```

### Cache Management

```python
from django_secrets import clear_cache

# Clear a specific secret from cache
clear_cache('prod/database')

# Clear entire cache
clear_cache()

# Bypass cache for a single request
fresh_secret = get_secret('prod/database', use_cache=False)
```

## Error Handling

The module raises standard boto3 exceptions:

```python
try:
    secret = get_secret('prod/database')
except ClientError as e:
    # Handle AWS-specific errors
    pass
except KeyError as e:
    # Handle missing key errors
    pass
```

## Performance Considerations

- The module maintains a single boto3 client instance
- Caching is enabled by default to minimize API calls
- Timeout settings: 2 seconds for both connect and read
- Maximum retry attempts: 3

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.