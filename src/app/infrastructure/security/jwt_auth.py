from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.common.exceptions import UnauthorizedException
from app.core.config import settings

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise UnauthorizedException("Invalid or expired token.") from exc

    user_id = payload.get("userId") or payload.get("sub")
    email = payload.get("email")

    if not user_id or not email:
        raise UnauthorizedException("Invalid token payload.")

    return {"id": user_id, "email": email}
