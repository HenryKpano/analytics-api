from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from os import getenv

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Verify the provided API key against valid keys from environment.
    Args:
        api_key: The API key from the request header
    Returns:
        The verified API key if valid
    Raises:
        HTTPException: If the API key is invalid
    """
    valid_keys = [getenv("API_KEY", "your-secret-api-key")]
    if api_key not in valid_keys:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key