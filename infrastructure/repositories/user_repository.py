from typing import Optional

from sqlalchemy.orm import Session

from infrastructure.models_orm import UserORM


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[UserORM]:
        return self.db.query(UserORM).filter(UserORM.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[UserORM]:
        return self.db.query(UserORM).filter(UserORM.username == username).first()

    def get_by_email(self, email: str) -> Optional[UserORM]:
        return self.db.query(UserORM).filter(UserORM.email == email).first()

    def create(self, username: str, email: str, hashed_password: str) -> UserORM:
        user = UserORM(username=username, email=email, hashed_password=hashed_password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
