from typing import Optional

from sqlalchemy.orm import Session

from domain.exceptions import ForbiddenError, TaskNotFoundError
from domain.models import TaskPriority, TaskStatus
from infrastructure.notifications import notify_task_assigned
from infrastructure.repositories.task_list_repository import TaskListRepository
from infrastructure.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, db: Session):
        self.task_repo = TaskRepository(db)
        self.task_list_repo = TaskListRepository(db)

    def _verify_task_list_owner(self, task_list_id: int, owner_id: int):
        # Raises ForbiddenError if the list does not exist or belongs to another user.
        task_list = self.task_list_repo.get_by_id(task_list_id)
        if not task_list:
            raise ForbiddenError()
        if task_list.owner_id != owner_id:
            raise ForbiddenError()

    def get_all(
        self,
        task_list_id: int,
        owner_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ):
        self._verify_task_list_owner(task_list_id, owner_id)
        return self.task_repo.get_all_by_task_list(
            task_list_id=task_list_id, status=status, priority=priority
        )

    def get_by_id(self, task_id: int, owner_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        self._verify_task_list_owner(task.task_list_id, owner_id)
        return task

    def create(
        self,
        task_list_id: int,
        owner_id: int,
        title: str,
        description: Optional[str],
        priority: TaskPriority = TaskPriority.MEDIUM,
        assigned_to: Optional[int] = None,
    ):
        self._verify_task_list_owner(task_list_id, owner_id)
        task = self.task_repo.create(
            title=title,
            description=description,
            task_list_id=task_list_id,
            priority=priority,
            assigned_to=assigned_to,
        )
        # Send a notification if the task was assigned to a user.
        if assigned_to is not None:
            notify_task_assigned(user_id=assigned_to, task_title=title)
        return task

    def update(
        self,
        task_id: int,
        owner_id: int,
        title: str,
        description: Optional[str],
        priority: TaskPriority,
        assigned_to: Optional[int] = None,
    ):
        task = self.get_by_id(task_id, owner_id)
        updated = self.task_repo.update(
            task=task,
            title=title,
            description=description,
            priority=priority,
            assigned_to=assigned_to,
        )
        # Send a notification if the task was assigned to a user.
        if assigned_to is not None:
            notify_task_assigned(user_id=assigned_to, task_title=title)
        return updated

    def change_status(self, task_id: int, owner_id: int, status: TaskStatus):
        task = self.get_by_id(task_id, owner_id)
        return self.task_repo.change_status(task=task, status=status)

    def delete(self, task_id: int, owner_id: int):
        task = self.get_by_id(task_id, owner_id)
        self.task_repo.delete(task)
