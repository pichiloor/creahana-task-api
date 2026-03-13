from typing import Optional

from sqlalchemy.orm import Session

from domain.models import TaskPriority, TaskStatus
from infrastructure.models_orm import TaskORM


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, task_id: int) -> Optional[TaskORM]:
        return self.db.query(TaskORM).filter(TaskORM.id == task_id).first()

    def get_all_by_task_list(
        self,
        task_list_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
    ) -> list[TaskORM]:
        query = self.db.query(TaskORM).filter(TaskORM.task_list_id == task_list_id)
        if status:
            query = query.filter(TaskORM.status == status)
        if priority:
            query = query.filter(TaskORM.priority == priority)
        return query.all()

    def create(
        self,
        title: str,
        description: Optional[str],
        task_list_id: int,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assigned_to: Optional[int] = None,
    ) -> TaskORM:
        task = TaskORM(
            title=title,
            description=description,
            task_list_id=task_list_id,
            priority=priority,
            assigned_to=assigned_to,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(
        self,
        task: TaskORM,
        title: str,
        description: Optional[str],
        priority: TaskPriority,
        assigned_to: Optional[int] = None,
    ) -> TaskORM:
        task.title = title
        task.description = description
        task.priority = priority
        task.assigned_to = assigned_to
        self.db.commit()
        self.db.refresh(task)
        return task

    def change_status(self, task: TaskORM, status: TaskStatus) -> TaskORM:
        task.status = status
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: TaskORM) -> None:
        self.db.delete(task)
        self.db.commit()
