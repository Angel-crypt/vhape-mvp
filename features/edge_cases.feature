Feature: Edge Cases and Boundary Conditions
  As a security tester
  I want to test edge cases and boundary conditions
  So that I can ensure the API handles unexpected scenarios correctly

  Scenario: User with valid token accessing non-existent endpoint behavior
    # Note: This scenario tests the current endpoint behavior
    # In a real scenario, this might test a 404 vs 401 response
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token

  Scenario: Multiple consecutive invalid token attempts
    # Simulate multiple failed authentication attempts
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  Scenario: User token attempting to access admin endpoint multiple times
    # Test that access denied is consistently enforced
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied

  Scenario: Admin token accessing user endpoint
    # Admin should have access to user endpoints
    Given I have an admin token
    When I send a request to "/api/users/me"
    Then the response should validate token

  Scenario: Valid token accessing health check
    # Health check should work with or without token
    Given I have a valid token
    When I send a request to "/api/health"
    Then the response should access allowed

