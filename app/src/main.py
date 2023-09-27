from fastapi import FastAPI

from api import task_history, tasks, users

app = FastAPI(title="bugtracker")

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(task_history.router)
