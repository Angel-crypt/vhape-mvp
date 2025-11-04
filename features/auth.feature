Feature: API Authentication and Authorization
  As a developer
  I want to validate API security
  So that I can ensure my API endpoints are properly protected

  Scenario: Valid token should grant access to user profile
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token

  Scenario: Invalid token should return 401
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  Scenario: Missing token should return 401
    Given I have no token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  Scenario: User token should be denied access to admin endpoint
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied

  Scenario: Admin token should allow access to admin endpoint
    Given I have an admin token
    When I send a request to "/api/admin/users"
    Then the response should access allowed

