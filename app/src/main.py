from fastapi import FastAPI
from api import tasks, users, task_history, task_linked

app = FastAPI(title='bugtracker')

app.include_router(tasks.router)
app.include_router(task_linked.router)
app.include_router(users.router)
app.include_router(task_history.router)