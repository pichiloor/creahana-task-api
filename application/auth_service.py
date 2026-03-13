from sqlalchemy.orm import Session

from domain.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.security import (create_access_token, hash_password,
                                     verify_password)


class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register(self, username: str, email: str, password: str):
        if self.user_repo.get_by_username(username):
            raise UserAlreadyExistsError(username)
        if self.user_repo.get_by_email(email):
            raise UserAlreadyExistsError(email)

        hashed = hash_password(password)
        return self.user_repo.create(
            username=username, email=email, hashed_password=hashed
        )

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        return create_access_token(data={"sub": str(user.id)})
