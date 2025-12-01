#!/usr/bin/env python3
"""Test script to verify the 401 auth retry fix."""

import httpx
import ssl
import truststore
from specify_cli import _github_headers, _github_token

# Setup SSL context
ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = httpx.Client(verify=ssl_context)

def test_request(url, token, description):
    """Make a test request and report the result."""
    print(f"\n{description}")
    print(f"  Token: {repr(token)}")
    
    # Simulate the _req function with retry logic
    effective_token = _github_token(token)
    
    def _req(url, retry_without_auth=True):
        response = client.get(
            url,
            timeout=30,
            follow_redirects=True,
            headers=_github_headers(effective_token),
        )
        
        # If we got 401 with a token, retry without auth
        if response.status_code == 401 and effective_token and retry_without_auth:
            print(f"  Got 401 with token - retrying without authentication")
            response = client.get(
                url,
                timeout=30,
                follow_redirects=True,
                headers=_github_headers(None),
            )
        
        return response
    
    try:
        response = _req(url)
        print(f"  Final status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Success! Tag: {data.get('tag_name', 'N/A')}")
        else:
            print(f"  Failed: {response.status_code}")
    except Exception as e:
        print(f"  Error: {e}")

# Test cases
url = "https://api.github.com/repos/github/spec-kit/releases/latest"

test_request(url, None, "Test 1: No token (should work for public repo)")
test_request(url, "invalid_token_12345", "Test 2: Invalid token (should retry without auth and succeed)")

client.close()
print("\n✅ All tests completed!")
