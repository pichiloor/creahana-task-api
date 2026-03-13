# This is a simulated email notification.
# In a real application, this would send an actual email using a service like SendGrid.
def notify_task_assigned(user_id: int, task_title: str) -> None:
    print(
        f"[EMAIL] Sending assignment notification "
        f"to user {user_id} for task '{task_title}'"
    )
