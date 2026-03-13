from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.schemas import TokenResponse, UserLoginRequest, UserRegisterRequest
from application.auth_service import AuthService
from domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from infrastructure.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: UserRegisterRequest, db: Session = Depends(get_db)):
    try:
        user = AuthService(db).register(
            username=body.username,
            email=body.email,
            password=body.password,
        )
        return {"id": user.id, "username": user.username, "email": user.email}
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(body: UserLoginRequest, db: Session = Depends(get_db)):
    try:
        token = AuthService(db).login(
            username=body.username,
            password=body.password,
        )
        return TokenResponse(access_token=token)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
