from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Set
import jwt
import hashlib
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)

# Server-side revoked tokens set (token jti or token hash / signature)
REVOKED_TOKENS: Set[str] = set()

def revoke_token(token: str) -> None:
    """Register token in server-side revocation registry."""
    if token:
        token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
        REVOKED_TOKENS.add(token_hash)

def is_token_revoked(token: str) -> bool:
    """Check if token hash exists in server-side revocation registry."""
    token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
    return token_hash in REVOKED_TOKENS

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    # Support modern bcrypt hashes ($2a$, $2b$, $2y$)
    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        try:
            import bcrypt
            return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
        except Exception:
            return False
    # Support Argon2 hashes ($argon2id$, $argon2i$)
    if hashed_password.startswith("$argon2"):
        try:
            from passlib.hash import argon2
            return argon2.verify(plain_password, hashed_password)
        except Exception:
            return False
    # Legacy SHA-256 fallback
    salt = "nagriksetu_salt"
    computed = hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()
    return computed == hashed_password

def get_password_hash(password: str) -> str:
    try:
        import bcrypt
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    except Exception:
        salt = "nagriksetu_salt"
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_access_token(token: str) -> Dict[str, Any]:
    if is_token_revoked(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session has been terminated. Token has been revoked on server.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security_bearer)) -> Dict[str, Any]:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token is required for this operation",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_payload = decode_access_token(credentials.credentials)
    user_payload["_raw_token"] = credentials.credentials
    return user_payload

# Explicit Role Hierarchy & Aliases:
# Standard Roles:
# 1. CITIZEN
# 2. GOVERNMENT_WELFARE_ADMIN (aliases: WELFARE_OFFICER, OFFICER)
# 3. PLATFORM_ADMIN (aliases: SWD_ADMIN)
# Note: ADMINISTRATOR is legacy and mapped strictly to Government Welfare Admin scrutiny level;
# it does NOT receive Platform Admin permissions.

ROLE_MAPPINGS = {
    "CITIZEN": {"CITIZEN"},
    "GOVERNMENT_WELFARE_ADMIN": {
        "GOVERNMENT_WELFARE_ADMIN", "WELFARE_OFFICER", "OFFICER", "ADMINISTRATOR"
    },
    "PLATFORM_ADMIN": {
        "PLATFORM_ADMIN", "SWD_ADMIN"
    }
}

def require_role(allowed_roles: list[str]):
    # Expand requested allowed roles according to strict mappings
    expanded_roles: Set[str] = set()
    for role in allowed_roles:
        r_upper = role.upper()
        if r_upper in ROLE_MAPPINGS:
            expanded_roles.update(ROLE_MAPPINGS[r_upper])
        elif r_upper in ["WELFARE_OFFICER", "OFFICER", "ADMINISTRATOR"]:
            expanded_roles.update(ROLE_MAPPINGS["GOVERNMENT_WELFARE_ADMIN"])
        elif r_upper in ["SWD_ADMIN"]:
            expanded_roles.update(ROLE_MAPPINGS["PLATFORM_ADMIN"])
        else:
            expanded_roles.add(r_upper)

    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        role = current_user.get("role", "CITIZEN").upper()
        if role not in expanded_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Operation requires one of the following roles: {', '.join(sorted(expanded_roles))}"
            )
        return current_user
    return role_checker

def verify_citizen_ownership(requested_citizen_id: str, current_user: Dict[str, Any]):
    role = (current_user.get("role") or "").upper()
    user_citizen_id = current_user.get("citizen_id")
    # Authorized administrative roles can inspect dossiers across all citizens
    admin_roles = (
        ROLE_MAPPINGS["GOVERNMENT_WELFARE_ADMIN"] | 
        ROLE_MAPPINGS["PLATFORM_ADMIN"]
    )
    if role in admin_roles:
        return True
    if user_citizen_id != requested_citizen_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You are not authorized to view or manage another citizen's records."
        )
    return True
