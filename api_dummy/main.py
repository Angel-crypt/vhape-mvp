"""
Vhape Dummy API - HU2 Implementation

Simple FastAPI server for testing DSL keywords:
- validate token
- access denied
"""

from fastapi import FastAPI, HTTPException, Depends, Header, status
from typing import Optional

app = FastAPI(
    title="Vhape Dummy API",
    description="Simple dummy API for testing authentication DSL keywords",
    version="1.0.0",
)

# Valid tokens
VALID_TOKENS = {
    "valid-token": {"user_id": "user1", "role": "admin"},
    "user-token": {"user_id": "user2", "role": "user"},
}


def validate_token(token: Optional[str] = None) -> dict:
    """Validate authentication token."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )
    
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        token = token[7:]
    
    if token in VALID_TOKENS:
        return VALID_TOKENS[token]
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication token",
    )


async def get_current_user(
    authorization: Optional[str] = Header(None, alias="Authorization")
) -> dict:
    """Dependency to validate token."""
    return validate_token(authorization)


async def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency to check admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return current_user


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/users/me")
async def get_current_user_profile(current_user: dict = Depends(get_current_user)):
    """
    DSL keywords: validate token / expect 401
    Get current user profile. Requires valid token.
    Returns 200 if valid, 401 if invalid/missing.
    Use without token or with invalid token to test "expect 401".
    """
    return {
        "user_id": current_user["user_id"],
        "role": current_user["role"],
        "message": "User profile retrieved successfully",
    }


@app.get("/api/admin/users")
async def get_all_users(admin_user: dict = Depends(get_admin_user)):
    """
    DSL keyword: access denied
    Get all users list. Admin only.
    Returns 403 if user is not admin, 200 if admin.
    """
    return {
        "users": [
            {"id": "user1", "role": "admin"},
            {"id": "user2", "role": "user"},
        ],
        "message": "Users list retrieved successfully",
        "accessed_by": admin_user["user_id"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_dummy.main:app", host="0.0.0.0", port=8000, reload=True)
