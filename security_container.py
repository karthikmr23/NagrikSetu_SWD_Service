from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import hashlib
from fastapi import HTTPException, Security, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security_bearer = HTTPBearer(auto_error=False)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = "nagriksetu_salt"
    computed = hashlib.sha256((plain_password + salt).encode('utf-8')).hexdigest()
    return computed == hashed_password

def get_password_hash(password: str) -> str:
    salt = "nagriksetu_salt"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    # PyJWT encode
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def decode_access_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except Exception as e:
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
    return decode_access_token(credentials.credentials)

def require_role(allowed_roles: list[str]):
    # Normalize aliases: SWD_ADMIN and ADMINISTRATOR, WELFARE_OFFICER, GOVERNMENT_WELFARE_ADMIN
    expanded_roles = set(allowed_roles)
    if "ADMINISTRATOR" in allowed_roles:
        expanded_roles.add("SWD_ADMIN")
        expanded_roles.add("PLATFORM_ADMIN")
        expanded_roles.add("GOVERNMENT_WELFARE_ADMIN")
    if "SWD_ADMIN" in allowed_roles:
        expanded_roles.add("ADMINISTRATOR")
        expanded_roles.add("PLATFORM_ADMIN")
        expanded_roles.add("GOVERNMENT_WELFARE_ADMIN")
    if "WELFARE_OFFICER" in allowed_roles:
        expanded_roles.add("OFFICER")
        expanded_roles.add("GOVERNMENT_WELFARE_ADMIN")

    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        role = current_user.get("role", "CITIZEN")
        if role not in expanded_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Operation requires one of the following roles: {', '.join(sorted(expanded_roles))}"
            )
        return current_user
    return role_checker

def verify_citizen_ownership(requested_citizen_id: str, current_user: Dict[str, Any]):
    role = current_user.get("role")
    user_citizen_id = current_user.get("citizen_id")
    if role in ["SWD_ADMIN", "ADMINISTRATOR", "WELFARE_OFFICER", "PLATFORM_ADMIN", "GOVERNMENT_WELFARE_ADMIN"]:
        return True
    if user_citizen_id != requested_citizen_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You are not authorized to view or manage another citizen's records."
        )
    return True
