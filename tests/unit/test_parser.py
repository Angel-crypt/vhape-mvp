"""
Unit tests for Vhape DSL Parser
"""

import pytest
from vhape.parser import StepParser, parse_step, DSLParseError


class TestStepParser:
    """Test cases for StepParser."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = StepParser()
    
    # Given steps tests
    def test_parse_given_valid_token(self):
        """Test parsing 'Given I have a valid token'."""
        result = self.parser.parse_step("Given I have a valid token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'valid'
    
    def test_parse_given_admin_token(self):
        """Test parsing 'Given I have an admin token'."""
        result = self.parser.parse_step("Given I have an admin token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'admin'
    
    def test_parse_given_user_token(self):
        """Test parsing 'Given I have a user token'."""
        result = self.parser.parse_step("Given I have a user token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'user'
    
    def test_parse_given_invalid_token(self):
        """Test parsing 'Given I have an invalid token'."""
        result = self.parser.parse_step("Given I have an invalid token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'invalid'
    
    def test_parse_given_no_token(self):
        """Test parsing 'Given I have no token'."""
        result = self.parser.parse_step("Given I have no token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'none'
    
    def test_parse_given_missing_token(self):
        """Test parsing 'Given I have a missing token'."""
        result = self.parser.parse_step("Given I have a missing token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'none'
    
    # When steps tests
    def test_parse_when_request(self):
        """Test parsing 'When I send a request to "/api/users/me"'."""
        result = self.parser.parse_step('When I send a request to "/api/users/me"')
        assert result['type'] == 'when'
        assert result['endpoint'] == '/api/users/me'
    
    def test_parse_when_request_admin_endpoint(self):
        """Test parsing 'When I send a request to "/api/admin/users"'."""
        result = self.parser.parse_step('When I send a request to "/api/admin/users"')
        assert result['type'] == 'when'
        assert result['endpoint'] == '/api/admin/users'
    
    # Then steps tests
    def test_parse_then_validate_token(self):
        """Test parsing 'Then the response should validate token'."""
        result = self.parser.parse_step("Then the response should validate token")
        assert result['type'] == 'then'
        assert result['validation'] == 'validate_token'
    
    def test_parse_then_expect_401(self):
        """Test parsing 'Then the response should expect 401'."""
        result = self.parser.parse_step("Then the response should expect 401")
        assert result['type'] == 'then'
        assert result['validation'] == 'expect_401'
    
    def test_parse_then_access_denied(self):
        """Test parsing 'Then the response should access denied'."""
        result = self.parser.parse_step("Then the response should access denied")
        assert result['type'] == 'then'
        assert result['validation'] == 'access_denied'
    
    def test_parse_then_access_allowed(self):
        """Test parsing 'Then the response should access allowed'."""
        result = self.parser.parse_step("Then the response should access allowed")
        assert result['type'] == 'then'
        assert result['validation'] == 'access_allowed'
    
    # Case insensitive tests
    def test_parse_case_insensitive(self):
        """Test that parsing is case insensitive."""
        result1 = self.parser.parse_step("GIVEN I HAVE A VALID TOKEN")
        result2 = self.parser.parse_step("given i have a valid token")
        assert result1 == result2
    
    # Error handling tests
    def test_parse_invalid_step(self):
        """Test that invalid steps raise DSLParseError."""
        with pytest.raises(DSLParseError):
            self.parser.parse_step("Invalid step text")
    
    def test_parse_empty_step(self):
        """Test that empty steps raise DSLParseError."""
        with pytest.raises(DSLParseError):
            self.parser.parse_step("")


class TestParseStepFunction:
    """Test cases for the convenience parse_step function."""
    
    def test_parse_step_function(self):
        """Test that the parse_step function works."""
        result = parse_step("Given I have a valid token")
        assert result['type'] == 'given'
        assert result['token_type'] == 'valid'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

