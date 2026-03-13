class TaskListNotFoundError(Exception):
    def __init__(self, task_list_id):
        super().__init__(f"Task list '{task_list_id}' not found.")


class TaskNotFoundError(Exception):
    def __init__(self, task_id):
        super().__init__(f"Task '{task_id}' not found.")


class UserNotFoundError(Exception):
    def __init__(self, identifier):
        super().__init__(f"User '{identifier}' not found.")


class UserAlreadyExistsError(Exception):
    def __init__(self, identifier):
        super().__init__(f"User '{identifier}' already exists.")


class ForbiddenError(Exception):
    def __init__(self, message: str = "Action not allowed."):
        super().__init__(message)


class InvalidCredentialsError(Exception):
    def __init__(self):
        super().__init__("Invalid username or password.")
