"""
secrets.py: Module to access AWS Secrets Manager and manage secrets caching.

This module provides functions to retrieve secrets stored in AWS Secrets Manager,
either directly or as lazy-loaded objects. It includes an optional caching mechanism
to reduce the number of API calls to AWS.
"""

import json
from typing import Any, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from django.utils.functional import SimpleLazyObject

# Initialize a single boto3 client instance for AWS Secrets Manager with retry and timeout
# configurations. This instance is reused across the module to avoid creating new clients
# for each request.
_secrets_client = boto3.session.Session().client(
    service_name='secretsmanager',
    config=Config(
        retries={'total_max_attempts': 3, 'mode': 'standard'},
        connect_timeout=2,
        read_timeout=2
    )
)

# Cache dictionary to store retrieved secrets for reuse within the application.
# The cache is structured as a dictionary with secret IDs as keys and the secret
# data (in dictionary format) as values.
_secrets_cache: dict[str, dict[str, Any]] = {}


def get_secret(
    secret_id: str,
    key: Optional[str] = None,
    use_cache: bool = True
) -> Any:
    """
    Retrieve a secret or specific key from AWS Secrets Manager, with optional caching.
    
    This function fetches the secret data from AWS Secrets Manager using the specified
    `secret_id`. If caching is enabled and the secret has been previously retrieved,
    the cached value is returned to avoid redundant API calls.
    
    Args:
        secret_id (str): The unique identifier or ARN of the secret in AWS Secrets Manager.
        key (Optional[str]): An optional specific key within the secret to retrieve. 
            If omitted, the entire secret dictionary is returned.
        use_cache (bool): Whether to use cached values (default is True).
        
    Returns:
        Any: The requested secret data. If `key` is specified, returns the specific key's value;
            otherwise, returns the entire secret dictionary.
    
    Raises:
        ClientError: If there is an error communicating with AWS Secrets Manager.
        KeyError: If the specified `key` is not found within the secret.
    """
    # Check the cache first if caching is enabled; if the secret is in cache, return it.
    if use_cache and secret_id in _secrets_cache:
        secret_dict = _secrets_cache[secret_id]
        return secret_dict[key] if key else secret_dict

    try:
        # Request the secret value from AWS Secrets Manager.
        response = _secrets_client.get_secret_value(SecretId=secret_id)
        secret_dict = json.loads(response['SecretString'])  # Parse JSON-formatted secret string.

        # Cache the secret if caching is enabled.
        if use_cache:
            _secrets_cache[secret_id] = secret_dict
        return secret_dict[key] if key else secret_dict  # Return specific key or full secret.

    except ClientError as e:
        # Raise AWS-specific client errors to the caller for logging or handling.
        raise e

    except KeyError as e:
        # Raise a clear error if the requested key is missing from the secret data.
        raise KeyError(f"Key '{key}' not found in secret '{secret_id}'") from e


def get_secret_lazy(
    secret_id: str,
    key: Optional[str] = None,
    use_cache: bool = True
) -> SimpleLazyObject:
    """
    Create a lazy-loaded secret object that fetches data only upon access.
    
    The function wraps a call to `get_secret` in a `SimpleLazyObject`, deferring
    the retrieval of the secret until it is accessed. This can improve efficiency
    when secrets are not always required immediately upon function call.
    
    Args:
        secret_id (str): The unique identifier or ARN of the secret in AWS Secrets Manager.
        key (Optional[str]): An optional specific key within the secret to retrieve.
            If omitted, the entire secret dictionary is deferred for retrieval.
        use_cache (bool): Whether to use cached values (default is True).
    
    Returns:
        SimpleLazyObject: A lazy object that retrieves the secret data upon first access.
    """
    # Wrap `get_secret` with SimpleLazyObject for deferred access to secret data.
    return SimpleLazyObject(lambda: get_secret(secret_id, key, use_cache))


def clear_cache(secret_id: Optional[str] = None) -> None:
    """
    Clear cached secrets, either a specific secret or the entire cache.
    
    This function removes either a specific secret from the cache or, if no
    `secret_id` is provided, clears all entries from the cache.
    
    Args:
        secret_id (Optional[str]): The unique identifier of the secret to clear
            from the cache. If None, clears the entire cache.
    """
    if secret_id:
        # Remove a specific secret from the cache if `secret_id` is specified.
        _secrets_cache.pop(secret_id, None)
    else:
        # Clear all cached secrets if no specific `secret_id` is provided.
        _secrets_cache.clear()
