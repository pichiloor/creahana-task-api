from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from domain.models import TaskPriority, TaskStatus

# ── Auth ─────────────────────────────────────────────────────────────────────


class UserRegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Task List ─────────────────────────────────────────────────────────────────


class TaskListRequest(BaseModel):
    title: str
    description: str | None = None


class TaskListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime


# ── Task ──────────────────────────────────────────────────────────────────────


class TaskRequest(BaseModel):
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: int | None = None


class TaskStatusRequest(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    task_list_id: int
    assigned_to: int | None
    created_at: datetime
    updated_at: datetime


class TaskWithCompletionResponse(TaskResponse):
    completion_percentage: float
