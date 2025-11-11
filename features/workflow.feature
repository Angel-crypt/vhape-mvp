Feature: Complete Authentication Workflow
  As a developer
  I want to test complete authentication workflows
  So that I can validate end-to-end security flows

  Scenario: Complete user authentication flow - success path
    # Simulate a user logging in and accessing their profile
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token

  Scenario: Complete user authentication flow - unauthorized access attempt
    # Simulate an unauthorized user trying to access protected resources
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  Scenario: Complete admin workflow - authorized admin access
    # Simulate an admin accessing admin-only resources
    Given I have an admin token
    When I send a request to "/api/admin/users"
    Then the response should access allowed

  Scenario: Complete admin workflow - unauthorized user access
    # Simulate a regular user trying to access admin resources
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied

  Scenario: Complete workflow - missing authentication
    # Simulate a request without authentication
    Given I have no token
    When I send a request to "/api/users/me"
    Then the response should expect 401

