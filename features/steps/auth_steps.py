"""
Behave step definitions for Vhape DSL authentication scenarios.

These steps use the DSL parser to interpret Gherkin steps and execute
HTTP requests to the dummy API, then validate the responses.
"""

import os
import requests
from behave import given, when, then, step
from vhape.parser import parse_step, DSLParseError


# API base URL - can be configured via environment variable
API_BASE_URL = os.getenv("VHAPE_API_URL", "http://localhost:8000")

# Token mapping from DSL to actual API tokens
TOKEN_MAP = {
    'valid': 'valid-token',      # Admin token
    'admin': 'valid-token',      # Admin token (same as valid)
    'user': 'user-token',        # User token
    'invalid': 'invalid-token',  # Invalid token
    'none': None,                # No token
}


@given('I have {token_description}')
@step('I have {token_description}')
def step_given_token(context, token_description):
    """
    Given step that sets up the authentication token.
    
    Uses the DSL parser to interpret token descriptions like:
    - "a valid token"
    - "an admin token"
    - "a user token"
    - "an invalid token"
    - "no token"
    """
    # Build the full step text to parse
    step_text = f"Given I have {token_description}"
    
    try:
        # Parse the step using our DSL parser
        parsed = parse_step(step_text)
        
        if parsed['type'] != 'given':
            raise ValueError(f"Expected 'given' step, got '{parsed['type']}'")
        
        # Get the token type and map it to actual token
        token_type = parsed['token_type']
        context.token = TOKEN_MAP.get(token_type)
        context.token_type = token_type
        
    except DSLParseError as e:
        # Fallback: try to map directly without parser for simple cases
        token_lower = token_description.lower()
        if 'valid' in token_lower or 'admin' in token_lower:
            context.token = TOKEN_MAP['valid']
            context.token_type = 'valid'
        elif 'user' in token_lower:
            context.token = TOKEN_MAP['user']
            context.token_type = 'user'
        elif 'invalid' in token_lower:
            context.token = TOKEN_MAP['invalid']
            context.token_type = 'invalid'
        elif 'no' in token_lower or 'missing' in token_lower:
            context.token = TOKEN_MAP['none']
            context.token_type = 'none'
        else:
            raise AssertionError(f"Failed to parse Given step: {e}")


@when('I send a request to "{endpoint}"')
@step('I send a request to "{endpoint}"')
def step_when_request(context, endpoint):
    """
    When step that sends an HTTP GET request to the specified endpoint.
    
    Uses the token from the Given step (if any) in the Authorization header.
    Stores the response in context for validation in Then steps.
    """
    # Build the full step text to parse (optional, but for consistency)
    step_text = f'When I send a request to "{endpoint}"'
    
    try:
        parsed = parse_step(step_text)
        
        if parsed['type'] != 'when':
            raise ValueError(f"Expected 'when' step, got '{parsed['type']}'")
        
        # Use the endpoint from the parsed step (or the parameter)
        endpoint_path = parsed.get('endpoint', endpoint)
        url = f"{API_BASE_URL}{endpoint_path}"
        
        # Prepare headers
        headers = {}
        if hasattr(context, 'token') and context.token:
            headers['Authorization'] = f'Bearer {context.token}'
        
        # Send GET request
        try:
            response = requests.get(url, headers=headers)
            context.response = response
            context.response_status = response.status_code
            context.response_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
        except requests.exceptions.ConnectionError as e:
            raise AssertionError(f"API server is not running or unreachable at {API_BASE_URL}. Error: {e}")
        except requests.exceptions.RequestException as e:
            raise AssertionError(f"Request to {url} failed: {e}")
        
    except DSLParseError as e:
        # Fallback: use the endpoint parameter directly
        url = f"{API_BASE_URL}{endpoint}"
        headers = {}
        if hasattr(context, 'token') and context.token:
            headers['Authorization'] = f'Bearer {context.token}'
        
        try:
            response = requests.get(url, headers=headers)
            context.response = response
            context.response_status = response.status_code
            context.response_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
        except requests.exceptions.ConnectionError as e:
            raise AssertionError(f"API server is not running or unreachable at {API_BASE_URL}. Error: {e}")
        except requests.exceptions.RequestException as e:
            raise AssertionError(f"Request to {url} failed: {e}")


@then('the response should {validation_description}')
@step('the response should {validation_description}')
def step_then_validate(context, validation_description):
    """
    Then step that validates the response based on DSL keywords.
    
    Validates:
    - "validate token" - expects 200 OK
    - "expect 401" - expects 401 Unauthorized
    - "access denied" - expects 403 Forbidden
    - "access allowed" - expects 200 OK
    """
    # Build the full step text to parse
    step_text = f"Then the response should {validation_description}"
    
    try:
        parsed = parse_step(step_text)
        
        if parsed['type'] != 'then':
            raise ValueError(f"Expected 'then' step, got '{parsed['type']}'")
        
        validation = parsed['validation']
        
    except DSLParseError as e:
        # Fallback: try to determine validation type directly
        validation_lower = validation_description.lower()
        if 'validate' in validation_lower and 'token' in validation_lower:
            validation = 'validate_token'
        elif '401' in validation_lower or 'expect' in validation_lower:
            validation = 'expect_401'
        elif 'denied' in validation_lower:
            validation = 'access_denied'
        elif 'allowed' in validation_lower:
            validation = 'access_allowed'
        else:
            raise AssertionError(f"Failed to parse Then step: {e}")
    
    # Ensure we have a response from the When step
    if not hasattr(context, 'response'):
        raise AssertionError("No response available. Did you call the When step?")
    
    # Validate based on DSL keyword
    if validation == 'validate_token':
        assert context.response_status == 200, \
            f"Expected 200 OK for validate_token, got {context.response_status}"
        assert 'user_id' in context.response_data or 'message' in context.response_data, \
            "Response should contain user information"
    
    elif validation == 'expect_401':
        assert context.response_status == 401, \
            f"Expected 401 Unauthorized, got {context.response_status}"
        assert 'detail' in context.response_data, \
            "Response should contain error detail"
    
    elif validation == 'access_denied':
        assert context.response_status == 403, \
            f"Expected 403 Forbidden, got {context.response_status}"
        assert 'detail' in context.response_data, \
            "Response should contain error detail"
        assert 'Access denied' in context.response_data.get('detail', ''), \
            "Response detail should mention access denied"
    
    elif validation == 'access_allowed':
        assert context.response_status == 200, \
            f"Expected 200 OK for access_allowed, got {context.response_status}"
        # Accept various response formats: user data, admin data, or health status
        assert ('users' in context.response_data or 
                'message' in context.response_data or 
                'status' in context.response_data or
                'user_id' in context.response_data), \
            "Response should contain data (users, message, status, or user_id)"
    
    else:
        raise AssertionError(f"Unknown validation: {validation}")
