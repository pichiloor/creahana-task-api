from sqlalchemy.orm import Session

from domain.exceptions import ForbiddenError, TaskListNotFoundError
from infrastructure.repositories.task_list_repository import TaskListRepository
from infrastructure.repositories.task_repository import TaskRepository


class TaskListService:
    def __init__(self, db: Session):
        self.task_list_repo = TaskListRepository(db)
        self.task_repo = TaskRepository(db)

    def get_all(self, owner_id: int):
        return self.task_list_repo.get_all_by_owner(owner_id)

    def get_by_id(self, task_list_id: int, owner_id: int):
        task_list = self.task_list_repo.get_by_id(task_list_id)
        if not task_list:
            raise TaskListNotFoundError(task_list_id)
        if task_list.owner_id != owner_id:
            raise ForbiddenError()
        return task_list

    def create(self, title: str, description: str, owner_id: int):
        return self.task_list_repo.create(
            title=title, description=description, owner_id=owner_id
        )

    def update(self, task_list_id: int, owner_id: int, title: str, description: str):
        task_list = self.get_by_id(task_list_id, owner_id)
        return self.task_list_repo.update(
            task_list=task_list, title=title, description=description
        )

    def delete(self, task_list_id: int, owner_id: int):
        task_list = self.get_by_id(task_list_id, owner_id)
        self.task_list_repo.delete(task_list)

    def get_completion_percentage(self, task_list_id: int, owner_id: int) -> float:
        self.get_by_id(task_list_id, owner_id)
        tasks = self.task_repo.get_all_by_task_list(task_list_id)
        if not tasks:
            return 0.0
        done = sum(1 for t in tasks if t.status.value == "done")
        return round((done / len(tasks)) * 100, 2)
