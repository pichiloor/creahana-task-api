from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from infrastructure.database import get_db
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.security import decode_access_token

# Reads the Bearer token from the Authorization header automatically.
bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Extract the raw token string from the header.
    token = credentials.credentials

    # Decode and validate the JWT. Returns None if invalid or expired.
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    # The user ID is stored in the "sub" field of the token.
    user_id = payload.get("sub")
    user = UserRepository(db).get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user
