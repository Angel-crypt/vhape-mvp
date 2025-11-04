"""
Vhape Dummy API - HU2 Implementation

A FastAPI-based dummy API server for testing authentication and authorization scenarios.
This API provides controlled endpoints to simulate different authentication behaviors
for BDD testing with DSL keywords like "validate token", "expect 401", "access denied".

The API is accessible via FastAPI's auto-generated documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Vhape Dummy API",
    description="A dummy API for testing authentication and authorization scenarios",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================================================
# Authentication Logic
# ============================================================================

# Valid tokens for testing (in real scenario, this would be more sophisticated)
VALID_TOKENS = {
    "valid-token-123": {"user_id": "user1", "role": "admin"},
    "valid-token-456": {"user_id": "user2", "role": "user"},
    "admin-token": {"user_id": "admin", "role": "admin"},
}

# Invalid token patterns
INVALID_TOKEN_MESSAGES = {
    "expired-token": "Token has expired",
    "invalid-token": "Invalid authentication token",
    "malformed-token": "Malformed token format",
}


def validate_token(token: Optional[str] = None) -> dict:
    """
    Validate authentication token.
    
    Args:
        token: The authentication token from Authorization header
        
    Returns:
        dict: User information if token is valid
        
    Raises:
        HTTPException: 401 if token is invalid or missing
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    # Check if token is valid
    if token in VALID_TOKENS:
        return VALID_TOKENS[token]
    
    # Check for specific invalid token patterns
    if token in INVALID_TOKEN_MESSAGES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INVALID_TOKEN_MESSAGES[token],
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generic invalid token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )


def check_admin_access(user_info: dict) -> dict:
    """
    Check if user has admin role.
    
    Args:
        user_info: User information from token validation
        
    Returns:
        dict: User information if admin
        
    Raises:
        HTTPException: 403 if user is not admin
    """
    if user_info.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Admin role required",
        )
    return user_info


# ============================================================================
# Dependencies
# ============================================================================

async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> dict:
    """
    Dependency to extract and validate token from Authorization header.
    Supports both "Bearer <token>" and direct token formats.
    """
    token = authorization
    return validate_token(token)


async def get_admin_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency to ensure user has admin role.
    """
    return check_admin_access(current_user)


# ============================================================================
# Response Models
# ============================================================================

class MessageResponse(BaseModel):
    """Standard message response model."""
    message: str
    status: str = "success"


class UserInfoResponse(BaseModel):
    """User information response model."""
    message: str
    user_id: str
    role: str


class DataResponse(BaseModel):
    """Data response model."""
    message: str
    data: dict


# ============================================================================
# Public Endpoints (No Authentication Required)
# ============================================================================

@app.get("/", tags=["Public"])
async def root():
    """Root endpoint - Public access."""
    return {
        "message": "Welcome to Vhape Dummy API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["Public"])
async def health_check():
    """Health check endpoint - Public access."""
    return {"status": "healthy", "service": "vhape-dummy-api"}


@app.get("/public", tags=["Public"])
async def public_endpoint():
    """Public endpoint - No authentication required."""
    return {
        "message": "This is a public endpoint",
        "access": "public",
        "status_code": 200,
    }


# ============================================================================
# Protected Endpoints (Authentication Required)
# ============================================================================

@app.get(
    "/protected",
    response_model=UserInfoResponse,
    tags=["Protected"],
    summary="Protected endpoint - Valid token required",
    description="Requires a valid authentication token. Returns 401 if token is missing or invalid.",
)
async def protected_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Protected endpoint that requires valid token.
    
    **DSL Testing:**
    - "validate token" - Use a valid token to access
    - "expect 401" - Omit token or use invalid token
    """
    return {
        "message": "Access granted to protected resource",
        "user_id": current_user["user_id"],
        "role": current_user["role"],
    }


@app.get(
    "/secure-data",
    response_model=DataResponse,
    tags=["Protected"],
    summary="Secure data endpoint - Valid token required",
    description="Endpoint that returns secure data when authenticated.",
)
async def secure_data(current_user: dict = Depends(get_current_user)):
    """
    Secure data endpoint.
    
    **DSL Testing:**
    - "validate token" - Use valid-token-123 or valid-token-456
    - "expect 401" - Use invalid-token or expired-token
    """
    return {
        "message": "Secure data accessed successfully",
        "data": {
            "user": current_user["user_id"],
            "resource": "confidential-data",
            "access_level": current_user["role"],
        },
    }


@app.get(
    "/admin-only",
    response_model=MessageResponse,
    tags=["Admin"],
    summary="Admin endpoint - Admin role required",
    description="Requires admin role. Returns 403 if user is not admin.",
)
async def admin_only(admin_user: dict = Depends(get_admin_user)):
    """
    Admin-only endpoint.
    
    **DSL Testing:**
    - "access denied" - Use valid-token-456 (non-admin user)
    - "validate token" + admin - Use admin-token or valid-token-123
    """
    return {
        "message": "Admin access granted",
        "status": "success",
    }


@app.get(
    "/admin/users",
    response_model=DataResponse,
    tags=["Admin"],
    summary="Admin users endpoint - Admin role required",
    description="Returns user list for admin users only.",
)
async def admin_users(admin_user: dict = Depends(get_admin_user)):
    """
    Admin users endpoint.
    
    **DSL Testing:**
    - "access denied" - Use non-admin token
    - "expect 403" - Use valid-token-456
    """
    return {
        "message": "User list retrieved",
        "data": {
            "users": [
                {"id": "user1", "role": "admin"},
                {"id": "user2", "role": "user"},
                {"id": "admin", "role": "admin"},
            ],
            "accessed_by": admin_user["user_id"],
        },
    }


# ============================================================================
# Test Endpoints for Specific Scenarios
# ============================================================================

@app.get(
    "/test/validate-token",
    tags=["Test Scenarios"],
    summary="Test endpoint for 'validate token' DSL keyword",
    description="Explicitly tests token validation. Returns 200 with user info if valid, 401 if invalid.",
)
async def test_validate_token(current_user: dict = Depends(get_current_user)):
    """
    Test endpoint for validating tokens.
    
    **Usage:**
    - Valid token: Authorization: Bearer valid-token-123
    - Invalid token: Authorization: Bearer invalid-token
    - Missing token: No Authorization header
    """
    return {
        "message": "Token validated successfully",
        "user": current_user,
        "validation": "passed",
    }


@app.get(
    "/test/expect-401",
    tags=["Test Scenarios"],
    summary="Test endpoint for 'expect 401' DSL keyword",
    description="Endpoint that returns 401 when token is invalid or missing.",
)
async def test_expect_401(current_user: dict = Depends(get_current_user)):
    """
    Test endpoint for 401 scenarios.
    
    This endpoint will return 401 if:
    - No Authorization header is provided
    - Invalid token is provided
    - Expired token is provided
    """
    return {
        "message": "This should not be reached with invalid token",
        "user": current_user,
    }


@app.get(
    "/test/access-denied",
    tags=["Test Scenarios"],
    summary="Test endpoint for 'access denied' DSL keyword",
    description="Endpoint that returns 403 for non-admin users.",
)
async def test_access_denied(admin_user: dict = Depends(get_admin_user)):
    """
    Test endpoint for access denied scenarios.
    
    Returns 403 if user is not admin.
    Use valid-token-456 (non-admin) to test access denied.
    """
    return {
        "message": "Access granted",
        "user": admin_user,
    }


@app.get(
    "/test/missing-token",
    tags=["Test Scenarios"],
    summary="Test endpoint that requires token but returns 401 if missing",
    description="Explicitly tests missing token scenario.",
)
async def test_missing_token(current_user: dict = Depends(get_current_user)):
    """
    Test endpoint for missing token scenario.
    
    Call without Authorization header to get 401.
    """
    return {
        "message": "Token was provided",
        "user": current_user,
    }


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        headers=exc.headers,
    )


# ============================================================================
# Run Server
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api_dummy.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

