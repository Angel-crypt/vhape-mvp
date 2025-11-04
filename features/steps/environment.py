"""
Behave environment configuration.

This file is automatically loaded by Behave before and after scenarios.
It handles setup and teardown operations.
"""

import os
import requests
from behave.model import Scenario


def before_all(context):
    """
    Hook that runs before all features.
    Checks if the API dummy server is running.
    """
    api_url = os.getenv("VHAPE_API_URL", "http://localhost:8000")
    print(f"\nVerifying API server accessibility at {api_url}...")
    context.api_url = api_url
    
    try:
        response = requests.get(f"{api_url}/api/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "healthy":
            print("✓ API server is running and healthy.")
        else:
            raise ConnectionError(f"API health check failed: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"✗ API server is not running or unreachable. Error: {e}")
        print("Please ensure the API dummy server is running. You can start it with: ./api_dummy/run.sh")
        exit(1)  # Exit Behave if API is not running
    except Exception as e:
        print(f"✗ An unexpected error occurred during API health check: {e}")
        exit(1)


def after_scenario(context, scenario: Scenario):
    """
    Hook that runs after each scenario.
    Cleans up context variables.
    """
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
