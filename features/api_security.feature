Feature: Comprehensive API Security Testing
  As a QA engineer
  I want to test various API security scenarios
  So that I can ensure comprehensive security coverage

  # Note: API server health check is performed automatically before all scenarios
  # via the before_all hook in vhape/steps/environment.py

  @smoke @authentication
  Scenario: Valid token should validate successfully
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token

  @smoke @authentication
  Scenario: Admin token should validate successfully
    Given I have an admin token
    When I send a request to "/api/users/me"
    Then the response should validate token

  @smoke @authentication
  Scenario: User token should validate successfully
    Given I have a user token
    When I send a request to "/api/users/me"
    Then the response should validate token

  @smoke @authentication
  Scenario: Invalid token should return 401
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  @smoke @authentication
  Scenario: Missing token should return 401
    Given I have no token
    When I send a request to "/api/users/me"
    Then the response should expect 401

  @authorization @role-based
  Scenario: Admin token should allow access to admin endpoint
    Given I have an admin token
    When I send a request to "/api/admin/users"
    Then the response should access allowed

  @authorization @role-based
  Scenario: User token should be denied access to admin endpoint
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied

  @authorization @role-based
  Scenario: Valid token (admin) should allow access to admin endpoint
    Given I have a valid token
    When I send a request to "/api/admin/users"
    Then the response should access allowed

  @authorization @role-based
  Scenario: Invalid token should return 401 on admin endpoint
    Given I have an invalid token
    When I send a request to "/api/admin/users"
    Then the response should expect 401

  @authorization @role-based
  Scenario: Missing token should return 401 on admin endpoint
    Given I have no token
    When I send a request to "/api/admin/users"
    Then the response should expect 401

  @security @edge-cases
  Scenario: Health check endpoint should be accessible without authentication
    Given I have no token
    When I send a request to "/api/health"
    Then the response should access allowed

  @security @negative
  Scenario: Invalid token format should be rejected
    Given I have an invalid token
    When I send a request to "/api/admin/users"
    Then the response should expect 401

  @security @negative
  Scenario: Missing token on protected endpoint should return 401
    Given I have no token
    When I send a request to "/api/admin/users"
    Then the response should expect 401

