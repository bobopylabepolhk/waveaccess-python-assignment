from fastapi import FastAPI

from api import mappers, tasks, users

app = FastAPI(title="bugtracker")

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(mappers.router)
