from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user
from api.schemas import TaskListRequest, TaskListResponse
from application.task_list_service import TaskListService
from domain.exceptions import ForbiddenError, TaskListNotFoundError
from infrastructure.database import get_db
from infrastructure.models_orm import UserORM

router = APIRouter(prefix="/lists", tags=["task-lists"])


@router.get("/", response_model=list[TaskListResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return TaskListService(db).get_all(owner_id=current_user.id)


@router.get("/{task_list_id}", response_model=TaskListResponse)
def get_by_id(
    task_list_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        return TaskListService(db).get_by_id(task_list_id, current_user.id)
    except TaskListNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.post("/", response_model=TaskListResponse, status_code=status.HTTP_201_CREATED)
def create(
    body: TaskListRequest,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    return TaskListService(db).create(
        title=body.title,
        description=body.description,
        owner_id=current_user.id,
    )


@router.put("/{task_list_id}", response_model=TaskListResponse)
def update(
    task_list_id: int,
    body: TaskListRequest,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        return TaskListService(db).update(
            task_list_id=task_list_id,
            owner_id=current_user.id,
            title=body.title,
            description=body.description,
        )
    except TaskListNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))


@router.delete("/{task_list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    task_list_id: int,
    db: Session = Depends(get_db),
    current_user: UserORM = Depends(get_current_user),
):
    try:
        TaskListService(db).delete(task_list_id, current_user.id)
    except TaskListNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ForbiddenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
