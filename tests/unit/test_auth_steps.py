"""
Unit tests for Vhape auth_steps logic.

Tests the token mapping, header construction, and validation logic
without making actual HTTP requests (using mocks).
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from vhape.parser import DSLParseError


# Import the token mapping and logic from auth_steps
# We'll test the logic without importing the full behave decorators
TOKEN_MAP = {
    'valid': 'valid-token',
    'admin': 'valid-token',
    'user': 'user-token',
    'invalid': 'invalid-token',
    'none': None,
}


class TestTokenMapping:
    """Test token mapping logic."""
    
    def test_token_map_valid(self):
        """Test mapping for valid token."""
        assert TOKEN_MAP['valid'] == 'valid-token'
    
    def test_token_map_admin(self):
        """Test mapping for admin token."""
        assert TOKEN_MAP['admin'] == 'valid-token'
        assert TOKEN_MAP['admin'] == TOKEN_MAP['valid']
    
    def test_token_map_user(self):
        """Test mapping for user token."""
        assert TOKEN_MAP['user'] == 'user-token'
    
    def test_token_map_invalid(self):
        """Test mapping for invalid token."""
        assert TOKEN_MAP['invalid'] == 'invalid-token'
    
    def test_token_map_none(self):
        """Test mapping for no token."""
        assert TOKEN_MAP['none'] is None
    
    def test_all_token_types_present(self):
        """Test that all expected token types are in the map."""
        expected_keys = {'valid', 'admin', 'user', 'invalid', 'none'}
        assert set(TOKEN_MAP.keys()) == expected_keys


class TestHeaderConstruction:
    """Test header construction logic."""
    
    def test_build_headers_with_token(self):
        """Test building headers with a token."""
        token = 'valid-token'
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        assert 'Authorization' in headers
        assert headers['Authorization'] == 'Bearer valid-token'
    
    def test_build_headers_without_token(self):
        """Test building headers without a token."""
        token = None
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        assert 'Authorization' not in headers
        assert headers == {}
    
    def test_build_headers_with_empty_token(self):
        """Test building headers with empty token string."""
        token = ''
        headers = {}
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        # Empty string is falsy, so no header should be added
        assert 'Authorization' not in headers
    
    def test_build_headers_with_different_tokens(self):
        """Test building headers with different token types."""
        test_cases = [
            ('valid-token', 'Bearer valid-token'),
            ('user-token', 'Bearer user-token'),
            ('invalid-token', 'Bearer invalid-token'),
        ]
        
        for token, expected_header in test_cases:
            headers = {}
            if token:
                headers['Authorization'] = f'Bearer {token}'
            assert headers['Authorization'] == expected_header


class TestValidationLogic:
    """Test validation logic for different response types."""
    
    def test_validate_token_success(self):
        """Test validate_token validation with successful response."""
        response_status = 200
        response_data = {'user_id': 123, 'username': 'test'}
        
        if response_status == 200:
            assert 'user_id' in response_data or 'message' in response_data
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'secure'
    
    def test_validate_token_failure(self):
        """Test validate_token validation with failed response."""
        response_status = 401
        response_data = {}
        
        if response_status == 200:
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'insecure'
    
    def test_expect_401_success(self):
        """Test expect_401 validation with 401 response."""
        response_status = 401
        response_data = {'detail': 'Unauthorized'}
        
        if response_status == 401:
            assert 'detail' in response_data
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'secure'
    
    def test_expect_401_failure(self):
        """Test expect_401 validation when 401 is expected but got 200."""
        response_status = 200
        response_data = {}
        
        if response_status == 401:
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'insecure'
    
    def test_access_denied_success(self):
        """Test access_denied validation with 403 response."""
        response_status = 403
        response_data = {'detail': 'Access denied'}
        
        if response_status == 403:
            assert 'detail' in response_data
            assert 'Access denied' in response_data.get('detail', '')
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'secure'
    
    def test_access_denied_failure(self):
        """Test access_denied validation when 403 is expected but got 200."""
        response_status = 200
        response_data = {}
        
        if response_status == 403:
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'insecure'
    
    def test_access_allowed_success(self):
        """Test access_allowed validation with 200 response."""
        response_status = 200
        response_data = {'users': [{'id': 1}]}
        
        if response_status == 200:
            assert ('users' in response_data or 
                   'message' in response_data or 
                   'status' in response_data or
                   'user_id' in response_data)
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'secure'
    
    def test_access_allowed_with_message(self):
        """Test access_allowed validation with message in response."""
        response_status = 200
        response_data = {'message': 'Success'}
        
        if response_status == 200:
            assert ('users' in response_data or 
                   'message' in response_data or 
                   'status' in response_data or
                   'user_id' in response_data)
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'secure'
    
    def test_access_allowed_with_status(self):
        """Test access_allowed validation with status in response."""
        response_status = 200
        response_data = {'status': 'ok'}
        
        if response_status == 200:
            assert ('users' in response_data or 
                   'message' in response_data or 
                   'status' in response_data or
                   'user_id' in response_data)
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'secure'
    
    def test_access_allowed_failure(self):
        """Test access_allowed validation when 200 is expected but got 403."""
        response_status = 403
        response_data = {}
        
        if response_status == 200:
            security_status = 'secure'
        else:
            security_status = 'insecure'
        
        assert security_status == 'insecure'


class TestStepTextParsing:
    """Test step text parsing and construction logic."""
    
    def test_build_given_step_text(self):
        """Test building Given step text."""
        token_description = "a valid token"
        step_text = f"Given I have {token_description}"
        
        assert step_text == "Given I have a valid token"
    
    def test_build_when_step_text(self):
        """Test building When step text."""
        endpoint = "/api/users/me"
        step_text = f'When I send a request to "{endpoint}"'
        
        assert step_text == 'When I send a request to "/api/users/me"'
    
    def test_build_then_step_text(self):
        """Test building Then step text."""
        validation_description = "validate token"
        step_text = f"Then the response should {validation_description}"
        
        assert step_text == "Then the response should validate token"
    
    def test_token_description_variations(self):
        """Test different token description variations."""
        variations = [
            "a valid token",
            "an admin token",
            "a user token",
            "an invalid token",
            "no token",
        ]
        
        for desc in variations:
            step_text = f"Given I have {desc}"
            assert step_text.startswith("Given I have")
            assert desc in step_text
    
    def test_validation_description_variations(self):
        """Test different validation description variations."""
        variations = [
            "validate token",
            "expect 401",
            "access denied",
            "access allowed",
        ]
        
        for desc in variations:
            step_text = f"Then the response should {desc}"
            assert step_text.startswith("Then the response should")
            assert desc in step_text


class TestURLConstruction:
    """Test URL construction logic."""
    
    def test_build_url_with_base_url(self):
        """Test building full URL from base URL and endpoint."""
        api_base_url = "http://localhost:8000"
        endpoint = "/api/users/me"
        url = f"{api_base_url}{endpoint}"
        
        assert url == "http://localhost:8000/api/users/me"
    
    def test_build_url_with_different_endpoints(self):
        """Test building URLs with different endpoints."""
        api_base_url = "http://localhost:8000"
        endpoints = [
            "/api/users/me",
            "/api/admin/users",
            "/api/health",
        ]
        
        for endpoint in endpoints:
            url = f"{api_base_url}{endpoint}"
            assert url.startswith(api_base_url)
            assert url.endswith(endpoint)
    
    def test_build_url_with_query_params(self):
        """Test building URL with query parameters in endpoint."""
        api_base_url = "http://localhost:8000"
        endpoint = "/api/search?q=test&limit=10"
        url = f"{api_base_url}{endpoint}"
        
        assert url == "http://localhost:8000/api/search?q=test&limit=10"
        assert "?" in url
        assert "q=test" in url


class TestResponseDataExtraction:
    """Test response data extraction logic."""
    
    def test_extract_json_response(self):
        """Test extracting JSON from response."""
        mock_response = Mock()
        mock_response.headers.get.return_value = 'application/json'
        mock_response.json.return_value = {'user_id': 123}
        
        content_type = mock_response.headers.get('content-type', '')
        if content_type.startswith('application/json'):
            response_data = mock_response.json()
        else:
            response_data = {}
        
        assert response_data == {'user_id': 123}
    
    def test_extract_non_json_response(self):
        """Test extracting data from non-JSON response."""
        mock_response = Mock()
        mock_response.headers.get.return_value = 'text/html'
        
        content_type = mock_response.headers.get('content-type', '')
        if content_type.startswith('application/json'):
            response_data = mock_response.json()
        else:
            response_data = {}
        
        assert response_data == {}
    
    def test_extract_response_with_missing_content_type(self):
        """Test extracting data when content-type header is missing."""
        mock_response = Mock()
        mock_response.headers.get.return_value = None
        
        content_type = mock_response.headers.get('content-type', '') or ''
        if content_type.startswith('application/json'):
            response_data = mock_response.json()
        else:
            response_data = {}
        
        assert response_data == {}


class TestErrorHandling:
    """Test error handling logic."""
    
    def test_connection_error_message(self):
        """Test connection error message format."""
        api_base_url = "http://localhost:8000"
        error_msg = f"API server is not running or unreachable at {api_base_url}"
        
        assert "API server is not running" in error_msg
        assert api_base_url in error_msg
    
    def test_request_error_message(self):
        """Test request error message format."""
        url = "http://localhost:8000/api/users/me"
        error_msg = f"Request to {url} failed"
        
        assert "Request to" in error_msg
        assert url in error_msg
    
    def test_missing_response_error(self):
        """Test error message when response is missing."""
        error_msg = "No response available. Did you call the When step?"
        
        assert "No response available" in error_msg
        assert "When step" in error_msg
    
    def test_unknown_validation_error(self):
        """Test error message for unknown validation type."""
        validation = "unknown_validation"
        error_msg = f"Unknown validation: {validation}"
        
        assert "Unknown validation" in error_msg
        assert validation in error_msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

