"""
Vhape Dummy API - HU2 Implementation

Simple FastAPI server for testing DSL keywords:
- validate token
- expect 401
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

# Invalid tokens
INVALID_TOKENS = ["invalid-token", "expired-token"]


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


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/validate-token")
async def validate_token_endpoint(current_user: dict = Depends(get_current_user)):
    """
    DSL keyword: validate token
    Requires valid token. Returns 200 if valid, 401 if invalid/missing.
    """
    return {
        "message": "Token validated",
        "user_id": current_user["user_id"],
    }


@app.get("/expect-401")
async def expect_401_endpoint(current_user: dict = Depends(get_current_user)):
    """
    DSL keyword: expect 401
    Returns 401 if token is missing or invalid.
    """
    return {"message": "Should not reach here"}


@app.get("/access-denied")
async def access_denied_endpoint(admin_user: dict = Depends(get_admin_user)):
    """
    DSL keyword: access denied
    Returns 403 if user is not admin, 200 if admin.
    """
    return {
        "message": "Access granted",
        "user_id": admin_user["user_id"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api_dummy.main:app", host="0.0.0.0", port=8000, reload=True)
