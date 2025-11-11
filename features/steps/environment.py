"""
Behave environment configuration.

This file is automatically loaded by Behave before and after scenarios.
It handles setup and teardown operations.
"""

import os
import sys
import requests
from pathlib import Path
from behave.model import Scenario, Feature, Step
from vhape.reporting.summary import TestSummary


# Global test summary instance
test_summary = TestSummary()


def before_all(context):
    """
    Hook that runs before all features.
    Checks if the API dummy server is running.
    Initializes the test summary.
    """
    api_url = os.getenv("VHAPE_API_URL", "http://localhost:8000")
    sys.stdout.write(f"\n{'='*60}\n")
    sys.stdout.write(f"  VHAPE - API Security Validation\n")
    sys.stdout.write(f"{'='*60}\n")
    sys.stdout.write(f"\n🔍 Verifying API server accessibility at {api_url}...\n")
    sys.stdout.flush()
    
    context.api_url = api_url
    
    # Initialize test summary in context
    context.test_summary = test_summary
    
    try:
        response = requests.get(f"{api_url}/api/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            sys.stdout.write("✅ API server is running and healthy.\n\n")
            sys.stdout.flush()
        else:
            raise ConnectionError(f"API health check failed: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError as e:
        sys.stdout.write(f"❌ API server is not running or unreachable. Error: {e}\n")
        sys.stdout.write("   Please ensure the API dummy server is running.\n")
        sys.stdout.write("   Start it with: ./api_dummy/run.sh\n\n")
        sys.stdout.flush()
        exit(1)  # Exit Behave if API is not running
    except Exception as e:
        sys.stdout.write(f"❌ An unexpected error occurred during API health check: {e}\n\n")
        sys.stdout.flush()
        exit(1)


def after_step(context, step: Step):
    """Hook that runs after each step."""
    if hasattr(context, 'test_summary'):
        status = 'passed' if step.status == 'passed' else 'failed'
        error = str(step.error) if hasattr(step, 'error') and step.error else None
        context.test_summary.add_step(step.name, status, error)


def after_scenario(context, scenario: Scenario):
    """
    Hook that runs after each scenario.
    Cleans up context variables and records scenario result.
    """
    # Record scenario result
    if hasattr(context, 'test_summary'):
        status = 'passed' if scenario.status == 'passed' else 'failed'
        feature_name = scenario.feature.name if hasattr(scenario, 'feature') else 'Unknown'
        context.test_summary.add_scenario(scenario.name, status, feature_name)
    
    # Clean up context variables
    if hasattr(context, 'token'):
        del context.token
    if hasattr(context, 'token_type'):
        del context.token_type
    if hasattr(context, 'response'):
        del context.response
    if hasattr(context, 'response_status'):
        del context.response_status
    if hasattr(context, 'response_data'):
        del context.response_data


def after_feature(context, feature: Feature):
    """Hook that runs after each feature."""
    if hasattr(context, 'test_summary'):
        status = 'passed' if feature.status == 'passed' else 'failed'
        context.test_summary.add_feature(feature.name, status)


def after_all(context):
    """
    Hook that runs after all features.
    Generates and displays the final summary.
    """
    if not hasattr(context, 'test_summary'):
        return
    
    # Debug: Check security issues before finalizing
    num_issues = len(context.test_summary.security_issues)
    if num_issues > 0:
        sys.stdout.write(f"\n🔍 Debug: Found {num_issues} security issues before finalizing\n")
        sys.stdout.flush()
    
    context.test_summary.finalize()
    
    # Print summary
    sys.stdout.write("\n")
    sys.stdout.flush()
    context.test_summary.print_summary()
    sys.stdout.flush()
    
    # Save JSON summary
    results_dir = Path('tests/results')
    results_dir.mkdir(parents=True, exist_ok=True)
    json_file = context.test_summary.save_json()
    sys.stdout.write(f"💾 Summary saved to: {json_file}\n\n")
    sys.stdout.flush()
    
    # Debug: Verify security issues after saving
    if num_issues > 0:
        sys.stdout.write(f"🔍 Debug: Saved {len(context.test_summary.security_issues)} security issues to JSON\n")
        sys.stdout.flush()
