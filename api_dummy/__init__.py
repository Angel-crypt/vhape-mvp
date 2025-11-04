"""
Vhape Dummy API Package

This package contains the dummy API server for testing authentication scenarios.
Provides a FastAPI-based dummy API for BDD testing with DSL keywords like:
- validate token
- expect 401
- access denied
"""

__version__ = "1.0.0"
__author__ = "Angel Cruz"
__description__ = "Dummy API server for testing authentication and authorization scenarios"

# Export the FastAPI app for convenience
# Import is deferred to avoid circular imports and ensure all routes are registered
def get_app():
    """
    Get the FastAPI application instance.
    
    Returns:
        FastAPI: The application instance from api_dummy.main
    """
    from api_dummy.main import app
    return app

# Package-level constants that might be useful
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8000
DOCS_URL = "/docs"
REDOC_URL = "/redoc"

__all__ = [
    "__version__",
    "__author__",
    "__description__",
    "get_app",
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    "DOCS_URL",
    "REDOC_URL",
]

