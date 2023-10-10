import asyncio
from httpx import AsyncClient
import pytest

from app.src.main import app
from app.src.core.settings import Settings
import app.src.core.settings as config


config.settings = Settings(_env_file=".env.test")

""" override pytest default function scoped event loop """


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


""" get test client """


@pytest.fixture(scope="session")
async def tc():
    async with AsyncClient(app=app, base_url=config.settings.base_url) as tc:
        yield tc


""" regiser users. get user tokens """


@pytest.fixture(autouse=True, scope="session")
async def register_test_users(tc: AsyncClient):
    manager_payload = {"login": "_manager", "password": "P@ssw0rd!", "role": 3}
    lead_payload = {"login": "_lead", "password": "P@ssw0rd!", "role": 1}
    dev_payload = {"login": "_dev", "password": "P@ssw0rd!", "role": 2}
    qa_payload = {"login": "_qa", "password": "P@ssw0rd!", "role": 4}

    await tc.post("/users/register", json=manager_payload)
    await tc.post("/users/register", json=lead_payload)
    await tc.post("/users/register", json=dev_payload)
    await tc.post("/users/register", json=qa_payload)


@pytest.fixture(scope="session")
async def user_manager(tc: AsyncClient):
    user_payload = {"login": "_manager", "password": "P@ssw0rd!"}
    response = await tc.post("/users/login", json=user_payload)
    res = response.json()
    token = res["access_token"]

    yield {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
async def user_lead(tc: AsyncClient):
    user_payload = {"login": "_lead", "password": "P@ssw0rd!"}
    response = await tc.post("/users/login", json=user_payload)
    res = response.json()
    token = res["access_token"]

    yield {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
async def user_dev(tc: AsyncClient):
    user_payload = {"login": "_dev", "password": "P@ssw0rd!"}
    response = await tc.post("/users/login", json=user_payload)
    res = response.json()
    token = res["access_token"]

    yield {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
async def user_qa(tc: AsyncClient):
    user_payload = {"login": "_qa", "password": "P@ssw0rd!"}
    response = await tc.post("/users/login", json=user_payload)
    res = response.json()
    token = res["access_token"]

    yield {"Authorization": f"Bearer {token}"}


""" tasks fixtures """


@pytest.fixture()
async def new_task_id(tc: AsyncClient, user_lead):
    payload = {
        "asignee": 3,
        "status": "To do",
        "task_type": "task",
        "priority": 2,
        "name": "name",
        "author": 1,
        "description": "desc",
    }
    response = await tc.post("/tasks/", json=payload, headers=user_lead)
    task_id: int = response.json()["id"]

    yield task_id
