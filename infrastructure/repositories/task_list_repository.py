from typing import Optional

from sqlalchemy.orm import Session

from infrastructure.models_orm import TaskListORM


class TaskListRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, task_list_id: int) -> Optional[TaskListORM]:
        return self.db.query(TaskListORM).filter(TaskListORM.id == task_list_id).first()

    def get_all_by_owner(self, owner_id: int) -> list[TaskListORM]:
        return self.db.query(TaskListORM).filter(TaskListORM.owner_id == owner_id).all()

    def create(
        self, title: str, description: Optional[str], owner_id: int
    ) -> TaskListORM:
        task_list = TaskListORM(title=title, description=description, owner_id=owner_id)
        self.db.add(task_list)
        self.db.commit()
        self.db.refresh(task_list)
        return task_list

    def update(
        self, task_list: TaskListORM, title: str, description: Optional[str]
    ) -> TaskListORM:
        task_list.title = title
        task_list.description = description
        self.db.commit()
        self.db.refresh(task_list)
        return task_list

    def delete(self, task_list: TaskListORM) -> None:
        self.db.delete(task_list)
        self.db.commit()
