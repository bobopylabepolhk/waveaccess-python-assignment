from httpx import AsyncClient


async def test_register_duplicate_users(tc: AsyncClient):
    payload = {"login": "dima", "password": "P@ssw0rd!", "role": 1}
    await tc.post("/users/register", json=payload)
    duplicate_response = await tc.post("/users/register", json=payload)

    assert duplicate_response.status_code == 409


async def test_register_wrong_role(tc: AsyncClient):
    payload = {"login": "maria", "password": "P@ssw0rd!", "role": 2122}
    response = await tc.post("/users/register", json=payload)

    assert response.status_code == 422


async def test_login_nonexistent_user(tc: AsyncClient):
    payload = {"login": "idontexist", "password": "P@ssw0rd!"}
    response = await tc.post("/users/login", json=payload)

    assert response.status_code == 401
