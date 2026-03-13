from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from api.schemas import (TaskListTasksResponse, TaskRequest, TaskResponse,
                         TaskStatusRequest)
from application.task_service import TaskService
from domain.exceptions import ForbiddenError, TaskNotFoundError
from domain.models import TaskPriority, TaskStatus
from infrastructure.database import get_db
from infrastructure.models_orm import UserORM

router = APIRouter(prefix="/lists/{task_list_id}/tasks", tags=["tasks"])


@router.get("/", response_model=TaskListTasksResponse)
def get_all(
    task_list_id: int,
    status_filter: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        tasks = TaskService(db).get_all(
            task_list_id=task_list_id,
            owner_id=current_user.id,
            status=status_filter,
            priority=priority,
        )
        return TaskListTasksResponse(tasks=tasks)
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
def get_by_id(
    task_list_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        return TaskService(db).get_by_id(task_id, current_user.id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create(
    task_list_id: int,
    body: TaskRequest,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        return TaskService(db).create(
            task_list_id=task_list_id,
            owner_id=current_user.id,
            title=body.title,
            description=body.description,
            priority=body.priority,
            assigned_to=body.assigned_to,
        )
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
def update(
    task_list_id: int,
    task_id: int,
    body: TaskRequest,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        return TaskService(db).update(
            task_id=task_id,
            owner_id=current_user.id,
            title=body.title,
            description=body.description,
            priority=body.priority,
            assigned_to=body.assigned_to,
        )
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.patch("/{task_id}/status", response_model=TaskResponse)
def change_status(
    task_list_id: int,
    task_id: int,
    body: TaskStatusRequest,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        return TaskService(db).change_status(
            task_id=task_id,
            owner_id=current_user.id,
            status=body.status,
        )
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    task_list_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        TaskService(db).delete(task_id, current_user.id)
    except TaskNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
