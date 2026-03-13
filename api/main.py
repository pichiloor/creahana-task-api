from fastapi import FastAPI

from api import auth, task_lists, tasks
from infrastructure.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crehana Task API",
    description="API para gestión de listas de tareas",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(task_lists.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "ok"}
