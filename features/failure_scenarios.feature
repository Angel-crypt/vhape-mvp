Feature: Failure Scenarios and Negative Testing
  As a developer
  I want to test scenarios that intentionally fail
  So that I can verify the reporting system works correctly for both success and failure cases

  @negative @testing @failure
  Scenario: Invalid token should fail when expecting valid token
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should validate token
    # This should FAIL - invalid token cannot validate

  @negative @testing @failure
  Scenario: Missing token should fail when expecting valid token
    Given I have no token
    When I send a request to "/api/users/me"
    Then the response should validate token
    # This should FAIL - missing token cannot validate

  @negative @testing @failure
  Scenario: Valid token should fail when expecting 401
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should expect 401
    # This should FAIL - valid token should not return 401

  @negative @testing @failure
  Scenario: Admin token should fail when expecting 401
    Given I have an admin token
    When I send a request to "/api/users/me"
    Then the response should expect 401
    # This should FAIL - admin token should not return 401

  @negative @testing @failure
  Scenario: User token should fail when expecting access allowed on admin endpoint
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access allowed
    # This should FAIL - user token should not have admin access

  @negative @testing @failure
  Scenario: Invalid token should fail when expecting access allowed
    Given I have an invalid token
    When I send a request to "/api/admin/users"
    Then the response should access allowed
    # This should FAIL - invalid token cannot have access

  @negative @testing @failure
  Scenario: Admin token should fail when expecting access denied on user endpoint
    Given I have an admin token
    When I send a request to "/api/users/me"
    Then the response should access denied
    # This should FAIL - admin token should have access to user endpoint

  @negative @testing @failure
  Scenario: Valid token should fail when expecting access denied on health endpoint
    Given I have a valid token
    When I send a request to "/api/health"
    Then the response should access denied
    # This should FAIL - health endpoint is public, no access denied

